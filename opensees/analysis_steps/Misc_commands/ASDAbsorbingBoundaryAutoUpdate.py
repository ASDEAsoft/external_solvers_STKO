import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
from scipy.spatial import KDTree
import numpy as np
import time

def _err(msg):
	return 'Error in "ASDAbsorbingBoundaryAutoUpdate" :\n{}'.format(msg)

def makeXObjectMetaData():
	xom = MpcXObjectMetaData()
	xom.name = 'ASDAbsorbingBoundaryAutoUpdate'
	xom.Xgroup = 'absorbingBoundaries'
	return xom

def _getSourceTreeData(doc, is2D):
	'''
	compute source data for the KDTree.
	returns a tuple (data, indices) where:
	- data = Nx3 numpy array with XYZ coordinates for the N nodes
	- indices = list of N integers, the tags of the element the i-th XYZ coordinates belong to
	'''
	data = []
	indices = []
	mesh = doc.mesh
	sfact = 0.99 # the shrink factor
	for _, geom in doc.geometries.items():
		mog = mesh.getMeshedGeometry(geom.id)
		if is2D and len(mog.solids) > 0:
			continue
		pas = geom.elementPropertyAssignment
		all_domains = mog.faces if is2D else mog.solids
		all_props = pas.onFaces if is2D else pas.onSolids
		for prop, domain in zip(all_props, all_domains):
			if prop and prop.XObject.name.startswith('ASDAbsorbingBoundary'):
				continue # avoid self
			for ele in domain.elements:
				center = ele.computeCenter()
				for node in ele.nodes:
					modpos = node.position - center
					distance = modpos.norm()
					if distance > 0.0:
						modpos /= distance
					modpos = center + sfact*distance*modpos
					data.append([modpos.x, modpos.y, modpos.z])
					indices.append(ele.id)
	data = np.array(data)
	return (data, indices)

def _getAbsorbingTreeData(doc):
	'''
	compute absorbing data for searching into the KDTree.
	returns a tuple (data, indices) where:
	- data = Nx3 numpy array with XYZ coordinates for the N nodes
	- indices = list of N integers, the tags of the element the i-th XYZ coordinates belong to
	'''
	data = []
	indices = []
	mesh = doc.mesh
	def _internal(prop, domain):
		if prop and prop.XObject.name.startswith('ASDAbsorbingBoundary'):
			for ele in domain.elements:
				center = ele.computeCenter()
				data.append([center.x, center.y, center.z])
				indices.append(ele.id)
	for _, geom in doc.geometries.items():
		mog = mesh.getMeshedGeometry(geom.id)
		pas = geom.elementPropertyAssignment
		# check edges for 2d auto
		for prop, domain in zip(pas.onEdges, mog.edges):
			_internal(prop, domain)
		# check faces for 2d manual or 3d auto
		for prop, domain in zip(pas.onFaces, mog.faces):
			_internal(prop, domain)
		# check solids for 3d manual
		for prop, domain in zip(pas.onSolids, mog.solids):
			_internal(prop, domain)
	data = np.array(data)
	return (data, indices)

class _tem:
	map_descr = '''# ASDAbsorbingBoundaryAutoUpdate
#
# An array that maps:
# key = index of the absorbing boundary element
# val = a triplet with:
#       - the PID of the absorbing boundary element
#       - the TAG of the source soil element
#       - the PID of the source soil element
'''
	result_alloc = '''#
# An array that maps each absorbing boundary element
# to the response obtained by the source element
array set ASD_ABS_BND_RESULTS {}
'''
	G_tangent = '''#
# A procedure to compute the result of the source element
proc ASD_ABS_BND_SOURCE_RESULT {src_ele} {
	set mean_G 0.0
	set num_gauss 0
	for {set gpi 1} {$gpi <= 100} {incr gpi} {
		set KT [eleResponse $src_ele material $gpi tangent]
		set n [llength $KT]
		# if the element does not support material keyword (1-point elements)...
		if {$n == 0} {
			if {$gpi == 1} {
				# try this
				set KT [eleResponse $src_ele tangent]
				set n [llength $KT]
			}
		}
		if {$n == 0} { break }
		incr num_gauss
		set G [lindex $KT [expr ($n-1)]]
		set mean_G [expr ($mean_G + $G)]
	}
	# do the gauss average
	if {$num_gauss > 0} {set mean_G [expr $mean_G/$num_gauss.0]}
	return $mean_G
}
'''
	G_secant = '''#
# A procedure to compute the result of the source element
proc ASD_ABS_BND_SOURCE_RESULT {src_ele} {
	set mean_G 0.0
	set num_gauss 0
	for {set gpi 1} {$gpi <= 100} {incr gpi} {
		set S [eleResponse $src_ele material $gpi stress]
		set n [llength $S]
		# if the element does not support material keyword (1-point elements)...
		if {$n == 0} {
			if {$gpi == 1} {
				# try this
				set S [eleResponse $src_ele stress]
				set n [llength $S]
			}
		}
		if {$n == 0} { break }
		incr num_gauss
		set s11 [expr [lindex $S 0]]
		set s22 [expr [lindex $S 1]]
		set s33 [expr [lindex $S 2]]
		set p [expr max(1.0, -($s11 + $s22 + $s33)/3.0)]
		set BB [eleResponse $src_ele material $gpi backbone $p]
		
		# or use octa shear strain
		set E [eleResponse $src_ele material $gpi strain]
		set g12 [expr abs([lindex $E 3])]
		set g23 [expr abs([lindex $E 4])]
		set g13 [expr abs([lindex $E 5])]
		set gamma [expr max($g12, max($g23, $g13))]
		
		# search
		set G 0.0
		set nbb [expr [llength $BB]/2.0-1]
		for {set i 0} {$i < $nbb} {incr i} {
			set j [expr $i*2 + 2]
			set k [expr $j + 1]
			set xx [lindex $BB $j]
			set yy [lindex $BB $k]
			set G $yy
			if {$gamma < $xx} {
				#puts "found: $xx $G"
				break
			}
		}
		
		set mean_G [expr ($mean_G + $G)]
	}
	# do the gauss average
	if {$num_gauss > 0} {set mean_G [expr $mean_G/$num_gauss.0]}
	return $mean_G
}
'''
	update_proc = '''#
# The update procedure
proc ASD_ABS_BND_UPDATE_PROCEDURE {} {
	global ASD_ABS_BND_MAP
	global ASD_ABS_BND_RESULTS
	set pid [getPID]
	puts "ABSUPDATE - Begin send-recv on P: $pid"
	foreach {abs_ele abs_info} [array get ASD_ABS_BND_MAP] {
		set abs_pid [lindex $abs_info 0]
		set src_ele [lindex $abs_info 1]
		set src_pid [lindex $abs_info 2]
		if {$abs_pid == $pid} {
			if {$src_pid == $pid} {
				# on same process
				set ASD_ABS_BND_RESULTS($abs_ele) [ASD_ABS_BND_SOURCE_RESULT $src_ele]
			} else {
				# recv
				recv -pid $src_pid the_result
				set ASD_ABS_BND_RESULTS($abs_ele) $the_result
			}
		} else {
			if {$src_pid == $pid} {
				# send
				send -pid $abs_pid  [ASD_ABS_BND_SOURCE_RESULT $src_ele]
			}
		}
	}
	barrier
	puts "ABSUPDATE - Begin UPDATE on P: $pid"
	foreach {abs_ele G} [array get ASD_ABS_BND_RESULTS] {
		setParameter -val $G -ele $abs_ele G
	}
}
#
# Add it to the list of custom functions to be called before each step
lappend STKO_VAR_OnBeforeAnalyze_CustomFunctions ASD_ABS_BND_UPDATE_PROCEDURE
'''

def writeTcl(pinfo):
	from io import StringIO
	
	# intial checks
	doc = App.caeDocument()
	if doc is None:
		raise Exception(_err('NULL document'))
	if doc.mesh is None:
		raise Exception(_err('NULL mesh'))
	
	# found absorbing elements and dimension:
	# avoid useless calculations
	is2D = False
	is3D = False
	found = False
	for _, ep in doc.elementProperties.items():
		xname = ep.XObject.name
		if xname.startswith('ASDAbsorbingBoundary2D'):
			found = True
			is2D = True
		elif xname.startswith('ASDAbsorbingBoundary3D'):
			found = True
			is3D = True
	if not found:
		# quick return
		return
	if is2D and is3D:
		raise Exception(_err('Cannot mix 2D and 3D absorbing elements in the same model'))
	
	# begin
	print('ASDAbsorbingBoundaryAutoUpdate begin building map...')
	time_start = time.time()
	
	# process
	src_data, src_indices = _getSourceTreeData(doc, is2D)
	abs_data, abs_indices = _getAbsorbingTreeData(doc)
	tree = KDTree(src_data)
	_, src_location = tree.query(abs_data, workers=-1)
	# abs_id abs_pid src_id src_pid
	mesh = doc.mesh
	pdata = mesh.partitionData
	out_data = [ [
		abs_indices[i], 
		pdata.elementPartition(abs_indices[i]),
		src_indices[j],
		pdata.elementPartition(src_indices[j])] for i,j in enumerate(src_location)]
	
	# build command
	ss = StringIO()
	# the ASD_ABS_BND_MAP
	ss.write(_tem.map_descr)
	for item in out_data:
		ss.write('{}set ASD_ABS_BND_MAP({}) {{{} {} {}}}\n'.format(pinfo.indent, *item))
	# the ASD_ABS_BND_RESULTS
	ss.write(_tem.result_alloc)
	# the ASD_ABS_BND_SOURCE_RESULT procedure
	ss.write(_tem.G_tangent)
	# The update function
	ss.write(_tem.update_proc)
	# write to file
	pinfo.out_file.write(ss.getvalue())
	
	# done
	time_end = time.time()
	print('... elapsed time: {} seconds'.format(time_end - time_start))


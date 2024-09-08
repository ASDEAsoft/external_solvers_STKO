import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
from opensees.utils.parameter_utils import ParameterManager

def _err(msg):
	return 'Error in "ASDAbsorbingBoundaryActivate" :\n{}'.format(msg)

def makeXObjectMetaData():
	xom = MpcXObjectMetaData()
	xom.name = 'ASDAbsorbingBoundaryActivate'
	xom.Xgroup = 'absorbingBoundaries'
	return xom

class _globals:
	ptypes = ['ASDAbsorbingBoundary2D', 'ASDAbsorbingBoundary3D']

def writeTcl(pinfo):
	
	from io import StringIO
	
	# find all elements
	# key = partition, values = listofint
	pid_ele_map = {}
	
	# start with manager for automatic elements
	def _copymanager(manager):
		if manager:
			for pid, source in manager.elements.items():
				dest = pid_ele_map.get(pid, None)
				if dest is None:
					dest = []
					pid_ele_map[pid] = dest
				for i in source: dest.append(i)
	for itype in _globals.ptypes:
		_copymanager(pinfo.custom_data.get(itype, None))
	
	# find manual elements
	doc = App.caeDocument()
	mesh = doc.mesh
	def _copymanual(prop, domain):
		if prop and prop.XObject.name in _globals.ptypes:
			for ele in domain.elements:
				pid = mesh.partitionData.elementPartition(ele.id)
				dest = pid_ele_map.get(pid, None)
				if dest is None:
					dest = []
					pid_ele_map[pid] = dest
				dest.append(ele.id)
	for _, geom in doc.geometries.items():
		mog = mesh.getMeshedGeometry(geom.id)
		pas = geom.elementPropertyAssignment
		# check edges for 2d auto
		for prop, domain in zip(pas.onEdges, mog.edges):
			_copymanual(prop, domain)
		# check faces for 2d manual or 3d auto
		for prop, domain in zip(pas.onFaces, mog.faces):
			_copymanual(prop, domain)
		# check solids for 3d manual
		for prop, domain in zip(pas.onSolids, mog.solids):
			_copymanual(prop, domain)
	
	# quick return
	empty = True
	for _, values in pid_ele_map.items():
		if len(values) > 0:
			empty = False
			break
	if empty:
		return
	
	# make command string
	def commandstring(eles, indent):
		stream = StringIO()
		stream.write('{}parameter {}\n'.format(indent, ParameterManager.ABSORBING_STAGE))
		stream.write('{}foreach ele_id [list \\\n'.format(indent))
		count = 0
		n = len(eles)
		for i in range(n):
			count += 1
			if count == 1:
				stream.write('{}{}'.format(indent, pinfo.tabIndent))
			stream.write('{} '.format(eles[i]))
			if count == 10 and i < n-1:
				count = 0
				stream.write('\\\n')
		stream.write('] {\n')
		stream.write('{}{}addToParameter {} element $ele_id stage\n'.format(pinfo.indent, pinfo.tabIndent, ParameterManager.ABSORBING_STAGE))
		stream.write('{}}}\n'.format(pinfo.indent))
		stream.write('{}updateParameter {} 1\n'.format(pinfo.indent, ParameterManager.ABSORBING_STAGE))
		stream.write('{}remove parameter {}\n'.format(pinfo.indent, ParameterManager.ABSORBING_STAGE))
		return stream.getvalue()
	
	# comment
	pinfo.out_file.write('\n{}# Activate Absorbing boundaries\n'.format(pinfo.indent))
	
	# check partitions
	if pinfo.process_count > 1:
		for partition_id, values in pid_ele_map.items():
			if(len(values) > 0):
				pinfo.out_file.write('{}if {{$STKO_VAR_process_id == {}}} {{\n'.format(pinfo.indent, partition_id))
				pinfo.out_file.write(commandstring(values, pinfo.indent+pinfo.tabIndent))
				pinfo.out_file.write('{}}}\n'.format(pinfo.indent))
	else:
		values = pid_ele_map[0]
		if(len(values) > 0):
			pinfo.out_file.write(commandstring(values, pinfo.indent))
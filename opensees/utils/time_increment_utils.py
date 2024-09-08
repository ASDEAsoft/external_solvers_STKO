from PyMpc import *
import os
from opensees.utils.parameter_utils import ParameterManager

class _globals:
	target_physical_properties = [
		'DamageTC1D', 'DamageTC3D',
		'ASDConcrete1D', 'ASDConcrete3D',
	]

def _find_phys_props(doc):
	'''
	find all physical properties using either the implex algorithm
	or the viscosity. they need a proper monotonically increasing time-step
	'''
	# first search
	direct = {}
	for id, prop in doc.physicalProperties.items():
		xobj = prop.XObject
		name = xobj.name
		if name in _globals.target_physical_properties:
			implex = xobj.getAttribute('integration').string == 'IMPL-EX'
			viscosity = xobj.getAttribute('eta').real != 0.0
			if implex or viscosity:
				direct[prop.id] = prop
	
	# find referencing components
	found = direct.copy()
	for id, prop in direct.items():
		ref = App.getReferencingComponents(prop)
		for item in ref:
			if item.indexSourceType == MpcAttributeIndexSourceType.PhysicalProperty:
				found[item.id] = item
	
	# done
	return found

def _find_geoms(doc, props, geoms, fun_get_assignment):
	'''
	find all geometries with the input properties as assignment.
	the input-output map has:
	- key = tuple(geom_id, subgeom_type[1:edge, 2:face, 3:solid], subgeom_id)
	- value = mesh domain
	'''
	mesh = doc.mesh
	for geom_id, geom in doc.geometries.items():
		asn = fun_get_assignment(geom)
		mog = mesh.getMeshedGeometry(geom_id)
		if mog is None: continue
		for _, prop in props.items():
			if prop in asn.mapOnEdges:
				subset = asn.mapOnEdges[prop]
				for i in subset:
					geoms[(geom_id, 1, i)] = mog.edges[i]
			if prop in asn.mapOnFaces:
				subset = asn.mapOnFaces[prop]
				for i in subset:
					geoms[(geom_id, 2, i)] = mog.faces[i]
			if prop in asn.mapOnSolids:
				subset = asn.mapOnSolids[prop]
				for i in subset:
					geoms[(geom_id, 3, i)] = mog.solids[i]

def process_document(pinfo):
	
	'''
	TODO:
	(when we do it with ImplexContact...
	find also element properties
	find also in interactions
	'''
	
	print('Running Time-Increment Utility...')
	
	# check document
	doc = App.caeDocument()
	if doc is None:
		return
	
	# a counter for target object in OpenSees with the IMPL-EX algorithm
	# or with the Viscosity
	target_count = 0
	
	# find physical properties
	phys_props = _find_phys_props(doc)
	
	# find geometries
	geoms = {}
	_find_geoms(doc, phys_props, geoms, lambda geom : geom.physicalPropertyAssignment)
	
	# find mesh elements
	mesh = doc.mesh
	for geom_key, domain in geoms.items():
		target_count += len(domain.elements)
	
	# quick return
	if target_count == 0:
		return
	
	# print info
	pinfo.out_file.write('\n\n# Time-Increment Utility Stats\n#\n')
	pinfo.out_file.write('# Found {} Physical Properties\n'.format(len(phys_props)))
	for id, prop in phys_props.items():
		pinfo.out_file.write('#    [{}] {}\n'.format(id, prop.name))
	pinfo.out_file.write('# Found {} Geometries\n'.format(len(geoms)))
	pinfo.out_file.write('# Found a total of {} elements\n'.format(target_count))
	
	# write the list of elements based on partitioning
	def write_loop(all_eles, indent):
		count = 0
		total_count = 0
		N = len(all_eles)
		pinfo.out_file.write('{}set STKO_VAR_TimeIncrementUpdateTargets [list '.format(indent))
		if N > 0:
			pinfo.out_file.write('\\\n')
			for ele_id in all_eles:
				count += 1
				total_count += 1
				if count == 1:
					pinfo.out_file.write('{}{}'.format(indent, pinfo.tabIndent))
				pinfo.out_file.write('{} '.format(ele_id))
				if count == 20 and total_count < N:
					count = 0
					pinfo.out_file.write('\\\n')
		pinfo.out_file.write(']\n')
	# get element list
	if pinfo.process_count > 1:
		all_eles = [[] for i in range(pinfo.process_count)]
		for geom_key, domain in geoms.items():
			for element in domain.elements:
				pid = doc.mesh.partitionData.elementPartition(element.id)
				all_eles[pid].append(element.id)
		for partition_id in range(pinfo.process_count):
			pinfo.out_file.write('{}if {{$STKO_VAR_process_id == {}}} {{\n'.format(pinfo.indent, partition_id))
			write_loop(all_eles[partition_id], pinfo.indent+pinfo.tabIndent)
			pinfo.out_file.write('{}}}\n'.format(pinfo.indent))
	else:
		all_eles = []
		for geom_key, domain in geoms.items():
			for element in domain.elements:
				all_eles.append(element.id)
		write_loop(all_eles, pinfo.indent)
	
	# write custom functions
	pinfo.out_file.write('''#
# Time-Increment Utility Functions.
# Define a function to be called before the current time step
proc STKO_DT_UTIL_OnBeforeAnalyze {} {
	global STKO_VAR_increment
	global STKO_VAR_time_increment
	global STKO_VAR_TimeIncrementUpdateTargets
	# update the initial time and the committed time for the first time
	foreach ele_id $STKO_VAR_TimeIncrementUpdateTargets {
		if {$STKO_VAR_increment == 1} {
			setParameter -val $STKO_VAR_time_increment -ele $ele_id dTimeCommit
			setParameter -val $STKO_VAR_time_increment -ele $ele_id dTimeInitial
		}
		# always update the current time increment
		setParameter -val $STKO_VAR_time_increment -ele $ele_id dTime
	}
}
# add it to the list of functions
lappend STKO_VAR_OnBeforeAnalyze_CustomFunctions STKO_DT_UTIL_OnBeforeAnalyze

''')
from PyMpc import *
import os
from opensees.utils import parameter_utils as paramutil

def _find_phys_props(doc):
	'''
	find all physical properties using the implex algorithm
	'''
	# first search
	direct = {}
	for id, prop in doc.physicalProperties.items():
		xobj = prop.XObject
		name = xobj.name
		if name == 'DamageTC3D' or name == 'DamageTC1D':
			implex = xobj.getAttribute('integration').string == 'IMPL-EX'
			if implex:
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
	
	print('Running IMPL-EX Utility...')
	
	# check document
	doc = App.caeDocument()
	if doc is None:
		return
	is_partitioned = (len(doc.mesh.partitionData.partitions) > 1)
	
	# find physical properties
	phys_props = _find_phys_props(doc)
	
	# find geometries
	geoms = {}
	_find_geoms(doc, phys_props, geoms, lambda geom : geom.physicalPropertyAssignment)
	
	# get mesh
	elements = []
	mesh = doc.mesh
	for geom_key, domain in geoms.items():
		for element in domain.elements:
			elements.append(element.id)
	elements = list(set(elements))
	
	# make file
	if len(elements) == 0:
		return
	file = open('{}{}IMPLEX_tools.tcl'.format(pinfo.out_dir, os.sep), 'w+')
	
	# print info
	file.write('# IMPLEX-Utilty Stats\n#\n')
	file.write('# Found {} Physical Properties\n'.format(len(phys_props)))
	for id, prop in phys_props.items():
		file.write('#   [{}] {}\n'.format(id, prop.name))
	file.write('# Found {} Geometries\n'.format(len(geoms)))
	for geom_key, domain in geoms.items():
		file.write('#   [{}] {} (# Elements: {})\n'.format(geom_key, domain, len(domain.elements)))
	
	# write element list
	def write_elist(el, ind=''):
		file.write('{}set STKO_IMPLEX_elements {{\\\n'.format(ind))
		counter = 0
		for i in el:
			if counter == 0:
				file.write('{}{}'.format(ind, pinfo.tabIndent))
			file.write('{} '.format(i))
			counter += 1
			if counter == 10:
				counter = 0
				file.write('\\\n')
		if counter != 0:
			file.write('\\\n')
		file.write('{}}}\n'.format(ind))
	file.write('\n\n# List of elements with the IMPL-EX algorithm\n')
	if is_partitioned:
		# write by parition
		for process_id in range(pinfo.process_count):
			part_elements = [elem_id for elem_id in elements if doc.mesh.partitionData.elementPartition(elem_id) == process_id]
			if len(part_elements) > 0:
				file.write('if {{$STKO_VAR_process_id == {}}} {{\n'.format(process_id))
				write_elist(part_elements, ind=pinfo.tabIndent)
				file.write('}\n')
	else:
		# write all elements
		write_elist(elements)
	
	# write parameters
	p_dt = paramutil.ParameterManager.IMPLEX_dT
	p_dt_commit = paramutil.ParameterManager.IMPLEX_dTcommit
	p_dt_0 = paramutil.ParameterManager.IMPLEX_dT0
	file.write('\n\n# Parameters for updating the time-step variables in the IMPL-EX elements\n')
	file.write('parameter {}; # dT\n'.format(p_dt))
	file.write('parameter {}; # dTcommit\n'.format(p_dt_commit))
	file.write('parameter {}; # dT0\n'.format(p_dt_0))
	file.write('''

# Add elements to parameters
foreach STKO_IMPLEX_ele $STKO_IMPLEX_elements {
	addToParameter %i element $STKO_IMPLEX_ele dT
	addToParameter %i element $STKO_IMPLEX_ele dTcommit
	addToParameter %i element $STKO_IMPLEX_ele dT0
}''' % (p_dt, p_dt_commit, p_dt_0))
	# write custom functions
	file.write('''

# Define a function to be called before the current time step
proc STKO_IMPLEX_OnBeforeAnalyze_UpdateParamFunction {} {
	global STKO_VAR_increment
	global STKO_VAR_time_increment
	puts "My Before Function: Incr: $STKO_VAR_increment - dT: $STKO_VAR_time_increment"
	# update the initial time and the committed time for the first time
	if {$STKO_VAR_increment == 1} {
		updateParameter %i $STKO_VAR_time_increment
		updateParameter %i $STKO_VAR_time_increment
	}
	# always update the current time increment
	updateParameter %i $STKO_VAR_time_increment
}
# add it to the list of functions
lappend STKO_VAR_OnBeforeAnalyze_CustomFunctions STKO_IMPLEX_OnBeforeAnalyze_UpdateParamFunction


# Define a function to be called after the current time step
proc STKO_IMPLEX_OnAfterAnalyze_UpdateParamFunction {} {
	global STKO_VAR_time_increment
	global STKO_VAR_analyze_done
	puts "My After Function: Incr: DONE? $STKO_VAR_analyze_done"
	# update the committed time increment
	if {$STKO_VAR_analyze_done == 0} {
		updateParameter %i $STKO_VAR_time_increment
	}
}
# add it to the list of functions
lappend STKO_VAR_OnAfterAnalyze_CustomFunctions STKO_IMPLEX_OnAfterAnalyze_UpdateParamFunction
''' % (p_dt_0, p_dt_commit, p_dt, p_dt_commit) )
	
	# done
	file.close()
	pinfo.out_file.write('# source IMPLEX_tools\nsource IMPLEX_tools.tcl\n')
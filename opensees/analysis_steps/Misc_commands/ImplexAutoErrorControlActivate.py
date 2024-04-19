import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
from opensees.utils.parameter_utils import ParameterManager

def _err(msg):
	return 'Error in "ImplexAutoErrorControlActivate" :\n{}'.format(msg)

def _find_phys_props(doc):
	'''
	find all physical properties using IMPLEX
	'''
	# first search
	direct = {}
	for id, prop in doc.physicalProperties.items():
		xobj = prop.XObject
		name = xobj.name
		if name == 'DamageTC3D' or name == 'DamageTC1D' or name == 'ASDConcrete3D':
			if xobj.getAttribute('integration').string == 'IMPL-EX':
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

def makeXObjectMetaData():
	
	def mka(name, group, descr, atype, adim = None, dval = None):
		a = MpcAttributeMetaData()
		a.type = atype
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	
	implex_tol = mka("Error Tolerance", "Default", 
		"The maximum allowed relative IMPL-EX error, in the range [0:1]", 
		MpcAttributeType.Real,
		dval=0.05)
	
	implex_red = mka("Time Reduction Limit", "Default", 
		"The pseudo-time-step reduction limit under which the implex error check is not performed, in the range [0:1]", 
		MpcAttributeType.Real,
		dval=0.01)
	
	err_type = mka("Error Type", "Default",
		"You can either choose to control the Max error, or the Average error",
		MpcAttributeType.String,
		dval="Max")
	err_type.sourceType = MpcAttributeSourceType.List
	err_type.setSourceList(['Max', 'Average'])
	
	xom = MpcXObjectMetaData()
	xom.name = 'ImplexAutoErrorControlActivate'
	xom.Xgroup = 'IMPL-EX'
	xom.addAttribute(implex_tol)
	xom.addAttribute(implex_red)
	xom.addAttribute(err_type)
	
	return xom

def writeTcl(pinfo):
	print('Running IMPLEX Error Control Tool ...')
	
	# check document
	doc = App.caeDocument()
	if doc is None:
		return
	
	# a counter for target object in OpenSees with the IMPL-EX algorithm
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
	
	# attributes
	xobj = pinfo.analysis_step.XObject
	tol = xobj.getAttribute('Error Tolerance').real
	red = xobj.getAttribute('Time Reduction Limit').real
	type = xobj.getAttribute('Error Type').string
	
	# print info
	pinfo.out_file.write('\n\n# Activate IMPL-EX Error Control\n#\n')
	pinfo.out_file.write('# Found {} Physical Properties\n'.format(len(phys_props)))
	for id, prop in phys_props.items():
		pinfo.out_file.write('#    [{}] {}\n'.format(id, prop.name))
	pinfo.out_file.write('# Found {} Geometries\n'.format(len(geoms)))
	for geom_key, domain in geoms.items():
		pinfo.out_file.write('#    [{}] {} (# Elements: {})\n'.format(geom_key, domain, len(domain.elements)))
	pinfo.out_file.write('# Found a total of {} elements\n'.format(target_count))
	
	# write the element list
	def write_targets(all_eles, indent):
		count = 0
		total_count = 0
		N = len(all_eles)
		if N > 0:
			pinfo.out_file.write('{}set STKO_IMPLEX_ErrorControl_TargetElements [list \\\n'.format(indent))
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
		else:
			pinfo.out_file.write('{}set STKO_IMPLEX_ErrorControl_TargetElements {{}}\n'.format(indent))
	# write element list
	if pinfo.process_count > 1:
		all_eles = [[] for i in range(pinfo.process_count)]
		for geom_key, domain in geoms.items():
			for element in domain.elements:
				pid = doc.mesh.partitionData.elementPartition(element.id)
				all_eles[pid].append(element.id)
		for partition_id in range(pinfo.process_count):
			pinfo.out_file.write('{}if {{$STKO_VAR_process_id == {}}} {{\n'.format(pinfo.indent, partition_id))
			write_targets(all_eles[partition_id], pinfo.indent+pinfo.tabIndent)
			pinfo.out_file.write('{}}}\n'.format(pinfo.indent))
	else:
		all_eles = []
		for geom_key, domain in geoms.items():
			for element in domain.elements:
				all_eles.append(element.id)
		write_targets(all_eles, pinfo.indent)
	
	# based on error type
	if type == 'Max':
		param_name = 'implexError'
		pre_op = 'set implex_error [expr max($implex_error, $other_implex_error)]'
		post_op = ''
	else:
		param_name = 'avgImplexError'
		pre_op = 'set implex_error [expr $implex_error + $other_implex_error]'
		post_op = 'set implex_error [expr $implex_error / double([getNP])]\n\t\t\t'
	
	# write the custom function
	pinfo.out_file.write('''#
# IMPL-EX Error Control Functions.
#
# Define a function to be called before the current time step
proc STKO_IMPLEX_ErrorControl_OnBeforeAnalyze {{}} {{
	global STKO_IMPLEX_ErrorControl_TargetElements
	if {{ [llength $STKO_IMPLEX_ErrorControl_TargetElements] > 0 }} {{
		set first_element_id [lindex $STKO_IMPLEX_ErrorControl_TargetElements 0]
		parameter {0}
		addToParameter {0} element $first_element_id {3}
		updateParameter {0} 0.0
		set implex_error [expr [getParamValue {0}]]
		remove parameter {0}
	}}
}}
# add it to the list of functions
lappend STKO_VAR_OnBeforeAnalyze_CustomFunctions STKO_IMPLEX_ErrorControl_OnBeforeAnalyze
#
# Define a function to be called after the current time step
proc STKO_IMPLEX_ErrorControl_OnAfterAnalyze {{}} {{
	global STKO_IMPLEX_ErrorControl_TargetElements
	global STKO_VAR_time_increment
	global STKO_VAR_initial_time_increment
	global STKO_VAR_afterAnalyze_done
	set implex_error 0.0
	if {{ [llength $STKO_IMPLEX_ErrorControl_TargetElements] > 0 }} {{
		set first_element_id [lindex $STKO_IMPLEX_ErrorControl_TargetElements 0]
		parameter {0}
		addToParameter {0} element $first_element_id {3}
		set implex_error [expr [getParamValue {0}]]
		remove parameter {0}
	}}
	# for parallel analysis (MP)
	if {{[getNP] > 1}} {{
		if {{[getPID] == 0}} {{
			for {{set pcounter 1}} {{$pcounter < [getNP]}} {{incr pcounter}} {{
				recv -pid $pcounter other_implex_error
				{4}
			}}
		}} else {{
			send -pid 0 $implex_error
		}}
		if {{[getPID] == 0}} {{
			{5}for {{set pcounter 1}} {{$pcounter < [getNP]}} {{incr pcounter}} {{
				send -pid $pcounter $implex_error
			}}
		}} else {{
			recv -pid 0 implex_error
		}}
	}}
	# check
	if {{$implex_error > {1}}} {{
		if {{$STKO_VAR_time_increment >= [expr {2} * $STKO_VAR_initial_time_increment]}} {{
			set STKO_VAR_afterAnalyze_done -1
		}}
	}}
}}
# add it to the list of functions
lappend STKO_VAR_OnAfterAnalyze_CustomFunctions STKO_IMPLEX_ErrorControl_OnAfterAnalyze
'''.format(ParameterManager.IMPLEX_Error, tol, red, param_name, pre_op, post_op))
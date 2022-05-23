import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# temp
	at_temp = MpcAttributeMetaData()
	at_temp.type = MpcAttributeType.QuantityVector
	at_temp.name = 'temp'
	at_temp.group = 'Group'
	at_temp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('temp')+'<br/>') +
		html_par('Four temps: Temp change at top node 1, bottom node 1, top node 2, bottom node 2;') +
		html_par('Two temps: temp change at top and bottom of element;') +
		html_par('One temp: uniform temp change in element') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_temp.dimension = u.T
	
	# ctype
	at_ctype = MpcAttributeMetaData()
	at_ctype.type = MpcAttributeType.Integer
	at_ctype.editable = False;
	at_ctype.name = 'ctype_constraint'
	at_ctype.group = 'Group'
	at_ctype.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ctype')+'<br/>') +
		html_par('ctype') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'eleLoad_beamTemp'
	xom.addAttribute(at_temp)
	xom.addAttribute(at_ctype)
	
	
	return xom

def makeConditionRepresentationData(xobj):
	'''
	Create the condition representation data for STKO.
	Here we want an arrow (vector) representation in local
	coordinate system, that can be applied only on faces.
	We need to allocate a 3d vector for the data attribute.
	The components of this vector will be set using
	@ref fillConditionRepresentationData
	'''
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Points
	d.orientation = MpcConditionVRepOrientation.Local
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = False
	d.on_edges = True
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = False
	return d

def writeTcl_eleLoad(pinfo, xobj):
	
	#eleLoad -ele $eleTag -type -beamTemp $temp1 <$temp2 $temp3 $temp4>
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	tag = xobj.parent.componentId
	
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	
	doc = App.caeDocument()
	
	
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			first_done = False
			for geom, item in all_geom.items():
				mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
				domain_collection = mesh_of_geom.edges
				eleTag = ''
				for i in item.edges:
					domain = domain_collection[i]
					for element in domain.elements:
						if doc.mesh.partitionData.elementPartition(element.id)!= process_id:
							continue
						if not first_done:
							if process_block_count == 0:
								pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
							else:
								pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
							first_done = True
						eleTag += ' {}'.format(element.id)
				# mandatory parameters
				temp_at = xobj.getAttribute('temp')
				if(temp_at is None):
					raise Exception('Error: cannot find "temp" attribute')
				temp = temp_at.quantityVector
				
				if eleTag:
				
					if (len(temp)==4):
						str_tcl = '{}{}eleLoad -ele{} -type -beamTemp {} {} {} {}\n'.format(pinfo.indent, pinfo.tabIndent, eleTag, temp.valueAt(0), temp.valueAt(1), temp.valueAt(2), temp.valueAt(3))
					elif(len(temp)==2):
						str_tcl = '{}{}eleLoad -ele{} -type -beamTemp {} {}\n'.format(pinfo.indent, pinfo.tabIndent, eleTag, temp.valueAt(0), temp.valueAt(1))
					elif(len(temp)==1):
						str_tcl = '{}{}eleLoad -ele{} -type -beamTemp {}\n'.format(pinfo.indent, pinfo.tabIndent, eleTag, temp.valueAt(0))
					else:
						raise Exception ('Error: the length of the vector must be either 4 or 2 or 1')
					# now write the string into the file
					pinfo.out_file.write(str_tcl)
					
			if is_partitioned :
				if first_done:
					process_block_count += 1
				if process_block_count > 0 and first_done:
					pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
	else :
		for geom, item in all_geom.items():
			mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
			domain_collection = mesh_of_geom.edges
			eleTag = ''
			for i in item.edges:
				domain = domain_collection[i]
				for element in domain.elements:
					eleTag += ' {}'.format(element.id)
			
			# mandatory parameters
			temp_at = xobj.getAttribute('temp')
			if(temp_at is None):
				raise Exception('Error: cannot find "temp" attribute')
			temp = temp_at.quantityVector
			
			if (len(temp)==4):
				str_tcl = '{}eleLoad -ele{} -type -beamTemp {} {} {} {}\n'.format(pinfo.indent, eleTag, temp.valueAt(0), temp.valueAt(1), temp.valueAt(2), temp.valueAt(3))
			elif(len(temp)==2):
				str_tcl = '{}eleLoad -ele{} -type -beamTemp {} {}\n'.format(pinfo.indent, eleTag, temp.valueAt(0), temp.valueAt(1))
			elif(len(temp)==1):
				str_tcl = '{}eleLoad -ele{} -type -beamTemp {}\n'.format(pinfo.indent, eleTag, temp.valueAt(0))
			else:
				raise Exception ('Error: the length of the vector must be either 4 or 2 or 1')
			
			# now write the string into the file
			pinfo.out_file.write(str_tcl)
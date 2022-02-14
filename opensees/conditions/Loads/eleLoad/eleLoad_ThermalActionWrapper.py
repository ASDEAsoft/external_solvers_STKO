import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import re

def makeXObjectMetaData():
	
	# approach
	at_approach = MpcAttributeMetaData()
	at_approach.type = MpcAttributeType.String
	at_approach.name = 'approach'
	at_approach.group = 'Group'
	at_approach.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('approach')+'<br/>') + 
		html_par('choose between "-nodeLoc" and "-node"') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper', 'eleLoad_ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	at_approach.sourceType = MpcAttributeSourceType.List
	at_approach.setSourceList(['-nodeLoc', '-node'])		#inserire nome adeguato
	at_approach.setDefault('-nodeLoc')
	
	# -nodeLoc
	at_nodeLoc = MpcAttributeMetaData()
	at_nodeLoc.type = MpcAttributeType.Boolean
	at_nodeLoc.name = '-nodeLoc'
	at_nodeLoc.group = 'Group'
	at_nodeLoc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-nodeLoc')+'<br/>') +
		html_par('') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper', 'eleLoad_ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	at_nodeLoc.editable = False
	
	# -node
	at_node = MpcAttributeMetaData()
	at_node.type = MpcAttributeType.Boolean
	at_node.name = '-node'
	at_node.group = 'Group'
	at_node.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-node')+'<br/>') +
		html_par('') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper', 'eleLoad_ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	at_node.editable = False
	'''
	# T
	at_T = MpcAttributeMetaData()
	at_T.type = MpcAttributeType.QuantityVector
	at_T.name = 'T'
	at_T.group = '-user'
	at_T.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('T')+'<br/>') +
		html_par('case1: T are the temperatures from T1 and T5') +
		html_par('case2: T are the temperatures from T1 to T15, 3D I section') +
		html_par('case3: T add to file') +
		html_par('case4: T add to file') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper', 'eleLoad_ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	
	# y
	at_y = MpcAttributeMetaData()
	at_y.type = MpcAttributeType.QuantityVector
	at_y.name = 'y'
	at_y.group = 'Group'
	at_y.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('y')+'<br/>') +
		html_par('case1: y are the coordinates from y1 and y5') +
		html_par('case2: y are the coordinates from y1 to y5, 3D I section') +
		html_par('case3: y are the coordinates from y1 and y2') +
		html_par('case4: y are the coordinates from y1 and y2') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper', 'eleLoad_ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	
	# z
	at_z = MpcAttributeMetaData()
	at_z.type = MpcAttributeType.QuantityVector
	at_z.name = 'z'
	at_z.group = 'Group'
	at_z.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('z')+'<br/>') +
		html_par('case1: without z') +
		html_par('case2: z are the coordinates from z1 to z5, 3D I section') +
		html_par('case3: z are the coordinates from z1 and z2') +
		html_par('case4: z are the coordinates from z1 and z2') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper', 'eleLoad_ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	'''
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
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper', 'eleLoad_ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'eleLoad_ThermalActionWrapper'
	xom.addAttribute(at_approach)
	xom.addAttribute(at_nodeLoc)
	xom.addAttribute(at_node)
	# xom.addAttribute(at_fileName)
	# xom.addAttribute(at_T)
	# xom.addAttribute(at_y)
	# xom.addAttribute(at_z)
	xom.addAttribute(at_ctype)
	
	'''
	# source-dep
	xom.setVisibilityDependency(at_source, at_fileName)
	xom.setVisibilityDependency(at_source, at_node)
	
	# user-dep
	xom.setVisibilityDependency(at_user, at_T)
	'''
	
	# auto-exclusive dependencies
	
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_approach, at_nodeLoc)
	xom.setBooleanAutoExclusiveDependency(at_approach, at_node)
	
	
	
	return xom

def fillConditionRepresentationData(xobj, pos, data):
	'''
	Fills the 3D vector data.
	
	Set the pressure value
	at the z component, since the orientation is set to local
	'''
	
	data[0] = 1
	data[1] = 1
	data[2] = 1

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
'''
def __regex(parameter):
	
	parameter = re.sub(r'\\+', '/', parameter)
	parameter = re.sub(r'/+', '/', parameter)
	
	return parameter
'''
def writeTcl_eleLoad(pinfo, xobj):
	
	#eleLoad -ele $eleTag -type -ThermalWrapper -nodeLoc $NodeTag1 $loc1 $NodeTag2 $loc2 <$NodeTag3 $loc3 $NodeTag4 $loc4 $NodeTag5 $loc5 $NodeTag6 $loc6>;
	#eleLoad -ele $eleTag -type -ThermalWrapper -node $NodeTag1 $NodeTag2 <$NodeTag3 $NodeTag4 $NodeTag5 $NodeTag6>;
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	tag = xobj.parent.componentId
	
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	#--------------------------------------↓ NUOVO ↓--------------------------------------
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	
	doc = App.caeDocument()
	for geom, item in all_geom.items():
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		domain_collection = mesh_of_geom.edges
		eleTag = ''
		for i in item.edges:
			domain = domain_collection[i]
			for element in domain.elements:
				eleTag += ' {}'.format(element.id)
				
				'''
				n = len(element.nodes)
				ngp = len(element.integrationRule.integrationPoints)
				data = [[0.0]*n*4]*ngp
				
				for gp in range(ngp):
					gauss_point = element.integrationRule.integrationPoints[gp]
					N = element.shapeFunctionsAt(gauss_point)
					det_J = element.jacobianAt(gauss_point).det()
					W = gauss_point.w
					gpdata = data[gp]
					
					# compute gp position in global coordinates
					x = 0.0
					y = 0.0
					z = 0.0
					for i in range(n):
						Ni = N[i]
						nodei = element.nodes[i]
						x += Ni * nodei.position.x
						y += Ni * nodei.position.y
						z += Ni * nodei.position.z
					
					for i in range(n):
						fact = N[i] * det_J * W
						
						j = i*4
						if (Mode == 'function'):
							
							dx = eval(sfx)		#spatial function x
							dy = eval(sfy)		#spatial function y
							dz = eval(sfz)		#spatial function z
							
							gpdata[j+1] += dx * fact
							gpdata[j+2] += dy * fact
							gpdata[j+3] += dz * fact
						
						else:
							gpdata[j+1] += F.x * fact
							gpdata[j+2] += F.y * fact
							gpdata[j+3] += F.z * fact
						
				for i in range(n):
					j = i*4
					gpdata[j] = element.nodes[i].id
	#--------------------------------------↑ NUOVO ↑--------------------------------------
	'''
	# mandatory parameters
	nodeLoc_at = xobj.getAttribute('-nodeLoc')
	if(nodeLoc_at is None):
		raise Exception('Error: cannot find "-nodeLoc" attribute')
	nodeLoc = nodeLoc_at.boolean
	
	node_at = xobj.getAttribute('-node')
	if(node_at is None):
		raise Exception('Error: cannot find "-node" attribute')
	node = node_at.boolean
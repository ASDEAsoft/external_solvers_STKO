import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
from opensees.conditions.utils import SpatialFunctionEval

class my_data:
	def __init__(self):
		# attributes will be set in the __control method
		pass

def makeXObjectMetaData():
	
	# Mode
	at_Mode = MpcAttributeMetaData()
	at_Mode.type = MpcAttributeType.String
	at_Mode.name = 'Mode'
	at_Mode.group = 'Group'
	at_Mode.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Mode')+'<br/>') +
		html_par('choose between "constant" and "function"') +
		html_end()
		)
	at_Mode.sourceType = MpcAttributeSourceType.List
	at_Mode.setSourceList(['constant', 'function'])
	at_Mode.setDefault('constant')
	
	# constant
	at_constant = MpcAttributeMetaData()
	at_constant.type = MpcAttributeType.Boolean
	at_constant.name = 'constant'
	at_constant.group = 'Data'
	at_constant.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('constant')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_constant.editable = False
	
	# function
	at_function = MpcAttributeMetaData()
	at_function.type = MpcAttributeType.Boolean
	at_function.name = 'function'
	at_function.group = 'Data'
	at_function.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('function')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Mass_Command','Mass Command')+'<br/>') +
		html_end()
		)
	at_function.editable = False
	
	# F_mx
	at_F_mx = MpcAttributeMetaData()
	at_F_mx.type = MpcAttributeType.String
	at_F_mx.name = 'F_mx'
	at_F_mx.group = 'Data'
	at_F_mx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('F_mx')+'<br/>') + 
		html_par('f(x) e.g.:') +
		html_par('(x**2+y**2)**0.5') +
		html_end()
		)
	at_F_mx.setDefault('0')
	
	# F_my
	at_F_my = MpcAttributeMetaData()
	at_F_my.type = MpcAttributeType.String
	at_F_my.name = 'F_my'
	at_F_my.group = 'Data'
	at_F_my.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('F_my')+'<br/>') + 
		html_par('f(y) e.g.:') +
		html_par('(y**2+y**2)**0.5') +
		html_end()
		)
	at_F_my.setDefault('0')
	
	
	# F_mz
	at_F_mz = MpcAttributeMetaData()
	at_F_mz.type = MpcAttributeType.String
	at_F_mz.name = 'F_mz'
	at_F_mz.group = 'Data'
	at_F_mz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('F_mz')+'<br/>') + 
		html_par('f(z) e.g.:') +
		html_par('(z**2+y**2)**0.5') +
		html_end()
		)
	at_F_mz.setDefault('0')
	
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.QuantityVector3
	at_mass.name = 'mass'
	at_mass.group = 'Data'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mass')+'<br/>') + 
		html_par('The 3d mass vector') +
		html_end()
		)
	at_mass.dimension = u.F/u.L**2
	# at_mz.dimension = u.M
	
	
	# ctype
	at_ctype = MpcAttributeMetaData()
	at_ctype.type = MpcAttributeType.Integer
	at_ctype.visible = False;
	at_ctype.editable = False;
	at_ctype.name = 'ctype_constraint'
	at_ctype.group = 'Constraint'
	at_ctype.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ctype')+'<br/>') + 
		html_par('ctype') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Mass_Command','Mass Command')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'NodeMass'
	xom.addAttribute(at_Mode)
	xom.addAttribute(at_constant)
	xom.addAttribute(at_function)
	xom.addAttribute(at_F_mx)
	xom.addAttribute(at_F_my)
	xom.addAttribute(at_F_mz)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_ctype)
	
	
	# constant-dep
	xom.setVisibilityDependency(at_constant, at_mass)
	
	# function-dep
	xom.setVisibilityDependency(at_function, at_F_mx)
	xom.setVisibilityDependency(at_function, at_F_my)
	xom.setVisibilityDependency(at_function, at_F_mz)
	
	# auto-exclusive dependencies
	xom.setBooleanAutoExclusiveDependency(at_Mode, at_constant)
	xom.setBooleanAutoExclusiveDependency(at_Mode, at_function)

	
	return xom

def __control(xobj):
	
	d = my_data()
	
	Mode_at = xobj.getAttribute('Mode')
	if(Mode_at is None):
		raise Exception('Error: cannot find "Mode" attribute')
	d.Mode = Mode_at.string
	
	mass_at = xobj.getAttribute('mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "mass" attribute')
	d.mass = mass_at.quantityVector3
	
	F_mx_at = xobj.getAttribute('F_mx')
	if(F_mx_at is None):
		raise Exception('Error: cannot find "F_mx" attribute')
	d.F_mx = F_mx_at.string
	
	F_my_at = xobj.getAttribute('F_my')
	if(F_my_at is None):
		raise Exception('Error: cannot find "F_my" attribute')
	d.F_my = F_my_at.string
	
	F_mz_at = xobj.getAttribute('F_mz')
	if(F_mz_at is None):
		raise Exception('Error: cannot find "F_mz" attribute')
	d.F_mz = F_mz_at.string
	
	return d

def fillConditionRepresentationData(xobj, pos, data):
	'''
	Fills the 3D vector data.
	
	Set the pressure value
	at the z component, since the orientation is set to local
	'''
	mass = xobj.getAttribute('mass').quantityVector3.value
	Mode = xobj.getAttribute('Mode').string
	
	sfx = mx_at = xobj.getAttribute('F_mx').string		#string function mass x
	sfy = my_at = xobj.getAttribute('F_my').string		#string function mass y
	sfz = mz_at = xobj.getAttribute('F_mz').string		#string function mass z
	
	if (Mode == 'function'):
		
		seval = SpatialFunctionEval(pos)
		
		dx = seval.make(sfx)		#spatial function x
		dy = seval.make(sfy)		#spatial function y
		dz = seval.make(sfz)		#spatial function z
		
		data[0] = dx
		data[1] = dy
		data[2] = dz
	
	else:
		data[0] = mass.x
		data[1] = mass.y
		data[2] = mass.z
	

def makeConditionRepresentationData(xobj):
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Points
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = True
	d.on_edges = False
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = False
	
	return d

def fillNodeMassMap(pinfo):
	
	xobj = pinfo.condition.XObject
	
	d = __control(xobj)
	
	sfx = d.F_mx
	sfy = d.F_my
	sfz = d.F_mz
	
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	
	doc = App.caeDocument()
	for geom, subset in all_geom.items():
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		for i in subset.vertices:
			domain = mesh_of_geom.vertices[i]
			node_id = domain.id
			
			if (d.Mode == 'function'):
				seval = SpatialFunctionEval(domain)
				dx = seval.make(sfx)
				dy = seval.make(sfy)
				dz = seval.make(sfz)
			else:
				dx = d.mass.value.x
				dy = d.mass.value.y
				dz = d.mass.value.z
			
			mass_value = [dx, dy, dz, 0.0, 0.0,0.0]
			
			if node_id in pinfo.mass_to_node_map:
				for j in range(len(pinfo.mass_to_node_map[node_id])):
					pinfo.mass_to_node_map[node_id][j]+= mass_value[j]
			else:
				pinfo.mass_to_node_map[node_id] = mass_value
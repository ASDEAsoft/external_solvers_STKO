import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
from PyMpc.Math import *
from opensees.conditions.utils import SpatialFunctionEval

class my_data:
	def __init__(self):
		# attributes will be set in the __control method
		pass

def makeXObjectMetaData():
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Options'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') + 
		html_par('Choose between 2D and 3D') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('2D')
	
	# ModelType
	at_ModelType = MpcAttributeMetaData()
	at_ModelType.type = MpcAttributeType.String
	at_ModelType.name = 'ModelType'
	at_ModelType.group = 'Options'
	at_ModelType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ModelType')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_ModelType.sourceType = MpcAttributeSourceType.List
	at_ModelType.setSourceList(['U (Displacement)', 'U-P (Displacement+Pressure)', 'U-R (Displacement+Rotation)'])
	at_ModelType.setDefault('U (Displacement)')
	
	# InputType
	at_InputType = MpcAttributeMetaData()
	at_InputType.type = MpcAttributeType.String
	at_InputType.name = 'Input Type'
	at_InputType.group = 'Options'
	at_InputType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Input Type')+'<br/>') + 
		html_par('The input can be either a constant (a scalar) or a function of x,y and z coordinates (python script)') +
		html_end()
		)
	at_InputType.sourceType = MpcAttributeSourceType.List
	at_InputType.setSourceList(['Constant', 'Function'])
	at_InputType.setDefault('Constant')
	
	# Relative
	at_Relative = MpcAttributeMetaData()
	at_Relative.type = MpcAttributeType.Boolean
	at_Relative.name = 'Relative'
	at_Relative.group = 'Options'
	at_Relative.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Relative')+'<br/>') + 
		html_par(
			'If this option is turned ON, the imposed displacement specified by the user will be relative to the current displacement.'
			'This is useful if you want to fix a point to the current displacement.') +
		html_end()
		)
	at_Relative.setDefault(False)
	
	# Constant
	at_Constant = MpcAttributeMetaData()
	at_Constant.type = MpcAttributeType.Boolean
	at_Constant.name = 'Constant'
	at_Constant.group = 'Options'
	at_Constant.editable = False
	# Function
	at_Function = MpcAttributeMetaData()
	at_Function.type = MpcAttributeType.Boolean
	at_Function.name = 'Function'
	at_Function.group = 'Options'
	at_Function.editable = False
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Options'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') + 
		html_par('2D model') +
		html_end()
		)
	at_2D.editable = False
	
	# 3D
	at_3D = MpcAttributeMetaData()
	at_3D.type = MpcAttributeType.Boolean
	at_3D.name = '3D'
	at_3D.group = 'Options'
	at_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('3D')+'<br/>') + 
		html_par('3D model') +
		html_end()
		)
	at_3D.editable = False
	
	# U
	at_U = MpcAttributeMetaData()
	at_U.type = MpcAttributeType.Boolean
	at_U.name = 'U (Displacement)'
	at_U.group = 'Options'
	at_U.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U (Displacement)')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_U.editable = False
	
	# UP
	at_UP = MpcAttributeMetaData()
	at_UP.type = MpcAttributeType.Boolean
	at_UP.name = 'U-P (Displacement+Pressure)'
	at_UP.group = 'Options'
	at_UP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U-P (Displacement+Pressure)')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_UP.editable = False
	
	# UR
	at_UR = MpcAttributeMetaData()
	at_UR.type = MpcAttributeType.Boolean
	at_UR.name = 'U-R (Displacement+Rotation)'
	at_UR.group = 'Options'
	at_UR.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U-R (Displacement+Rotation)')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_UR.editable = False
	
	# Ux
	at_Ux_flag = MpcAttributeMetaData()
	at_Ux_flag.type = MpcAttributeType.Boolean
	at_Ux_flag.name = 'Ux'
	at_Ux_flag.group = 'Values'
	at_Ux_flag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ux')+'<br/>') + 
		html_par('Toggle to prescribe a value for Ux DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)

	at_Ux_val = MpcAttributeMetaData()
	at_Ux_val.type = MpcAttributeType.Real
	at_Ux_val.name = 'Ux value'
	at_Ux_val.group = 'Values'
	at_Ux_val.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ux value')+'<br/>') + 
		html_par('Prescribed value for Ux DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Ux_fun = MpcAttributeMetaData()
	at_Ux_fun.type = MpcAttributeType.String
	at_Ux_fun.name = 'Ux function'
	at_Ux_fun.group = 'Values'
	at_Ux_fun.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ux function')+'<br/>') + 
		html_par('Prescribed value for Ux DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	# Uy
	at_Uy_flag = MpcAttributeMetaData()
	at_Uy_flag.type = MpcAttributeType.Boolean
	at_Uy_flag.name = 'Uy'
	at_Uy_flag.group = 'Values'
	at_Uy_flag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Uy')+'<br/>') + 
		html_par('Toggle to prescribe a value for Uy DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Uy_val = MpcAttributeMetaData()
	at_Uy_val.type = MpcAttributeType.Real
	at_Uy_val.name = 'Uy value'
	at_Uy_val.group = 'Values'
	at_Uy_val.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Uy value')+'<br/>') + 
		html_par('Prescribed value for Uy DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Uy_fun = MpcAttributeMetaData()
	at_Uy_fun.type = MpcAttributeType.String
	at_Uy_fun.name = 'Uy function'
	at_Uy_fun.group = 'Values'
	at_Uy_fun.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Uy function')+'<br/>') + 
		html_par('Prescribed value for Uy DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	# Uz
	at_Uz_flag = MpcAttributeMetaData()
	at_Uz_flag.type = MpcAttributeType.Boolean
	at_Uz_flag.name = 'Uz'
	at_Uz_flag.group = 'Values'
	at_Uz_flag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Uz')+'<br/>') + 
		html_par('Toggle to prescribe a value for Uz DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Uz_val = MpcAttributeMetaData()
	at_Uz_val.type = MpcAttributeType.Real
	at_Uz_val.name = 'Uz value'
	at_Uz_val.group = 'Values'
	at_Uz_val.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Uz value')+'<br/>') + 
		html_par('Prescribed value for Uz DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Uz_fun = MpcAttributeMetaData()
	at_Uz_fun.type = MpcAttributeType.String
	at_Uz_fun.name = 'Uz function'
	at_Uz_fun.group = 'Values'
	at_Uz_fun.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Uz function')+'<br/>') + 
		html_par('Prescribed value for Uz DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	# Rx
	at_Rx_flag = MpcAttributeMetaData()
	at_Rx_flag.type = MpcAttributeType.Boolean
	at_Rx_flag.name = 'Rx'
	at_Rx_flag.group = 'Values'
	at_Rx_flag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rx')+'<br/>') + 
		html_par('Toggle to prescribe a value for Rx DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Rx_val = MpcAttributeMetaData()
	at_Rx_val.type = MpcAttributeType.Real
	at_Rx_val.name = 'Rx value'
	at_Rx_val.group = 'Values'
	at_Rx_val.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rx value')+'<br/>') + 
		html_par('Prescribed value for Rx DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Rx_fun = MpcAttributeMetaData()
	at_Rx_fun.type = MpcAttributeType.String
	at_Rx_fun.name = 'Rx function'
	at_Rx_fun.group = 'Values'
	at_Rx_fun.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rx function')+'<br/>') + 
		html_par('Prescribed value for Rx DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	# Ry
	at_Ry_flag = MpcAttributeMetaData()
	at_Ry_flag.type = MpcAttributeType.Boolean
	at_Ry_flag.name = 'Ry'
	at_Ry_flag.group = 'Values'
	at_Ry_flag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ry')+'<br/>') + 
		html_par('Toggle to prescribe a value for Ry DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Ry_val = MpcAttributeMetaData()
	at_Ry_val.type = MpcAttributeType.Real
	at_Ry_val.name = 'Ry value'
	at_Ry_val.group = 'Values'
	at_Ry_val.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ry value')+'<br/>') + 
		html_par('Prescribed value for Ry DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Ry_fun = MpcAttributeMetaData()
	at_Ry_fun.type = MpcAttributeType.String
	at_Ry_fun.name = 'Ry function'
	at_Ry_fun.group = 'Values'
	at_Ry_fun.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ry function')+'<br/>') + 
		html_par('Prescribed value for Ry DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	# Rz_3D
	at_Rz_flag = MpcAttributeMetaData()
	at_Rz_flag.type = MpcAttributeType.Boolean
	at_Rz_flag.name = 'Rz'
	at_Rz_flag.group = 'Values'
	at_Rz_flag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rz')+'<br/>') + 
		html_par('Toggle to prescribe a value for Rz DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Rz_val = MpcAttributeMetaData()
	at_Rz_val.type = MpcAttributeType.Real
	at_Rz_val.name = 'Rz value'
	at_Rz_val.group = 'Values'
	at_Rz_val.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rz value')+'<br/>') + 
		html_par('Prescribed value for Rz DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_Rz_fun = MpcAttributeMetaData()
	at_Rz_fun.type = MpcAttributeType.String
	at_Rz_fun.name = 'Rz function'
	at_Rz_fun.group = 'Values'
	at_Rz_fun.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rz function')+'<br/>') + 
		html_par('Prescribed value for Rz DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	# P
	at_P_flag = MpcAttributeMetaData()
	at_P_flag.type = MpcAttributeType.Boolean
	at_P_flag.name = 'P'
	at_P_flag.group = 'Values'
	at_P_flag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('P')+'<br/>') + 
		html_par('Toggle to prescribe a value for P DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_P_val = MpcAttributeMetaData()
	at_P_val.type = MpcAttributeType.Real
	at_P_val.name = 'P value'
	at_P_val.group = 'Values'
	at_P_val.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('P value')+'<br/>') + 
		html_par('Prescribed value for P DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	at_P_fun = MpcAttributeMetaData()
	at_P_fun.type = MpcAttributeType.String
	at_P_fun.name = 'P function'
	at_P_fun.group = 'Values'
	at_P_fun.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('P value')+'<br/>') + 
		html_par('Prescribed value for P DOF') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	# ctype
	at_ctype = MpcAttributeMetaData()
	at_ctype.type = MpcAttributeType.Integer
	at_ctype.visible = False;
	at_ctype.editable = False;
	at_ctype.name = 'ctype_constraint'
	at_ctype.group = 'Options'
	at_ctype.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ctype')+'<br/>') + 
		html_par('ctype') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Sp_Command','Sp Command')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'sp(prescribedNodalValue)'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_ModelType)
	xom.addAttribute(at_InputType)
	xom.addAttribute(at_Relative)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_U)
	xom.addAttribute(at_UP)
	xom.addAttribute(at_UR)
	xom.addAttribute(at_Constant)
	xom.addAttribute(at_Function)
	xom.addAttribute(at_Ux_flag)
	xom.addAttribute(at_Ux_val)
	xom.addAttribute(at_Ux_fun)
	xom.addAttribute(at_Uy_flag)
	xom.addAttribute(at_Uy_val)
	xom.addAttribute(at_Uy_fun)
	xom.addAttribute(at_Uz_flag)
	xom.addAttribute(at_Uz_val)
	xom.addAttribute(at_Uz_fun)
	xom.addAttribute(at_Rx_flag)
	xom.addAttribute(at_Rx_val)
	xom.addAttribute(at_Rx_fun)
	xom.addAttribute(at_Ry_flag)
	xom.addAttribute(at_Ry_val)
	xom.addAttribute(at_Ry_fun)
	xom.addAttribute(at_Rz_flag)
	xom.addAttribute(at_Rz_val)
	xom.addAttribute(at_Rz_fun)
	xom.addAttribute(at_P_flag)
	xom.addAttribute(at_P_val)
	xom.addAttribute(at_P_fun)
	xom.addAttribute(at_ctype)
	
	
	# visibility dependencies
	
	# UP
	xom.setVisibilityDependency(at_UP, at_P_flag)
	xom.setVisibilityDependency(at_UP, at_P_val)
	xom.setVisibilityDependency(at_UP, at_P_fun)
	
	# UR
	xom.setVisibilityDependency(at_UR, at_Rx_flag)
	xom.setVisibilityDependency(at_UR, at_Ry_flag)
	xom.setVisibilityDependency(at_UR, at_Rz_flag)
	xom.setVisibilityDependency(at_UR, at_Rx_val)
	xom.setVisibilityDependency(at_UR, at_Ry_val)
	xom.setVisibilityDependency(at_UR, at_Rz_val)
	xom.setVisibilityDependency(at_UR, at_Rx_fun)
	xom.setVisibilityDependency(at_UR, at_Ry_fun)
	xom.setVisibilityDependency(at_UR, at_Rz_fun)
	
	# 3D
	xom.setVisibilityDependency(at_3D, at_Uz_flag)
	xom.setVisibilityDependency(at_3D, at_Rx_flag)
	xom.setVisibilityDependency(at_3D, at_Ry_flag)
	xom.setVisibilityDependency(at_3D, at_Uz_val)
	xom.setVisibilityDependency(at_3D, at_Rx_val)
	xom.setVisibilityDependency(at_3D, at_Ry_val)
	xom.setVisibilityDependency(at_3D, at_Uz_fun)
	xom.setVisibilityDependency(at_3D, at_Rx_fun)
	xom.setVisibilityDependency(at_3D, at_Ry_fun)
	
	# input type
	xom.setVisibilityDependency(at_Constant, at_Ux_val)
	xom.setVisibilityDependency(at_Constant, at_Uy_val)
	xom.setVisibilityDependency(at_Constant, at_Uz_val)
	xom.setVisibilityDependency(at_Constant, at_Rx_val)
	xom.setVisibilityDependency(at_Constant, at_Ry_val)
	xom.setVisibilityDependency(at_Constant, at_Rz_val)
	xom.setVisibilityDependency(at_Constant,  at_P_val)
	xom.setVisibilityDependency(at_Function, at_Ux_fun)
	xom.setVisibilityDependency(at_Function, at_Uy_fun)
	xom.setVisibilityDependency(at_Function, at_Uz_fun)
	xom.setVisibilityDependency(at_Function, at_Rx_fun)
	xom.setVisibilityDependency(at_Function, at_Ry_fun)
	xom.setVisibilityDependency(at_Function, at_Rz_fun)
	xom.setVisibilityDependency(at_Function,  at_P_fun)
	
	# flag to value
	xom.setVisibilityDependency(at_Ux_flag, at_Ux_val)
	xom.setVisibilityDependency(at_Ux_flag, at_Ux_fun)
	xom.setVisibilityDependency(at_Uy_flag, at_Uy_val)
	xom.setVisibilityDependency(at_Uy_flag, at_Uy_fun)
	xom.setVisibilityDependency(at_Uz_flag, at_Uz_val)
	xom.setVisibilityDependency(at_Uz_flag, at_Uz_fun)
	xom.setVisibilityDependency(at_Rx_flag, at_Rx_val)
	xom.setVisibilityDependency(at_Rx_flag, at_Rx_fun)
	xom.setVisibilityDependency(at_Ry_flag, at_Ry_val)
	xom.setVisibilityDependency(at_Ry_flag, at_Ry_fun)
	xom.setVisibilityDependency(at_Rz_flag, at_Rz_val)
	xom.setVisibilityDependency(at_Rz_flag, at_Rz_fun)
	xom.setVisibilityDependency(at_P_flag, at_P_val)
	xom.setVisibilityDependency(at_P_flag, at_P_fun)
	
	# auto-exclusive dependencies
	
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	# U, UP or UR
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_U)
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_UP)
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_UR)
	
	# constant or function
	xom.setBooleanAutoExclusiveDependency(at_InputType, at_Constant)
	xom.setBooleanAutoExclusiveDependency(at_InputType, at_Function)
	
	return xom

def makeConditionRepresentationData(xobj):
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.ConstraintGlyph
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = True
	d.on_edges = True
	d.on_faces = True
	d.on_solids = True
	d.on_interactions = False
	return d

def controlInternal(pinfo, xobj, node):
	
	# util: get attributes and check it
	def get_xobj_attribute(attribute_name):
		attribute = xobj.getAttribute(attribute_name)
		if attribute is None:
			raise Exception('Error: cannot find "{}" attribute'.format(attribute_name))
		return attribute
	
	# options
	is_3d = get_xobj_attribute('3D').boolean
	is_constant = get_xobj_attribute('Constant').boolean
	is_relative = get_xobj_attribute('Relative').boolean
	UR = get_xobj_attribute('U-R (Displacement+Rotation)').boolean
	UP = get_xobj_attribute('U-P (Displacement+Pressure)').boolean
	
	# flags
	Ux = get_xobj_attribute('Ux').boolean
	Uy = get_xobj_attribute('Uy').boolean
	if is_3d:
		Uz = get_xobj_attribute('Uz').boolean
		if UR:
			Rx = get_xobj_attribute('Rx').boolean
			Ry = get_xobj_attribute('Ry').boolean
			Rz = get_xobj_attribute('Rz').boolean
	else:
		if UR:
			Rz = get_xobj_attribute('Rz').boolean
	if UP:
		P = get_xobj_attribute('P').boolean
		
	# util: write value
	
	def write_value(attribute_prefix, dof_id):
		# get constant or function-based value
		if is_constant:
			value = get_xobj_attribute('{} value'.format(attribute_prefix)).real
		else:
			seval = SpatialFunctionEval(node.position)
			value = seval.make(get_xobj_attribute('{} function'.format(attribute_prefix)).string)
		# in case of relative displacement....
		if is_relative:
			current_value = value
			value = '[expr {} + [nodeDisp {} {}]]'.format(current_value, node.id, dof_id)
		# write the sp command
		pinfo.out_file.write('{}{}sp {} {} {}\n'.format(pinfo.indent, pinfo.tabIndent, node.id, dof_id, value))
		
	# values
	if Ux:
		write_value('Ux', 1)
	if Uy:
		write_value('Uy', 2)
	if is_3d:
		if Uz:
			write_value('Uz', 3)
		if UR:
			if Rx:
				write_value('Rx', 4)
			if Ry:
				write_value('Ry', 5)
			if Rz:
				write_value('Rz', 6)
		elif UP:
			write_value('P', 4)
	else:
		if UR:
			if Rz:
				write_value('Rz', 3)
		elif UP:
			write_value('P', 3)

def __process_sp(pinfo, xobj, doc, all_geom, is_partitioned, process_id, process_block_count):
	first_done = False
	for geom, subset in all_geom.items():
		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		'''
		vertices
		'''
		for i in subset.vertices:
			domain = mesh_of_geom.vertices[i]
			node_id = domain.id
			if not is_partitioned :
				pinfo.out_file.write('{} # sp node\n'.format(pinfo.indent))
			if is_partitioned :
				if not doc.mesh.partitionData.isNodeOnParition(node_id, process_id):
					continue
			if is_partitioned :
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
					first_done = True
					pinfo.out_file.write('{} # sp node\n'.format(pinfo.indent))
			controlInternal(pinfo, xobj, domain)
		'''
		edges
		'''
		node_list = {}
		for i in subset.edges:
			domain = mesh_of_geom.edges[i]
			if not is_partitioned :
				pinfo.out_file.write('{} # sp edge\n'.format(pinfo.indent))
			for elem in domain.elements:
				for node in elem.nodes:
					node_list[node.id] = node
		for node_id, node in node_list.items():
			if is_partitioned :
				if not doc.mesh.partitionData.isNodeOnParition(node_id, process_id):
					continue
			if is_partitioned :
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
					first_done = True
					pinfo.out_file.write('{} # sp edge\n'.format(pinfo.indent))
			controlInternal(pinfo, xobj, node)
		'''
		faces
		'''
		node_list = {}
		for i in subset.faces:
			domain = mesh_of_geom.faces[i]
			if not is_partitioned :
				pinfo.out_file.write('{} # sp face\n'.format(pinfo.indent))
			for elem in domain.elements:
				for node in elem.nodes:
					node_list[node.id] = node
		for node_id, node in node_list.items():
			if is_partitioned :
				if not doc.mesh.partitionData.isNodeOnParition(node_id, process_id):
					continue
			if is_partitioned :
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
					first_done = True
					pinfo.out_file.write('{} # sp face\n'.format(pinfo.indent))
			controlInternal(pinfo, xobj, node)
		'''
		solids
		'''
		node_list = {}
		for i in subset.solids:
			domain = mesh_of_geom.solids[i]
			for elem in domain.elements:
				if not is_partitioned :
					pinfo.out_file.write('{} # sp face\n'.format(pinfo.indent))
				for node in elem.nodes:
					node_list[node.id] = node
		for node_id, node in node_list.items():
			if is_partitioned :
				if not doc.mesh.partitionData.isNodeOnParition(node_id, process_id):
					continue
			if is_partitioned :
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', process_id, '} {'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', process_id, '} {'))
					first_done = True
					pinfo.out_file.write('{} # sp solids\n'.format(pinfo.indent))
			controlInternal(pinfo, xobj, node)
			
	if is_partitioned :
		if first_done:
			process_block_count += 1
		if process_block_count > 0 and first_done:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count

def writeTcl_sp(pinfo, xobj):
	
	# sp $nodeTag $dofTag $dofValue

	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName

	doc = App.caeDocument()
	
	tag = xobj.parent.componentId
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			process_block_count = __process_sp(pinfo, xobj, doc, all_geom, is_partitioned, process_id, process_block_count)
	else :
		__process_sp(pinfo, xobj, doc, all_geom, is_partitioned, 0, 0)
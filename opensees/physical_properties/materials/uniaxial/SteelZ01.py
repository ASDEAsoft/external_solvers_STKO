# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# fy
	at_fy = MpcAttributeMetaData()
	at_fy.type = MpcAttributeType.QuantityScalar
	at_fy.name = 'fy'
	at_fy.group = 'Non-linear'
	at_fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fy')+'<br/>') + 
		html_par('yield strength bare steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','ConcreteZ01')+'<br/>') +
		html_end()
		)
	at_fy.dimension = u.F/u.L**2
	
	# E0
	at_E0 = MpcAttributeMetaData()
	at_E0.type = MpcAttributeType.QuantityScalar
	at_E0.name = 'E0'
	at_E0.group = 'Non-linear'
	at_E0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E0')+'<br/>') + 
		html_par('initial stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','ConcreteZ01')+'<br/>') +
		html_end()
		)
	at_E0.dimension = u.F/u.L**2
	
	# fpc
	at_fpc = MpcAttributeMetaData()
	at_fpc.type = MpcAttributeType.QuantityScalar
	at_fpc.name = 'fpc'
	at_fpc.group = 'Non-linear'
	at_fpc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fpc')+'<br/>') + 
		html_par('Concrete compressive strength at 28 days (compression is negative)*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','ConcreteZ01')+'<br/>') +
		html_end()
		)
	at_fpc.dimension = u.F/u.L**2
	
	# rou
	at_rou = MpcAttributeMetaData()
	at_rou.type = MpcAttributeType.Real
	at_rou.name = 'rou'
	at_rou.group = 'Non-linear'
	at_rou.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rou')+'<br/>') + 
		html_par('steel ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','ConcreteZ01')+'<br/>') +
		html_end()
		)
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('to activate "ac" and "rc"') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','ConcreteZ01')+'<br/>') +
		html_end()
		)
	
	# ac
	at_ac = MpcAttributeMetaData()
	at_ac.type = MpcAttributeType.Real
	at_ac.name = 'ac'
	at_ac.group = 'Optional parameters'
	at_ac.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ac')+'<br/>') + 
		html_par('unloading path parameter (default = 1.9)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','ConcreteZ01')+'<br/>') +
		html_end()
		)
	at_ac.setDefault(1.9)
	
	# rc
	at_rc = MpcAttributeMetaData()
	at_rc.type = MpcAttributeType.Real
	at_rc.name = 'rc'
	at_rc.group = 'Optional parameters'
	at_rc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rc')+'<br/>') + 
		html_par('reloading path parameter (default = 10.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','ConcreteZ01')+'<br/>') +
		html_end()
		)
	at_rc.setDefault(10.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'SteelZ01'
	xom.Xgroup = 'Steel and Reinforcing-Steel Materials'
	xom.addAttribute(at_fy)
	xom.addAttribute(at_E0)
	xom.addAttribute(at_fpc)
	xom.addAttribute(at_rou)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_ac)
	xom.addAttribute(at_rc)
	
	# ac, rc-dep
	xom.setVisibilityDependency(at_Optional, at_ac)
	xom.setVisibilityDependency(at_Optional, at_rc)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial SteelZ01 tag? fy? E0? fpc? rou? <ac?> <rc?>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fy_at = xobj.getAttribute('fy')
	if(fy_at is None):
		raise Exception('Error: cannot find "fy" attribute')
	fy = fy_at.quantityScalar
	
	E0_at = xobj.getAttribute('E0')
	if(E0_at is None):
		raise Exception('Error: cannot find "E0" attribute')
	E0 = E0_at.quantityScalar
	
	fpc_at = xobj.getAttribute('fpc')
	if(fpc_at is None):
		raise Exception('Error: cannot find "fpc" attribute')
	fpc = fpc_at.quantityScalar
	
	rou_at = xobj.getAttribute('rou')
	if(rou_at is None):
		raise Exception('Error: cannot find "rou" attribute')
	rou = rou_at.real
	
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		ac_at = xobj.getAttribute('ac')
		if(ac_at is None):
			raise Exception('Error: cannot find "ac" attribute')
		ac = ac_at.real
		
		rc_at = xobj.getAttribute('rc')
		if(rc_at is None):
			raise Exception('Error: cannot find "rc" attribute')
		rc = rc_at.real
		
		sopt += '{} {}'.format(ac, rc)
	
	
	str_tcl = '{}uniaxialMaterial SteelZ01 {} {} {} {} {} {}\n'.format(pinfo.indent, tag, fy.value, E0.value, fpc.value, rou, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
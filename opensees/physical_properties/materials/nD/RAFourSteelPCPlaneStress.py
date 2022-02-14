import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Non linear'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') + 
		html_par('material density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	#at_rho.dimension = u.M/u.L**3
	
	# UniaxiaMatTag1
	at_UniaxiaMatTag1 = MpcAttributeMetaData()
	at_UniaxiaMatTag1.type = MpcAttributeType.Index
	at_UniaxiaMatTag1.name = 'UniaxiaMatTag1'
	at_UniaxiaMatTag1.group = 'Non linear'
	at_UniaxiaMatTag1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('UniaxiaMatTag1')+'<br/>') + 
		html_par('integer tag identifying material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	at_UniaxiaMatTag1.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_UniaxiaMatTag1.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# UniaxiaMatTag2
	at_UniaxiaMatTag2 = MpcAttributeMetaData()
	at_UniaxiaMatTag2.type = MpcAttributeType.Index
	at_UniaxiaMatTag2.name = 'UniaxiaMatTag2'
	at_UniaxiaMatTag2.group = 'Non linear'
	at_UniaxiaMatTag2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('UniaxiaMatTag2')+'<br/>') + 
		html_par('integer tag identifying material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	at_UniaxiaMatTag2.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_UniaxiaMatTag2.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# UniaxiaMatTag3
	at_UniaxiaMatTag3 = MpcAttributeMetaData()
	at_UniaxiaMatTag3.type = MpcAttributeType.Index
	at_UniaxiaMatTag3.name = 'UniaxiaMatTag3'
	at_UniaxiaMatTag3.group = 'Non linear'
	at_UniaxiaMatTag3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('UniaxiaMatTag3')+'<br/>') + 
		html_par('integer tag identifying material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	at_UniaxiaMatTag3.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_UniaxiaMatTag3.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# UniaxiaMatTag4
	at_UniaxiaMatTag4 = MpcAttributeMetaData()
	at_UniaxiaMatTag4.type = MpcAttributeType.Index
	at_UniaxiaMatTag4.name = 'UniaxiaMatTag4'
	at_UniaxiaMatTag4.group = 'Non linear'
	at_UniaxiaMatTag4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('UniaxiaMatTag4')+'<br/>') + 
		html_par('integer tag identifying material') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	at_UniaxiaMatTag4.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_UniaxiaMatTag4.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# angle1
	at_angle1 = MpcAttributeMetaData()
	at_angle1.type = MpcAttributeType.Real
	at_angle1.name = 'angle1'
	at_angle1.group = 'Non linear'
	at_angle1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('angle1')+'<br/>') + 
		html_par('angle of i\'th (steel or tendon) layer to x coordinate') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	
	# angle2
	at_angle2 = MpcAttributeMetaData()
	at_angle2.type = MpcAttributeType.Real
	at_angle2.name = 'angle2'
	at_angle2.group = 'Non linear'
	at_angle2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('angle2')+'<br/>') + 
		html_par('angle of i\'th (steel or tendon) layer to x coordinate') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	
	# rou1
	at_rou1 = MpcAttributeMetaData()
	at_rou1.type = MpcAttributeType.Real
	at_rou1.name = 'rou1'
	at_rou1.group = 'Non linear'
	at_rou1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rou1')+'<br/>') + 
		html_par('steel ratio of the i\'th layer.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	
	# rou2
	at_rou2 = MpcAttributeMetaData()
	at_rou2.type = MpcAttributeType.Real
	at_rou2.name = 'rou2'
	at_rou2.group = 'Non linear'
	at_rou2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rou2')+'<br/>') + 
		html_par('steel ratio of the i\'th layer.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	
	# pstrain
	at_pstrain = MpcAttributeMetaData()
	at_pstrain.type = MpcAttributeType.Real
	at_pstrain.name = 'pstrain'
	at_pstrain.group = 'Non linear'
	at_pstrain.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pstrain')+'<br/>') + 
		html_par('initial strain in tendons') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	
	# fpc
	at_fpc = MpcAttributeMetaData()
	at_fpc.type = MpcAttributeType.QuantityScalar
	at_fpc.name = 'fpc'
	at_fpc.group = 'Non linear'
	at_fpc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fpc')+'<br/>') + 
		html_par('compressive strength of concrete') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	at_fpc.dimension = u.F/u.L**2
	
	# fyT
	at_fyT = MpcAttributeMetaData()
	at_fyT.type = MpcAttributeType.QuantityScalar
	at_fyT.name = 'fyT'
	at_fyT.group = 'Non linear'
	at_fyT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fyT')+'<br/>') + 
		html_par('yield strength of tendons') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	at_fyT.dimension = u.F/u.L**2
	
	# fy
	at_fy = MpcAttributeMetaData()
	at_fy.type = MpcAttributeType.QuantityScalar
	at_fy.name = 'fy'
	at_fy.group = 'Non linear'
	at_fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fy')+'<br/>') + 
		html_par('yield strength of steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	at_fy.dimension = u.F/u.L**2
	
	# E0
	at_E0 = MpcAttributeMetaData()
	at_E0.type = MpcAttributeType.QuantityScalar
	at_E0.name = 'E0'
	at_E0.group = 'Non linear'
	at_E0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E0')+'<br/>') + 
		html_par('initial stiffness of steel (Young\'s Modulus)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	at_E0.dimension = u.F/u.L**2
	
	# epsc0
	at_epsc0 = MpcAttributeMetaData()
	at_epsc0.type = MpcAttributeType.Real
	at_epsc0.name = 'epsc0'
	at_epsc0.group = 'Non linear'
	at_epsc0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsc0')+'<br/>') + 
		html_par('compressive strain of concrete') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Concrete_Materials','Plane Stress Concrete Materials')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'RAFourSteelPCPlaneStress'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_rho)
	xom.addAttribute(at_UniaxiaMatTag1)
	xom.addAttribute(at_UniaxiaMatTag2)
	xom.addAttribute(at_UniaxiaMatTag3)
	xom.addAttribute(at_UniaxiaMatTag4)
	xom.addAttribute(at_angle1)
	xom.addAttribute(at_angle2)
	xom.addAttribute(at_rou1)
	xom.addAttribute(at_rou2)
	xom.addAttribute(at_pstrain)
	xom.addAttribute(at_fpc)
	xom.addAttribute(at_fyT)
	xom.addAttribute(at_fy)
	xom.addAttribute(at_E0)
	xom.addAttribute(at_epsc0)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial RAFourSteelPCPlaneStress matTag? rho? UniaxiaMatTag1? UniaxiaMatTag2? UniaxiaMatTag3?
	# UniaxiaMatTag4? angle1? angle2? rou1? rou2? pstrain? fpc? fyT? fy? E0? epsc0?
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	rho_at = xobj.getAttribute('rho')
	if(rho_at is None):
		raise Exception('Error: cannot find "rho" attribute')
	rho = rho_at.quantityScalar
	
	UniaxiaMatTag1_at = xobj.getAttribute('UniaxiaMatTag1')
	if(UniaxiaMatTag1_at is None):
		raise Exception('Error: cannot find "UniaxiaMatTag1" attribute')
	UniaxiaMatTag1 = UniaxiaMatTag1_at.index
	
	UniaxiaMatTag2_at = xobj.getAttribute('UniaxiaMatTag2')
	if(UniaxiaMatTag2_at is None):
		raise Exception('Error: cannot find "UniaxiaMatTag2" attribute')
	UniaxiaMatTag2 = UniaxiaMatTag2_at.index
	
	UniaxiaMatTag3_at = xobj.getAttribute('UniaxiaMatTag3')
	if(UniaxiaMatTag3_at is None):
		raise Exception('Error: cannot find "UniaxiaMatTag3" attribute')
	UniaxiaMatTag3 = UniaxiaMatTag3_at.index
	
	UniaxiaMatTag4_at = xobj.getAttribute('UniaxiaMatTag4')
	if(UniaxiaMatTag4_at is None):
		raise Exception('Error: cannot find "UniaxiaMatTag4" attribute')
	UniaxiaMatTag4 = UniaxiaMatTag4_at.index
	
	angle1_at = xobj.getAttribute('angle1')
	if(angle1_at is None):
		raise Exception('Error: cannot find "angle1" attribute')
	angle1 = angle1_at.real
	
	angle2_at = xobj.getAttribute('angle2')
	if(angle2_at is None):
		raise Exception('Error: cannot find "angle2" attribute')
	angle2 = angle2_at.real
	
	rou1_at = xobj.getAttribute('rou1')
	if(rou1_at is None):
		raise Exception('Error: cannot find "rou1" attribute')
	rou1 = rou1_at.real
	
	rou2_at = xobj.getAttribute('rou2')
	if(rou2_at is None):
		raise Exception('Error: cannot find "rou2" attribute')
	rou2 = rou2_at.real
	
	pstrain_at = xobj.getAttribute('pstrain')
	if(pstrain_at is None):
		raise Exception('Error: cannot find "pstrain" attribute')
	pstrain = pstrain_at.real
	
	fpc_at = xobj.getAttribute('fpc')
	if(fpc_at is None):
		raise Exception('Error: cannot find "fpc" attribute')
	fpc = fpc_at.quantityScalar
	
	fyT_at = xobj.getAttribute('fyT')
	if(fyT_at is None):
		raise Exception('Error: cannot find "fyT" attribute')
	fyT = fyT_at.quantityScalar
	
	fy_at = xobj.getAttribute('fy')
	if(fy_at is None):
		raise Exception('Error: cannot find "fy" attribute')
	fy = fy_at.quantityScalar
	
	E0_at = xobj.getAttribute('E0')
	if(E0_at is None):
		raise Exception('Error: cannot find "E0" attribute')
	E0 = E0_at.quantityScalar
	
	epsc0_at = xobj.getAttribute('epsc0')
	if(epsc0_at is None):
		raise Exception('Error: cannot find "epsc0" attribute')
	epsc0 = epsc0_at.real
	
	str_tcl = '{}nDMaterial RAFourSteelPCPlaneStress {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, rho.value, UniaxiaMatTag1, UniaxiaMatTag2, UniaxiaMatTag3, UniaxiaMatTag4, angle1,
			angle2, rou1, rou2, pstrain, fpc.value, fyT.value, fy.value, E0.value, epsc0)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
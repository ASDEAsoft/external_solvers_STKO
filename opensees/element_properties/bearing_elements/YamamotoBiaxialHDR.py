import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Tp
	at_Tp = MpcAttributeMetaData()
	at_Tp.type = MpcAttributeType.Integer
	at_Tp.name = 'Tp'
	at_Tp.group = 'Group'
	at_Tp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Tp')+'<br/>') +
		html_par('compound type = 1 : X0.6R manufactured by Bridgestone corporation.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/YamamotoBiaxialHDR_Element','YamamotoBiaxialHDR Element')+'<br/>') +
		html_end()
		)
	at_Tp.setDefault(1)
	
	# DDo
	at_DDo = MpcAttributeMetaData()
	at_DDo.type = MpcAttributeType.QuantityScalar
	at_DDo.name = 'DDo'
	at_DDo.group = 'Group'
	at_DDo.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('DDo')+'<br/>') +
		html_par('outer diameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/YamamotoBiaxialHDR_Element','YamamotoBiaxialHDR Element')+'<br/>') +
		html_end()
		)
	at_DDo.dimension = u.L
	
	# DDi
	at_DDi = MpcAttributeMetaData()
	at_DDi.type = MpcAttributeType.QuantityScalar
	at_DDi.name = 'DDi'
	at_DDi.group = 'Group'
	at_DDi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('DDi')+'<br/>') +
		html_par('bore diameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/YamamotoBiaxialHDR_Element','YamamotoBiaxialHDR Element')+'<br/>') +
		html_end()
		)
	at_DDi.dimension = u.L
	
	# Hr
	at_Hr = MpcAttributeMetaData()
	at_Hr.type = MpcAttributeType.QuantityScalar
	at_Hr.name = 'Hr'
	at_Hr.group = 'Group'
	at_Hr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Hr')+'<br/>') +
		html_par('total thickness of rubber layer') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/YamamotoBiaxialHDR_Element','YamamotoBiaxialHDR Element')+'<br/>') +
		html_end()
		)
	at_Hr.dimension = u.L
	
	# -coRS
	at_coRS = MpcAttributeMetaData()
	at_coRS.type = MpcAttributeType.Boolean
	at_coRS.name = '-coRS'
	at_coRS.group = 'Group'
	at_coRS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-coRS')+'<br/>') +
		html_par('coefficients for shear stress components of τr and τs') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/YamamotoBiaxialHDR_Element','YamamotoBiaxialHDR Element')+'<br/>') +
		html_end()
		)
	
	# cr
	at_cr = MpcAttributeMetaData()
	at_cr.type = MpcAttributeType.Real
	at_cr.name = 'cr'
	at_cr.group = '-coRS'
	at_cr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cr')+'<br/>') +
		html_par('coefficients for shear stress components of τr') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/YamamotoBiaxialHDR_Element','YamamotoBiaxialHDR Element')+'<br/>') +
		html_end()
		)
	
	# cs
	at_cs = MpcAttributeMetaData()
	at_cs.type = MpcAttributeType.Real
	at_cs.name = 'cs'
	at_cs.group = '-coRS'
	at_cs.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cs')+'<br/>') +
		html_par('coefficients for shear stress components of τs') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/YamamotoBiaxialHDR_Element','YamamotoBiaxialHDR Element')+'<br/>') +
		html_end()
		)
	
	# -orient
	at_orient = MpcAttributeMetaData()
	at_orient.type = MpcAttributeType.Boolean
	at_orient.name = '-orient'
	at_orient.group = 'Group'
	at_orient.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-orient')+'<br/>') +
		html_par('activate vector components in global coordinates') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/YamamotoBiaxialHDR_Element','YamamotoBiaxialHDR Element')+'<br/>') +
		html_end()
		)
	
	
	# -mass
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.Boolean
	at_mass.name = '-mass'
	at_mass.group = 'Group'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-mass')+'<br/>') +
		html_par('element mass') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/YamamotoBiaxialHDR_Element','YamamotoBiaxialHDR Element')+'<br/>') +
		html_end()
		)
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.QuantityScalar
	at_m.name = 'm'
	at_m.group = '-mass'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') +
		html_par('element mass') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/YamamotoBiaxialHDR_Element','YamamotoBiaxialHDR Element')+'<br/>') +
		html_end()
		)
	# at_m.dimension = u.M
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'YamamotoBiaxialHDR'
	xom.addAttribute(at_Tp)
	xom.addAttribute(at_DDo)
	xom.addAttribute(at_DDi)
	xom.addAttribute(at_Hr)
	xom.addAttribute(at_coRS)
	xom.addAttribute(at_cr)
	xom.addAttribute(at_cs)
	xom.addAttribute(at_orient)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_m)
	
	
	# visibility dependencies
	
	# cr, cs-dep
	xom.setVisibilityDependency(at_coRS, at_cr)
	xom.setVisibilityDependency(at_coRS, at_cs)
	
	# m-dep
	xom.setVisibilityDependency(at_mass, at_m)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	# YamamotoBiaxialHDR eleTag? iNode? jNode? Tp? DDo? DDi? Hr?  <-coRS cr? cs?> <-orient <x1? x2? x3?> y1? y2? y3?> <-mass m?>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	pinfo.updateModelBuilder(3,6)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=2):
		raise Exception('Error: invalid number of nodes')
	
	Tp_at = xobj.getAttribute('Tp')
	if(Tp_at is None):
		raise Exception('Error: cannot find "Tp" attribute')
	Tp = Tp_at.integer
	
	DDo_at = xobj.getAttribute('DDo')
	if(DDo_at is None):
		raise Exception('Error: cannot find "DDo" attribute')
	DDo = DDo_at.quantityScalar.value
	
	DDi_at = xobj.getAttribute('DDi')
	if(DDi_at is None):
		raise Exception('Error: cannot find "DDi" attribute')
	DDi = DDi_at.quantityScalar.value
	
	Hr_at = xobj.getAttribute('Hr')
	if(Hr_at is None):
		raise Exception('Error: cannot find "Hr" attribute')
	Hr = Hr_at.quantityScalar.value
	
	
	# optional paramters
	sopt = ''
	
	coRS_at = xobj.getAttribute('-coRS')
	if(coRS_at is None):
		raise Exception('Error: cannot find "coRS" attribute')
	coRS = coRS_at.boolean
	if coRS:
		
		cr_at = xobj.getAttribute('cr')
		if(cr_at is None):
			raise Exception('Error: cannot find "cr" attribute')
		cr = cr_at.real
		
		cs_at = xobj.getAttribute('cs')
		if(cs_at is None):
			raise Exception('Error: cannot find "cs" attribute')
		cs = cs_at.real
		sopt += ' -coRS {} {}'.format(cr,cs)
	
	
	orient_at = xobj.getAttribute('-orient')
	if(orient_at is None):
		raise Exception('Error: cannot find "-orient" attribute')
	if orient_at.boolean:
		vect_x=elem.orientation.computeOrientation().col(0)
		vect_y=elem.orientation.computeOrientation().col(1)
		
		sopt += ' -orient {} {} {} {} {} {}'.format (vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
		
	mass_at = xobj.getAttribute('-mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "mass" attribute')
	mass = mass_at.boolean
	if mass:
		m_at = xobj.getAttribute('m')
		if(m_at is None):
			raise Exception('Error: cannot find "m" attribute')
		m = m_at.quantityScalar
		
		sopt += ' -mass {}'.format(m.value)
	
	
	str_tcl = '{}element YamamotoBiaxialHDR {}{} {} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, Tp, DDo, DDi, Hr, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
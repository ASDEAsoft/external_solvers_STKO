import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# nSpring
	at_nSpring = MpcAttributeMetaData()
	at_nSpring.type = MpcAttributeType.Integer
	at_nSpring.name = 'nSpring'
	at_nSpring.group = 'Group'
	at_nSpring.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nSpring')+'<br/>') +
		html_par('number of springs') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MultipleShearSpring_Element','MultipleShearSpring Element')+'<br/>') +
		html_end()
		)
	
	# -lim
	at_lim = MpcAttributeMetaData()
	at_lim.type = MpcAttributeType.Boolean
	at_lim.name = '-lim'
	at_lim.group = 'Group'
	at_lim.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-lim')+'<br/>') +
		html_par('minimum deformation to calculate equivalent coefficient (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MultipleShearSpring_Element','MultipleShearSpring Element')+'<br/>') +
		html_end()
		)
	
	# dsp
	at_dsp = MpcAttributeMetaData()
	at_dsp.type = MpcAttributeType.Real
	at_dsp.name = 'dsp'
	at_dsp.group = '-lim'
	at_dsp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dsp')+'<br/>') +
		html_par('minimum deformation to calculate equivalent coefficient (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MultipleShearSpring_Element','MultipleShearSpring Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MultipleShearSpring_Element','MultipleShearSpring Element')+'<br/>') +
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
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MultipleShearSpring_Element','MultipleShearSpring Element')+'<br/>') +
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
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/MultipleShearSpring_Element','MultipleShearSpring Element')+'<br/>') +
		html_end()
		)
	at_m.setDefault(0.0)
	#at_m.dimension = u.M
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'multipleShearSpring'
	xom.addAttribute(at_nSpring)
	xom.addAttribute(at_lim)
	xom.addAttribute(at_dsp)
	xom.addAttribute(at_orient)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_m)
	
	
	# visibility dependencies
	
	# dsp-dep
	xom.setVisibilityDependency(at_lim, at_dsp)
	
	# m-dep
	xom.setVisibilityDependency(at_mass, at_m)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	# multipleShearSpring eleTag? iNode? jNode? nSpring? -mat matTag? <-lim limDisp?>  <-orient <x1? x2? x3?> yp1? yp2? yp3?> <-mass m?>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	pinfo.updateModelBuilder(3,6)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh=phys_prop.XObject.Xnamespace
	if namePh != 'materials.uniaxial':
		raise Exception('Error: physical property must be "materials.uniaxial" and not: "{}"'.format(namePh))
	
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=2):
		raise Exception('Error: number of nodes')
	
	
	# optional paramters
	
	sopt = ''
	nSpring_at = xobj.getAttribute('nSpring')
	if(nSpring_at is None):
		raise Exception('Error: cannot find "nSpring" attribute')
	nSpring = nSpring_at.integer
	
	lim_at = xobj.getAttribute('-lim')
	if(lim_at is None):
		raise Exception('Error: cannot find "-lim" attribute')
	lim = lim_at.boolean
	if lim:
		dsp_at = xobj.getAttribute('dsp')
		if(dsp_at is None):
			raise Exception('Error: cannot find "dsp" attribute')
		dsp = dsp_at.real
		
		sopt += ' -lim {}'.format(dsp)
	
	
	orient_at = xobj.getAttribute('-orient')
	if(orient_at is None):
		raise Exception('Error: cannot find "-orient" attribute')
	if orient_at.boolean:
		vect_x=elem.orientation.computeOrientation().col(0)
		vect_y=elem.orientation.computeOrientation().col(1)
		
		sopt += ' -orient {} {} {} {} {} {}'.format (vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
		
	mass_at = xobj.getAttribute('-mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "-mass" attribute')
	mass = mass_at.boolean
	if mass:
		m_at = xobj.getAttribute('m')
		if(m_at is None):
			raise Exception('Error: cannot find "m" attribute')
		m = m_at.quantityScalar
		
		sopt += ' -mass {}'.format(m.value)
	
	str_tcl = '{}element multipleShearSpring {}{} {} -mat {}{}\n'.format(pinfo.indent, tag, nstr, nSpring, matTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
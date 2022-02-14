import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Group'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('elastic modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bidirectional_Section','Bidirectional Section')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# Fy
	at_Fy = MpcAttributeMetaData()
	at_Fy.type = MpcAttributeType.QuantityScalar
	at_Fy.name = 'Fy'
	at_Fy.group = 'Group'
	at_Fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fy')+'<br/>') + 
		html_par('yield force') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bidirectional_Section','Bidirectional Section')+'<br/>') +
		html_end()
		)
	at_Fy.dimension = u.F
	
	# Hiso
	at_Hiso = MpcAttributeMetaData()
	at_Hiso.type = MpcAttributeType.QuantityScalar
	at_Hiso.name = 'Hiso'
	at_Hiso.group = 'Group'
	at_Hiso.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Hiso')+'<br/>') + 
		html_par('isotropic hardening modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bidirectional_Section','Bidirectional Section')+'<br/>') +
		html_end()
		)
	at_Hiso.dimension = u.F/u.L**2
	
	# Hkin
	at_Hkin = MpcAttributeMetaData()
	at_Hkin.type = MpcAttributeType.QuantityScalar
	at_Hkin.name = 'Hkin'
	at_Hkin.group = 'Group'
	at_Hkin.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Hkin')+'<br/>') + 
		html_par('kinematic hardening modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bidirectional_Section','Bidirectional Section')+'<br/>') +
		html_end()
		)
	at_Hkin.dimension = u.F/u.L**2
	
	# use_code1_code2
	at_use_code1_code2 = MpcAttributeMetaData()
	at_use_code1_code2.type = MpcAttributeType.Boolean
	at_use_code1_code2.name = 'use_code1_code2'
	at_use_code1_code2.group = 'Group'
	at_use_code1_code2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_code1_code2')+'<br/>') + 
		html_par('section force code for direction 1 and direction 2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bidirectional_Section','Bidirectional Section')+'<br/>') +
		html_end()
		)
	
	# code1
	at_code1 = MpcAttributeMetaData()
	at_code1.type = MpcAttributeType.QuantityScalar
	at_code1.name = 'code1'
	at_code1.group = 'Optional parameters'
	at_code1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('code1')+'<br/>') + 
		html_par('section force code for direction 1 (default = Vy)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bidirectional_Section','Bidirectional Section')+'<br/>') +
		html_end()
		)
	at_code1.dimension = u.F
	
	# code2
	at_code2 = MpcAttributeMetaData()
	at_code2.type = MpcAttributeType.QuantityScalar
	at_code2.name = 'code2'
	at_code2.group = 'Optional parameters'
	at_code2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('code2')+'<br/>') + 
		html_par('section force code for direction 2 (default = P)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Bidirectional_Section','Bidirectional Section')+'<br/>') +
		html_end()
		)
	at_code2.dimension = u.F
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'Bidirectional'
	xom.addAttribute(at_E)
	xom.addAttribute(at_Fy)
	xom.addAttribute(at_Hiso)
	xom.addAttribute(at_Hkin)
	xom.addAttribute(at_use_code1_code2)
	xom.addAttribute(at_code1)
	xom.addAttribute(at_code2)
	
	
	# visibility dependencies
	
	# use_code1_code2-dep
	xom.setVisibilityDependency(at_use_code1_code2, at_code1)
	xom.setVisibilityDependency(at_use_code1_code2, at_code2)
	
	return xom

def writeTcl(pinfo):
	
	#section Bidirectional $secTag $E $Fy $Hiso $Hkin <$code1 $code2>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	E_at = xobj.getAttribute('E')
	if(E_at is None):
		raise Exception('Error: cannot find "E" attribute')
	E = E_at.quantityScalar
	
	Fy_at = xobj.getAttribute('Fy')
	if(Fy_at is None):
		raise Exception('Error: cannot find "Fy" attribute')
	Fy = Fy_at.quantityScalar
	
	Hiso_at = xobj.getAttribute('Hiso')
	if(Hiso_at is None):
		raise Exception('Error: cannot find "Hiso" attribute')
	Hiso = Hiso_at.quantityScalar
	
	Hkin_at = xobj.getAttribute('Hkin')
	if(Hkin_at is None):
		raise Exception('Error: cannot find "Hkin" attribute')
	Hkin = Hkin_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	use_code1_code2_at = xobj.getAttribute('use_code1_code2')
	if(use_code1_code2_at is None):
		raise Exception('Error: cannot find "use_code1_code2" attribute')
	use_code1_code2 = use_code1_code2_at.boolean
	if use_code1_code2:
		code1_at = xobj.getAttribute('code1')
		if(code1_at is None):
			raise Exception('Error: cannot find "code1" attribute')
		code1 = code1_at.quantityScalar
		
		code2_at = xobj.getAttribute('code2')
		if(code2_at is None):
			raise Exception('Error: cannot find "code2" attribute')
		code2 = code2_at.quantityScalar
		
		sopt += '{} {}'.format(code1.value, code2.value)
	
	
	str_tcl = '{}section Bidirectional {} {} {} {} {}{}\n'.format(
			pinfo.indent, tag, E.value, Fy.value, Hiso.value, Hkin.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
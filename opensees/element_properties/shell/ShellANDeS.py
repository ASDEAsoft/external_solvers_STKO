import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# thick
	at_thick = MpcAttributeMetaData()
	at_thick.type = MpcAttributeType.QuantityScalar
	at_thick.name = 'thick'
	at_thick.group = 'Group'
	at_thick.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('thick')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_thick.dimension=u.L
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Group'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_E.dimension=u.F/u.L**2
	
	# nu
	at_nu = MpcAttributeMetaData()
	at_nu.type = MpcAttributeType.Real
	at_nu.name = 'nu'
	at_nu.group = 'Group'
	at_nu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nu')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.Real
	at_rho.name = 'rho'
	at_rho.group = 'Group'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ShellANDeS'
	xom.addAttribute(at_thick)
	xom.addAttribute(at_E)
	xom.addAttribute(at_nu)
	xom.addAttribute(at_rho)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6),(3,6)]	#(ndm, ndf)

def writeTcl(pinfo):
	import opensees.element_properties.shell.shell_utils as shelu
	# element ShellANDeS $tag $iNode $jNode $kNode $thick $E $nu $rho
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# NODE
	nstr = shelu.getNodeString(elem)
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Triangle or len(elem.nodes)!=3:
		raise Exception('Error: invalid type of element or number of nodes')
	
	# mandatory parameters
	thick_at = xobj.getAttribute('thick')
	if(thick_at is None):
		raise Exception('Error: cannot find "thick" attribute')
	thick = thick_at.quantityScalar.value
	
	E_at = xobj.getAttribute('E')
	if(E_at is None):
		raise Exception('Error: cannot find "E" attribute')
	E = E_at.quantityScalar.value
	
	nu_at = xobj.getAttribute('nu')
	if(nu_at is None):
		raise Exception('Error: cannot find "nu" attribute')
	nu = nu_at.real
	
	rho_at = xobj.getAttribute('rho')
	if(rho_at is None):
		raise Exception('Error: cannot find "rho" attribute')
	rho = rho_at.real
	
	str_tcl = '{}element ShellANDeS {} {} {} {} {} {}\n'.format(pinfo.indent, tag, nstr, thick, E ,nu, rho )
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
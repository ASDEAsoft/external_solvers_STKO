from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# updateBasis
	at_updateBasis = MpcAttributeMetaData()
	at_updateBasis.type = MpcAttributeType.Boolean
	at_updateBasis.name = '-updateBasis'
	at_updateBasis.group = 'Group'
	at_updateBasis.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-updateBasis')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Shell_Element','Shell Element')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ShellMITC4'
	xom.addAttribute(at_updateBasis)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6),(3,6),(3,6)]	#(ndm, ndf)

def writeTcl(pinfo):
	import opensees.element_properties.shell.shell_utils as shelu
	
	# element ShellMITC4 $tag $iNode $jNoe $kNode $lNode $secTag <-updateBasis>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	secTag = phys_prop.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh = phys_prop.XObject.Xnamespace
	if namePh != 'sections':
		raise Exception('Error: physical property must be "sections" and not: "{}"'.format(namePh))
	
	# NODE
	nstr = shelu.getNodeString(elem)
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Quadrilateral or len(elem.nodes)!=4:
		raise Exception('Error: invalid type of element or number of nodes')
	
	# optional paramters
	sopt = ''
	
	updateBasis_at = xobj.getAttribute('-updateBasis')
	if(updateBasis_at is None):
		raise Exception('Error: cannot find "-updateBasis" attribute')
	updateBasis = updateBasis_at.boolean
	if updateBasis:
		sopt += ' -updateBasis'
	
	str_tcl = '{}element ShellMITC4 {} {} {}{}\n'.format(pinfo.indent, tag, nstr, secTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	def mka(name, type, group):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(html_href("https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/ASDShellQ4.html", 'ASDShellQ4 Element')+'<br/>') +
			html_end()
			)
		return a
	
	# updateBasis
	at_kin = mka('Kinematics', MpcAttributeType.String, 'Group')
	at_kin.sourceType = MpcAttributeSourceType.List
	at_kin.setSourceList(['Linear', 'Corotational'])
	at_kin.setDefault('Linear')
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDShellQ4'
	xom.addAttribute(at_kin)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6),(3,6),(3,6)]	#(ndm, ndf)

def writeTcl(pinfo):
	import opensees.element_properties.shell.shell_utils as shelu
	
	# element ASDShellQ4 $tag $iNode $jNoe $kNode $lNode $secTag <-corotational>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	secTag = phys_prop.id
	xobj = elem_prop.XObject
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Quadrilateral or len(elem.nodes)!=4:
		raise Exception('Error: invalid type of element or number of nodes')
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh = phys_prop.XObject.Xnamespace
	if namePh != 'sections':
		raise Exception('Error: physical property must be "sections" and not: "{}"'.format(namePh))
	
	def geta(name):
		at = xobj.getAttribute(name)
		if(at is None):
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	# NODE
	nstr = shelu.getNodeString(elem)
	
	# optional paramters
	sopt = ''
	
	if geta('Kinematics').string == 'Corotational':
		sopt += ' -corotational'
	
	str_tcl = '{}element ASDShellQ4 {} {} {}{}\n'.format(pinfo.indent, tag, nstr, secTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
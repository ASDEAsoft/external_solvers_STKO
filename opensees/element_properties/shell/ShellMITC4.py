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
	
	# -scaleDrilling
	at_scaleDrilling = MpcAttributeMetaData()
	at_scaleDrilling.type = MpcAttributeType.Boolean
	at_scaleDrilling.name = '-scaleDrilling'
	at_scaleDrilling.group = 'Group'
	at_scaleDrilling.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-scaleDrilling')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Shell_Element','Shell Element')+'<br/>') +
		html_end()
		)
	at_scaleDrilling.setDefault(True)
	
	# drillingScaleFactor
	at_drillingScaleFactor = MpcAttributeMetaData()
	at_drillingScaleFactor.type = MpcAttributeType.Real
	at_drillingScaleFactor.name = 'drillingScaleFactor'
	at_drillingScaleFactor.group = 'Group'
	at_drillingScaleFactor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('drillingScaleFactor')+'<br/>') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Shell_Element','Shell Element')+'<br/>') +
		html_end()
		)
	at_drillingScaleFactor.setDefault(0.01)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ShellMITC4'
	xom.addAttribute(at_updateBasis)
	xom.addAttribute(at_scaleDrilling)
	xom.addAttribute(at_drillingScaleFactor)
	
	xom.setVisibilityDependency(at_scaleDrilling, at_drillingScaleFactor)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6),(3,6),(3,6)]	#(ndm, ndf)

def writeTcl(pinfo):
	import opensees.element_properties.shell.shell_utils as shelu
	
	# element ShellMITC4 $tag $iNode $jNoe $kNode $lNode $secTag <-updateBasis> <-scaleDrilling $drillingScaleFactor>
	
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
	
	scaleDrilling_at = xobj.getAttribute('-scaleDrilling')
	if(scaleDrilling_at is None):
		raise Exception('Error: cannot find "-scaleDrilling" attribute')
	if scaleDrilling_at.boolean:
		drillingScaleFactor_at = xobj.getAttribute('drillingScaleFactor')
		if drillingScaleFactor_at is None:
			raise Exception('Error: cannot find "drillingScaleFactor" attribute')
		drillingScaleFactor = drillingScaleFactor_at.real
		if drillingScaleFactor < 0.0:
			drillingScaleFactor = 0.0
		if drillingScaleFactor > 1.0:
			drillingScaleFactor = 1.0
		sopt += ' -scaleDrilling {}'.format(drillingScaleFactor)
	
	str_tcl = '{}element ShellMITC4 {} {} {}{}\n'.format(pinfo.indent, tag, nstr, secTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
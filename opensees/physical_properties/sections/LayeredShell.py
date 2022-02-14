import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# matTag
	at_matTag = MpcAttributeMetaData()
	at_matTag.type = MpcAttributeType.IndexVector
	at_matTag.name = 'matTag'
	at_matTag.group = 'Non linear'
	at_matTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') + 
		html_par('material tag of n-th layer') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Define the Section of the Multi-layer Shell element')+'<br/>') +
		html_end()
		)
	at_matTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag.indexSource.addAllowedNamespace('materials.nD')
	
	# thickness
	at_thickness = MpcAttributeMetaData()
	at_thickness.type = MpcAttributeType.QuantityVector
	at_thickness.name = 'thickness'
	at_thickness.group = 'Non linear'
	at_thickness.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('thickness')+'<br/>') + 
		html_par('thickness of n-th layer') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Define the Section of the Multi-layer Shell element')+'<br/>') +
		html_end()
		)
	at_thickness.dimension = u.L
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'LayeredShell'
	#xom.addAttribute(at_nLayers)
	xom.addAttribute(at_matTag)
	xom.addAttribute(at_thickness)
	
	return xom

def writeTcl(pinfo):
	
	#section LayeredShell $sectionTag $nLayers $matTag1 $thickness1...$matTagn $thicknessn
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	matTag_at = xobj.getAttribute('matTag')
	if(matTag_at is None):
		raise Exception('Error: cannot find "matTag" attribute')
	matTag = matTag_at.indexVector
	
	thickness_at = xobj.getAttribute('thickness')
	if(thickness_at is None):
		raise Exception('Error: cannot find "thickness" attribute')
	thickness = thickness_at.quantityVector
	
	nLayers = len(matTag)
	if nLayers != len(thickness):
		raise Exception('Error: thickness and material vectors must have the same length')
	if nLayers < 1:
		raise Exception('Error: at least 1 layer must be defined')
	
	str_layers = []
	counter = 0
	indent = pinfo.indent
	indent2 = '{}{}'.format(indent, pinfo.tabIndent)
	for i in range(nLayers):
		counter += 1
		if counter == 1:
			str_layers.append(indent2)
		str_layers.append(' {} {} '.format(matTag[i], thickness.valueAt(i)))
		if counter == 4:
			str_layers.append(' \\\n')
			counter = 0
	str_tcl = '{}section LayeredShell {} {} \\\n{}\n'.format(indent, tag, nLayers, ''.join(str_layers))
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
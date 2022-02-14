import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# matTag
	at_matTag = MpcAttributeMetaData()
	at_matTag.type = MpcAttributeType.Index
	at_matTag.name = 'matTag'
	at_matTag.group = 'Non linear'
	at_matTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') + 
		html_par('integer tag identifying uniaxial steel material') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional Reinforcement Material')+'<br/>') +
		html_end()
		)
	at_matTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# sita
	at_sita = MpcAttributeMetaData()
	at_sita.type = MpcAttributeType.Real
	at_sita.name = 'sita'
	at_sita.group = 'Non linear'
	at_sita.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sita')+'<br/>') + 
		html_par('define the angle of steel layer, 90° (longitudinal steel), 0° (tranverse steel)') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional Reinforcement Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'PlateRebar'
	xom.Xgroup = 'Materials for Modeling Concrete Walls'
	xom.addAttribute(at_matTag)
	xom.addAttribute(at_sita)
	
	return xom

def writeTcl(pinfo):
	
	#nDmaterial PlateRebar $newmatTag $matTag $sita
	xobj = pinfo.phys_prop.XObject
	newmatTag = xobj.parent.componentId
	
	# mandatory parameters
	matTag_at = xobj.getAttribute('matTag')
	if(matTag_at is None):
		raise Exception('Error: cannot find "matTag" attribute')
	matTag = matTag_at.index
	
	sita_at = xobj.getAttribute('sita')
	if(sita_at is None):
		raise Exception('Error: cannot find "sita" attribute')
	sita = sita_at.real
	
	str_tcl = '{}nDMaterial PlateRebar {} {} {}\n'.format(
			pinfo.indent, newmatTag, matTag, sita)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
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
		html_par('integer tag identifying PlaneStressUserMaterial') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional concrete model')+'<br/>') +
		html_end()
		)
	at_matTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag.indexSource.addAllowedNamespace('materials.nD')
	#at_matTag.indexSource.addAllowedClass('PlaneStressUserMaterial')
	
	# OutofPlaneModulus
	at_OutofPlaneModulus = MpcAttributeMetaData()
	at_OutofPlaneModulus.type = MpcAttributeType.QuantityScalar
	at_OutofPlaneModulus.name = 'OutofPlaneModulus'
	at_OutofPlaneModulus.group = 'Non linear'
	at_OutofPlaneModulus.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OutofPlaneModulus')+'<br/>') + 
		html_par('shear modulus of out plane') +
		html_par(html_href('http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm','Multi-dimensional concrete model')+'<br/>') +
		html_end()
		)
	at_OutofPlaneModulus.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'PlateFromPlaneStress'
	xom.Xgroup = 'Materials for Modeling Concrete Walls'
	xom.addAttribute(at_matTag)
	xom.addAttribute(at_OutofPlaneModulus)
	
	return xom

def writeTcl(pinfo):
	
	#nDmaterial PlateFromPlaneStress $newmatTag $matTag $OutofPlaneModulus
	xobj = pinfo.phys_prop.XObject
	newmatTag = xobj.parent.componentId
	
	# mandatory parameters
	matTag_at = xobj.getAttribute('matTag')
	if(matTag_at is None):
		raise Exception('Error: cannot find "matTag" attribute')
	matTag = matTag_at.index
	
	OutofPlaneModulus_at = xobj.getAttribute('OutofPlaneModulus')
	if(OutofPlaneModulus_at is None):
		raise Exception('Error: cannot find "OutofPlaneModulus" attribute')
	OutofPlaneModulus = OutofPlaneModulus_at.quantityScalar
	
	str_tcl = '{}nDMaterial PlateFromPlaneStress {} {} {}\n'.format(
			pinfo.indent, newmatTag, matTag, OutofPlaneModulus.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
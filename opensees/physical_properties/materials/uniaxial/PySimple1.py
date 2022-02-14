# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# soilType
	at_soilType = MpcAttributeMetaData()
	at_soilType.type = MpcAttributeType.Integer
	at_soilType.name = 'soilType'
	at_soilType.group = 'Non-linear'
	at_soilType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('soilType')+'<br/>') + 
		html_par('soilType = 1 Backbone of p-y curve approximates Matlock (1970) soft clay relation.') +
		html_par('soilType = 2 Backbone of p-y curve approximates API (1993) sand relation.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PySimple1_Material','PySimple1 Material')+'<br/>') +
		html_end()
		)
	at_soilType.sourceType = MpcAttributeSourceType.List
	at_soilType.setSourceList([1, 2])
	at_soilType.setDefault(1)
	
	# pult
	at_pult = MpcAttributeMetaData()
	at_pult.type = MpcAttributeType.QuantityScalar
	at_pult.name = 'pult'
	at_pult.group = 'Non-linear'
	at_pult.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pult')+'<br/>') + 
		html_par('Ultimate capacity of the p-y material. Note that "p" or "pult" are distributed loads [force per length of pile] in common design equations, but are both loads for this uniaxialMaterial [i.e., distributed load times the tributary length of the pile].') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PySimple1_Material','PySimple1 Material')+'<br/>') +
		html_end()
		)
	at_pult.dimension = u.F/u.L
	
	# Y50
	at_Y50 = MpcAttributeMetaData()
	at_Y50.type = MpcAttributeType.QuantityScalar
	at_Y50.name = 'Y50'
	at_Y50.group = 'Non-linear'
	at_Y50.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Y50')+'<br/>') + 
		html_par('Displacement at which 50% of pult is mobilized in monotonic loading.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PySimple1_Material','PySimple1 Material')+'<br/>') +
		html_end()
		)
	at_Y50.dimension = u.L
	
	# Cd
	at_Cd = MpcAttributeMetaData()
	at_Cd.type = MpcAttributeType.Real
	at_Cd.name = 'Cd'
	at_Cd.group = 'Non-linear'
	at_Cd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Cd')+'<br/>') + 
		html_par('Variable that sets the drag resistance within a fully-mobilized gap as Cd*pult.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PySimple1_Material','PySimple1 Material')+'<br/>') +
		html_end()
		)
	
	# use_c
	at_use_c = MpcAttributeMetaData()
	at_use_c.type = MpcAttributeType.Boolean
	at_use_c.name = 'use_c'
	at_use_c.group = 'Non-linear'
	at_use_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_c')+'<br/>') + 
		html_par('The viscous damping term (dashpot) on the far-field (elastic) component of the displacement rate (velocity). (optional Default = 0.0). Nonzero c values are used to represent radiation damping effects') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PySimple1_Material','PySimple1 Material')+'<br/>') +
		html_end()
		)
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.Real
	at_c.name = 'c'
	at_c.group = 'Optional parameters'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') + 
		html_par('The viscous damping term (dashpot) on the far-field (elastic) component of the displacement rate (velocity). (optional Default = 0.0). Nonzero c values are used to represent radiation damping effects') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PySimple1_Material','PySimple1 Material')+'<br/>') +
		html_end()
		)
	at_c.setDefault(0.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'PySimple1'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_soilType)
	xom.addAttribute(at_pult)
	xom.addAttribute(at_Y50)
	xom.addAttribute(at_Cd)
	xom.addAttribute(at_use_c)
	xom.addAttribute(at_c)
	
	# c-dep
	xom.setVisibilityDependency(at_use_c, at_c)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial PySimple1 $matTag $soilType $pult $Y50 $Cd <$c>
	
	xobj = pinfo.phys_prop.XObject
	matTag = xobj.parent.componentId
	
	# mandatory parameters
	soilType_at = xobj.getAttribute('soilType')
	if(soilType_at is None):
		raise Exception('Error: cannot find "soilType" attribute')
	soilType = soilType_at.integer
	
	pult_at = xobj.getAttribute('pult')
	if(pult_at is None):
		raise Exception('Error: cannot find "pult" attribute')
	pult = pult_at.quantityScalar
	
	Y50_at = xobj.getAttribute('Y50')
	if(Y50_at is None):
		raise Exception('Error: cannot find "Y50" attribute')
	Y50 = Y50_at.quantityScalar
	
	Cd_at = xobj.getAttribute('Cd')
	if(Cd_at is None):
		raise Exception('Error: cannot find "Cd" attribute')
	Cd = Cd_at.real
	
	
	# optional paramters
	sopt = ''
	
	use_c_at = xobj.getAttribute('use_c')
	if(use_c_at is None):
		raise Exception('Error: cannot find "use_c" attribute')
	use_c = use_c_at.boolean
	if use_c:
		c_at = xobj.getAttribute('c')
		if(c_at is None):
			raise Exception('Error: cannot find "c" attribute')
		c = c_at.real
		
		sopt += '{}'.format(c)
	
	
	str_tcl = '{}uniaxialMaterial PySimple1 {} {} {} {} {} {}\n'.format(
			pinfo.indent, matTag, soilType, pult.value, Y50.value, Cd, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
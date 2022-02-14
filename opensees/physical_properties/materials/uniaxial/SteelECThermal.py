# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Fy
	at_Fy = MpcAttributeMetaData()
	at_Fy.type = MpcAttributeType.QuantityScalar
	at_Fy.name = 'Fy'
	at_Fy.group = 'Non-linear'
	at_Fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fy')+'<br/>') + 
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','SteelECThermal')+'<br/>') +
		html_end()
		)
	at_Fy.dimension = u.F/u.L**2
	
	# E0
	at_E0 = MpcAttributeMetaData()
	at_E0.type = MpcAttributeType.QuantityScalar
	at_E0.name = 'E0'
	at_E0.group = 'Non-linear'
	at_E0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E0')+'<br/>') + 
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','SteelECThermal')+'<br/>') +
		html_end()
		)
	at_E0.dimension = u.F/u.L**2
	
	#use_steelType
	at_use_steelType = MpcAttributeMetaData()
	at_use_steelType.type = MpcAttributeType.Boolean
	at_use_steelType.name = 'use_steelType'
	at_use_steelType.group = 'Group'
	at_use_steelType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_steelType')+'<br/>') + 
		html_par('to activate "-SteelSoft" or "-ConcreteSoft"') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','ElasticThermal')+'<br/>') +
		html_end()
		)
	
	# steelType
	at_softindex = MpcAttributeMetaData()
	at_softindex.type = MpcAttributeType.String
	at_softindex.name = 'steelType'
	at_softindex.group = 'Optional parameters'
	at_softindex.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('steelType')+'<br/>') + 
		html_par('choose between "-SteelSoft" and "-ConcreteSoft"') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/MaterialCmds.html','ElasticThermal')+'<br/>') +
		html_end()
		)
	at_softindex.sourceType = MpcAttributeSourceType.List
	at_softindex.setSourceList(['EC3', 'EC2Nh', 'EC2Nc', 'EC2x'])
	at_softindex.setDefault('EC3')
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'SteelECThermal'
	xom.Xgroup = 'Thermal'
	xom.addAttribute(at_Fy)
	xom.addAttribute(at_E0)
	xom.addAttribute(at_use_steelType)
	xom.addAttribute(at_softindex)
	
	# at_use_steelType-at_softindex
	xom.setVisibilityDependency(at_use_steelType, at_softindex)
	
	
	return xom

def writeTcl(pinfo):
	
	# uniaxialMaterial SteelECThermal $matTag <$steelType> $Fy $E0
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	
	Fy_at = xobj.getAttribute('Fy')
	if(Fy_at is None):
		raise Exception('Error: cannot find "Fy" attribute')
	Fy = Fy_at.quantityScalar
	
	E0_at = xobj.getAttribute('E0')
	if(E0_at is None):
		raise Exception('Error: cannot find "E0" attribute')
	E0 = E0_at.quantityScalar
	
	
	sopt = ''
	use_steelType_at = xobj.getAttribute('use_steelType')
	if(use_steelType_at is None):
		raise Exception('Error: cannot find "use_steelType" attribute')
	use_steelType = use_steelType_at.boolean
	if use_steelType:
		steelType_at = xobj.getAttribute('steelType')
		if(steelType_at is None):
			raise Exception('Error: cannot find "steelType" attribute')
		steelType = steelType_at.string
		
		sopt += ' {}'.format(steelType)
	
	
	str_tcl = '{}uniaxialMaterial SteelECThermal {}{} {} {}\n'.format(pinfo.indent, tag, sopt, Fy.value, E0.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
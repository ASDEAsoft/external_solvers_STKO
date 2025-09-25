# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Elasticity'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('tangent') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Uniaxial_Material','Elastic Material')+'<br/>') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# use_eta
	at_use_eta = MpcAttributeMetaData()
	at_use_eta.type = MpcAttributeType.Boolean
	at_use_eta.name = 'use_eta'
	at_use_eta.group = 'Non-linear'
	at_use_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_eta')+'<br/>') + 
		html_par('damping tangent (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Uniaxial_Material','Elastic Material')+'<br/>') +
		html_end()
		)
	
	# eta
	at_eta = MpcAttributeMetaData()
	at_eta.type = MpcAttributeType.Real
	at_eta.name = 'eta'
	at_eta.group = 'Optional parameters'
	at_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eta')+'<br/>') + 
		html_par('damping tangent (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Uniaxial_Material','Elastic Material')+'<br/>') +
		html_end()
		)
	at_eta.setDefault(0.0)
	
	#use_Eneg
	at_use_Eneg = MpcAttributeMetaData()
	at_use_Eneg.type = MpcAttributeType.Boolean
	at_use_Eneg.name = 'use_Eneg'
	at_use_Eneg.group = 'Non-linear'
	at_use_Eneg.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_Eneg')+'<br/>') + 
		html_par('tangent in compression (optional, default=E)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Uniaxial_Material','Elastic Material')+'<br/>') +
		html_end()
		)
	
	# Eneg
	at_Eneg = MpcAttributeMetaData()
	at_Eneg.type = MpcAttributeType.QuantityScalar
	at_Eneg.name = 'Eneg'
	at_Eneg.group = 'Optional parameters'
	at_Eneg.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Eneg')+'<br/>') + 
		html_par('tangent in compression (optional, default=E)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Uniaxial_Material','Elastic Material')+'<br/>') +
		html_end()
		)
	at_Eneg.dimension = u.F/u.L**2

	xom = MpcXObjectMetaData()
	xom.name = 'Elastic'
	xom.Xgroup = 'Some Standard Uniaxial Materials'
	xom.addAttribute(at_E)
	xom.addAttribute(at_use_eta)
	xom.addAttribute(at_eta)
	xom.addAttribute(at_use_Eneg)
	xom.addAttribute(at_Eneg)
	
	# eta-dep
	xom.setVisibilityDependency(at_use_eta, at_eta)
	
	# Eneg-dep
	xom.setVisibilityDependency(at_use_Eneg, at_Eneg)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial Elastic $matTag $E <$eta> <$Eneg>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	E_at = xobj.getAttribute('E')
	if(E_at is None):
		raise Exception('Error: cannot find "E" attribute')
	E = E_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	use_eta_at = xobj.getAttribute('use_eta')
	if(use_eta_at is None):
		raise Exception('Error: cannot find "use_eta" attribute')
	use_eta = use_eta_at.boolean
	if use_eta:
		eta_at = xobj.getAttribute('eta')
		if(eta_at is None):
			raise Exception('Error: cannot find "eta" attribute')
		eta = eta_at.real
		
		sopt += '{}'.format(eta)
	
	use_Eneg_at = xobj.getAttribute('use_Eneg')
	if(use_Eneg_at is None):
		raise Exception('Error: cannot find "use_Eneg" attribute')
	use_Eneg = use_Eneg_at.boolean
	if use_Eneg:
		Eneg_at = xobj.getAttribute('Eneg')
		if(Eneg_at is None):
			raise Exception('Error: cannot find "Eneg" attribute')
		Eneg = Eneg_at.quantityScalar
		
		sopt += ' {}'.format(Eneg.value)
	
	
	str_tcl = '{}uniaxialMaterial Elastic {} {} {}\n'.format(pinfo.indent, tag, E.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
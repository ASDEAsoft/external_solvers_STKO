# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Kmax
	at_Kmax = MpcAttributeMetaData()
	at_Kmax.type = MpcAttributeType.QuantityScalar
	at_Kmax.name = 'Kmax'
	at_Kmax.group = 'Non-linear'
	at_Kmax.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kmax')+'<br/>') + 
		html_par('initial stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hyperbolic_Gap_Material','Hyperbolic Gap Material')+'<br/>') +
		html_end()
		)
	at_Kmax.dimension = u.F/u.L
	
	# Kur
	at_Kur = MpcAttributeMetaData()
	at_Kur.type = MpcAttributeType.QuantityScalar
	at_Kur.name = 'Kur'
	at_Kur.group = 'Non-linear'
	at_Kur.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kur')+'<br/>') + 
		html_par('unloading/reloading stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hyperbolic_Gap_Material','Hyperbolic Gap Material')+'<br/>') +
		html_end()
		)
	at_Kur.dimension = u.F/u.L
	
	# Rf
	at_Rf = MpcAttributeMetaData()
	at_Rf.type = MpcAttributeType.Real
	at_Rf.name = 'Rf'
	at_Rf.group = 'Non-linear'
	at_Rf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Rf')+'<br/>') + 
		html_par('failure ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hyperbolic_Gap_Material','Hyperbolic Gap Material')+'<br/>') +
		html_end()
		)
	
	# Fult
	at_Fult = MpcAttributeMetaData()
	at_Fult.type = MpcAttributeType.QuantityScalar
	at_Fult.name = 'Fult'
	at_Fult.group = 'Non-linear'
	at_Fult.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fult')+'<br/>') + 
		html_par('ultimate (maximum) passive resistance*') +
		html_par('This material is implemented as a compression-only gap material. Fult and gap should be input as negative values.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hyperbolic_Gap_Material','Hyperbolic Gap Material')+'<br/>') +
		html_end()
		)
	at_Fult.dimension = u.F
	
	# gap
	at_gap = MpcAttributeMetaData()
	at_gap.type = MpcAttributeType.QuantityScalar
	at_gap.name = 'gap'
	at_gap.group = 'Non-linear'
	at_gap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gap')+'<br/>') + 
		html_par('initial gap*') +
		html_par('This material is implemented as a compression-only gap material. Fult and gap should be input as negative values.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Hyperbolic_Gap_Material','Hyperbolic Gap Material')+'<br/>') +
		html_end()
		)
	at_gap.dimension = u.L
	
	xom = MpcXObjectMetaData()
	xom.name = 'HyperbolicGapMaterial'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_Kmax)
	xom.addAttribute(at_Kur)
	xom.addAttribute(at_Rf)
	xom.addAttribute(at_Fult)
	xom.addAttribute(at_gap)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial HyperbolicGapMaterial $matTag $Kmax $Kur $Rf $Fult $gap
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	Kmax_at = xobj.getAttribute('Kmax')
	if(Kmax_at is None):
		raise Exception('Error: cannot find "Kmax" attribute')
	Kmax = Kmax_at.quantityScalar
	
	Kur_at = xobj.getAttribute('Kur')
	if(Kur_at is None):
		raise Exception('Error: cannot find "Kur" attribute')
	Kur = Kur_at.quantityScalar
	
	Rf_at = xobj.getAttribute('Rf')
	if(Rf_at is None):
		raise Exception('Error: cannot find "Rf" attribute')
	Rf = Rf_at.real
	
	Fult_at = xobj.getAttribute('Fult')
	if(Fult_at is None):
		raise Exception('Error: cannot find "Fult" attribute')
	Fult = Fult_at.quantityScalar
	
	gap_at = xobj.getAttribute('gap')
	if(gap_at is None):
		raise Exception('Error: cannot find "gap" attribute')
	gap = gap_at.quantityScalar
	
	
	str_tcl = '{}uniaxialMaterial HyperbolicGapMaterial {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, Kmax.value, Kur.value, Rf, Fult.value, gap.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
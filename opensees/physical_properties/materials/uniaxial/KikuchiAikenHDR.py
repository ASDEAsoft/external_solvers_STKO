# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# tp
	at_tp = MpcAttributeMetaData()
	at_tp.type = MpcAttributeType.String
	at_tp.name = 'tp'
	at_tp.group = 'Non-linear'
	at_tp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tp')+'<br/>') + 
		html_par('rubber type (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenHDR_Material','KikuchiAikenHDR Material')+'<br/>') +
		html_end()
		)
	at_tp.sourceType = MpcAttributeSourceType.List
	at_tp.setSourceList(['X0.6', 'X0.6-0MPa', 'X0.4', 'X0.4-0MPa', 'X0.3', 'X0.3-0MPa'])
	at_tp.setDefault('X0.6')
	
	# ar
	at_ar = MpcAttributeMetaData()
	at_ar.type = MpcAttributeType.QuantityScalar
	at_ar.name = 'ar'
	at_ar.group = 'Non-linear'
	at_ar.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ar')+'<br/>') + 
		html_par('area of rubber (see note 2)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenHDR_Material','KikuchiAikenHDR Material')+'<br/>') +
		html_end()
		)
	at_ar.dimension = u.L**2
	
	# hr
	at_hr = MpcAttributeMetaData()
	at_hr.type = MpcAttributeType.QuantityScalar
	at_hr.name = 'hr'
	at_hr.group = 'Non-linear'
	at_hr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('hr')+'<br/>') + 
		html_par('total thickness of rubber (see note 2)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenHDR_Material','KikuchiAikenHDR Material')+'<br/>') +
		html_end()
		)
	at_hr.dimension = u.L
	
	# -coGHU
	at_coGHU = MpcAttributeMetaData()
	at_coGHU.type = MpcAttributeType.Boolean
	at_coGHU.name = '-coGHU'
	at_coGHU.group = 'Non-linear'
	at_coGHU.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-coGHU')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenHDR_Material','KikuchiAikenHDR Material')+'<br/>') +
		html_end()
		)
	
	# cg
	at_cg = MpcAttributeMetaData()
	at_cg.type = MpcAttributeType.Real
	at_cg.name = 'cg'
	at_cg.group = '-coGHU'
	at_cg.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cg')+'<br/>') + 
		html_par('correction coefficient for equivalent shear modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenHDR_Material','KikuchiAikenHDR Material')+'<br/>') +
		html_end()
		)
	
	# ch
	at_ch = MpcAttributeMetaData()
	at_ch.type = MpcAttributeType.Real
	at_ch.name = 'ch'
	at_ch.group = '-coGHU'
	at_ch.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ch')+'<br/>') + 
		html_par('equivalent viscous daming ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenHDR_Material','KikuchiAikenHDR Material')+'<br/>') +
		html_end()
		)
	
	# cu
	at_cu = MpcAttributeMetaData()
	at_cu.type = MpcAttributeType.Real
	at_cu.name = 'cu'
	at_cu.group = '-coGHU'
	at_cu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cu')+'<br/>') + 
		html_par('ratio of shear force at zero displacement') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenHDR_Material','KikuchiAikenHDR Material')+'<br/>') +
		html_end()
		)
	
	# -coMSS
	at_coMSS = MpcAttributeMetaData()
	at_coMSS.type = MpcAttributeType.Boolean
	at_coMSS.name = '-coMSS'
	at_coMSS.group = 'Non-linear'
	at_coMSS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-coMSS')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenHDR_Material','KikuchiAikenHDR Material')+'<br/>') +
		html_end()
		)
	
	# rs
	at_rs = MpcAttributeMetaData()
	at_rs.type = MpcAttributeType.Real
	at_rs.name = 'rs'
	at_rs.group = '-coMSS'
	at_rs.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rs')+'<br/>') + 
		html_par('reduction rate for stiffness (see note 3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenHDR_Material','KikuchiAikenHDR Material')+'<br/>') +
		html_end()
		)
	
	# rf
	at_rf = MpcAttributeMetaData()
	at_rf.type = MpcAttributeType.Real
	at_rf.name = 'rf'
	at_rf.group = '-coMSS'
	at_rf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rf')+'<br/>') + 
		html_par('reduction rate for force (see note 3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenHDR_Material','KikuchiAikenHDR Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'KikuchiAikenHDR'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_tp)
	xom.addAttribute(at_ar)
	xom.addAttribute(at_hr)
	xom.addAttribute(at_coGHU)
	xom.addAttribute(at_cg)
	xom.addAttribute(at_ch)
	xom.addAttribute(at_cu)
	xom.addAttribute(at_coMSS)
	xom.addAttribute(at_rs)
	xom.addAttribute(at_rf)
	
	# coGHU-dep
	xom.setVisibilityDependency(at_coGHU, at_cg)
	xom.setVisibilityDependency(at_coGHU, at_ch)
	xom.setVisibilityDependency(at_coGHU, at_cu)
	
	# coMSS-dep
	xom.setVisibilityDependency(at_coMSS, at_rs)
	xom.setVisibilityDependency(at_coMSS, at_rf)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial KikuchiAikenHDR $matTag $tp $ar $hr <-coGHU $cg $ch $cu> <-coMSS $rs $rf>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	tp_at = xobj.getAttribute('tp')
	if(tp_at is None):
		raise Exception('Error: cannot find "tp" attribute')
	tp = tp_at.string
	
	ar_at = xobj.getAttribute('ar')
	if(ar_at is None):
		raise Exception('Error: cannot find "ar" attribute')
	ar = ar_at.quantityScalar
	
	hr_at = xobj.getAttribute('hr')
	if(hr_at is None):
		raise Exception('Error: cannot find "hr" attribute')
	hr = hr_at.quantityScalar
	
	
	# optional paramters
	sopt = ''
	
	coGHU_at = xobj.getAttribute('-coGHU')
	if(coGHU_at is None):
		raise Exception('Error: cannot find "-coGHU" attribute')
	coGHU = coGHU_at.boolean
	if coGHU:
		cg_at = xobj.getAttribute('cg')
		if(cg_at is None):
			raise Exception('Error: cannot find "cg" attribute')
		cg = cg_at.real
		
		ch_at = xobj.getAttribute('ch')
		if(ch_at is None):
			raise Exception('Error: cannot find "ch" attribute')
		ch = ch_at.real
		
		cu_at = xobj.getAttribute('cu')
		if(cu_at is None):
			raise Exception('Error: cannot find "cu" attribute')
		cu = cu_at.real
		
		sopt += '{} {} {}'.format(cg, ch, cu)
	
	coMSS_at = xobj.getAttribute('-coMSS')
	if(coMSS_at is None):
		raise Exception('Error: cannot find "-coMSS" attribute')
	coMSS = coMSS_at.boolean
	if coMSS:
		rs_at = xobj.getAttribute('rs')
		if(rs_at is None):
			raise Exception('Error: cannot find "rs" attribute')
		rs = rs_at.real
		
		rf_at = xobj.getAttribute('rf')
		if(rf_at is None):
			raise Exception('Error: cannot find "rf" attribute')
		rf = rf_at.real
		
		sopt += ' {} {}'.format(rs, rf)
	
	
	str_tcl = '{}uniaxialMaterial KikuchiAikenHDR {} {} {} {} {}\n'.format(
			pinfo.indent, tag, tp, ar.value, hr.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
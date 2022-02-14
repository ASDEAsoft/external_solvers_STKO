# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# type
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.String
	at_type.name = 'type'
	at_type.group = 'Non-linear'
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('type')+'<br/>') + 
		html_par('rubber type (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	at_type.sourceType = MpcAttributeSourceType.List
	at_type.setSourceList(['lead-rubber bearing'])
	at_type.setDefault('lead-rubber bearing')
	
	# ar
	at_ar = MpcAttributeMetaData()
	at_ar.type = MpcAttributeType.QuantityScalar
	at_ar.name = 'ar'
	at_ar.group = 'Non-linear'
	at_ar.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ar')+'<br/>') + 
		html_par('area of rubber') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
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
		html_par('total thickness of rubber') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	at_hr.dimension = u.L
	
	# gr
	at_gr = MpcAttributeMetaData()
	at_gr.type = MpcAttributeType.QuantityScalar
	at_gr.name = 'gr'
	at_gr.group = 'Non-linear'
	at_gr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gr')+'<br/>') + 
		html_par('shear modulus of rubber') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	at_gr.dimension = u.F/u.L**2
	
	# ap
	at_ap = MpcAttributeMetaData()
	at_ap.type = MpcAttributeType.QuantityScalar
	at_ap.name = 'ap'
	at_ap.group = 'Non-linear'
	at_ap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ap')+'<br/>') + 
		html_par('area of lead plug') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	at_ap.dimension = u.L**2
	
	# tp
	at_tp = MpcAttributeMetaData()
	at_tp.type = MpcAttributeType.QuantityScalar
	at_tp.name = 'tp'
	at_tp.group = 'Non-linear'
	at_tp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tp')+'<br/>') + 
		html_par('yield stress of lead plug') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	at_tp.dimension = u.F/u.L**2
	
	# alph
	at_alph = MpcAttributeMetaData()
	at_alph.type = MpcAttributeType.QuantityScalar
	at_alph.name = 'alph'
	at_alph.group = 'Non-linear'
	at_alph.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alph')+'<br/>') + 
		html_par('shear modulus of lead plug') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	at_alph.dimension = u.F/u.L**2
	
	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = 'Non-linear'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') + 
		html_par('ratio of initial stiffness to yielding stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	
	# -T
	at_T = MpcAttributeMetaData()
	at_T.type = MpcAttributeType.Boolean
	at_T.name = '-T'
	at_T.group = 'Non-linear'
	at_T.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-T')+'<br/>') + 
		html_par('temperature') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	
	# temp
	at_temp = MpcAttributeMetaData()
	at_temp.type = MpcAttributeType.QuantityScalar
	at_temp.name = 'temp'
	at_temp.group = '-T'
	at_temp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('temp')+'<br/>') + 
		html_par('temperature') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	at_temp.dimension = u.T
	
	# -coKQ
	at_coKQ = MpcAttributeMetaData()
	at_coKQ.type = MpcAttributeType.Boolean
	at_coKQ.name = '-coKQ'
	at_coKQ.group = 'Non-linear'
	at_coKQ.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-coKQ')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	
	# rk
	at_rk = MpcAttributeMetaData()
	at_rk.type = MpcAttributeType.Real
	at_rk.name = 'rk'
	at_rk.group = '-coKQ'
	at_rk.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rk')+'<br/>') + 
		html_par('reduction rate for yielding stiffness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	
	# rq
	at_rq = MpcAttributeMetaData()
	at_rq.type = MpcAttributeType.Real
	at_rq.name = 'rq'
	at_rq.group = '-coKQ'
	at_rq.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rq')+'<br/>') + 
		html_par('reduction rate for yielding force at zero displacement') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiAikenLRB_Material','KikuchiAikenLRB Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'KikuchiAikenLRB'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_type)
	xom.addAttribute(at_ar)
	xom.addAttribute(at_hr)
	xom.addAttribute(at_gr)
	xom.addAttribute(at_ap)
	xom.addAttribute(at_tp)
	xom.addAttribute(at_alph)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_T)
	xom.addAttribute(at_temp)
	xom.addAttribute(at_coKQ)
	xom.addAttribute(at_rk)
	xom.addAttribute(at_rq)
	xom.addAttribute(at_coMSS)
	xom.addAttribute(at_rs)
	xom.addAttribute(at_rf)
	
	# use_T-dep
	xom.setVisibilityDependency(at_T, at_temp)
	
	# coKQ-dep
	xom.setVisibilityDependency(at_coKQ, at_rk)
	xom.setVisibilityDependency(at_coKQ, at_rq)
	
	# coMSS-dep
	xom.setVisibilityDependency(at_coMSS, at_rs)
	xom.setVisibilityDependency(at_coMSS, at_rf)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial KikuchiAikenLRB $matTag $type $ar $hr $gr $ap $tp $alph $beta
	#<-T $temp> <-coKQ $rk $rq> <-coMSS $rs $rf>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	ar_at = xobj.getAttribute('ar')
	if(ar_at is None):
		raise Exception('Error: cannot find "ar" attribute')
	ar = ar_at.quantityScalar.value
	
	hr_at = xobj.getAttribute('hr')
	if(hr_at is None):
		raise Exception('Error: cannot find "hr" attribute')
	hr = hr_at.quantityScalar.value
	
	gr_at = xobj.getAttribute('gr')
	if(gr_at is None):
		raise Exception('Error: cannot find "gr" attribute')
	gr = gr_at.quantityScalar.value
	
	ap_at = xobj.getAttribute('ap')
	if(ap_at is None):
		raise Exception('Error: cannot find "ap" attribute')
	ap = ap_at.quantityScalar.value
	
	tp_at = xobj.getAttribute('tp')
	if(tp_at is None):
		raise Exception('Error: cannot find "tp" attribute')
	tp = tp_at.quantityScalar.value
	
	alph_at = xobj.getAttribute('alph')
	if(alph_at is None):
		raise Exception('Error: cannot find "alph" attribute')
	alph = alph_at.quantityScalar.value
	
	beta_at = xobj.getAttribute('beta')
	if(beta_at is None):
		raise Exception('Error: cannot find "beta" attribute')
	beta = beta_at.real
	
	
	# optional paramters
	sopt = ''
	
	T_at = xobj.getAttribute('-T')
	if(T_at is None):
		raise Exception('Error: cannot find "-T" attribute')
	T = T_at.boolean
	if T:
		temp_at = xobj.getAttribute('temp')
		if(temp_at is None):
			raise Exception('Error: cannot find "temp" attribute')
		temp = temp_at.quantityScalar.value
		
		sopt += ' -T {}'.format(temp)
	
	coKQ_at = xobj.getAttribute('-coKQ')
	if(coKQ_at is None):
		raise Exception('Error: cannot find "-coKQ" attribute')
	coKQ = coKQ_at.boolean
	if coKQ:
		rk_at = xobj.getAttribute('rk')
		if(rk_at is None):
			raise Exception('Error: cannot find "rk" attribute')
		rk = rk_at.real
		
		rq_at = xobj.getAttribute('rq')
		if(rq_at is None):
			raise Exception('Error: cannot find "rq" attribute')
		rq = rq_at.real
		
		sopt += ' -coKQ {} {}'.format(rk, rq)
	
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
		
		sopt += ' -coMSS {} {}'.format(rs, rf)
	
	type = 1 # this should be taken from the type attribute (string) and converted to int
	# now the only option is 1!
	
	str_tcl = '{}uniaxialMaterial KikuchiAikenLRB {}  {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, type, ar, hr, gr, ap, tp, alph, beta, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
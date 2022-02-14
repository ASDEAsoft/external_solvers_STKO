# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
    
	def mka(name, group, descr, atype, adim = None, dval = None):
		a = MpcAttributeMetaData()
		a.type = atype
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('https://portwooddigital.com/2019/12/08/an-update-of-the-imk-models/','IMKPeakOriented')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# uniaxialMaterial IMKPeakOriented tag? Ke? Up_pos? Upc_pos? Uu_pos? Fy_pos? FmaxFy_pos? ResF_pos? Up_neg? Upc_neg? Uu_neg? Fy_neg? 
	# FmaxFy_neg? ResF_neg? LamdaS? LamdaC? LamdaA? LamdaK? Cs? Cc? Ca? Ck? D_pos? D_neg?

	Ke = mka("Ke", "Group", "Initial elastic stiffness", MpcAttributeType.Real)
	Up_pos = mka("Up_pos", "Group", "", MpcAttributeType.Real)
	Upc_pos = mka("Upc_pos", "Group", "", MpcAttributeType.Real)
	Uu_pos = mka("Uu_pos", "Group", "", MpcAttributeType.Real)
	Fy_pos = mka("Fy_pos", "Group", "Initial effective plastic force", MpcAttributeType.Real)
	FmaxFy_pos = mka("FmaxFy_pos", "Group", "Initial maximum-to-effective plastic force", MpcAttributeType.Real)
	ResF_pos = mka("ResF_pos", "Group", "Residual force", MpcAttributeType.Real)
	Up_neg = mka("Up_neg", "Group", "", MpcAttributeType.Real)
	Upc_neg = mka("Upc_neg", "Group", "", MpcAttributeType.Real)
	Uu_neg = mka("Uu_neg", "Group", "", MpcAttributeType.Real)
	Fy_neg = mka("Fy_neg", "Group", "Initial effective plastic force", MpcAttributeType.Real)
	FmaxFy_neg = mka("FmaxFy_neg", "Group", "Initial maximum-to-effective plastic force", MpcAttributeType.Real)
	ResF_neg = mka("ResF_neg", "Group", "Residual force", MpcAttributeType.Real)
	LamdaS = mka("LamdaS", "Group", "Cyclic deterioration parameter for strength deterioration", MpcAttributeType.Real)
	LamdaC = mka("LamdaC", "Group", "Cyclic deterioration parameter for post-capping strength deterioration", MpcAttributeType.Real)
	LamdaA = mka("LamdaA", "Group", "Cyclic deterioration parameter for acceleration reloading stiffness deterioration", MpcAttributeType.Real)
	LamdaK = mka("LamdaK", "Group", "Cyclic deterioration parameter for unloading stiffness deterioration", MpcAttributeType.Real)
	Cs = mka("Cs", "Group", "Rate of strength deterioration", MpcAttributeType.Real)
	Cc = mka("Cc", "Group", "Rate of post-capping strength deterioration", MpcAttributeType.Real)
	Ca = mka("Ca", "Group", "Rate of accelerated reloading deterioration", MpcAttributeType.Real)
	Ck = mka("Ck", "Group", "Rate of unloading stiffness deterioration", MpcAttributeType.Real)
	D_pos = mka("D_pos", "Group", "Rate of cyclic deterioration in the +ve loading direction", MpcAttributeType.Real)
	D_neg = mka("D_neg", "Group", "Rate of cyclic deterioration in the -ve loading direction", MpcAttributeType.Real)

	xom = MpcXObjectMetaData()
	xom.name = 'IMKPeakOriented'
	xom.Xgroup = 'Other Uniaxial Materials'

	xom.addAttribute(Ke)
	xom.addAttribute(Up_pos)
	xom.addAttribute(Upc_pos)
	xom.addAttribute(Uu_pos)
	xom.addAttribute(Fy_pos)
	xom.addAttribute(FmaxFy_pos)
	xom.addAttribute(ResF_pos)
	xom.addAttribute(Up_neg)
	xom.addAttribute(Upc_neg)
	xom.addAttribute(Uu_neg)
	xom.addAttribute(Fy_neg)
	xom.addAttribute(FmaxFy_neg)
	xom.addAttribute(ResF_neg)
	xom.addAttribute(LamdaS)
	xom.addAttribute(LamdaC)
	xom.addAttribute(LamdaA)
	xom.addAttribute(LamdaK)
	xom.addAttribute(Cs)
	xom.addAttribute(Cc)
	xom.addAttribute(Ca)
	xom.addAttribute(Ck)
	xom.addAttribute(D_pos)
	xom.addAttribute(D_neg)

	return xom

def writeTcl(pinfo):

	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	# uniaxialMaterial IMKPeakOriented tag? Ke? Up_pos? Upc_pos? Uu_pos? Fy_pos? FmaxFy_pos? ResF_pos? Up_neg? Upc_neg? Uu_neg? Fy_neg? 
	# FmaxFy_neg? ResF_neg? LamdaS? LamdaC? LamdaA? LamdaK? Cs? Cc? Ca? Ck? D_pos? D_neg?
	str_tcl = '{}uniaxialMaterial IMKPeakOriented {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
		pinfo.indent,
		tag,
		geta('Ke').real,
		geta('Up_pos').real,
		geta('Upc_pos').real,
		geta('Uu_pos').real,
		geta('Fy_pos').real,
		geta('FmaxFy_pos').real,
		geta('ResF_pos').real,
		geta('Up_neg').real,
		geta('Upc_neg').real,
		geta('Uu_neg').real,
		geta('Fy_neg').real,
		geta('FmaxFy_neg').real,
		geta('ResF_neg').real,
		geta('LamdaS').real,
		geta('LamdaC').real,
		geta('LamdaA').real,
		geta('LamdaK').real,
		geta('Cs').real,
		geta('Cc').real,
		geta('Ca').real,
		geta('Ck').real,
		geta('D_pos').real,
		geta('D_neg').real
		)

	# uniaxialMaterial IMKPeakOriented tag? Ke? Up_pos? Upc_pos? Uu_pos? Fy_pos? FmaxFy_pos? ResF_pos? Up_neg? Upc_neg? Uu_neg? Fy_neg? 
	# FmaxFy_neg? ResF_neg? LamdaS? LamdaC? LamdaA? LamdaK? Cs? Cc? Ca? Ck? D_pos? D_neg?
	pinfo.out_file.write(str_tcl)
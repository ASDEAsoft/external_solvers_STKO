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
			html_par(html_href('https://portwooddigital.com/2019/12/08/an-update-of-the-imk-models/','IMKBilin')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# uniaxialMaterial IMKBilin tag? Ke? Theta_p_pos? Theta_pc_pos? Theta_u_pos? Mpe_pos? MmaxMpe_pos? 
	# ResM_pos? Theta_p_neg? Theta_pc_neg? Theta_u_neg? Mpe_neg? MmaxMpe_neg? ResM_neg? LamdaS? 
	# LamdaC? LamdaK? Cs? Cc? Ck? D_pos? D_neg?

	Ke = mka("Ke", "Group", "Initial elastic stiffness", MpcAttributeType.Real)
	Theta_p_pos = mka("Theta_p_pos", "Group", "Initial pre-capping plastic rotation in the +ve loading direction", MpcAttributeType.Real)
	Theta_pc_pos = mka("Theta_pc_pos", "Group", "Initial post-capping plastic rotation in the +ve loading direction", MpcAttributeType.Real)
	Theta_u_pos = mka("Theta_u_pos", "Group", "Ultimate rotation in the +ve loading direction", MpcAttributeType.Real)
	Mpe_pos = mka("Mpe_pos", "Group", "Initial effective plastic moment in the +ve loading direction", MpcAttributeType.Real)
	MmaxMpe_pos = mka("MmaxMpe_pos", "Group", "Initial maximum-to-effective plastic moment ratio in the +ve loading direction", MpcAttributeType.Real)
	ResM_pos = mka("ResM_pos", "Group", "Residual moment in the +ve loading direction", MpcAttributeType.Real)
	Theta_p_neg = mka("Theta_p_neg", "Group", "Initial pre-capping plastic rotation in the -ve loading direction", MpcAttributeType.Real)
	Theta_pc_neg = mka("Theta_pc_neg", "Group", "Initial post-capping plastic rotation in the -ve loading direction", MpcAttributeType.Real)
	Theta_u_neg = mka("Theta_u_neg", "Group", "Ultimate rotation in the -ve loading direction", MpcAttributeType.Real)
	Mpe_neg = mka("Mpe_neg", "Group", "Initial effective plastic moment in the -ve loading direction", MpcAttributeType.Real)
	MmaxMpe_neg = mka("MmaxMpe_neg", "Group", "Initial maximum-to-effective plastic moment ratio in the -ve loading direction", MpcAttributeType.Real)
	ResM_neg = mka("ResM_neg", "Group", "Residual moment in the -ve loading direction", MpcAttributeType.Real)
	LamdaS = mka("LamdaS", "Group", "Cyclic deterioration parameter for strength deterioration", MpcAttributeType.Real)
	LamdaC = mka("LamdaC", "Group", "Cyclic deterioration parameter for post-capping strength deterioration", MpcAttributeType.Real)
	LamdaK = mka("LamdaK", "Group", "Cyclic deterioration parameter for unloading stiffness deterioration", MpcAttributeType.Real)
	Cs = mka("Cs", "Group", "Rate of strength deterioration", MpcAttributeType.Real)
	Cc = mka("Cc", "Group", "Rate of post-capping strength deterioration", MpcAttributeType.Real)
	Ck = mka("Ck", "Group", "Rate of unloading stiffness deterioration", MpcAttributeType.Real)
	D_pos = mka("D_pos", "Group", "Rate of cyclic deterioration in the +ve loading direction", MpcAttributeType.Real)
	D_neg = mka("D_neg", "Group", "Rate of cyclic deterioration in the -ve loading direction", MpcAttributeType.Real)

	xom = MpcXObjectMetaData()
	xom.name = 'IMKBilin'
	xom.Xgroup = 'Other Uniaxial Materials'

	xom.addAttribute(Ke)
	xom.addAttribute(Theta_p_pos)
	xom.addAttribute(Theta_pc_pos)
	xom.addAttribute(Theta_u_pos)
	xom.addAttribute(Mpe_pos)
	xom.addAttribute(MmaxMpe_pos)
	xom.addAttribute(ResM_pos)
	xom.addAttribute(Theta_p_neg)
	xom.addAttribute(Theta_pc_neg)
	xom.addAttribute(Theta_u_neg)
	xom.addAttribute(Mpe_neg)
	xom.addAttribute(MmaxMpe_neg)
	xom.addAttribute(ResM_neg)
	xom.addAttribute(LamdaS)
	xom.addAttribute(LamdaC)
	xom.addAttribute(LamdaK)
	xom.addAttribute(Cs)
	xom.addAttribute(Cc)
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

	# uniaxialMaterial IMKBilin tag? Ke? Theta_p_pos? Theta_pc_pos? Theta_u_pos? Mpe_pos? MmaxMpe_pos? 
	# ResM_pos? Theta_p_neg? Theta_pc_neg? Theta_u_neg? Mpe_neg? MmaxMpe_neg? ResM_neg? LamdaS? 
	# LamdaC? LamdaK? Cs? Cc? Ck? D_pos? D_neg?
	str_tcl = '{}uniaxialMaterial IMKBilin {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
		pinfo.indent,
		tag,
		geta('Ke').real,
		geta('Theta_p_pos').real,
		geta('Theta_pc_pos').real,
		geta('Theta_u_pos').real,
		geta('Mpe_pos').real,
		geta('MmaxMpe_pos').real,
		geta('ResM_pos').real,
		geta('Theta_p_neg').real,
		geta('Theta_pc_neg').real,
		geta('Theta_u_neg').real,
		geta('Mpe_neg').real,
		geta('MmaxMpe_neg').real,
		geta('ResM_neg').real,
		geta('LamdaS').real,
		geta('LamdaC').real,
		geta('LamdaK').real,
		geta('Cs').real,
		geta('Cc').real,
		geta('Ck').real,
		geta('D_pos').real,
		geta('D_neg').real,
		)

	# now write the string into the file
	pinfo.out_file.write(str_tcl)
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
			html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/PM4Silt_Material_(Beta)','PM4Silt')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# nDMaterial PM4Silt $matTag $S_u $Su_Rat $G_o $h_po $Den   <$Su_factor $Patm $nu $nG $h0 $eInit $lambda $phicv $nb_wet $nb_dry $nd $Ado $ru_max $zmax $cz $ce $Cgd $ckaf $m_m $CG_consol>
	S_u = mka("S_u", "Mandatory Parameters", "Undrained shear strength", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Su_Rat = mka("Su_Rat", "Mandatory Parameters", "Undrained shear strength ratio. If both S_u and Su_Rat values are specified, the value of S_u is used.", MpcAttributeType.QuantityScalar)
	G_o = mka("G_o", "Mandatory Parameters", "Shear modulus constant", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	h_po = mka("h_po", "Mandatory Parameters", "Contraction rate parameter", MpcAttributeType.QuantityScalar)
	Den = mka("Den", "Mandatory Parameters", "Mass density of the material", MpcAttributeType.QuantityScalar)

	# Optional parameters
	Optional = mka("Use Optional Parameters", "Optional parameters", "", MpcAttributeType.Boolean)
	Su_factor = mka("Su_factor", "Optional parameters", "Undrained shear strength reduction factor", MpcAttributeType.Real)
	Patm = mka("Patm", "Optional parameters", "Atmospheric pressure", MpcAttributeType.Real)
	nu = mka("nu", "Optional parameters", "Poisson's ratio. Default value is 0.3.", MpcAttributeType.Real, dval = 0.3)
	nG = mka("nG", "Optional parameters", "Shear modulus exponent. Default value is 0.75.", MpcAttributeType.Real, dval = 0.75)
	h0 = mka("h0", "Optional parameters", "Variable that adjusts the ratio of plastic modulus to elastic modulus. Default value is 0.5.", MpcAttributeType.Real, dval = 0.5)
	eInit = mka("eInit", "Optional parameters", "Initial void ratios. Default value is 0.90.", MpcAttributeType.Real, dval = 0.9)
	lambda_ = mka("lambda", "Optional parameters", "The slope of critical state line in e-ln(p) space. Default value is 0.060.", MpcAttributeType.Real, dval = 0.06)
	phicv = mka("phicv", "Optional parameters", "Critical state effective friction angle. Default value is 32 degrees.", MpcAttributeType.Real, dval = 32.0)
	nb_wet = mka("nb_wet", "Optional parameters", "Bounding surface parameter for loose of critical state conditions, 1.0 ≥ $nb_wet ≥ 0.01. Default value is 0.8.", MpcAttributeType.Real, dval = 0.8)
	nb_dry = mka("nb_dry", "Optional parameters", "Bounding surface parameter for dense of critical state conditions, $nb_dry ≥ 0. Default value is 0.5.", MpcAttributeType.Real, dval = 0.5)
	nd = mka("nd", "Optional parameters", "Dilatancy surface parameter $nd ≥ 0. Default value is 0.3.", MpcAttributeType.Real, dval = 0.3)
	Ado = mka("Ado", "Optional parameters", "Dilatancy parameter. Default value is 0.8.", MpcAttributeType.Real, dval = 0.8)
	ru_max = mka("ru_max", "Optional parameters", "Maximum pore pressure ratio based on p'.", MpcAttributeType.Real, dval = -1.0)
	zmax = mka("zmax", "Optional parameters", "Fabric-dilatancy tensor parameter", MpcAttributeType.Real, dval = -1.0)
	cz = mka("cz", "Optional parameters", "Fabric-dilatancy tensor parameter. Default value is 100.0.", MpcAttributeType.Real, dval = 100.0)
	ce = mka("ce", "Optional parameters", "Variable that adjusts the rate of strain accumulation in cyclic loading", MpcAttributeType.Real, dval = -1.0)
	Cgd = mka("Cgd", "Optional parameters", "Variable that adjusts degradation of elastic modulus with accumulation of fabric. Default value is 3.0.", MpcAttributeType.Real, dval = 3.0)
	ckaf = mka("ckaf", "Optional parameters", "Variable that controls the effect that sustained static shear stresses have on plastic modulus. Default value is 4.0.", MpcAttributeType.Real, dval = 4.0)
	m_m = mka("m_m", "Optional parameters", "Yield surface constant (radius of yield surface in stress ratio space). Default value is 0.01.", MpcAttributeType.Real, dval = 0.01)
	CG_consol = mka("CG_consol", "Optional parameters", "Reduction factor of elastic modulus for reconsolidation. $CG_consol ≥ 1. Default value is 2.0.", MpcAttributeType.Real, dval = 2.0)

	# Parameters
	xom = MpcXObjectMetaData()
	xom.name = 'PM4Silt'
	xom.Xgroup = 'Other nD Materials'
	
	# mandatory
	pmandatory = [S_u, Su_Rat, G_o, h_po, Den]
	for i in pmandatory:
		xom.addAttribute(i)

	# optional
	xom.addAttribute(Optional)
	poptional = [Su_factor, Patm, nu, nG, h0, eInit, lambda_, phicv, nb_wet, nb_dry, nd, Ado, ru_max, zmax, cz, ce, Cgd, ckaf, m_m, CG_consol]
	for i in poptional:
		xom.addAttribute(i)
		
	# visibility dependency
	for i in poptional:
		xom.setVisibilityDependency(Optional, i)
	
	return xom

def writeTcl(pinfo):
	# nDMaterial PM4Silt $matTag $S_u $Su_Rat $G_o $h_po $Den   <$Su_factor $Patm $nu $nG $h0 $eInit $lambda $phicv $nb_wet $nb_dry $nd $Ado $ru_max $zmax $cz $ce $Cgd $ckaf $m_m $CG_consol>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId

	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	# mandatory
	pmandatory = ["S_u","Su_Rat","G_o","h_po","Den"]
	smandatory = ' '.join(str(geta(i).quantityScalar.value) for i in pmandatory)
	
	# optional
	soptional = ''
	if geta('Use Optional Parameters').boolean:
		poptional = ["Su_factor","Patm","nu","nG","h0","eInit","lambda","phicv","nb_wet","nb_dry","nd","Ado","ru_max","zmax","cz","ce","Cgd","ckaf","m_m","CG_consol"]
		soptional = ' '.join(str(geta(i).real) for i in poptional)
	
	# nDMaterial PM4Silt $matTag $Dr $G0 $hpo $Den <$patm $h0 $emax $emin $nb $nd $Ado $zmax $cz $ce $phic $nu $cgd $cdr $ckaf $Q $R $m $Fsed_min $p_sedo>
	str_tcl = '{}nDMaterial PM4Silt {} {} {}\n'.format(
			pinfo.indent,
			tag,
			smandatory,
			soptional)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
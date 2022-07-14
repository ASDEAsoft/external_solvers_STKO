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
			html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/PM4Sand_Material','PM4Sand')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	# nDMaterial PM4Sand $matTag $Dr $G0 $hpo $Den <$patm $h0 $emax $emin $nb $nd $Ado $zmax $cz $ce $phic $nu $cgd $cdr $ckaf $Q $R $m $Fsed_min $p_sedo>
	Dr = mka("Dr", "Group", "Relative density, in fraction", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	G0 = mka("G0", "Group", "Shear modulus constant", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	hpo = mka("hpo", "Group", "Contraction rate parameter", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)
	Den = mka("Den", "Group", "Mass density of the material", MpcAttributeType.QuantityScalar, adim=u.F/u.L**2)

	# Optional parameters
	Optional = mka("Optional", "Optional parameters", "", MpcAttributeType.Boolean)
	P_atm = mka("P_atm", "Optional parameters", "Atmospheric pressure", MpcAttributeType.Real)
	h0 = mka("h0", "Optional parameters", "Variable that adjusts the ratio of plastic modulus to elastic modulus", MpcAttributeType.Real)
	emax = mka("emax", "Optional parameters", "Maximum void ratios", MpcAttributeType.Real)
	emin = mka("emin", "Optional parameters", "Minimum  void ratios", MpcAttributeType.Real)
	nb = mka("nb", "Optional parameters", "Bounding surface parameter, nb >= 0", MpcAttributeType.Real)
	nd = mka("nd", "Optional parameters", "Dilatancy surface parameter nd >= 0", MpcAttributeType.Real)
	Ado = mka("Ado", "Optional parameters", "Dilatancy parameter, will be computed at the time of initialization if input value is negative", MpcAttributeType.Real)
	z_max = mka("z_max", "Optional parameters", "Fabric-dilatancy tensor parameter", MpcAttributeType.Real)
	cz = mka("cz", "Optional parameters", "Fabric-dilatancy tensor parameter", MpcAttributeType.Real)
	ce = mka("ce", "Optional parameters", "Variable that adjusts the rate of strain accumulation in cyclic loading", MpcAttributeType.Real)
	phic = mka("phic", "Optional parameters", "Critical state effective friction angle", MpcAttributeType.Real)
	nu = mka("nu", "Optional parameters", "Poisson's ratio", MpcAttributeType.Real)
	cgd = mka("cgd", "Optional parameters", "Variable that adjusts degradation of elastic modulus with accumulation of fabric", MpcAttributeType.Real)
	cdr = mka("cdr", "Optional parameters", "Variable that controls the rotated dilatancy surface", MpcAttributeType.Real)
	ckaf = mka("ckaf", "Optional parameters", "Variable that controls the effect that sustained static shear stresses have on plastic modulus", MpcAttributeType.Real)
	Q = mka("Q", "Optional parameters", "Critical state line parameter", MpcAttributeType.Real)
	R = mka("R", "Optional parameters", "Critical state line parameter", MpcAttributeType.Real)
	m = mka("m", "Optional parameters", "Yield surface constant (radius of yield surface in stress ratio space)", MpcAttributeType.Real)
	Fsed_min = mka("Fsed_min", "Optional parameters", "Variable that controls the minimum value the reduction factor of the elastic moduli can get during reconsolidation", MpcAttributeType.Real)
	p_sedo = mka("p_sedo", "Optional parameters", "Mean effective stress up to which reconsolidation strains are enhanced", MpcAttributeType.Real)

	# Parameters
	xom = MpcXObjectMetaData()
	xom.name = 'PM4Sand'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(Dr)
	xom.addAttribute(G0)
	xom.addAttribute(hpo)
	xom.addAttribute(Den)

	# Optional parameters
	xom.addAttribute(Optional)
	xom.addAttribute(P_atm)
	xom.addAttribute(h0)
	xom.addAttribute(emax)
	xom.addAttribute(emin)
	xom.addAttribute(nb)
	xom.addAttribute(nd)
	xom.addAttribute(Ado)
	xom.addAttribute(z_max)
	xom.addAttribute(cz)
	xom.addAttribute(ce)
	xom.addAttribute(phic)
	xom.addAttribute(nu)
	xom.addAttribute(cgd)
	xom.addAttribute(cdr)
	xom.addAttribute(ckaf)
	xom.addAttribute(Q)
	xom.addAttribute(R)
	xom.addAttribute(m)
	xom.addAttribute(Fsed_min)
	xom.addAttribute(p_sedo)

	# Optional parameters
	xom.setVisibilityDependency(Optional, P_atm)
	xom.setVisibilityDependency(Optional, h0)
	xom.setVisibilityDependency(Optional, emax)
	xom.setVisibilityDependency(Optional, emin)
	xom.setVisibilityDependency(Optional, nb)
	xom.setVisibilityDependency(Optional, nd)
	xom.setVisibilityDependency(Optional, Ado)
	xom.setVisibilityDependency(Optional, z_max)
	xom.setVisibilityDependency(Optional, cz)
	xom.setVisibilityDependency(Optional, ce)
	xom.setVisibilityDependency(Optional, phic)
	xom.setVisibilityDependency(Optional, nu)
	xom.setVisibilityDependency(Optional, cgd)
	xom.setVisibilityDependency(Optional, cdr)
	xom.setVisibilityDependency(Optional, ckaf)
	xom.setVisibilityDependency(Optional, Q)
	xom.setVisibilityDependency(Optional, R)
	xom.setVisibilityDependency(Optional, m)
	xom.setVisibilityDependency(Optional, Fsed_min)
	xom.setVisibilityDependency(Optional, p_sedo)

	return xom

def writeTcl(pinfo):
	# nDMaterial PM4Sand $matTag $Dr $G0 $hpo $Den <$patm $h0 $emax $emin $nb $nd $Ado $zmax $cz $ce $phic $nu $cgd $cdr $ckaf $Q $R $m $Fsed_min $p_sedo>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId

	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	# optional paramters
	sopt = ''
	if geta('Optional').boolean:
		sopt += ' {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(geta('P_atm').real
		, geta('h0').real
		, geta('emax').real
		, geta('emin').real
		, geta('nb').real
		, geta('nd').real
		, geta('Ado').real
		, geta('z_max').real
		, geta('cz').real
		, geta('ce').real
		, geta('phic').real
		, geta('nu').real
		, geta('cgd').real
		, geta('cdr').real
		, geta('ckaf').real
		, geta('Q').real
		, geta('R').real
		, geta('m').real
		, geta('Fsed_min').real
		, geta('p_sedo').real)

	# nDMaterial PM4Sand $matTag $Dr $G0 $hpo $Den <$patm $h0 $emax $emin $nb $nd $Ado $zmax $cz $ce $phic $nu $cgd $cdr $ckaf $Q $R $m $Fsed_min $p_sedo>
	str_tcl = '{}nDMaterial PM4Sand {} {} {} {} {}{}\n'.format(
			pinfo.indent,
			tag,
			geta('Dr').quantityScalar.value,
			geta('G0').quantityScalar.value,
			geta('hpo').quantityScalar.value,
			geta('Den').quantityScalar.value,
			sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
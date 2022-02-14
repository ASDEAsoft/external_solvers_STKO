# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# fpc1
	at_fpc1 = MpcAttributeMetaData()
	at_fpc1.type = MpcAttributeType.QuantityScalar
	at_fpc1.name = 'fpc1'
	at_fpc1.group = 'Non-linear'
	at_fpc1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fpc1')+'<br/>') + 
		html_par('Concrete core compressive strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_fpc1.dimension = u.F/u.L**2
	
	# fpc2
	at_fpc2 = MpcAttributeMetaData()
	at_fpc2.type = MpcAttributeType.QuantityScalar
	at_fpc2.name = 'fpc2'
	at_fpc2.group = 'Non-linear'
	at_fpc2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fpc2')+'<br/>') + 
		html_par('Concrete cover compressive strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_fpc2.dimension = u.F/u.L**2
	
	# epsc0
	at_epsc0 = MpcAttributeMetaData()
	at_epsc0.type = MpcAttributeType.Real
	at_epsc0.name = 'epsc0'
	at_epsc0.group = 'Non-linear'
	at_epsc0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epsc0')+'<br/>') + 
		html_par('strain corresponding to unconfined concrete strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	
	# D
	at_D = MpcAttributeMetaData()
	at_D.type = MpcAttributeType.QuantityScalar
	at_D.name = 'D'
	at_D.group = 'Misc'
	at_D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D')+'<br/>') + 
		html_par('diameter of the circular section.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_D.dimension = u.L
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.QuantityScalar
	at_c.name = 'c'
	at_c.group = 'Misc'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') + 
		html_par('Dimension of concrete cover (until the outer edge of steel stirrups)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_c.dimension = u.L
	
	# Ej
	at_Ej = MpcAttributeMetaData()
	at_Ej.type = MpcAttributeType.QuantityScalar
	at_Ej.name = 'Ej'
	at_Ej.group = 'Elasticity'
	at_Ej.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ej')+'<br/>') + 
		html_par('Elastic modulus of the fiber reinforced polymer (FRP) jacket') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_Ej.dimension = u.F/u.L**2
	
	# Sj
	at_Sj = MpcAttributeMetaData()
	at_Sj.type = MpcAttributeType.QuantityScalar
	at_Sj.name = 'Sj'
	at_Sj.group = 'Misc'
	at_Sj.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Sj')+'<br/>') + 
		html_par('Clear spacing of the FRP strips - zero if FRP jacket is continuous') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_Sj.dimension = u.L
	
	# tj
	at_tj = MpcAttributeMetaData()
	at_tj.type = MpcAttributeType.QuantityScalar
	at_tj.name = 'tj'
	at_tj.group = 'Misc'
	at_tj.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tj')+'<br/>') + 
		html_par('Total thickness of the FRP jacket') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_tj.dimension = u.L
	
	# eju
	at_eju = MpcAttributeMetaData()
	at_eju.type = MpcAttributeType.Real
	at_eju.name = 'eju'
	at_eju.group = 'Non-linear'
	at_eju.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eju')+'<br/>') + 
		html_par('Rupture strain of the FRP jacket from tensile coupons') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
		
	# S
	at_S = MpcAttributeMetaData()
	at_S.type = MpcAttributeType.QuantityScalar
	at_S.name = 'S'
	at_S.group = 'Misc'
	at_S.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('S')+'<br/>') + 
		html_par('Spacing of the steel spiral/stirrups') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_S.dimension = u.L
	
	# fyh
	at_fyh = MpcAttributeMetaData()
	at_fyh.type = MpcAttributeType.QuantityScalar
	at_fyh.name = 'fyh'
	at_fyh.group = 'Non-linear'
	at_fyh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fyh')+'<br/>') + 
		html_par('Yielding strength of the steel spiral/stirrups') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_fyh.dimension = u.F/u.L**2
	
	# dlong
	at_dlong = MpcAttributeMetaData()
	at_dlong.type = MpcAttributeType.QuantityScalar
	at_dlong.name = 'dlong'
	at_dlong.group = 'Misc'
	at_dlong.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dlong')+'<br/>') + 
		html_par('diameter of the longitudinal bars of the circular section') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_dlong.dimension = u.L
	
		
	# dtrans
	at_dtrans = MpcAttributeMetaData()
	at_dtrans.type = MpcAttributeType.QuantityScalar
	at_dtrans.name = 'dtrans'
	at_dtrans.group = 'Misc'
	at_dtrans.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dtrans')+'<br/>') + 
		html_par('Diameter of the steel spiral/stirrups') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_dtrans.dimension = u.L
	
	# Es
	at_Es = MpcAttributeMetaData()
	at_Es.type = MpcAttributeType.QuantityScalar
	at_Es.name = 'Es'
	at_Es.group = 'Elasticity'
	at_Es.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Es')+'<br/>') + 
		html_par('elastic modulus of steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	at_Es.dimension = u.F/u.L**2
	
	# vo
	at_vo = MpcAttributeMetaData()
	at_vo.type = MpcAttributeType.Real
	at_vo.name = 'vo'
	at_vo.group = 'Elasticity'
	at_vo.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('vo')+'<br/>') + 
		html_par('Initial Poisson’s coefficient for concrete') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)
	
	# k
	at_k = MpcAttributeMetaData()
	at_k.type = MpcAttributeType.Real
	at_k.name = 'k'
	at_k.group = 'Misc'
	at_k.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('k')+'<br/>') + 
		html_par('Reduction factor for the rupture strain of the FRP jacket, recommended values 0.5-0.8') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FRPConfinedConcrete','FRPConfinedConcrete Material')+'<br/>') +
		html_end()
		)

	
	xom = MpcXObjectMetaData()
	xom.name = 'FRPConfinedConcrete'
	xom.Xgroup = 'Concrete Materials'
	xom.addAttribute(at_fpc1)
	xom.addAttribute(at_fpc2)
	xom.addAttribute(at_epsc0)
	xom.addAttribute(at_D)
	xom.addAttribute(at_c)
	xom.addAttribute(at_Ej)
	xom.addAttribute(at_Sj)
	xom.addAttribute(at_tj)
	xom.addAttribute(at_eju)
	xom.addAttribute(at_S)
	xom.addAttribute(at_fyh)
	xom.addAttribute(at_dlong)
	xom.addAttribute(at_dtrans)
	xom.addAttribute(at_Es)
	xom.addAttribute(at_vo)
	xom.addAttribute(at_k)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial FRPConfinedConcrete $matTag $fpc1 $fpc2 $epsc0 $D $c $Ej $Sj $tj $eju $S $fyh $dlong $dtrans $Es $vo $k
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fpc1_at = xobj.getAttribute('fpc1')
	if(fpc1_at is None):
		raise Exception('Error: cannot find "fpc1" attribute')
	fpc1 = fpc1_at.quantityScalar
	
	fpc2_at = xobj.getAttribute('fpc2')
	if(fpc2_at is None):
		raise Exception('Error: cannot find "fpc2" attribute')
	fpc2 = fpc2_at.quantityScalar
	
	epsc0_at = xobj.getAttribute('epsc0')
	if(epsc0_at is None):
		raise Exception('Error: cannot find "epsc0" attribute')
	epsc0 = epsc0_at.real
	
	D_at = xobj.getAttribute('D')
	if(D_at is None):
		raise Exception('Error: cannot find "D" attribute')
	D = D_at.quantityScalar
	
	c_at = xobj.getAttribute('c')
	if(c_at is None):
		raise Exception('Error: cannot find "c" attribute')
	c = c_at.quantityScalar
	
	Ej_at = xobj.getAttribute('Ej')
	if(Ej_at is None):
		raise Exception('Error: cannot find "Ej" attribute')
	Ej = Ej_at.quantityScalar
	
	Sj_at = xobj.getAttribute('Sj')
	if(Sj_at is None):
		raise Exception('Error: cannot find "Sj" attribute')
	Sj = Sj_at.quantityScalar
	
	tj_at = xobj.getAttribute('tj')
	if(tj_at is None):
		raise Exception('Error: cannot find "tj" attribute')
	tj = tj_at.quantityScalar
	
	eju_at = xobj.getAttribute('eju')
	if(eju_at is None):
		raise Exception('Error: cannot find "eju" attribute')
	eju = eju_at.real
	
	S_at = xobj.getAttribute('S')
	if(S_at is None):
		raise Exception('Error: cannot find "S" attribute')
	S = S_at.quantityScalar
	
	fyh_at = xobj.getAttribute('fyh')
	if(fyh_at is None):
		raise Exception('Error: cannot find "fyh" attribute')
	fyh = fyh_at.quantityScalar
	
	dlong_at = xobj.getAttribute('dlong')
	if(dlong_at is None):
		raise Exception('Error: cannot find "dlong" attribute')
	dlong = dlong_at.quantityScalar
	
	dtrans_at = xobj.getAttribute('dtrans')
	if(dtrans_at is None):
		raise Exception('Error: cannot find "dtrans" attribute')
	dtrans = dtrans_at.quantityScalar
	
	Es_at = xobj.getAttribute('Es')
	if(Es_at is None):
		raise Exception('Error: cannot find "Es" attribute')
	Es = Es_at.quantityScalar
	
	vo_at = xobj.getAttribute('vo')
	if(vo_at is None):
		raise Exception('Error: cannot find "vo" attribute')
	vo = vo_at.real
	
	k_at = xobj.getAttribute('k')
	if(k_at is None):
		raise Exception('Error: cannot find "k" attribute')
	k = k_at.real
	
	
	str_tcl = '{}uniaxialMaterial FRPConfinedConcrete {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fpc1.value, fpc2.value, epsc0, D.value, c.value, Ej.value, Sj.value, tj.value,
			eju, S.value, fyh.value, dlong.value, dtrans.value, Es.value, vo, k)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
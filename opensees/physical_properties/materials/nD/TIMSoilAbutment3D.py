# enable default 3D TIM tester for this module
from opensees.physical_properties.utils.tester.EnableTesterTIM3D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# util
	def mka(name, group, type, description, dim=None, dval=None):
		# todo: update URL
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(description) +
			html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Isotropic_Material','Soil Abutment 3D')+'<br/>') +
			html_end()
			)
		if dim is not None:
			a.dimension = dim
		if dval is not None:
			a.setDefault(dval)
		return a
	
	H11el = mka('H11el', 'Initial Stiffness', MpcAttributeType.QuantityScalar, 'First coefficient of Initial Stiffness tensor', dim = u.F/u.L, dval=0.0)
	H22el = mka('H22el', 'Initial Stiffness', MpcAttributeType.QuantityScalar, 'Second coefficient of Initial Stiffness tensor', dim = u.F/u.L, dval=0.0)
	H33el = mka('H33el', 'Initial Stiffness', MpcAttributeType.QuantityScalar, 'Third coefficient of Initial Stiffness tensor', dim = u.F/u.L, dval=0.0)
	
	aMult = mka('aMult', 'Ultimate Surface', MpcAttributeType.QuantityScalar, 'Major semi-axis of the utlimate surface ellipse', dim = u.F/u.L, dval=0.0)
	aiult = mka('aiult', 'Ultimate Surface', MpcAttributeType.QuantityScalar, 'Intermediate semi-axis of the utlimate surface ellipse', dim = u.F/u.L, dval=0.0)
	alult = mka('alult', 'Ultimate Surface', MpcAttributeType.QuantityScalar, 'Lower semi-axis of the utlimate surface ellipse', dim = u.F/u.L, dval=0.0)
	delta = mka('delta', 'Ultimate Surface', MpcAttributeType.Real, 'Orientation (in degrees) of the ultimate surface', dval=15.0)
	Mc1 = mka('Mc1', 'Ultimate Surface', MpcAttributeType.Real, 'Factor controlling the asymmetry of the ultimate surface along the first axis', dval=3.0)
	Mc3 = mka('Mc3', 'Ultimate Surface', MpcAttributeType.Real, 'Factor controlling the asymmetry of the ultimate surface along the third axis', dval=0.95)
	
	nYield = mka('nYield', 'Misc', MpcAttributeType.Integer, 'Number of yield surfaces', dval=5)
	tol = mka('tol', 'Misc', MpcAttributeType.Real, 'Relative tolerance used for internal iterations', dval=1.0e-2)
	niter = mka('niter', 'Misc', MpcAttributeType.Integer, 'Max number of iterations', dval=100)
	
	xom = MpcXObjectMetaData()
	xom.name = 'TIMSoilAbutment3D'
	xom.Xgroup = 'TIM'
	xom.addAttribute(H11el)
	xom.addAttribute(H22el)
	xom.addAttribute(H33el)
	xom.addAttribute(aMult)
	xom.addAttribute(aiult)
	xom.addAttribute(alult)
	xom.addAttribute(delta)
	xom.addAttribute(Mc1)
	xom.addAttribute(Mc3)
	xom.addAttribute(nYield)
	xom.addAttribute(tol)
	xom.addAttribute(niter)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial TIMSoilAbutment3D $tag $nYield  $H11el    $H22el   $H33el    $aMult     $aiult    $alult    $delta  $tol   $niter  $YieldShape
	
	# get current instance and tag
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# util
	def err(msg):
		raise Exception('Error in SoilAbutment3D @ [{}] {}: {}'.format(
			tag, xobj.parent.name, msg))
	def geta(name):
		a = xobj.getAttribute(name)
		if a is None:
			err('Error: cannot find "{}" attribute'.format(name))
		return a
	
	# mandatory parameters
	nYield = geta('nYield').integer
	
	H11el = geta('H11el').quantityScalar.value
	H22el = geta('H22el').quantityScalar.value
	H33el = geta('H33el').quantityScalar.value
	
	aMult = geta('aMult').quantityScalar.value
	aiult = geta('aiult').quantityScalar.value
	alult = geta('alult').quantityScalar.value
	delta = geta('delta').real
	Mc1 = geta('Mc1').real
	Mc3 = geta('Mc3').real
	
	tol = geta('tol').real
	niter = geta('niter').integer
	
	# check values
	if H11el < 0.0:
		err('H11el must be positive ( >= 0 )')
	# todo: others
	
	# done
	str_tcl = '{}nDMaterial TIMSoilAbutment3D {}   {}   {} {} {}   {} {} {} {}   {}   {} {}   {}\n'.format(
		pinfo.indent, tag,
		nYield, H11el, H22el, H33el,
		aMult, aiult, alult, delta,
		Mc1, Mc3, tol, niter)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
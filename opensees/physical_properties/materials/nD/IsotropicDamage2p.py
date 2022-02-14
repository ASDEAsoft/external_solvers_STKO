# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	def mka(name, type, group, descr, dim = None, default = None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Elastic_Isotropic_Material','Elastic Isotropic Material')+'<br/>') +
			html_end()
			)
		if dim:
			a.dimension = dim
		if default:
			a.setDefault(default)
		return a
	
	rho = mka('rho', MpcAttributeType.QuantityScalar, 'Mass', "The Mass density")
	E = mka('E', MpcAttributeType.QuantityScalar, 'Elasticity', "The Young's modulus", dim = u.F/u.L/u.L)
	v = mka('v', MpcAttributeType.Real, 'Elasticity', "The Poisson's ratio", )
	yt0 = mka('Yt0', MpcAttributeType.Real, 'Tension', "Initial damage threshold")
	at = mka('at', MpcAttributeType.Real, 'Tension', "Hardening-Softening law parameter", default = 1.0)
	bt = mka('bt', MpcAttributeType.Real, 'Tension', "Hardening-Softening law parameter", default = 0.001)
	yc0 = mka('Yc0', MpcAttributeType.Real, 'Compression', "Initial damage threshold")
	ac = mka('ac', MpcAttributeType.Real, 'Compression', "Hardening-Softening law parameter", default = 1.0)
	bc = mka('bc', MpcAttributeType.Real, 'Compression', "Hardening-Softening law parameter", default = 0.01)
	beta = mka('beta', MpcAttributeType.Real, 'Compression', "Biaxial compression parameter", default = -0.5)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'IsotropicDamage2p'
	xom.Xgroup = 'ASDEASoftware'
	xom.addAttribute(rho)
	xom.addAttribute(E)
	xom.addAttribute(v)
	xom.addAttribute(yt0)
	xom.addAttribute(at)
	xom.addAttribute(bt)
	xom.addAttribute(yc0)
	xom.addAttribute(ac)
	xom.addAttribute(bc)
	xom.addAttribute(beta)
	
	return xom

def writeTcl(pinfo):
	
	# nDMaterial IsotropicDamage2p $tag $E $nu $yt0 $yco $bt $bc $at $ac <-beta $beta> <-rho $rho>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# utils
	def geta(name):
		a = xobj.getAttribute(name)
		if a is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return a
	
	rho = geta('rho').quantityScalar.value
	E = geta('E').quantityScalar.value
	v = geta('v').real
	yt0 = geta('Yt0').real
	at = geta('at').real
	bt = geta('bt').real
	yc0 = geta('Yc0').real
	ac = geta('ac').real
	bc = geta('bc').real
	beta = geta('beta').real
	
	# now write the string into the file
	pinfo.out_file.write(
		'{}nDMaterial IsotropicDamage2p {} {} {} {} {} {} {} {} {} -beta {} -rho {}\n'.format(
			pinfo.indent, tag, E, v, yt0, yc0, bt, bc, at, ac, beta, rho))
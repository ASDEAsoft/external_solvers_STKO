import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# E
	at_E = MpcAttributeMetaData()
	at_E.type = MpcAttributeType.QuantityScalar
	at_E.name = 'E'
	at_E.group = 'Elasticity'
	at_E.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('E')+'<br/>') + 
		html_par('elastic Modulus') +
		html_end()
		)
	at_E.dimension = u.F/u.L**2
	
	# v
	at_v = MpcAttributeMetaData()
	at_v.type = MpcAttributeType.Real
	at_v.name = 'v'
	at_v.group = 'Elasticity'
	at_v.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('v')+'<br/>') + 
		html_par('Poisson\'s ratio') +
		html_end()
		)
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.QuantityScalar
	at_rho.name = 'rho'
	at_rho.group = 'Elasticity'
	at_rho.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('rho')+'<br/>') + 
		html_par('mass density') +
		html_end()
		)
	at_rho.setDefault(0.0)
	#at_rho.dimension = u.M/u.L**3
	
	# use optional parameters
	at_opt = MpcAttributeMetaData()
	at_opt.type = MpcAttributeType.Boolean
	at_opt.name = 'use optional parameters'
	at_opt.group = 'Optional Parameters'
	at_opt.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use optional parameters')+'<br/>') + 
		html_par('Check it if you want to input all optional parameters') +
		html_end()
		)
	
	# expp
	at_expp = MpcAttributeMetaData()
	at_expp.type = MpcAttributeType.QuantityScalar
	at_expp.name = 'expp'
	at_expp.group = 'Optional Parameters'
	at_expp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('expp')+'<br/>') + 
		html_par('exponent of the pressure sensitive elastic material') +
		html_end()
		)
	at_expp.setDefault(0.0)
	
	# prp
	at_prp = MpcAttributeMetaData()
	at_prp.type = MpcAttributeType.QuantityScalar
	at_prp.name = 'prp'
	at_prp.group = 'Optional Parameters'
	at_prp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('prp')+'<br/>') + 
		html_par('reference pressure of the pressure sensitive elastic material') +
		html_end()
		)
	at_prp.dimension = u.F/u.L**2
	at_prp.setDefault(0.0)
	
	# pop
	at_pop = MpcAttributeMetaData()
	at_pop.type = MpcAttributeType.QuantityScalar
	at_pop.name = 'pop'
	at_pop.group = 'Optional Parameters'
	at_pop.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pop')+'<br/>') + 
		html_par('cutoff pressure po of the pressure sensitive elastic material') +
		html_end()
		)
	at_pop.dimension = u.F/u.L**2
	at_pop.setDefault(0.0)
	
	xom = MpcXObjectMetaData()
	xom.name = 'PressureDependentElastic3D'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_E)
	xom.addAttribute(at_v)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_opt)
	xom.addAttribute(at_expp)
	xom.addAttribute(at_prp)
	xom.addAttribute(at_pop)
	
	# dependencies
	xom.setVisibilityDependency(at_opt, at_expp)
	xom.setVisibilityDependency(at_opt, at_prp)
	xom.setVisibilityDependency(at_opt, at_pop)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial PressureDependentElastic3D $matTag $E $v $rho <$expp $prp $pop>
	xobj = pinfo.phys_prop.XObject
	tag =  pinfo.phys_prop.id
	
	# util to get parameters
	def get_attr(pname):
		at = xobj.getAttribute(pname)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(pname))
		return at
	
	# mandatory parameters
	E = get_attr('E').quantityScalar.value
	v = get_attr('v').real
	rho = get_attr('rho').quantityScalar.value
	
	# optional paramters
	sopt = ''
	if get_attr('use optional parameters').boolean:
		expp = get_attr('expp').quantityScalar.value
		prp = get_attr('prp').quantityScalar.value
		pop = get_attr('pop').quantityScalar.value
		sopt += ' {} {} {}'.format(expp, prp, pop)
	
	# now write the string into the file
	pinfo.out_file.write('{}nDMaterial PressureDependentElastic3D {} {} {} {}{}\n'.format(pinfo.indent, tag, E, v, rho, sopt))
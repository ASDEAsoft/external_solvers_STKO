# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# fc
	at_fc = MpcAttributeMetaData()
	at_fc.type = MpcAttributeType.QuantityScalar
	at_fc.name = 'fc'
	at_fc.group = 'Non-linear'
	at_fc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fc')+'<br/>') + 
		html_par('concrete compressive strength at 28 days (compression is negative)*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_fc.dimension = u.F/u.L**2
	
	# fy
	at_fy = MpcAttributeMetaData()
	at_fy.type = MpcAttributeType.QuantityScalar
	at_fy.name = 'fy'
	at_fy.group = 'Non-linear'
	at_fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fy')+'<br/>') + 
		html_par('positive floating point value defining the yield strength of the reinforcing steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_fy.dimension = u.F/u.L**2
	
	# Es
	at_Es = MpcAttributeMetaData()
	at_Es.type = MpcAttributeType.QuantityScalar
	at_Es.name = 'Es'
	at_Es.group = 'Non-linear'
	at_Es.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Es')+'<br/>') + 
		html_par('floating point value defining the modulus of elasticity of the reinforcing steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_Es.dimension = u.F/u.L**2
	
	# fu
	at_fu = MpcAttributeMetaData()
	at_fu.type = MpcAttributeType.QuantityScalar
	at_fu.name = 'fu'
	at_fu.group = 'Non-linear'
	at_fu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fu')+'<br/>') + 
		html_par('positive floating point value defining the ultimate strength of the reinforcing steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_fu.dimension = u.F/u.L**2
	
	# Eh
	at_Eh = MpcAttributeMetaData()
	at_Eh.type = MpcAttributeType.QuantityScalar
	at_Eh.name = 'Eh'
	at_Eh.group = 'Non-linear'
	at_Eh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Eh')+'<br/>') + 
		html_par('floating point value defining the hardening modulus of the reinforcing steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_Eh.dimension = u.F/u.L**2
	
	# ld
	at_ld = MpcAttributeMetaData()
	at_ld.type = MpcAttributeType.QuantityScalar
	at_ld.name = 'ld'
	at_ld.group = 'Non-linear'
	at_ld.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ld')+'<br/>') + 
		html_par('floating point value defining the development length of the reinforcing steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_ld.dimension = u.L
	
	# db
	at_db = MpcAttributeMetaData()
	at_db.type = MpcAttributeType.QuantityScalar
	at_db.name = 'db'
	at_db.group = 'Non-linear'
	at_db.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('db')+'<br/>') + 
		html_par('point value defining the diameter of reinforcing steel') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_db.dimension = u.L
	
	# nb
	at_nb = MpcAttributeMetaData()
	at_nb.type = MpcAttributeType.Integer
	at_nb.name = 'nb'
	at_nb.group = 'Non-linear'
	at_nb.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nb')+'<br/>') + 
		html_par('an integer defining the number of anchored bars') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	
	# depth
	at_depth = MpcAttributeMetaData()
	at_depth.type = MpcAttributeType.QuantityScalar
	at_depth.name = 'depth'
	at_depth.group = 'Non-linear'
	at_depth.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('depth')+'<br/>') + 
		html_par('floating point value defining the dimension of the member (beam or column) perpendicular to the dimension of the plane of the paper') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_depth.dimension = u.L
	
	# height
	at_height = MpcAttributeMetaData()
	at_height.type = MpcAttributeType.QuantityScalar
	at_height.name = 'height'
	at_height.group = 'Non-linear'
	at_height.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('height')+'<br/>') + 
		html_par('floating point value defining the height of the flexural member, perpendicular to direction in which the reinforcing steel is placed, but in the plane of the paper') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_height.dimension = u.L
	
	# bsFlag
	at_bsFlag = MpcAttributeMetaData()
	at_bsFlag.type = MpcAttributeType.String
	at_bsFlag.name = 'bsFlag'
	at_bsFlag.group = 'Non-linear'
	at_bsFlag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bsFlag')+'<br/>') + 
		html_par('string indicating relative bond strength for the anchored reinforcing bar (options: "Strong" or "Weak")') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_bsFlag.sourceType = MpcAttributeSourceType.List
	at_bsFlag.setSourceList(['Strong', 'Weak'])
	at_bsFlag.setDefault('Strong')
	
	# type
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.String
	at_type.name = 'type'
	at_type.group = 'Non-linear'
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('type')+'<br/>') + 
		html_par('string indicating where the reinforcing bar is placed. (options: "beamtop", "beambot" or "column")') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_type.sourceType = MpcAttributeSourceType.List
	at_type.setSourceList(['beamtop', 'beambot', 'column'])
	at_type.setDefault('beamtop')
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	
	# damage
	at_damage = MpcAttributeMetaData()
	at_damage.type = MpcAttributeType.String
	at_damage.name = 'damage'
	at_damage.group = 'Optional parameters'
	at_damage.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('damage')+'<br/>') + 
		html_par('string indicating type of damage:whether there is full damage in the material or no damage (optional, options: "Damage", "NoDamage" ; default: Damage)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_damage.sourceType = MpcAttributeSourceType.List
	at_damage.setSourceList(['Damage', 'NoDamage'])
	at_damage.setDefault('Damage')
	
	# unit
	at_unit = MpcAttributeMetaData()
	at_unit.type = MpcAttributeType.String
	at_unit.name = 'unit'
	at_unit.group = 'Optional parameters'
	at_unit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('unit')+'<br/>') + 
		html_par('string indicating the type of unit system used (optional, options: "psi", "MPa", "Pa", "psf", "ksi", "ksf") (default: "psi" / "MPa")*') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/BARSLIP_Material','BARSLIP Material')+'<br/>') +
		html_end()
		)
	at_unit.sourceType = MpcAttributeSourceType.List
	at_unit.setSourceList(['psi', 'MPa', 'Pa', 'psf', 'ksi', 'ksf'])
	at_unit.setDefault('Mpa')
	
	xom = MpcXObjectMetaData()
	xom.name = 'BarSlip'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_fc)
	xom.addAttribute(at_fy)
	xom.addAttribute(at_Es)
	xom.addAttribute(at_fu)
	xom.addAttribute(at_Eh)
	xom.addAttribute(at_ld)
	xom.addAttribute(at_db)
	xom.addAttribute(at_nb)
	xom.addAttribute(at_depth)
	xom.addAttribute(at_height)
	xom.addAttribute(at_bsFlag)
	xom.addAttribute(at_type)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_damage)
	xom.addAttribute(at_unit)
	
	
	# Optional-dep
	xom.setVisibilityDependency(at_Optional, at_damage)
	xom.setVisibilityDependency(at_Optional, at_unit)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial BarSlip $matTag $fc $fy $Es $fu $Eh $db $ld $nb $depth $height $bsFlag $type <$damage $unit>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	fc_at = xobj.getAttribute('fc')
	if(fc_at is None):
		raise Exception('Error: cannot find "fc" attribute')
	fc = fc_at.quantityScalar
	
	fy_at = xobj.getAttribute('fy')
	if(fy_at is None):
		raise Exception('Error: cannot find "fy" attribute')
	fy = fy_at.quantityScalar
	
	Es_at = xobj.getAttribute('Es')
	if(Es_at is None):
		raise Exception('Error: cannot find "Es" attribute')
	Es = Es_at.quantityScalar
	
	fu_at = xobj.getAttribute('fu')
	if(fu_at is None):
		raise Exception('Error: cannot find "fu" attribute')
	fu = fu_at.quantityScalar
	
	Eh_at = xobj.getAttribute('Eh')
	if(Eh_at is None):
		raise Exception('Error: cannot find "Eh" attribute')
	Eh = Eh_at.quantityScalar
	
	db_at = xobj.getAttribute('db')
	if(db_at is None):
		raise Exception('Error: cannot find "db" attribute')
	db = db_at.quantityScalar
	
	ld_at = xobj.getAttribute('ld')
	if(ld_at is None):
		raise Exception('Error: cannot find "ld" attribute')
	ld = ld_at.quantityScalar
	
	nb_at = xobj.getAttribute('nb')
	if(nb_at is None):
		raise Exception('Error: cannot find "nb" attribute')
	nb = nb_at.integer
	
	depth_at = xobj.getAttribute('depth')
	if(depth_at is None):
		raise Exception('Error: cannot find "depth" attribute')
	depth = depth_at.quantityScalar
	
	height_at = xobj.getAttribute('height')
	if(height_at is None):
		raise Exception('Error: cannot find "height" attribute')
	height = height_at.quantityScalar
	
	bsFlag_at = xobj.getAttribute('bsFlag')
	if(bsFlag_at is None):
		raise Exception('Error: cannot find "bsFlag" attribute')
	bsFlag = bsFlag_at.string
	
	type_at = xobj.getAttribute('type')
	if(type_at is None):
		raise Exception('Error: cannot find "type" attribute')
	type = type_at.string
	
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		damage_at = xobj.getAttribute('damage')
		if(damage_at is None):
			raise Exception('Error: cannot find "damage" attribute')
		damage = damage_at.string
		
		unit_at = xobj.getAttribute('unit')
		if(unit_at is None):
			raise Exception('Error: cannot find "unit" attribute')
		unit = unit_at.string
		
		sopt += '{} {}'.format(damage, unit)
	
	str_tcl = '{}uniaxialMaterial BarSlip {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, fc.value, fy.value, Es.value, fu.value, Eh.value, db.value, ld.value, nb, depth.value, height.value, bsFlag, type, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
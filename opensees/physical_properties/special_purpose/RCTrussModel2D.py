import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib

####################################################################################
# Utilities
####################################################################################

def _description(title, body):
	return (
		html_par(html_begin()) +
		html_par(html_boldtext(title)+'<br/>') + 
		html_par(body) +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/ConcretewBeta_Material','RCTrussModel2D')) +
		html_end()
		)

####################################################################################
# Main methods
####################################################################################

def makeXObjectMetaData():
	
	####################################################################################
	# Concrete attributes
	####################################################################################
	
	# Vertical concrete
	at_vc = MpcAttributeMetaData()
	at_vc.type = MpcAttributeType.Index
	at_vc.name = 'Vertical Concrete Material'
	at_vc.group = 'Concrete'
	at_vc.description = _description('Vertical Concrete Material', 'A previously defined uniaxial concrete material')
	at_vc.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_vc.indexSource.addAllowedNamespace('materials.uniaxial')
	at_vc.indexSource.addAllowedClass('ConcretewBeta')
	
	# Horizontal concrete
	at_hc = MpcAttributeMetaData()
	at_hc.type = MpcAttributeType.Index
	at_hc.name = 'Horizontal Concrete Material'
	at_hc.group = 'Concrete'
	at_hc.description = _description('Horizontal Concrete Material', 'A previously defined uniaxial concrete material')
	at_hc.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_hc.indexSource.addAllowedNamespace('materials.uniaxial')
	at_hc.indexSource.addAllowedClass('ConcretewBeta')
	
	# Diagonal concrete
	at_dc = MpcAttributeMetaData()
	at_dc.type = MpcAttributeType.Index
	at_dc.name = 'Diagonal Concrete Material'
	at_dc.group = 'Concrete'
	at_dc.description = _description('Diagonal Concrete Material', 'A previously defined uniaxial concrete material')
	at_dc.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_dc.indexSource.addAllowedNamespace('materials.uniaxial')
	at_dc.indexSource.addAllowedClass('ConcretewBeta')
	
	# Thickness
	at_thickness = MpcAttributeMetaData()
	at_thickness.type = MpcAttributeType.QuantityScalar
	at_thickness.name = 'Thickness'
	at_thickness.group = 'Concrete'
	at_thickness.description = _description('Thickness', 'The concrete thickness in the out-of-plane direction')
	at_thickness.dimension = u.L
	
	####################################################################################
	# Rebars attributes
	####################################################################################
	
	# Steel
	at_rm = MpcAttributeMetaData()
	at_rm.type = MpcAttributeType.Index
	at_rm.name = 'Rebars Material'
	at_rm.group = 'Rebars'
	at_rm.description = _description('Rebars Material', 'A previously defined uniaxial steel material')
	at_rm.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_rm.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# hdiam
	at_hdiam = MpcAttributeMetaData()
	at_hdiam.type = MpcAttributeType.QuantityScalar
	at_hdiam.name = 'Horizontal Diameter'
	at_hdiam.group = 'Rebars'
	at_hdiam.description = _description('Horizontal Diameter', 'Diameter of horizontal rebars')
	at_hdiam.dimension = u.L
	
	# vdiam
	at_vdiam = MpcAttributeMetaData()
	at_vdiam.type = MpcAttributeType.QuantityScalar
	at_vdiam.name = 'Vertical Diameter'
	at_vdiam.group = 'Rebars'
	at_vdiam.description = _description('Vertical Diameter', 'Diameter of vertical rebars')
	at_vdiam.dimension = u.L
	
	# vspac
	at_vspac = MpcAttributeMetaData()
	at_vspac.type = MpcAttributeType.QuantityScalar
	at_vspac.name = 'Vertical Spacing'
	at_vspac.group = 'Rebars'
	at_vspac.description = _description('Vertical Spacing', 'Spacing of vertical rebars')
	at_vspac.dimension = u.L
	
	# hspac
	at_hspac = MpcAttributeMetaData()
	at_hspac.type = MpcAttributeType.QuantityScalar
	at_hspac.name = 'Horizontal Spacing'
	at_hspac.group = 'Rebars'
	at_hspac.description = _description('Horizontal Spacing', 'Spacing of horizontal rebars')
	at_hspac.dimension = u.L
	
	xom = MpcXObjectMetaData()
	xom.name = 'RCTrussModel2D'
	xom.Xgroup = 'RC Beam-Truss Models'
	xom.addAttribute(at_vc)
	xom.addAttribute(at_hc)
	xom.addAttribute(at_dc)
	xom.addAttribute(at_thickness)
	xom.addAttribute(at_rm)
	xom.addAttribute(at_vdiam)
	xom.addAttribute(at_vspac)
	xom.addAttribute(at_hdiam)
	xom.addAttribute(at_hspac)
	
	return xom


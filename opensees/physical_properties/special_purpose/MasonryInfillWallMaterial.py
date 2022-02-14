import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# utilties
	def mka(name, group, description, type, dim = None, default = None, slist = None):
		at = MpcAttributeMetaData()
		at.type = type
		at.name = name
		at.group = group
		at.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(description) +
			html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Infill_Wall_Model_and_Element_Removal','MasonryInfillWallMaterial')+'<br/>') +
			html_end()
			)
		if dim is not None:
			at.dim = dim
		if slist is not None:
			at.sourceType = MpcAttributeSourceType.List
			at.setSourceList(slist)
		if default is not None:
			at.setDefault(default)
		return at
	
	# Masonry parameters
	Em = mka('Em', 'Masonry parameters', 'Masonry modulus of elasticity', MpcAttributeType.QuantityScalar, dim = u.F/u.L**2, default = 500.0)
	fme = mka('fme', 'Masonry parameters', 'Masonry expected compressive strength', MpcAttributeType.QuantityScalar, dim = u.F/u.L**2, default = 1.0)
	vte = mka('vte', 'Masonry parameters', 'Average bed joint strength', MpcAttributeType.QuantityScalar, dim = u.F/u.L**2, default = 0.9)
	fvie = mka('fvie', 'Masonry parameters', 'see FEMA356, Section 7.5.2.2', MpcAttributeType.QuantityScalar, dim = u.F/u.L**2, default = 0.05)
	# Wall parameters
	tinf = mka('tinf', 'Wall parameters', 'Thickness of masonry infill wall', MpcAttributeType.QuantityScalar, dim = u.L, default = 6.0)
	gamma_inf = mka('gamma_inf', 'Wall parameters', 'Weight density of the infill bricks', MpcAttributeType.QuantityScalar, dim = u.F/u.L**3, default = 5.5259378050700276e-05)
	# Misc
	ForceUnit = mka('Force unit', 'Misc', 'Force unit system for the input values', MpcAttributeType.String, slist = ['kip','N','daN','hN','kN'], default = 'kip')
	LengthUnit = mka('Length unit', 'Misc', 'Length unit system for the input values', MpcAttributeType.String, slist = ['in','m','dm','cm','mm','ft'], default = 'in')
	
	# Xom
	xom = MpcXObjectMetaData()
	xom.name = 'MasonryInfillWallMaterial'
	xom.Xgroup = 'Masonry Infill Wall'
	xom.addAttribute(Em)
	xom.addAttribute(fme)
	xom.addAttribute(vte)
	xom.addAttribute(fvie)
	xom.addAttribute(tinf)
	xom.addAttribute(gamma_inf)
	xom.addAttribute(ForceUnit)
	xom.addAttribute(LengthUnit)
	
	return xom
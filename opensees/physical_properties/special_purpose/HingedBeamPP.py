import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.physical_properties.sections.extrusion_utils as exutils

def _geta(xobj, name):
	a = xobj.getAttribute(name)
	if a is None:
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	return a

def makeXObjectMetaData():
	
	# PP_Beam
	at_PP_Beam = MpcAttributeMetaData()
	at_PP_Beam.type = MpcAttributeType.Index
	at_PP_Beam.name = 'PP_Beam'
	at_PP_Beam.group = 'Beam'
	at_PP_Beam.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Physical properties Beam')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_PP_Beam.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	''' INSERIRE I NAMESPACE '''
	# at_PP_Beam.indexSource.addAllowedNamespace("beam_column_elements")
	
	# zeroLength_i
	at_zeroLength_i = MpcAttributeMetaData()
	at_zeroLength_i.type = MpcAttributeType.Index
	at_zeroLength_i.name = 'zeroLength_i'
	at_zeroLength_i.group = 'ZeroLength'
	at_zeroLength_i.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('zeroLength')+'<br/>') +
		html_par('zeroLengthMaterial at the node i') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLength_Element','ZeroLength Element')+'<br/>') +
		html_end()
		)
	at_zeroLength_i.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_zeroLength_i.indexSource.addAllowedNamespace("special_purpose")
	at_zeroLength_i.indexSource.addAllowedClass("zeroLengthMaterial")
	
	# zeroLength_j
	at_zeroLength_j = MpcAttributeMetaData()
	at_zeroLength_j.type = MpcAttributeType.Index
	at_zeroLength_j.name = 'zeroLength_j'
	at_zeroLength_j.group = 'ZeroLength'
	at_zeroLength_j.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('zeroLength')+'<br/>') +
		html_par('zeroLengthMaterial at the node j') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLength_Element','ZeroLength Element')+'<br/>') +
		html_end()
		)
	at_zeroLength_j.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_zeroLength_j.indexSource.addAllowedNamespace("special_purpose")
	at_zeroLength_j.indexSource.addAllowedClass("zeroLengthMaterial")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'HingedBeamPP'
	xom.Xgroup = 'HingedBeam'
	xom.addAttribute(at_PP_Beam)
	xom.addAttribute(at_zeroLength_i)
	xom.addAttribute(at_zeroLength_j)
	
	
	return xom

def makeExtrusionBeamDataCompoundInfo(xobj):
	
	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')
	
	info = MpcSectionExtrusionBeamDataCompoundInfo()
	'''
	here the property that has the extrusion source (MpcBeamFiberSection)
	is the property whose id is stored in the attribute 'sectionTag', and not
	this property (Aggregator). So we first get the attribute and check
	whether the user decided to use a fiber beam cross section for the P-My-Mz part
	of the Aggregator. If so, get the indexed property from the document. That
	will be the one containing the extrusion source. See the opensees.physical_properties.sections.Fiber.py module.
	'''
	
	PP_Beam = _geta(xobj, 'PP_Beam').index
	# get extrusion info for the inner beam property
	inner_items = exutils.getExtrusionDataAllItems(doc.getPhysicalProperty(PP_Beam))
	if inner_items and len(inner_items) > 0:
		# scale all parametric weights so that their sum is 0.9 (0.1 is reserved for hinge gaps)
		sum_param_weight = 0.0
		for item in inner_items:
			if item.isParametric:
				sum_param_weight += item.weight
		if sum_param_weight > 0.0:
			param_weight_scale = 0.9/sum_param_weight
			for item in inner_items:
				if item.isParametric:
					item.weight *= param_weight_scale
		# add all inner properties and end hinge gaps
		yOffset = 0.0
		zOffset = 0.0
		exutils.checkOffsetCompatibility(inner_items)
		if len(inner_items) > 0:
			yOffset = inner_items[0].yOffset
			zOffset = inner_items[0].zOffset
		if _geta(xobj, 'zeroLength_i').index != 0:
			info.add(None, 0.05, True, True, yOffset, zOffset)
		exutils.checkOffsetCompatibility(inner_items)
		for item in inner_items:
			info.add(item.property, item.weight, item.isParametric, False, item.yOffset, item.zOffset)
		if _geta(xobj, 'zeroLength_j').index != 0:
			info.add(None, 0.05, True, True, yOffset, zOffset)
	
	return info

def getSectionOffset(xobj):
	offset_y = 0.0
	offset_z = 0.0
	info = makeExtrusionBeamDataCompoundInfo(xobj)
	if info is not None:
		if len(info.items) > 0:
			item = info.items[0]
			offset_y = item.yOffset
			offset_z = item.zOffset
	return offset_y, offset_z
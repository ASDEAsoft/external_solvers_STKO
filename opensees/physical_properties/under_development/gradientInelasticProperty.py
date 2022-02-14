import PyMpc.IO
from PyMpc import *
from mpc_utils_html import *


def makeXObjectMetaData():
	
	def mka(name, type, group, body=''):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(body) +
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/gradientInelasticBeamColumn.html', 'gradientInelasticBeamColumn Element')+'<br/>') +
			html_end()
			)
		return a

	# numIntgrPts
	at_numIntgrPts = mka('numIntgrPts', MpcAttributeType.Integer, 'Group', 'total number of integration points - recommended to exceed (1.5L ⁄ lc + 1) when default integration method is used (L = beam length and lc = characteristic length)')
	at_numIntgrPts.setDefault(5)

	# endSecTag1
	at_endSecTag1 = mka('endSecTag1', MpcAttributeType.Index, 'Group', 'near-end part\'s section tag')
	at_endSecTag1.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_endSecTag1.indexSource.addAllowedNamespace('sections')
	
	# intSecTag
	at_intSecTag = mka('intSecTag', MpcAttributeType.Index, 'Group', 'intermediate part\'s sections tag')
	at_intSecTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_intSecTag.indexSource.addAllowedNamespace('sections')

	# endSecTag2
	at_endSecTag2 = mka('endSecTag2', MpcAttributeType.Index, 'Group', 'far-end part\'s section tag')
	at_endSecTag2.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_endSecTag2.indexSource.addAllowedNamespace('sections')
	
	# lc
	at_lc = mka('lc', MpcAttributeType.QuantityScalar, 'Group', 'characteristic length - it can be taken as plastic hinge length')

	# -integration
	at_integration = mka('-integration', MpcAttributeType.Boolean, 'Optional', 'to activate integration type')
	
	# integrType
	at_integrType = mka('integrType', MpcAttributeType.String, 'Optional', 'Options: \'NewtonCotes\', \'Simpson\', or \'Trapezoidal\' (default: \'Simpson\') – if Simpson\'s rule is used, $numIntgrPts should be an odd number')
	at_integrType.sourceType = MpcAttributeSourceType.List
	at_integrType.setSourceList(['NewtonCotes', 'Simpson', 'Trapezoidal'])
	at_integrType.setDefault('Simpson')

	xom = MpcXObjectMetaData()
	xom.name = 'gradientInelasticProperty'
	xom.addAttribute(at_numIntgrPts)
	xom.addAttribute(at_endSecTag1)
	xom.addAttribute(at_intSecTag)
	xom.addAttribute(at_endSecTag2)
	xom.addAttribute(at_lc)
	xom.addAttribute(at_integration)
	xom.addAttribute(at_integrType)

	xom.setVisibilityDependency(at_integration, at_integrType)

	return xom
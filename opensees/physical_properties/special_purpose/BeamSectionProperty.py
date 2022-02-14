import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.physical_properties.special_purpose.beam_section_utils as bsutils
import opensees.physical_properties.sections.extrusion_utils as exutils

def makeXObjectMetaData():
	
	# OPTION_1
	at_OPTION_1 = MpcAttributeMetaData()
	at_OPTION_1.type = MpcAttributeType.Boolean
	at_OPTION_1.name = 'StandardIntegrationTypes'
	at_OPTION_1.group = 'Group'
	at_OPTION_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OPTION_1')+'<br/>') +
		html_par('standard integration types') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_OPTION_1.editable = False
	
	# IntegrationType_1
	at_IntegrationType_1 = MpcAttributeMetaData()
	at_IntegrationType_1.type = MpcAttributeType.String
	at_IntegrationType_1.name = 'IntegrationType/1'
	at_IntegrationType_1.group = 'StandardIntegrationTypes'
	at_IntegrationType_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_IntegrationType_1.sourceType = MpcAttributeSourceType.List
	at_IntegrationType_1.setSourceList(['Lobatto', 'Legendre', 'Radau', 'NewtonCotes', 'Trapezoidal', 'CompositeSimpson'])
	at_IntegrationType_1.setDefault('Lobatto')
	
	# secTag_1
	at_secTag_1 = MpcAttributeMetaData()
	at_secTag_1.type = MpcAttributeType.Index
	at_secTag_1.name = 'secTag/1'
	at_secTag_1.group = 'StandardIntegrationTypes'
	at_secTag_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTag')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTag_1.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTag_1.indexSource.addAllowedNamespace("sections")
	
	# numIntPts_1
	at_numIntPts_1 = MpcAttributeMetaData()
	at_numIntPts_1.type = MpcAttributeType.Integer
	at_numIntPts_1.name = 'numIntPts/1'
	at_numIntPts_1.group = 'StandardIntegrationTypes'
	at_numIntPts_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIntPts')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_numIntPts_1.setDefault(5)
	
	# OPTION_2
	at_OPTION_2 = MpcAttributeMetaData()
	at_OPTION_2.type = MpcAttributeType.Boolean
	at_OPTION_2.name = 'UserDefined'
	at_OPTION_2.group = 'Group'
	at_OPTION_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OPTION_2')+'<br/>') +
		html_par('user defined') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_OPTION_2.editable = False
	
	# IntegrationType_2
	at_IntegrationType_2 = MpcAttributeMetaData()
	at_IntegrationType_2.type = MpcAttributeType.String
	at_IntegrationType_2.name = 'IntegrationType/2'
	at_IntegrationType_2.group = 'UserDefined'
	at_IntegrationType_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_IntegrationType_2.setDefault('UserDefined')
	at_IntegrationType_2.editable = False
	
	# numIntPts_2
	at_numIntPts_2 = MpcAttributeMetaData()
	at_numIntPts_2.type = MpcAttributeType.Integer
	at_numIntPts_2.name = 'numIntPts/2'
	at_numIntPts_2.group = 'UserDefined'
	at_numIntPts_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIntPts')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_numIntPts_2.setDefault(5)
	
	# secTag_2
	at_secTag_2 = MpcAttributeMetaData()
	at_secTag_2.type = MpcAttributeType.IndexVector
	at_secTag_2.name = 'secTag/2'
	at_secTag_2.group = 'UserDefined'
	at_secTag_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTag')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTag_2.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTag_2.indexSource.addAllowedNamespace("sections")
	
	# positions_2
	at_positions_2 = MpcAttributeMetaData()
	at_positions_2.type = MpcAttributeType.QuantityVector
	at_positions_2.name = 'positions/2'
	at_positions_2.group = 'UserDefined'
	at_positions_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('positions')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# weights_2
	at_weights_2 = MpcAttributeMetaData()
	at_weights_2.type = MpcAttributeType.QuantityVector
	at_weights_2.name = 'weights/2'
	at_weights_2.group = 'UserDefined'
	at_weights_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('weights')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# OPTION_3
	at_OPTION_3 = MpcAttributeMetaData()
	at_OPTION_3.type = MpcAttributeType.Boolean
	at_OPTION_3.name = 'Hinge'
	at_OPTION_3.group = 'Group'
	at_OPTION_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OPTION_3')+'<br/>') +
		html_par('beam with hinges') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_OPTION_3.editable = False
	
	# IntegrationType_3
	at_IntegrationType_3 = MpcAttributeMetaData()
	at_IntegrationType_3.type = MpcAttributeType.String
	at_IntegrationType_3.name = 'IntegrationType/3'
	at_IntegrationType_3.group = 'Hinge'
	at_IntegrationType_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_IntegrationType_3.sourceType = MpcAttributeSourceType.List
	at_IntegrationType_3.setSourceList(['HingeMidpoint', 'HingeRadau', 'HingeRadauTwo', 'HingeEndpoint'])
	at_IntegrationType_3.setDefault('HingeRadau')
	
	# secTagI_3
	at_secTagI_3 = MpcAttributeMetaData()
	at_secTagI_3.type = MpcAttributeType.Index
	at_secTagI_3.name = 'secTagI/3'
	at_secTagI_3.group = 'Hinge'
	at_secTagI_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTagI')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagI_3.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagI_3.indexSource.addAllowedNamespace("sections")
	
	# lpI_3
	at_lpI_3 = MpcAttributeMetaData()
	at_lpI_3.type = MpcAttributeType.QuantityScalar
	at_lpI_3.name = 'lpI/3'
	at_lpI_3.group = 'Hinge'
	at_lpI_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lpI')+'<br/>') +
		html_par('plastic hinge length at node I') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_lpI_3.dimension = u.L
	
	# secTagJ_3
	at_secTagJ_3 = MpcAttributeMetaData()
	at_secTagJ_3.type = MpcAttributeType.Index
	at_secTagJ_3.name = 'secTagJ/3'
	at_secTagJ_3.group = 'Hinge'
	at_secTagJ_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTagJ')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagJ_3.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagJ_3.indexSource.addAllowedNamespace("sections")
	
	# lpJ_3
	at_lpJ_3 = MpcAttributeMetaData()
	at_lpJ_3.type = MpcAttributeType.QuantityScalar
	at_lpJ_3.name = 'lpJ/3'
	at_lpJ_3.group = 'Hinge'
	at_lpJ_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lpJ')+'<br/>') +
		html_par('plastic hinge length at node J') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_lpJ_3.dimension = u.L
	
	# secTagE_3
	at_secTagE_3 = MpcAttributeMetaData()
	at_secTagE_3.type = MpcAttributeType.Index
	at_secTagE_3.name = 'secTagE/3'
	at_secTagE_3.group = 'Hinge'
	at_secTagE_3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTagE')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagE_3.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagE_3.indexSource.addAllowedNamespace("sections")
	
	# OPTION_4
	at_OPTION_4 = MpcAttributeMetaData()
	at_OPTION_4.type = MpcAttributeType.Boolean
	at_OPTION_4.name = 'UserHinge'
	at_OPTION_4.group = 'Group'
	at_OPTION_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OPTION_4')+'<br/>') +
		html_par('beam with hinges') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_OPTION_4.editable = False
	
	# IntegrationType_4
	at_IntegrationType_4 = MpcAttributeMetaData()
	at_IntegrationType_4.type = MpcAttributeType.String
	at_IntegrationType_4.name = 'IntegrationType/4'
	at_IntegrationType_4.group = 'UserHinge'
	at_IntegrationType_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_IntegrationType_4.setDefault('UserHinge')
	at_IntegrationType_4.editable = False
	
	# secTagE_4
	at_secTagE_4 = MpcAttributeMetaData()
	at_secTagE_4.type = MpcAttributeType.Index
	at_secTagE_4.name = 'secTagE/4'
	at_secTagE_4.group = 'UserHinge'
	at_secTagE_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTagE')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagE_4.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagE_4.indexSource.addAllowedNamespace("sections")
	
	# npI
	at_npI = MpcAttributeMetaData()
	at_npI.type = MpcAttributeType.Integer
	at_npI.name = 'npI'
	at_npI.group = 'UserHinge'
	at_npI.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('npI')+'<br/>') +
		html_par('number of integration points at node I') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# npJ
	at_npJ = MpcAttributeMetaData()
	at_npJ.type = MpcAttributeType.Integer
	at_npJ.name = 'npJ'
	at_npJ.group = 'UserHinge'
	at_npJ.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('npJ')+'<br/>') +
		html_par('number of integration points at node J') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# secTagI_4
	at_secTagI_4 = MpcAttributeMetaData()
	at_secTagI_4.type = MpcAttributeType.IndexVector
	at_secTagI_4.name = 'secTagI/4'
	at_secTagI_4.group = 'UserHinge'
	at_secTagI_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sections at node I')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagI_4.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagI_4.indexSource.addAllowedNamespace("sections")
	
	# positionsI
	at_positionsI = MpcAttributeMetaData()
	at_positionsI.type = MpcAttributeType.QuantityVector
	at_positionsI.name = 'positionsI'
	at_positionsI.group = 'UserHinge'
	at_positionsI.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('positionsI')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# weightsI
	at_weightsI = MpcAttributeMetaData()
	at_weightsI.type = MpcAttributeType.QuantityVector
	at_weightsI.name = 'weightsI'
	at_weightsI.group = 'UserHinge'
	at_weightsI.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('weightsI')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# secTagJ_4
	at_secTagJ_4 = MpcAttributeMetaData()
	at_secTagJ_4.type = MpcAttributeType.IndexVector
	at_secTagJ_4.name = 'secTagJ/4'
	at_secTagJ_4.group = 'UserHinge'
	at_secTagJ_4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sections at node J')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagJ_4.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagJ_4.indexSource.addAllowedNamespace("sections")
	
	# positionsJ
	at_positionsJ = MpcAttributeMetaData()
	at_positionsJ.type = MpcAttributeType.QuantityVector
	at_positionsJ.name = 'positionsJ'
	at_positionsJ.group = 'UserHinge'
	at_positionsJ.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('positionsJ')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# weightsJ
	at_weightsJ = MpcAttributeMetaData()
	at_weightsJ.type = MpcAttributeType.QuantityVector
	at_weightsJ.name = 'weightsJ'
	at_weightsJ.group = 'UserHinge'
	at_weightsJ.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('weightsJ')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# OPTION_5
	at_OPTION_5 = MpcAttributeMetaData()
	at_OPTION_5.type = MpcAttributeType.Boolean
	at_OPTION_5.name = 'DistHinge'
	at_OPTION_5.group = 'Group'
	at_OPTION_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OPTION_5')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_OPTION_5.editable = False
	
	# IntegrationType_5
	at_IntegrationType_5 = MpcAttributeMetaData()
	at_IntegrationType_5.type = MpcAttributeType.String
	at_IntegrationType_5.name = 'IntegrationType/5'
	at_IntegrationType_5.group = 'DistHinge'
	at_IntegrationType_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_IntegrationType_5.setDefault('DistHinge')
	at_IntegrationType_5.editable = False
	
	# HingeIntegrationType_5
	at_HingeIntegrationType_5 = MpcAttributeMetaData()
	at_HingeIntegrationType_5.type = MpcAttributeType.String
	at_HingeIntegrationType_5.name = 'HingeIntegrationType/5'
	at_HingeIntegrationType_5.group = 'DistHinge'
	at_HingeIntegrationType_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('HingeIntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_HingeIntegrationType_5.sourceType = MpcAttributeSourceType.List
	at_HingeIntegrationType_5.setSourceList(['Lobatto', 'Legendre', 'Radau', 'NewtonCotes', 'Trapezoidal', 'CompositeSimpson'])
	at_HingeIntegrationType_5.setDefault('Lobatto')
	
	# numIntPts_5
	at_numIntPts_5 = MpcAttributeMetaData()
	at_numIntPts_5.type = MpcAttributeType.Integer
	at_numIntPts_5.name = 'numIntPts/5'
	at_numIntPts_5.group = 'DistHinge'
	at_numIntPts_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIntPts')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_numIntPts_5.setDefault(5)
	
	# secTagI_5
	at_secTagI_5 = MpcAttributeMetaData()
	at_secTagI_5.type = MpcAttributeType.Index
	at_secTagI_5.name = 'secTagI/5'
	at_secTagI_5.group = 'DistHinge'
	at_secTagI_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTagI')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagI_5.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagI_5.indexSource.addAllowedNamespace("sections")
	
	# lpI_5
	at_lpI_5 = MpcAttributeMetaData()
	at_lpI_5.type = MpcAttributeType.QuantityScalar
	at_lpI_5.name = 'lpI/5'
	at_lpI_5.group = 'DistHinge'
	at_lpI_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lpI')+'<br/>') +
		html_par('plastic hinge length at node I') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_lpI_5.dimension = u.L
	
	# secTagJ_5
	at_secTagJ_5 = MpcAttributeMetaData()
	at_secTagJ_5.type = MpcAttributeType.Index
	at_secTagJ_5.name = 'secTagJ/5'
	at_secTagJ_5.group = 'DistHinge'
	at_secTagJ_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTagJ')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagJ_5.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagJ_5.indexSource.addAllowedNamespace("sections")
	
	# lpJ_5
	at_lpJ_5 = MpcAttributeMetaData()
	at_lpJ_5.type = MpcAttributeType.QuantityScalar
	at_lpJ_5.name = 'lpJ/5'
	at_lpJ_5.group = 'DistHinge'
	at_lpJ_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lpJ')+'<br/>') +
		html_par('plastic hinge length at node J') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_lpJ_5.dimension = u.L
	
	# secTagE_5
	at_secTagE_5 = MpcAttributeMetaData()
	at_secTagE_5.type = MpcAttributeType.Index
	at_secTagE_5.name = 'secTagE/5'
	at_secTagE_5.group = 'DistHinge'
	at_secTagE_5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTagE')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagE_5.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagE_5.indexSource.addAllowedNamespace("sections")
	
	# OPTION_6
	at_OPTION_6 = MpcAttributeMetaData()
	at_OPTION_6.type = MpcAttributeType.Boolean
	at_OPTION_6.name = 'RegularizedHinge'
	at_OPTION_6.group = 'Group'
	at_OPTION_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OPTION_6')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_OPTION_6.editable = False
	
	# IntegrationType_6
	at_IntegrationType_6 = MpcAttributeMetaData()
	at_IntegrationType_6.type = MpcAttributeType.String
	at_IntegrationType_6.name = 'IntegrationType/6'
	at_IntegrationType_6.group = 'RegularizedHinge'
	at_IntegrationType_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_IntegrationType_6.setDefault('RegularizedHinge')
	at_IntegrationType_6.editable = False
	
	# HingeIntegrationType_6
	at_HingeIntegrationType_6 = MpcAttributeMetaData()
	at_HingeIntegrationType_6.type = MpcAttributeType.String
	at_HingeIntegrationType_6.name = 'HingeIntegrationType/6'
	at_HingeIntegrationType_6.group = 'RegularizedHinge'
	at_HingeIntegrationType_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('HingeIntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_HingeIntegrationType_6.sourceType = MpcAttributeSourceType.List
	at_HingeIntegrationType_6.setSourceList(['Lobatto', 'Legendre', 'Radau', 'NewtonCotes', 'Trapezoidal', 'CompositeSimpson'])
	at_HingeIntegrationType_6.setDefault('Lobatto')
	
	# numIntPts_6
	at_numIntPts_6 = MpcAttributeMetaData()
	at_numIntPts_6.type = MpcAttributeType.Integer
	at_numIntPts_6.name = 'numIntPts/6'
	at_numIntPts_6.group = 'RegularizedHinge'
	at_numIntPts_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIntPts')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_numIntPts_6.setDefault(5)
	
	# secTagI_6
	at_secTagI_6 = MpcAttributeMetaData()
	at_secTagI_6.type = MpcAttributeType.Index
	at_secTagI_6.name = 'secTagI/6'
	at_secTagI_6.group = 'RegularizedHinge'
	at_secTagI_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTagI')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagI_6.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagI_6.indexSource.addAllowedNamespace("sections")
	
	# lpI_6
	at_lpI_6 = MpcAttributeMetaData()
	at_lpI_6.type = MpcAttributeType.QuantityScalar
	at_lpI_6.name = 'lpI/6'
	at_lpI_6.group = 'RegularizedHinge'
	at_lpI_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lpI')+'<br/>') +
		html_par('plastic hinge length at node I') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_lpI_6.dimension = u.L
	
	# zetaI
	at_zetaI = MpcAttributeMetaData()
	at_zetaI.type = MpcAttributeType.QuantityScalar
	at_zetaI.name = 'zetaI'
	at_zetaI.group = 'RegularizedHinge'
	at_zetaI.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('zetaI')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# secTagJ_6
	at_secTagJ_6 = MpcAttributeMetaData()
	at_secTagJ_6.type = MpcAttributeType.Index
	at_secTagJ_6.name = 'secTagJ/6'
	at_secTagJ_6.group = 'RegularizedHinge'
	at_secTagJ_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTagJ')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagJ_6.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagJ_6.indexSource.addAllowedNamespace("sections")
	
	# lpJ_6
	at_lpJ_6 = MpcAttributeMetaData()
	at_lpJ_6.type = MpcAttributeType.QuantityScalar
	at_lpJ_6.name = 'lpJ/6'
	at_lpJ_6.group = 'RegularizedHinge'
	at_lpJ_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lpJ')+'<br/>') +
		html_par('plastic hinge length at node J') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_lpJ_6.dimension = u.L
	
	# zetaJ
	at_zetaJ = MpcAttributeMetaData()
	at_zetaJ.type = MpcAttributeType.QuantityScalar
	at_zetaJ.name = 'zetaJ'
	at_zetaJ.group = 'RegularizedHinge'
	at_zetaJ.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('zetaJ')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# secTagE_6
	at_secTagE_6 = MpcAttributeMetaData()
	at_secTagE_6.type = MpcAttributeType.Index
	at_secTagE_6.name = 'secTagE/6'
	at_secTagE_6.group = 'RegularizedHinge'
	at_secTagE_6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTagE')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTagE_6.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTagE_6.indexSource.addAllowedNamespace("sections")
	
	# OPTION_7
	at_OPTION_7 = MpcAttributeMetaData()
	at_OPTION_7.type = MpcAttributeType.Boolean
	at_OPTION_7.name = 'FixedLocation'
	at_OPTION_7.group = 'Group'
	at_OPTION_7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OPTION_7')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_OPTION_7.editable = False
	
	# IntegrationType_7
	at_IntegrationType_7 = MpcAttributeMetaData()
	at_IntegrationType_7.type = MpcAttributeType.String
	at_IntegrationType_7.name = 'IntegrationType/7'
	at_IntegrationType_7.group = 'FixedLocation'
	at_IntegrationType_7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_IntegrationType_7.setDefault('FixedLocation')
	at_IntegrationType_7.editable = False
	
	# numIntPts_7
	at_numIntPts_7 = MpcAttributeMetaData()
	at_numIntPts_7.type = MpcAttributeType.Integer
	at_numIntPts_7.name = 'numIntPts/7'
	at_numIntPts_7.group = 'FixedLocation'
	at_numIntPts_7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIntPts')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_numIntPts_7.setDefault(5)
	
	# secTag_7
	at_secTag_7 = MpcAttributeMetaData()
	at_secTag_7.type = MpcAttributeType.IndexVector
	at_secTag_7.name = 'secTag/7'
	at_secTag_7.group = 'FixedLocation'
	at_secTag_7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTag')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTag_7.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTag_7.indexSource.addAllowedNamespace("sections")
	
	# positions_7
	at_positions_7 = MpcAttributeMetaData()
	at_positions_7.type = MpcAttributeType.QuantityVector
	at_positions_7.name = 'positions/7'
	at_positions_7.group = 'FixedLocation'
	at_positions_7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('positions')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# OPTION_8
	at_OPTION_8 = MpcAttributeMetaData()
	at_OPTION_8.type = MpcAttributeType.Boolean
	at_OPTION_8.name = 'LowOrder'
	at_OPTION_8.group = 'Group'
	at_OPTION_8.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OPTION_8')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_OPTION_8.editable = False
	
	# IntegrationType_8
	at_IntegrationType_8 = MpcAttributeMetaData()
	at_IntegrationType_8.type = MpcAttributeType.String
	at_IntegrationType_8.name = 'IntegrationType/8'
	at_IntegrationType_8.group = 'LowOrder'
	at_IntegrationType_8.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_IntegrationType_8.setDefault('LowOrder')
	at_IntegrationType_8.editable = False
	
	# numIntPts_8
	at_numIntPts_8 = MpcAttributeMetaData()
	at_numIntPts_8.type = MpcAttributeType.Integer
	at_numIntPts_8.name = 'numIntPts/8'
	at_numIntPts_8.group = 'LowOrder'
	at_numIntPts_8.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIntPts')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_numIntPts_8.setDefault(5)
	
	# secTag_8
	at_secTag_8 = MpcAttributeMetaData()
	at_secTag_8.type = MpcAttributeType.IndexVector
	at_secTag_8.name = 'secTag/8'
	at_secTag_8.group = 'LowOrder'
	at_secTag_8.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTag')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTag_8.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTag_8.indexSource.addAllowedNamespace("sections")
	
	# positions_8
	at_positions_8 = MpcAttributeMetaData()
	at_positions_8.type = MpcAttributeType.QuantityVector
	at_positions_8.name = 'positions/8'
	at_positions_8.group = 'LowOrder'
	at_positions_8.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('positions')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# weights_8
	at_weights_8 = MpcAttributeMetaData()
	at_weights_8.type = MpcAttributeType.QuantityVector
	at_weights_8.name = 'weights/8'
	at_weights_8.group = 'LowOrder'
	at_weights_8.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('weights')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	# OPTION_9
	at_OPTION_9 = MpcAttributeMetaData()
	at_OPTION_9.type = MpcAttributeType.Boolean
	at_OPTION_9.name = 'MidDistance'
	at_OPTION_9.group = 'Group'
	at_OPTION_9.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('OPTION_9')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_OPTION_9.editable = False
	
	# IntegrationType_9
	at_IntegrationType_9 = MpcAttributeMetaData()
	at_IntegrationType_9.type = MpcAttributeType.String
	at_IntegrationType_9.name = 'IntegrationType/9'
	at_IntegrationType_9.group = 'MidDistance'
	at_IntegrationType_9.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('IntegrationType')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_IntegrationType_9.setDefault('MidDistance')
	at_IntegrationType_9.editable = False
	
	# numIntPts_9
	at_numIntPts_9 = MpcAttributeMetaData()
	at_numIntPts_9.type = MpcAttributeType.Integer
	at_numIntPts_9.name = 'numIntPts/9'
	at_numIntPts_9.group = 'MidDistance'
	at_numIntPts_9.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIntPts')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_numIntPts_9.setDefault(5)
	
	# secTag_9
	at_secTag_9 = MpcAttributeMetaData()
	at_secTag_9.type = MpcAttributeType.IndexVector
	at_secTag_9.name = 'secTag/9'
	at_secTag_9.group = 'MidDistance'
	at_secTag_9.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secTag')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_secTag_9.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_secTag_9.indexSource.addAllowedNamespace("sections")
	
	# positions_9
	at_positions_9 = MpcAttributeMetaData()
	at_positions_9.type = MpcAttributeType.QuantityVector
	at_positions_9.name = 'positions/9'
	at_positions_9.group = 'MidDistance'
	at_positions_9.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('positions')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	#aex_option
	at_aex_option = MpcAttributeMetaData()
	at_aex_option.type = MpcAttributeType.String
	at_aex_option.name = 'Option'
	at_aex_option.group = 'Group'
	at_aex_option.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Option')+'<br/>') + 
		html_par('Choose OPTION') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Force-Based_Beam-Column_Element','Force-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	at_aex_option.sourceType = MpcAttributeSourceType.List
	at_aex_option.setSourceList(['StandardIntegrationTypes', 'UserDefined', 'Hinge', 'UserHinge', 'DistHinge',
								'RegularizedHinge', 'FixedLocation', 'LowOrder', 'MidDistance'])
	at_aex_option.setDefault('StandardIntegrationTypes')
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'BeamSectionProperty'
	xom.Xgroup = 'Beam-Column'
	xom.addAttribute(at_OPTION_1)
	xom.addAttribute(at_IntegrationType_1)
	xom.addAttribute(at_secTag_1)
	xom.addAttribute(at_numIntPts_1)
	xom.addAttribute(at_OPTION_2)
	xom.addAttribute(at_IntegrationType_2)
	xom.addAttribute(at_numIntPts_2)
	xom.addAttribute(at_secTag_2)
	xom.addAttribute(at_positions_2)
	xom.addAttribute(at_weights_2)
	xom.addAttribute(at_OPTION_3)
	xom.addAttribute(at_IntegrationType_3)
	xom.addAttribute(at_secTagI_3)
	xom.addAttribute(at_lpI_3)
	xom.addAttribute(at_secTagJ_3)
	xom.addAttribute(at_lpJ_3)
	xom.addAttribute(at_secTagE_3)
	xom.addAttribute(at_OPTION_4)
	xom.addAttribute(at_IntegrationType_4)
	xom.addAttribute(at_secTagE_4)
	xom.addAttribute(at_npI)
	xom.addAttribute(at_npJ)
	xom.addAttribute(at_secTagI_4)
	xom.addAttribute(at_positionsI)
	xom.addAttribute(at_weightsI)
	xom.addAttribute(at_secTagJ_4)
	xom.addAttribute(at_positionsJ)
	xom.addAttribute(at_weightsJ)
	xom.addAttribute(at_OPTION_5)
	xom.addAttribute(at_IntegrationType_5)
	xom.addAttribute(at_HingeIntegrationType_5)
	xom.addAttribute(at_numIntPts_5)
	xom.addAttribute(at_secTagI_5)
	xom.addAttribute(at_lpI_5)
	xom.addAttribute(at_secTagJ_5)
	xom.addAttribute(at_lpJ_5)
	xom.addAttribute(at_secTagE_5)
	xom.addAttribute(at_OPTION_6)
	xom.addAttribute(at_IntegrationType_6)
	xom.addAttribute(at_HingeIntegrationType_6)
	xom.addAttribute(at_numIntPts_6)
	xom.addAttribute(at_secTagI_6)
	xom.addAttribute(at_lpI_6)
	xom.addAttribute(at_zetaI)
	xom.addAttribute(at_secTagJ_6)
	xom.addAttribute(at_lpJ_6)
	xom.addAttribute(at_zetaJ)
	xom.addAttribute(at_secTagE_6)
	xom.addAttribute(at_OPTION_7)
	xom.addAttribute(at_IntegrationType_7)
	xom.addAttribute(at_numIntPts_7)
	xom.addAttribute(at_secTag_7)
	xom.addAttribute(at_positions_7)
	xom.addAttribute(at_OPTION_8)
	xom.addAttribute(at_IntegrationType_8)
	xom.addAttribute(at_numIntPts_8)
	xom.addAttribute(at_secTag_8)
	xom.addAttribute(at_positions_8)
	xom.addAttribute(at_weights_8)
	xom.addAttribute(at_OPTION_9)
	xom.addAttribute(at_IntegrationType_9)
	xom.addAttribute(at_numIntPts_9)
	xom.addAttribute(at_secTag_9)
	xom.addAttribute(at_positions_9)
	xom.addAttribute(at_aex_option)
	
	
	# OPTION_1-dep
	xom.setVisibilityDependency(at_OPTION_1, at_IntegrationType_1)
	xom.setVisibilityDependency(at_OPTION_1, at_secTag_1)
	xom.setVisibilityDependency(at_OPTION_1, at_numIntPts_1)
	
	# OPTION_2-dep
	xom.setVisibilityDependency(at_OPTION_2, at_IntegrationType_2)
	xom.setVisibilityDependency(at_OPTION_2, at_numIntPts_2)
	xom.setVisibilityDependency(at_OPTION_2, at_secTag_2)
	xom.setVisibilityDependency(at_OPTION_2, at_positions_2)
	xom.setVisibilityDependency(at_OPTION_2, at_weights_2)
	
	# OPTION_3-dep
	xom.setVisibilityDependency(at_OPTION_3, at_IntegrationType_3)
	xom.setVisibilityDependency(at_OPTION_3, at_secTagI_3)
	xom.setVisibilityDependency(at_OPTION_3, at_lpI_3)
	xom.setVisibilityDependency(at_OPTION_3, at_secTagJ_3)
	xom.setVisibilityDependency(at_OPTION_3, at_lpJ_3)
	xom.setVisibilityDependency(at_OPTION_3, at_secTagE_3)
	
	# OPTION_4-dep
	xom.setVisibilityDependency(at_OPTION_4, at_IntegrationType_4)
	xom.setVisibilityDependency(at_OPTION_4, at_secTagE_4)
	xom.setVisibilityDependency(at_OPTION_4, at_npI)
	xom.setVisibilityDependency(at_OPTION_4, at_npJ)
	xom.setVisibilityDependency(at_OPTION_4, at_secTagI_4)
	xom.setVisibilityDependency(at_OPTION_4, at_positionsI)
	xom.setVisibilityDependency(at_OPTION_4, at_weightsI)
	xom.setVisibilityDependency(at_OPTION_4, at_secTagJ_4)
	xom.setVisibilityDependency(at_OPTION_4, at_positionsJ)
	xom.setVisibilityDependency(at_OPTION_4, at_weightsJ)
	
	# OPTION_5-dep
	xom.setVisibilityDependency(at_OPTION_5, at_IntegrationType_5)
	xom.setVisibilityDependency(at_OPTION_5, at_HingeIntegrationType_5)
	xom.setVisibilityDependency(at_OPTION_5, at_numIntPts_5)
	xom.setVisibilityDependency(at_OPTION_5, at_secTagI_5)
	xom.setVisibilityDependency(at_OPTION_5, at_lpI_5)
	xom.setVisibilityDependency(at_OPTION_5, at_secTagJ_5)
	xom.setVisibilityDependency(at_OPTION_5, at_lpJ_5)
	xom.setVisibilityDependency(at_OPTION_5, at_secTagE_5)
	
	# OPTION_6-dep
	xom.setVisibilityDependency(at_OPTION_6, at_IntegrationType_6)
	xom.setVisibilityDependency(at_OPTION_6, at_HingeIntegrationType_6)
	xom.setVisibilityDependency(at_OPTION_6, at_numIntPts_6)
	xom.setVisibilityDependency(at_OPTION_6, at_secTagI_6)
	xom.setVisibilityDependency(at_OPTION_6, at_lpI_6)
	xom.setVisibilityDependency(at_OPTION_6, at_zetaI)
	xom.setVisibilityDependency(at_OPTION_6, at_secTagJ_6)
	xom.setVisibilityDependency(at_OPTION_6, at_lpJ_6)
	xom.setVisibilityDependency(at_OPTION_6, at_zetaJ)
	xom.setVisibilityDependency(at_OPTION_6, at_secTagE_6)
	
	# OPTION_7-dep
	xom.setVisibilityDependency(at_OPTION_7, at_IntegrationType_7)
	xom.setVisibilityDependency(at_OPTION_7, at_numIntPts_7)
	xom.setVisibilityDependency(at_OPTION_7, at_secTag_7)
	xom.setVisibilityDependency(at_OPTION_7, at_positions_7)
	
	# OPTION_8-dep
	xom.setVisibilityDependency(at_OPTION_8, at_IntegrationType_8)
	xom.setVisibilityDependency(at_OPTION_8, at_numIntPts_8)
	xom.setVisibilityDependency(at_OPTION_8, at_secTag_8)
	xom.setVisibilityDependency(at_OPTION_8, at_positions_8)
	xom.setVisibilityDependency(at_OPTION_8, at_weights_8)
	
	# OPTION_9-dep
	xom.setVisibilityDependency(at_OPTION_9, at_numIntPts_9)
	xom.setVisibilityDependency(at_OPTION_9, at_secTag_9)
	xom.setVisibilityDependency(at_OPTION_9, at_positions_9)
	
	
	# auto-exclusive dependencies
	# OPTION_1 ... OPTION_9
	xom.setBooleanAutoExclusiveDependency(at_aex_option, at_OPTION_1)
	xom.setBooleanAutoExclusiveDependency(at_aex_option, at_OPTION_2)
	xom.setBooleanAutoExclusiveDependency(at_aex_option, at_OPTION_3)
	xom.setBooleanAutoExclusiveDependency(at_aex_option, at_OPTION_4)
	xom.setBooleanAutoExclusiveDependency(at_aex_option, at_OPTION_5)
	xom.setBooleanAutoExclusiveDependency(at_aex_option, at_OPTION_6)
	xom.setBooleanAutoExclusiveDependency(at_aex_option, at_OPTION_7)
	xom.setBooleanAutoExclusiveDependency(at_aex_option, at_OPTION_8)
	xom.setBooleanAutoExclusiveDependency(at_aex_option, at_OPTION_9)
	
	
	return xom

def makeExtrusionBeamDataCompoundInfo(xobj):
	
	doc = App.caeDocument()
	if doc is None:
		raise Exception('no active cae document')
	
	info = MpcSectionExtrusionBeamDataCompoundInfo()
	'''
	here we may have 1 or multiple cross sections. 
	If we have only 1 cross section return an info with just 1 item, 
	regardless of the integration rule
	since this is fine for visualization purposes (i.e. the cross section does not change along
	the curve).
	If we have multiple cross section we also need to get information
	about the integraton rule to give a meaningful representation of the
	variation of the cross section along the curve.
	Note that the references properties may or may not have a cross section
	representation (they have it if they are for example Elastic Fiber or Aggregator with Fiber).
	To make sure the referenced properties have a representation, we check for the 
	makeExtrusionBeamDataCompoundInfo in their xobject
	
	notes for filling info object.
	note that with hinge integration we dont have the length of the element at this point.
	so we do the following:
	weights related to the plastic hinge length are input as is (in real world scale)
	weights related to internal points are input as parametric and their sum must be 1
	STKO will take care of post-processing them when the property will be assigned to each element
	for proper visualization.
	the info.add method by default takes 2 arguments (property and weight, assuming the weigth be parametric)
	otherwise we can explicitly tell if it is parametric or not using the 
	info.add method with 3 parameters, the third one being a boolean, True for parametric and False for real-scale
	'''
	
	at_option = xobj.getAttribute('StandardIntegrationTypes')
	if(at_option is None):
		raise Exception('Error: cannot find "StandardIntegrationTypes" attribute')
	if at_option.boolean:
		'''
		option 1. single section with one of the standard rules.
		'''
		at_secTag = xobj.getAttribute('secTag/1')
		if(at_secTag is None):
			raise Exception('Error: cannot find "secTag/1" attribute')
		secTag = at_secTag.index
		prop = doc.getPhysicalProperty(secTag)
		info_item = exutils.getExtrusionDataSingleItem(prop)
		info.add(info_item.property, 1.0, True, False, info_item.yOffset, info_item.zOffset)
		return info
	
	at_option = xobj.getAttribute('UserDefined')
	if(at_option is None):
		raise Exception('Error: cannot find "UserDefined" attribute')
	if at_option.boolean:
		'''
		option 2. multiple sections with user defined rule.
		'''
		at_secTag_2 = xobj.getAttribute('secTag/2')
		if(at_secTag_2 is None):
			raise Exception('Error: cannot find "secTag/2" attribute')
		secTag_2 = at_secTag_2.indexVector
		at_weights_2 = xobj.getAttribute('weights/2')
		if(at_weights_2 is None):
			raise Exception('Error: cannot find "weights/2" attribute')
		weights_2 = at_weights_2.quantityVector
		n = len(secTag_2)
		if n != len(weights_2):
			raise Exception('Error: vectors "secTag/2" and "weights/2" must have the same size')
		if n == 0:
			return info # quick return
		'''
		here we allow some of the n properties to be None. but not all of them!
		'''
		num_valid = 0
		processed_info_items = [None]*n
		for i in range(n):
			prop = doc.getPhysicalProperty(secTag_2[i])
			info_item = exutils.getExtrusionDataSingleItem(prop)
			processed_info_items[i] = info_item
			if info_item is not None:
				num_valid += 1
		if num_valid == 0:
			return info # quick return
		'''
		fill info
		'''
		exutils.checkOffsetCompatibility(processed_info_items)
		for i in range(n):
			info_item = processed_info_items[i]
			info.add(info_item.property, weights_2.valueAt(i), True, False, info_item.yOffset, info_item.zOffset)
		return info
	
	at_option = xobj.getAttribute('Hinge')
	if(at_option is None):
		raise Exception('Error: cannot find "Hinge" attribute')
	if at_option.boolean:
		'''
		option 3. standard hinge rules.
		'''
		at_secTagE_3 = xobj.getAttribute('secTagE/3')
		if(at_secTagE_3 is None):
			raise Exception('Error: cannot find "secTagE/3" attribute')
		secTagE_3 = at_secTagE_3.index
		at_secTagI_3 = xobj.getAttribute('secTagI/3')
		if(at_secTagI_3 is None):
			raise Exception('Error: cannot find "secTagI/3" attribute')
		secTagI_3 = at_secTagI_3.index
		at_secTagJ_3 = xobj.getAttribute('secTagJ/3')
		if(at_secTagJ_3 is None):
			raise Exception('Error: cannot find "secTagJ/3" attribute')
		secTagJ_3 = at_secTagJ_3.index
		at_lpI_3 = xobj.getAttribute('lpI/3')
		if(at_lpI_3 is None):
			raise Exception('Error: cannot find "lpI/3" attribute')
		lpI_3 = at_lpI_3.quantityScalar.value
		at_lpJ_3 = xobj.getAttribute('lpJ/3')
		if(at_lpJ_3 is None):
			raise Exception('Error: cannot find "lpJ/3" attribute')
		lpJ_3 = at_lpJ_3.quantityScalar.value
		'''
		here we allow some of the n properties to be None. but not all of them!
		'''
		prop_I = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagI_3))
		prop_J = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagJ_3))
		prop_E = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagE_3))
		if (prop_I is None) and (prop_J is None) and (prop_E is None):
			return info # quick return
		'''
		fill info.
		'''
		# print(prop_I, prop_J, prop_E)
		exutils.checkOffsetCompatibility([prop_I, prop_E, prop_J])
		info.add(prop_I.property, lpI_3, False, False, prop_I.yOffset, prop_I.zOffset)
		info.add(prop_E.property,   1.0,  True, False, prop_E.yOffset, prop_E.zOffset)
		info.add(prop_J.property, lpJ_3, False, False, prop_J.yOffset, prop_J.zOffset)
		return info
	
	at_option = xobj.getAttribute('UserHinge')
	if(at_option is None):
		raise Exception('Error: cannot find "UserHinge" attribute')
	if at_option.boolean:
		'''
		option 4. user-defined hinge rule.
		'''
		at_secTagE_4 = xobj.getAttribute('secTagE/4')
		if(at_secTagE_4 is None):
			raise Exception('Error: cannot find "secTagE/4" attribute')
		secTagE_4 = at_secTagE_4.index
		at_secTagI_4 = xobj.getAttribute('secTagI/4')
		if(at_secTagI_4 is None):
			raise Exception('Error: cannot find "secTagI/4" attribute')
		secTagI_4 = at_secTagI_4.indexVector
		at_secTagJ_4 = xobj.getAttribute('secTagJ/4')
		if(at_secTagJ_4 is None):
			raise Exception('Error: cannot find "secTagJ/4" attribute')
		secTagJ_4 = at_secTagJ_4.indexVector
		at_weightsI = xobj.getAttribute('weightsI')
		if(at_weightsI is None):
			raise Exception('Error: cannot find "weightsI" attribute')
		weightsI = at_weightsI.quantityVector
		at_weightsJ = xobj.getAttribute('weightsJ')
		if(at_weightsJ is None):
			raise Exception('Error: cannot find "weightsJ" attribute')
		weightsJ = at_weightsJ.quantityVector
		nI = len(secTagI_4)
		if nI != len(weightsI):
			raise Exception('section tags and weights vectors at node I must have the same size')
		nJ = len(secTagJ_4)
		if nJ != len(weightsJ):
			raise Exception('section tags and weights vectors at node J must have the same size')
		'''
		here we allow some of the n properties to be None. but not all of them!
		'''
		props_I = []
		weights_I = []
		props_J = []
		weights_J = []
		num_valid = 0
		for i in range(nI):
			iprop = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagI_4[i]))
			iweight = weightsI.valueAt(i)
			if (iweight < 0.0) or (iweight > 1.0):
				raise Exception('weights and positions should be in the range 0-1')
			props_I.append(iprop)
			weights_I.append(iweight)
			if iprop is not None:
				num_valid += 1
		for i in range(nJ):
			iprop = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagJ_4[i]))
			iweight = weightsJ.valueAt(i)
			if (iweight < 0.0) or (iweight > 1.0):
				raise Exception('weights and positions should be in the range 0-1')
			props_J.append(iprop)
			weights_J.append(iweight)
			if iprop is not None:
				num_valid += 1
		prop_E = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagE_4))
		if prop_E is not None:
			num_valid += 1
		if num_valid == 0:
			return info # quick return
		'''
		fill info.
		'''
		exutils.checkOffsetCompatibility(props_I + [prop_E] + props_J)
		for i in range(len(props_I)):
			info_item = props_I[i]
			info.add(info_item.property, weights_I[i], False, False, info_item.yOffset, info_item.zOffset)
		info.add(prop_E.property, 1.0, True, False, prop_E.yOffset, prop_E.zOffset)
		for i in range(len(props_J)):
			info_item = props_J[i]
			info.add(info_item.property, weights_J[i], False, False, info_item.yOffset, info_item.zOffset)
		return info
	
	at_option = xobj.getAttribute('DistHinge')
	if(at_option is None):
		raise Exception('Error: cannot find "DistHinge" attribute')
	if at_option.boolean:
		'''
		option 5. distributed hinge rule.
		'''
		at_secTagE_5 = xobj.getAttribute('secTagE/5')
		if(at_secTagE_5 is None):
			raise Exception('Error: cannot find "secTagE/5" attribute')
		secTagE_5 = at_secTagE_5.index
		at_secTagI_5 = xobj.getAttribute('secTagI/5')
		if(at_secTagI_5 is None):
			raise Exception('Error: cannot find "secTagI/5" attribute')
		secTagI_5 = at_secTagI_5.index
		at_secTagJ_5 = xobj.getAttribute('secTagJ/5')
		if(at_secTagJ_5 is None):
			raise Exception('Error: cannot find "secTagJ/5" attribute')
		secTagJ_5 = at_secTagJ_5.index
		at_lpI_5 = xobj.getAttribute('lpI/5')
		if(at_lpI_5 is None):
			raise Exception('Error: cannot find "lpI/5" attribute')
		lpI_5 = at_lpI_5.quantityScalar.value
		at_lpJ_5 = xobj.getAttribute('lpJ/5')
		if(at_lpJ_5 is None):
			raise Exception('Error: cannot find "lpJ/5" attribute')
		lpJ_5 = at_lpJ_5.quantityScalar.value
		'''
		here we allow some of the n properties to be None. but not all of them!
		'''
		prop_I = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagI_5))
		prop_J = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagJ_5))
		prop_E = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagE_5))
		if (prop_I is None) and (prop_J is None) and (prop_E is None):
			return info # quick return
		'''
		fill info.
		'''
		exutils.checkOffsetCompatibility([prop_I, prop_E, prop_J])
		info.add(prop_I.property, lpI_5, False, False, prop_I.yOffset, prop_I.zOffset)
		info.add(prop_E.property,   1.0,  True, False, prop_E.yOffset, prop_E.zOffset)
		info.add(prop_J.property, lpJ_5, False, False, prop_J.yOffset, prop_J.zOffset)
		return info
	
	at_option = xobj.getAttribute('RegularizedHinge')
	if(at_option is None):
		raise Exception('Error: cannot find "RegularizedHinge" attribute')
	if at_option.boolean:
		'''
		option 6. distributed hinge rule.
		'''
		at_secTagE_6 = xobj.getAttribute('secTagE/6')
		if(at_secTagE_6 is None):
			raise Exception('Error: cannot find "secTagE/6" attribute')
		secTagE_6 = at_secTagE_6.index
		at_secTagI_6 = xobj.getAttribute('secTagI/6')
		if(at_secTagI_6 is None):
			raise Exception('Error: cannot find "secTagI/6" attribute')
		secTagI_6 = at_secTagI_6.index
		at_secTagJ_6 = xobj.getAttribute('secTagJ/6')
		if(at_secTagJ_6 is None):
			raise Exception('Error: cannot find "secTagJ/6" attribute')
		secTagJ_6 = at_secTagJ_6.index
		at_lpI_6 = xobj.getAttribute('lpI/6')
		if(at_lpI_6 is None):
			raise Exception('Error: cannot find "lpI/6" attribute')
		lpI_6 = at_lpI_6.quantityScalar.value
		at_lpJ_6 = xobj.getAttribute('lpJ/6')
		if(at_lpJ_6 is None):
			raise Exception('Error: cannot find "lpJ/6" attribute')
		lpJ_6 = at_lpJ_6.quantityScalar.value
		'''
		here we allow some of the n properties to be None. but not all of them!
		'''
		prop_I = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagI_6))
		prop_J = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagJ_6))
		prop_E = exutils.getExtrusionDataSingleItem(doc.getPhysicalProperty(secTagE_6))
		if (prop_I is None) and (prop_J is None) and (prop_E is None):
			return info # quick return
		'''
		fill info.
		'''
		exutils.checkOffsetCompatibility([prop_I, prop_E, prop_J])
		info.add(prop_I.property, lpI_6, False, False, prop_I.yOffset, prop_I.zOffset)
		info.add(prop_E.property,   1.0,  True, False, prop_E.yOffset, prop_E.zOffset)
		info.add(prop_J.property, lpJ_6, False, False, prop_J.yOffset, prop_J.zOffset)
		return info
	
	at_option = xobj.getAttribute('FixedLocation')
	if(at_option is None):
		raise Exception('Error: cannot find "FixedLocation" attribute')
	if at_option.boolean:
		'''
		option 7. multiple sections with fixed locations.
		'''
		at_secTag_7 = xobj.getAttribute('secTag/7')
		if(at_secTag_7 is None):
			raise Exception('Error: cannot find "secTag/7" attribute')
		secTag_7 = at_secTag_7.indexVector
		at_positions_7 = xobj.getAttribute('positions/7')
		if(at_positions_7 is None):
			raise Exception('Error: cannot find "positions/7" attribute')
		positions_7 = at_positions_7.quantityVector
		n = len(secTag_7)
		if n != len(positions_7):
			raise Exception('Error: vectors "secTag/7" and "positions/7" must have the same size')
		if n == 0:
			return info # quick return
		'''
		here we allow some of the n properties to be None. but not all of them!
		'''
		num_valid = 0
		processed_info_items = [None]*n
		for i in range(n):
			prop = doc.getPhysicalProperty(at_secTag_7[i])
			info_item = exutils.getExtrusionDataSingleItem(prop)
			processed_info_items[i] = info_item
			if info_item is not None:
				num_valid += 1
		if num_valid == 0:
			return info # quick return
		'''
		get weights for fixed locations
		'''
		R = Math.vec(n)
		M = Math.mat(n,n)
		for i in range(n):
			R[i] = 1.0/(i+1)
			for j in range(n):
				pj = positions_7.valueAt(j)
				if (pj < 0.0) or (pj > 1.0):
					raise Exception('section location is outside the valid range (0,1)')
				M[i,j] = pj**i
		weights = M.solve(R)
		'''
		fill info
		'''
		exutils.checkOffsetCompatibility(processed_info_items)
		for i in range(n):
			info_item = processed_info_items[i]
			info.add(info_item.property, weights[i], True, False, info_item.yOffset, info_item.zOffset)
		return info
	
	at_option = xobj.getAttribute('LowOrder')
	if(at_option is None):
		raise Exception('Error: cannot find "LowOrder" attribute')
	if at_option.boolean:
		'''
		option 8. multiple sections with low order rule.
		'''
		at_secTag_8 = xobj.getAttribute('secTag/8')
		if(at_secTag_8 is None):
			raise Exception('Error: cannot find "secTag/8" attribute')
		secTag_8 = at_secTag_8.indexVector
		at_positions_8 = xobj.getAttribute('positions/8')
		if(at_positions_8 is None):
			raise Exception('Error: cannot find "positions/8" attribute')
		positions_8 = at_positions_8.quantityVector
		at_weights_8 = xobj.getAttribute('weights/8')
		if(at_weights_8 is None):
			raise Exception('Error: cannot find "weights/8" attribute')
		weights_8 = at_weights_8.quantityVector
		n = len(secTag_8)
		if n != len(positions_8):
			raise Exception('Error: vectors "secTag/8" and "positions/8" must have the same size')
		if n > len(weights_8):
			raise Exception('Error: size of "weights/8" vector should not be larger then the size of vectors "secTag/8" and "positions/8"')
		if n == 0:
			return info # quick return
		'''
		here we allow some of the n properties to be None. but not all of them!
		'''
		num_valid = 0
		processed_info_items = [None]*n
		for i in range(n):
			prop = doc.getPhysicalProperty(at_secTag_8[i])
			info_item = exutils.getExtrusionDataSingleItem(prop)
			processed_info_items[i] = info_item
			if info_item is not None:
				num_valid += 1
		if num_valid == 0:
			return info # quick return
		'''
		get the weights not specified by the user
		'''
		nc = len(weights_8)
		nf = n - nc
		if nf > 0:
			pts = [0.0]*n
			for i in range(n):
				ip = positions_8.valueAt(i)
				if (ip < 0.0) or (ip > 1.0):
					raise Exception('section location is outside the valid range (0,1)')
				pts[i] = ip
			R = Math.vec(n)
			for i in range(nf):
				sum = 0.0
				for j in range(nc):
					sum += (pts[j]**i)*weights_8.valueAt(j)
				R[i] = 1.0/(i+1) - sum
			M = Math.mat(nf,nf)
			for i in range(n):
				for j in range(n):
					M[i,j] = pts[nc+j]**i
			weights = M.solve(R)
		else:
			weigths = [weights_8.valueAt(i) for i in range(nc)]
		'''
		fill info
		'''
		exutils.checkOffsetCompatibility(processed_info_items)
		for i in range(n):
			info_item = processed_info_items[i]
			info.add(info_item.property, weights[i], True, False, info_item.yOffset, info_item.zOffset)
		return info
	
	at_option = xobj.getAttribute('MidDistance')
	if(at_option is None):
		raise Exception('Error: cannot find "MidDistance" attribute')
	if at_option.boolean:
		'''
		option 9. multiple sections with mid distace rule.
		'''
		at_secTag_9 = xobj.getAttribute('secTag/9')
		if(at_secTag_9 is None):
			raise Exception('Error: cannot find "secTag/9" attribute')
		secTag_9 = at_secTag_9.indexVector
		at_positions_9 = xobj.getAttribute('positions/9')
		if(at_positions_9 is None):
			raise Exception('Error: cannot find "positions/9" attribute')
		positions_9 = at_positions_9.quantityVector
		n = len(secTag_9)
		if n != len(positions_9):
			raise Exception('Error: vectors "secTag/9" and "positions/9" must have the same size')
		if n == 0:
			return info # quick return
		'''
		here we allow some of the n properties to be None. but not all of them!
		'''
		num_valid = 0
		processed_info_items = [None]*n
		for i in range(n):
			prop = doc.getPhysicalProperty(at_secTag_9[i])
			info_item = exutils.getExtrusionDataSingleItem(prop)
			processed_info_items[i] = info_item
			if info_item is not None:
				num_valid += 1
		if num_valid == 0:
			return info # quick return
		'''
		compute sorted position vector. then compute weights
		'''
		pts = sorted([positions_9.valueAt(i) for i in range(n)])
		for ip in pts:
			if (ip < 0.0) or (ip > 1.0):
				raise Exception('section location is outside the valid range (0,1)')
		mids = [0.5*(pts[i]+pts[i+1]) for i in range(n-1)]
		weights = [0.0]*n
		weights[0] = mids[0]
		weights[n-1] = 1.0-mids[n-2]
		for i in range(1,n-1):
			weights[i] = mids[i] - mids[i-1]
		'''
		fill info
		'''
		exutils.checkOffsetCompatibility(processed_info_items)
		for i in range(n):
			info_item = processed_info_items[i]
			info.add(info_item.property, weights[i], True, False, info_item.yOffset, info_item.zOffset)
		return info
	
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
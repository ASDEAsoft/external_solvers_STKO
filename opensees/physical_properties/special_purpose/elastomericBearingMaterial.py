import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Group'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') +
		html_par('choose between 2D and 3D') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('2D')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Group'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_2D.editable = False
	
	# 3D
	at_3D = MpcAttributeMetaData()
	at_3D.type = MpcAttributeType.Boolean
	at_3D.name = '3D'
	at_3D.group = 'Group'
	at_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('3D')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# matTagP
	at_matTagP = MpcAttributeMetaData()
	at_matTagP.type = MpcAttributeType.Index
	at_matTagP.name = 'matTagP'
	at_matTagP.group = '-P'
	at_matTagP.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTagP')+'<br/>') +
		html_par('tag associated with previously-defined UniaxialMaterial in axial direction') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_matTagP.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagP.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# matTagT
	at_matTagT = MpcAttributeMetaData()
	at_matTagT.type = MpcAttributeType.Index
	at_matTagT.name = 'matTagT'
	at_matTagT.group = '-T'
	at_matTagT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTagT')+'<br/>') +
		html_par('tag associated with previously-defined UniaxialMaterial in axial direction') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_matTagT.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagT.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# matTagMy
	at_matTagMy = MpcAttributeMetaData()
	at_matTagMy.type = MpcAttributeType.Index
	at_matTagMy.name = 'matTagMy'
	at_matTagMy.group = '-My'
	at_matTagMy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTagMy')+'<br/>') +
		html_par('tag associated with previously-defined UniaxialMaterial in axial direction') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_matTagMy.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagMy.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# matTagMz
	at_matTagMz = MpcAttributeMetaData()
	at_matTagMz.type = MpcAttributeType.Index
	at_matTagMz.name = 'matTagMz'
	at_matTagMz.group = '-Mz'
	at_matTagMz.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTagMz')+'<br/>') +
		html_par('tag associated with previously-defined UniaxialMaterial in axial direction') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_matTagMz.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTagMz.indexSource.addAllowedNamespace("materials.uniaxial")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'elastomericBearingMaterial'
	xom.Xgroup = 'Bearing Material'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_matTagP)
	xom.addAttribute(at_matTagT)
	xom.addAttribute(at_matTagMy)
	xom.addAttribute(at_matTagMz)
	
	
	# 3D-dep
	xom.setVisibilityDependency(at_3D, at_matTagT)
	xom.setVisibilityDependency(at_3D, at_matTagMy)
	
	
	# auto-exclusive dependencies
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	
	return xom
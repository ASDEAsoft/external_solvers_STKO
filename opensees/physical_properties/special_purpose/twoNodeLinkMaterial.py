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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('2D')
	
	# ModelType
	at_ModelType = MpcAttributeMetaData()
	at_ModelType.type = MpcAttributeType.String
	at_ModelType.name = 'ModelType'
	at_ModelType.group = 'Group'
	at_ModelType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ModelType')+'<br/>') + 
		html_par('choose between "U (Displacement)" and "U-R (Displacement+Rotation)"') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_ModelType.sourceType = MpcAttributeSourceType.List
	at_ModelType.setSourceList(['U (Displacement)', 'U-R (Displacement+Rotation)'])
	at_ModelType.setDefault('U (Displacement)')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Group'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# D
	at_D = MpcAttributeMetaData()
	at_D.type = MpcAttributeType.Boolean
	at_D.name = 'U (Displacement)'
	at_D.groD = 'Constraint'
	at_D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U (Displacement)')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_D.editable = False
	
	# UR
	at_UR = MpcAttributeMetaData()
	at_UR.type = MpcAttributeType.Boolean
	at_UR.name = 'U-R (Displacement+Rotation)'
	at_UR.group = 'Constraint'
	at_UR.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U-R (Displacement+Rotation)')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_UR.editable = False
	
	# dir1
	at_dir1 = MpcAttributeMetaData()
	at_dir1.type = MpcAttributeType.Boolean
	at_dir1.name = 'dir1'
	at_dir1.group = 'Group'
	at_dir1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dir1')+'<br/>') +
		html_par('translation along local x axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# matTag1
	at_matTag1 = MpcAttributeMetaData()
	at_matTag1.type = MpcAttributeType.Index
	at_matTag1.name = 'matTag1'
	at_matTag1.group = 'Optional parameters'
	at_matTag1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag1')+'<br/>') +
		html_par('tags associated with previously-defined UniaxialMaterials') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_matTag1.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag1.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# dir2
	at_dir2 = MpcAttributeMetaData()
	at_dir2.type = MpcAttributeType.Boolean
	at_dir2.name = 'dir2'
	at_dir2.group = 'Group'
	at_dir2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dir2')+'<br/>') +
		html_par('translation along local y axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# matTag2
	at_matTag2 = MpcAttributeMetaData()
	at_matTag2.type = MpcAttributeType.Index
	at_matTag2.name = 'matTag2'
	at_matTag2.group = 'Optional parameters'
	at_matTag2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag2')+'<br/>') +
		html_par('tags associated with previously-defined UniaxialMaterials') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_matTag2.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag2.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# dir3_2D
	at_dir3_2D = MpcAttributeMetaData()
	at_dir3_2D.type = MpcAttributeType.Boolean
	at_dir3_2D.name = 'dir3/2D'
	at_dir3_2D.group = 'Group'
	at_dir3_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dir3')+'<br/>') +
		html_par('rotation about local z axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# matTag3_2D
	at_matTag3_2D = MpcAttributeMetaData()
	at_matTag3_2D.type = MpcAttributeType.Index
	at_matTag3_2D.name = 'matTag3/2D'
	at_matTag3_2D.group = 'Optional parameters'
	at_matTag3_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag3')+'<br/>') +
		html_par('tags associated with previously-defined UniaxialMaterials') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_matTag3_2D.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag3_2D.indexSource.addAllowedNamespace("materials.uniaxial")
		
	# dir3_3D
	at_dir3_3D = MpcAttributeMetaData()
	at_dir3_3D.type = MpcAttributeType.Boolean
	at_dir3_3D.name = 'dir3/3D'
	at_dir3_3D.group = 'Group'
	at_dir3_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dir3')+'<br/>') +
		html_par('translation along local z axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# matTag3_3D
	at_matTag3_3D = MpcAttributeMetaData()
	at_matTag3_3D.type = MpcAttributeType.Index
	at_matTag3_3D.name = 'matTag3/3D'
	at_matTag3_3D.group = 'Optional parameters'
	at_matTag3_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag3')+'<br/>') +
		html_par('tags associated with previously-defined UniaxialMaterials') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_matTag3_3D.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag3_3D.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# dir4
	at_dir4 = MpcAttributeMetaData()
	at_dir4.type = MpcAttributeType.Boolean
	at_dir4.name = 'dir4'
	at_dir4.group = 'Group'
	at_dir4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dir4')+'<br/>') +
		html_par('rotation about local x axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# matTag4
	at_matTag4 = MpcAttributeMetaData()
	at_matTag4.type = MpcAttributeType.Index
	at_matTag4.name = 'matTag4'
	at_matTag4.group = 'Optional parameters'
	at_matTag4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag4')+'<br/>') +
		html_par('tags associated with previously-defined UniaxialMaterials') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_matTag4.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag4.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# dir5
	at_dir5 = MpcAttributeMetaData()
	at_dir5.type = MpcAttributeType.Boolean
	at_dir5.name = 'dir5'
	at_dir5.group = 'Group'
	at_dir5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dir5')+'<br/>') +
		html_par('rotation about local y axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# matTag5
	at_matTag5 = MpcAttributeMetaData()
	at_matTag5.type = MpcAttributeType.Index
	at_matTag5.name = 'matTag5'
	at_matTag5.group = 'Optional parameters'
	at_matTag5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag5')+'<br/>') +
		html_par('tags associated with previously-defined UniaxialMaterials') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_matTag5.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag5.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# dir6
	at_dir6 = MpcAttributeMetaData()
	at_dir6.type = MpcAttributeType.Boolean
	at_dir6.name = 'dir6'
	at_dir6.group = 'Group'
	at_dir6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dir6')+'<br/>') +
		html_par('rotation about local z axis') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	
	# matTag6
	at_matTag6 = MpcAttributeMetaData()
	at_matTag6.type = MpcAttributeType.Index
	at_matTag6.name = 'matTag6'
	at_matTag6.group = 'Optional parameters'
	at_matTag6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag6')+'<br/>') +
		html_par('tags associated with previously-defined UniaxialMaterials') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Two_Node_Link_Element','Two Node Link Element')+'<br/>') +
		html_end()
		)
	at_matTag6.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag6.indexSource.addAllowedNamespace("materials.uniaxial")
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'twoNodeLinkMaterial'
	xom.Xgroup = 'twoNodeLink Material'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_ModelType)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_D)
	xom.addAttribute(at_UR)
	xom.addAttribute(at_dir1)
	xom.addAttribute(at_matTag1)
	xom.addAttribute(at_dir2)
	xom.addAttribute(at_matTag2)
	xom.addAttribute(at_dir3_2D)
	xom.addAttribute(at_matTag3_2D)
	xom.addAttribute(at_dir3_3D)
	xom.addAttribute(at_matTag3_3D)
	xom.addAttribute(at_dir4)
	xom.addAttribute(at_matTag4)
	xom.addAttribute(at_dir5)
	xom.addAttribute(at_matTag5)
	xom.addAttribute(at_dir6)
	xom.addAttribute(at_matTag6)
	
	
	# matTag1-dep
	xom.setVisibilityDependency(at_dir1, at_matTag1)
	
	# matTag2-dep
	xom.setVisibilityDependency(at_dir2, at_matTag2)
	
	# dir3_2D-dep
	xom.setVisibilityDependency(at_2D, at_dir3_2D)
	xom.setVisibilityDependency(at_UR, at_dir3_2D)
	
	# matTag3_2D-dep
	xom.setVisibilityDependency(at_2D, at_matTag3_2D)
	xom.setVisibilityDependency(at_UR, at_matTag3_2D)
	xom.setVisibilityDependency(at_dir3_2D, at_matTag3_2D)
	
	# dir3_3D-dep
	xom.setVisibilityDependency(at_3D, at_dir3_3D)
	xom.setVisibilityDependency(at_3D, at_matTag3_3D)
	
	# matTag3_3D-dep
	xom.setVisibilityDependency(at_dir3_3D, at_matTag3_3D)
	
	# dir4_3D, dir5_3D, dir6_3D, -dep
	xom.setVisibilityDependency(at_3D, at_dir4)
	xom.setVisibilityDependency(at_UR, at_dir4)
	
	xom.setVisibilityDependency(at_3D, at_dir5)
	xom.setVisibilityDependency(at_UR, at_dir5)
	
	xom.setVisibilityDependency(at_3D, at_dir6)
	xom.setVisibilityDependency(at_UR, at_dir6)
	
	# matTag4_3D, matTag5_3D, matTag6_3D, -dep
	xom.setVisibilityDependency(at_3D, at_matTag4)
	xom.setVisibilityDependency(at_UR, at_matTag4)
	xom.setVisibilityDependency(at_dir4, at_matTag4)
	
	xom.setVisibilityDependency(at_3D, at_matTag5)
	xom.setVisibilityDependency(at_UR, at_matTag5)
	xom.setVisibilityDependency(at_dir5, at_matTag5)
	
	xom.setVisibilityDependency(at_3D, at_matTag6)
	xom.setVisibilityDependency(at_UR, at_matTag6)
	xom.setVisibilityDependency(at_dir6, at_matTag6)
	
	
	# auto-exclusive dependencies
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	# 2D or 2D Beam or 3D or 3D Beam
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_D)
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_UR)
	
	
	return xom
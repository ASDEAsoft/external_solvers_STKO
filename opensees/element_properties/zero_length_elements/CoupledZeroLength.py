import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

class my_data:
	def __init__(self):
		# attributes will be set in the __control method
		pass

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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +
		html_end()
		)
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('3D')
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Group'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') + 
		html_par('Dx Constraint') +
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
		html_par('Dx Constraint') +
		html_end()
		)
	at_3D.editable = False
	
	# ModelType
	at_ModelType = MpcAttributeMetaData()
	at_ModelType.type = MpcAttributeType.String
	at_ModelType.name = 'ModelType'
	at_ModelType.group = 'Group'
	at_ModelType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ModelType')+'<br/>') + 
		html_par('choose between "U (Displacement)" and "U-R (Displacement+Rotation)"') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +		html_end()
		)
	at_ModelType.sourceType = MpcAttributeSourceType.List
	at_ModelType.setSourceList(['U (Displacement)', 'U-R (Displacement+Rotation)'])
	at_ModelType.setDefault('U-R (Displacement+Rotation)')
	
	# D
	at_D = MpcAttributeMetaData()
	at_D.type = MpcAttributeType.Boolean
	at_D.name = 'U (Displacement)'
	at_D.groD = 'Group'
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
	at_UR.group = 'Group'
	at_UR.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('U-R (Displacement+Rotation)')+'<br/>') + 
		html_par('') +
		html_end()
		)
	at_UR.editable = False
	
	# # Dir1_2D_D
	at_Dir1_2D_D = MpcAttributeMetaData()
	at_Dir1_2D_D.type = MpcAttributeType.Integer
	at_Dir1_2D_D.name = 'Dir1/2D_D'
	at_Dir1_2D_D.group = 'Group'
	at_Dir1_2D_D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dir1')+'<br/>') + 
		html_par('the two directions, 1 through ndof.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +
		html_end()
		)
	at_Dir1_2D_D.sourceType = MpcAttributeSourceType.List
	at_Dir1_2D_D.setSourceList([1, 2])
	at_Dir1_2D_D.setDefault(1)
	
	# # Dir2_2D-U
	at_Dir2_2D_D = MpcAttributeMetaData()
	at_Dir2_2D_D.type = MpcAttributeType.Integer
	at_Dir2_2D_D.name = 'Dir2/2D_D'
	at_Dir2_2D_D.group = 'Group'
	at_Dir2_2D_D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dir2')+'<br/>') + 
		html_par('the two directions, 1 through ndof.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +
		html_end()
		)
	at_Dir2_2D_D.sourceType = MpcAttributeSourceType.List
	at_Dir2_2D_D.setSourceList([1, 2])
	at_Dir2_2D_D.setDefault(2)
	
	# # Dir1_2D
	at_Dir1_2D = MpcAttributeMetaData()
	at_Dir1_2D.type = MpcAttributeType.Integer
	at_Dir1_2D.name = 'Dir1/2D'
	at_Dir1_2D.group = 'Group'
	at_Dir1_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dir1')+'<br/>') + 
		html_par('the two directions, 1 through ndof.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +
		html_end()
		)
	at_Dir1_2D.sourceType = MpcAttributeSourceType.List
	at_Dir1_2D.setSourceList([1, 2, 3])
	at_Dir1_2D.setDefault(1)
	
	# # Dir2_2D
	at_Dir2_2D = MpcAttributeMetaData()
	at_Dir2_2D.type = MpcAttributeType.Integer
	at_Dir2_2D.name = 'Dir2/2D'
	at_Dir2_2D.group = 'Group'
	at_Dir2_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dir2')+'<br/>') + 
		html_par('the two directions, 1 through ndof.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +
		html_end()
		)
	at_Dir2_2D.sourceType = MpcAttributeSourceType.List
	at_Dir2_2D.setSourceList([1, 2, 3])
	at_Dir2_2D.setDefault(2)
	
	# # Dir1_3D_D
	at_Dir1_3D_D = MpcAttributeMetaData()
	at_Dir1_3D_D.type = MpcAttributeType.Integer
	at_Dir1_3D_D.name = 'Dir1/3D_D'
	at_Dir1_3D_D.group = 'Group'
	at_Dir1_3D_D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dir1')+'<br/>') + 
		html_par('the two directions, 1 through ndof.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +
		html_end()
		)
	at_Dir1_3D_D.sourceType = MpcAttributeSourceType.List
	at_Dir1_3D_D.setSourceList([1, 2, 3])
	at_Dir1_3D_D.setDefault(1)
	
	# # Dir2_3D_D
	at_Dir2_3D_D = MpcAttributeMetaData()
	at_Dir2_3D_D.type = MpcAttributeType.Integer
	at_Dir2_3D_D.name = 'Dir2/3D_D'
	at_Dir2_3D_D.group = 'Group'
	at_Dir2_3D_D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dir2')+'<br/>') + 
		html_par('the two directions, 1 through ndof.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +
		html_end()
		)
	at_Dir2_3D_D.sourceType = MpcAttributeSourceType.List
	at_Dir2_3D_D.setSourceList([1, 2, 3])
	at_Dir2_3D_D.setDefault(2)
	
	# Dir1_3D
	at_Dir1_3D = MpcAttributeMetaData()
	at_Dir1_3D.type = MpcAttributeType.Integer
	at_Dir1_3D.name = 'Dir1/3D'
	at_Dir1_3D.group = 'Group'
	at_Dir1_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dir1')+'<br/>') + 
		html_par('the two directions, 1 through ndof.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +
		html_end()
		)
	at_Dir1_3D.sourceType = MpcAttributeSourceType.List
	at_Dir1_3D.setSourceList([1, 2, 3, 4, 5, 6])
	at_Dir1_3D.setDefault(1)
	
	# Dir2_3D
	at_Dir2_3D = MpcAttributeMetaData()
	at_Dir2_3D.type = MpcAttributeType.Integer
	at_Dir2_3D.name = 'Dir2/3D'
	at_Dir2_3D.group = 'Group'
	at_Dir2_3D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dir2')+'<br/>') + 
		html_par('the two directions, 1 through ndof.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +
		html_end()
		)
	at_Dir2_3D.sourceType = MpcAttributeSourceType.List
	at_Dir2_3D.setSourceList([1, 2, 3, 4, 5, 6])
	at_Dir2_3D.setDefault(6)
	
	#-doRayleigh
	at_doRayleigh = MpcAttributeMetaData()
	at_doRayleigh.type = MpcAttributeType.Boolean
	at_doRayleigh.name = 'doRayleigh'
	at_doRayleigh.group = 'Group'
	at_doRayleigh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('doRayleigh')+'<br/>') +
		html_par('optional, default = 0') +
		html_par('rFlag = 0 NO RAYLEIGH DAMPING (default)') +
		html_par('rFlag = 1 include rayleigh damping') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CoupledZeroLength_Element','CoupledZeroLength  Element')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'CoupledZeroLength'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	
	xom.addAttribute(at_3D)
	xom.addAttribute(at_ModelType)
	xom.addAttribute(at_D)
	xom.addAttribute(at_UR)
	
	xom.addAttribute(at_Dir1_2D)
	xom.addAttribute(at_Dir2_2D)
	
	xom.addAttribute(at_Dir1_2D_D)
	xom.addAttribute(at_Dir2_2D_D)
	
	xom.addAttribute(at_Dir1_3D)
	xom.addAttribute(at_Dir2_3D)
	
	xom.addAttribute(at_Dir1_3D_D)
	xom.addAttribute(at_Dir2_3D_D)
	
	xom.addAttribute(at_doRayleigh)
	
	# auto-exclusive dependencies
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_D)
	xom.setBooleanAutoExclusiveDependency(at_ModelType, at_UR)
	
	xom.setVisibilityDependency(at_2D, at_Dir1_2D_D)
	xom.setVisibilityDependency(at_2D, at_Dir2_2D_D)
	
	xom.setVisibilityDependency(at_D, at_Dir1_2D_D)
	xom.setVisibilityDependency(at_D, at_Dir2_2D_D)
	
	xom.setVisibilityDependency(at_2D, at_Dir1_2D)
	xom.setVisibilityDependency(at_2D, at_Dir2_2D)
	
	xom.setVisibilityDependency(at_UR, at_Dir1_2D)
	xom.setVisibilityDependency(at_UR, at_Dir2_2D)
	
	xom.setVisibilityDependency(at_3D, at_Dir1_3D_D)
	xom.setVisibilityDependency(at_3D, at_Dir2_3D_D)
	
	xom.setVisibilityDependency(at_D, at_Dir1_3D_D)
	xom.setVisibilityDependency(at_D, at_Dir2_3D_D)
	
	xom.setVisibilityDependency(at_3D, at_Dir1_3D)
	xom.setVisibilityDependency(at_3D, at_Dir2_3D)
	
	xom.setVisibilityDependency(at_UR, at_Dir1_3D)
	xom.setVisibilityDependency(at_UR, at_Dir2_3D)
	
	return xom

def __control(xobj):
	
	d = my_data()
	
	Dimension_at = xobj.getAttribute('Dimension')
	if(Dimension_at is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	d.Dimension = Dimension_at.string
	
	D_at = xobj.getAttribute('U (Displacement)')
	if(D_at is None):
		raise Exception('Error: cannot find "U (Displacement)" attribute')
	d.D = D_at.boolean
	
	
	if d.Dimension == '2D':
		d.ndm = 2
		if d.D:
			d.ndf = 2
		else:
			d.ndf = 3
	else:
		d.ndm = 3
		if d.D:
			d.ndf = 3
		else:
			d.ndf = 6
	
	return d

def getNodalSpatialDim(xobj, xobj_phys_prop):
	
	d = __control(xobj)
	
	return [(d.ndm,d.ndf),(d.ndm,d.ndf)]

def writeTcl(pinfo):
	# element CoupledZeroLength $eleTag $iNode $jNode $dirn1 $dirn2 $matTag <$rFlag>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	d = __control(xobj)
	matTag = phys_prop.id
	
	pinfo.updateModelBuilder(d.ndm, d.ndf)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=2):
		raise Exception('Error: invalid number of nodes')
	
	doRayleigh_at = xobj.getAttribute('doRayleigh')
	if(doRayleigh_at is None):
		raise Exception('Error: cannot find "doRayleigh" attribute')
	sopt = ''
	if doRayleigh_at.boolean:
		sopt += ' 1'
		
	dir1 = ''
	dir2 = ''
	if d.Dimension == '2D':
		if d.D :
			dir1_2D_at = xobj.getAttribute('Dir1/2D_D')
			if(dir1_2D_at is None):
				raise Exception('Error: cannot find "Dir1/2D_D" attribute')
			dir1  = dir1_2D_at.integer
			
			dir2_2D_at = xobj.getAttribute('Dir2/2D_D')
			if(dir2_2D_at is None):
				raise Exception('Error: cannot find "Dir2/2D_D" attribute')
			dir2  = dir2_2D_at.integer
			
		else:
			dir1_2D_at = xobj.getAttribute('Dir1/2D')
			if(dir1_2D_at is None):
				raise Exception('Error: cannot find "Dir1/2D" attribute')
			dir1  = dir1_2D_at.integer
			
			dir2_2D_at = xobj.getAttribute('Dir2/2D')
			if(dir2_2D_at is None):
				raise Exception('Error: cannot find "Dir2/2D" attribute')
			dir2  = dir2_2D_at.integer
			
	else:
		if d.D :
			dir1_3D_at = xobj.getAttribute('Dir1/3D_D')
			if(dir1_3D_at is None):
				raise Exception('Error: cannot find "Dir1/3D_D" attribute')
			dir1  = dir1_3D_at.integer
			
			dir2_3D_at = xobj.getAttribute('Dir2/3D_D')
			if(dir2_3D_at is None):
				raise Exception('Error: cannot find "Dir2/3D_D" attribute')
			dir2  = dir2_3D_at.integer
			
		else:
			dir1_3D_at = xobj.getAttribute('Dir1/3D')
			if(dir1_3D_at is None):
				raise Exception('Error: cannot find "Dir1/3D" attribute')
			dir1  = dir1_3D_at.integer
			
			dir2_3D_at = xobj.getAttribute('Dir2/3D')
			if(dir2_3D_at is None):
				raise Exception('Error: cannot find "Dir2/3D" attribute')
			dir2  = dir2_3D_at.integer
			
	
	str_tcl = '{}element CoupledZeroLength {}{} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, dir1, dir2, matTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
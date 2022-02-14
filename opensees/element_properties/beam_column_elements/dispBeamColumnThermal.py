import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.element_properties.utils.geomTransf as gtran

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
		html_par(html_href('http://openseesforfire.github.io/Subpages/commands.html','Displacement Beam Column Thermal')+'<br/>') +
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
		html_par('') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/commands.html','Displacement Beam Column Thermal')+'<br/>') +
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
		html_par(html_href('http://openseesforfire.github.io/Subpages/commands.html','Displacement Beam Column Thermal')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	# transType
	at_transType = gtran.makeAttribute('Group')
	
	# -mass
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.Boolean
	at_mass.name = '-mass'
	at_mass.group = 'Group'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-mass')+'<br/>') +
		html_par('element mass density (per unit length), from which a lumped-mass matrix is formed (optional, default = 0.0)') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/commands.html','Displacement Beam Column Thermal')+'<br/>') +
		html_end()
		)
	
	# massDens
	at_massDens = MpcAttributeMetaData()
	at_massDens.type = MpcAttributeType.QuantityScalar
	at_massDens.name = 'massDens'
	at_massDens.group = '-mass'
	at_massDens.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('massDens')+'<br/>') +
		html_par('element mass density (per unit length), from which a lumped-mass matrix is formed (optional, default = 0.0)') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/commands.html','Displacement Beam Column Thermal')+'<br/>') +
		html_end()
		)
	at_massDens.setDefault(0.0)
	# at_massDens.dimension = u.M/u.L**3
	
	
	 # <-iter numIter tol> 
	# -iter
	at_iter = MpcAttributeMetaData()
	at_iter.type = MpcAttributeType.Boolean
	at_iter.name = '-iter'
	at_iter.group = 'Group'
	at_iter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-iter')+'<br/>') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/commands.html','Displacement Beam Column Thermal')+'<br/>') +
		html_end()
		)
	
	# numIter
	at_numIter = MpcAttributeMetaData()
	at_numIter.type = MpcAttributeType.Integer
	at_numIter.name = 'numIter'
	at_numIter.group = '-iter'
	at_numIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('numIter')+'<br/>') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/commands.html','Displacement Beam Column Thermal')+'<br/>') +
		html_end()
		)
	at_numIter.setDefault(5)
	
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = '-iter'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/DispBeamColumnWithSensitivity','DispBeamColumnWithSensitivity')+'<br/>') +
		html_end()
		)
	at_tol.setDefault(1.0e-12)
	
	# -cMass
	at_cMass = MpcAttributeMetaData()
	at_cMass.type = MpcAttributeType.Boolean
	at_cMass.name = '-cMass'
	at_cMass.group = 'Group'
	at_cMass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-cMass')+'<br/>') +
		html_par('to form consistent mass matrix (optional, default = lumped mass matrix)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement-Based_Beam-Column_Element','Displacement-Based Beam-Column Element')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'dispBeamColumnThermal'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_transType)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_massDens)
	xom.addAttribute(at_iter)
	xom.addAttribute(at_numIter)
	xom.addAttribute(at_tol)
	xom.addAttribute(at_cMass)
	
	# visibility dependencies
	xom.setVisibilityDependency(at_mass, at_massDens)
	xom.setVisibilityDependency(at_iter, at_numIter)
	xom.setVisibilityDependency(at_iter, at_tol)
	
	# auto-exclusive dependencies
	#
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	Dimension2 = Dimension2_at.boolean

	if Dimension2:
		ndm = 2
		ndf = 3

	else:
		ndm = 3
		ndf = 6
	return [(ndm,ndf),(ndm,ndf)]

def writeTcl(pinfo):
	
	# element dispBeamColumnThermal $tag $iNode $jNode $numIntgrPts $secTag $transfTag <-mass $massDens>
	# element dispBeamColumnThermal $eleTag $iNode $jNode $numIntgrPts $secTag $transfTag <-iter numIter tol> <-mass $massDens> <-cMass> <-integration $intType>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	secTag = phys_prop.id
	
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# mandatory parameters
	str1 = ''
	
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	Dimension2 = Dimension2_at.boolean
	if Dimension2:
		ndm = 2
		ndf = 3
	
	else:
		ndm = 3
		ndf = 6
	
	# getSpatialDim
	pinfo.updateModelBuilder(ndm,ndf)
	
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
	
	# ***special_purpose***
	if phys_prop.XObject.name != 'BeamSectionProperty(old)':
		raise Exception('Wrong physical property type for "{}" element. Expected: "BeamSectionProperty(old)", given: "{}"'.format(ClassName, phys_prop.XObject.name))
	
	Constant_section_at = phys_prop.XObject.getAttribute('Constant section')
	if(Constant_section_at is None):
		raise Exception('Error: cannot find "Constant section" attribute')
	if Constant_section_at.boolean:
		numIntgrPts_at = phys_prop.XObject.getAttribute('numIntgrPts')
		if(numIntgrPts_at is None):
			raise Exception('Error: cannot find "numIntgrPts" attribute')
		numIntgrPts = numIntgrPts_at.integer
		
		secTag_at = phys_prop.XObject.getAttribute('secTag')
		if(secTag_at is None):
			raise Exception('Error: cannot find "secTag" attribute')
		secTag = secTag_at.index
	
	else:
		# Multiple section
		secTag_n_at = phys_prop.XObject.getAttribute('secTag/n')
		if(secTag_n_at is None):
			raise Exception('Error: cannot find "secTag/n" attribute')
		secTag_n = secTag_n_at.indexVector
		
		numIntgrPts = len(secTag_n)
		
		secTag = '-sections'		# section string
		for section in secTag_n:
			secTag += ' {}'.format(section)
	
	IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType')
	if(IntegrationType_at is None):
		raise Exception('Error: cannot find "IntegrationType" attribute')
	IntegrationType = IntegrationType_at.string
	
	
	# optional paramters
	sopt = ''
	
	iter_at = xobj.getAttribute('-iter')
	if(iter_at is None):
		raise Exception('Error: cannot find "-iter" attribute')
	if iter_at.boolean:
		numIter_at = xobj.getAttribute('numIter')
		if(numIter_at is None):
			raise Exception('Error: cannot find "numIter" attribute')
		numIter = numIter_at.integer
		
		tol_at = xobj.getAttribute('tol')
		if(tol_at is None):
			raise Exception('Error: cannot find "tol" attribute')
		tol = tol_at.real
		
		sopt += ' -iter {} {}'.format(numIter, tol)
	
	mass_at = xobj.getAttribute('-mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "-mass" attribute')
	mass = mass_at.boolean
	if mass:
		massDens_at = xobj.getAttribute('massDens')
		if(massDens_at is None):
			raise Exception('Error: cannot find "massDens" attribute')
		massDens = massDens_at.quantityScalar
		
		sopt += ' -mass {}'.format(massDens.value)
	
	cMass_at = xobj.getAttribute('-cMass')
	if(cMass_at is None):
		raise Exception('Error: cannot find "-cMass" attribute')
	if cMass_at.boolean:
		
		sopt += ' -cMass'
	
	integration_at = phys_prop.XObject.getAttribute('-integration')
	if(integration_at is None):
		raise Exception('Error: cannot find "-integration" attribute')
	if integration_at.boolean:
		IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType')
		if(IntegrationType_at is None):
			raise Exception('Error: cannot find "IntegrationType" attribute')
		IntegrationType = IntegrationType_at.string
		
		sopt += ' -integration {}'.format(IntegrationType)
	
	# geometric transformation command
	pinfo.out_file.write(gtran.writeGeomTransf(pinfo, (not Dimension2)))
	
	str_tcl = '{}element dispBeamColumnThermal {}{} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, numIntgrPts, secTag, tag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
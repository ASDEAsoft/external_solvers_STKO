import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# transType
	at_transType = MpcAttributeMetaData()
	at_transType.type = MpcAttributeType.String
	at_transType.name = 'transType'
	at_transType.group = 'Group'
	at_transType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('transType')+'<br/>') +
		html_par(' The geometric-transformation command is used to construct a coordinate-transformation ') +
		html_par('(CrdTransf) object, which transforms beam element stiffness and resisting force from the ') +
		html_par('basic system to the global-coordinate system.The command has at least one argument, the transformation type.') +
		html_end()
		)
	at_transType.sourceType = MpcAttributeSourceType.List
	at_transType.setSourceList(['Linear', 'PDelta', 'Corotational'])
	at_transType.setDefault('Linear')
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = 'Group'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tol')+'<br/>') +
		html_par('A tolerance on the axial force unbalance $tol in the sections MUST be specified;') +
		html_par('It represents the unbalance in axial force at each IP that is deemed acceptable.') +
		html_par('It depends on the analysis performed and on the employed units') +
		html_end()
		)
	at_tol.setDefault(1.0e-12)
	
	 # <-iter numIter maxIter> 
	# -iter
	at_iter = MpcAttributeMetaData()
	at_iter.type = MpcAttributeType.Boolean
	at_iter.name = '-iter'
	at_iter.group = 'Group'
	at_iter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-iter')+'<br/>') +
		html_end()
		)
	
	# maxIter
	at_maxIter = MpcAttributeMetaData()
	at_maxIter.type = MpcAttributeType.Real
	at_maxIter.name = 'maxIter'
	at_maxIter.group = 'Group'
	at_maxIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxIter')+'<br/>') +
		html_par('A max num of internal element iterations can be specified. Default value is : $maxIters=20') +
		html_end()
		)
	at_tol.setDefault(1.0e-12)
	
	xom = MpcXObjectMetaData()
	xom.name = 'AxEqDispBeamColumn2d'
	xom.addAttribute(at_transType)
	xom.addAttribute(at_tol)
	xom.addAttribute(at_iter)
	xom.addAttribute(at_maxIter)
	
	# visibility dependencies
	xom.setVisibilityDependency(at_iter, at_maxIter)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2, 3),(2, 3)]

def writeTcl(pinfo):
	
	# element AxEqDispBeamColumn2d  $eleTag $iNode $jNode $numIntgrPts $-$secTag $$transfTa? $tol <-integration $intType> <-iter $maxIters>
	
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
	
	str1 = ''
	pinfo.updateModelBuilder(2, 3)
	
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
	
	#Geometric transformation command
	transTipe_at = xobj.getAttribute('transType')
	if(transTipe_at is None):
		raise Exception('Error: cannot find "transType" attribute')
	transType = transTipe_at.string
	geomTransf = '# Geometric transformation command\n'
	geomTransf += 'geomTransf {} {}'.format(transType, tag)
	geomTransf += '\n'
	
	# optional paramters
	sopt = ''
	
	tol_at = xobj.getAttribute('tol')
	if(tol_at is None):
		raise Exception('Error: cannot find "tol" attribute')
	tol = tol_at.real
	
	integration_at = phys_prop.XObject.getAttribute('-integration')
	if(integration_at is None):
		raise Exception('Error: cannot find "-integration" attribute')
	if integration_at.boolean:
		IntegrationType_at = phys_prop.XObject.getAttribute('IntegrationType')
		if(IntegrationType_at is None):
			raise Exception('Error: cannot find "IntegrationType" attribute')
		IntegrationType = IntegrationType_at.string
		sopt += ' -integration {}'.format(IntegrationType)
	
	iter_at = xobj.getAttribute('-iter')
	if(iter_at is None):
		raise Exception('Error: cannot find "-iter" attribute')
	if iter_at.boolean:
		maxIter_at = xobj.getAttribute('maxIter')
		if(maxIter_at is None):
			raise Exception('Error: cannot find "maxIter" attribute')
		maxIter = maxIter_at.integer
		sopt += ' -iter {}'.format(maxIter)
	
	# now write the geomTransf into the file
	pinfo.out_file.write(geomTransf)
	
	str_tcl = '{}element AxEqDispBeamColumn2d {}{} {} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, numIntgrPts, secTag, tag, tol, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
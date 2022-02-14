import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# shape
	at_shape = MpcAttributeMetaData()
	at_shape.type = MpcAttributeType.String
	at_shape.name = 'shape'
	at_shape.group = '-shape'
	at_shape.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('shape')+'<br/>') +
		html_par('number of springs') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	at_shape.sourceType = MpcAttributeSourceType.List
	at_shape.setSourceList(['round', 'square'])
	at_shape.setDefault('round')
	
	# size
	at_size = MpcAttributeMetaData()
	at_size.type = MpcAttributeType.QuantityScalar
	at_size.name = 'size'
	at_size.group = '-size'
	at_size.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('size')+'<br/>') +
		html_par('diameter (round shape), length of edge (square shape)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	at_size.dimension = u.L
	
	# totalRubber
	at_totalRubber = MpcAttributeMetaData()
	at_totalRubber.type = MpcAttributeType.QuantityScalar
	at_totalRubber.name = 'totalRubber'
	at_totalRubber.group = 'Group'
	at_totalRubber.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('totalRubber')+'<br/>') +
		html_par('total rubber thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	at_totalRubber.dimension = u.L
	
	# -totalHeight
	at_use_totalHeight = MpcAttributeMetaData()
	at_use_totalHeight.type = MpcAttributeType.Boolean
	at_use_totalHeight.name = '-totalHeight'
	at_use_totalHeight.group = 'Optional parameters'
	at_use_totalHeight.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-totalHeight')+'<br/>') +
		html_par('total height of the bearing (defaulut: distance between iNode and jNode)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# totalHeight
	at_totalHeight = MpcAttributeMetaData()
	at_totalHeight.type = MpcAttributeType.QuantityScalar
	at_totalHeight.name = 'totalHeight'
	at_totalHeight.group = '-totalHeight'
	at_totalHeight.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('totalHeight')+'<br/>') +
		html_par('total height of the bearing (defaulut: distance between iNode and jNode)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	at_totalHeight.dimension = u.L
	
	# nMSS
	at_nMSS = MpcAttributeMetaData()
	at_nMSS.type = MpcAttributeType.Integer
	at_nMSS.name = 'nMSS'
	at_nMSS.group = '-nMSS'
	at_nMSS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nMSS')+'<br/>') +
		html_par('number of springs in MSS = nMSS') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# -limDisp
	at_use_limDisp = MpcAttributeMetaData()
	at_use_limDisp.type = MpcAttributeType.Boolean
	at_use_limDisp.name = '-limDisp'
	at_use_limDisp.group = 'Optional parameters'
	at_use_limDisp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-limDisp')+'<br/>') +
		html_par('minimum deformation to calculate equivalent coefficient of MSS (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# limDisp
	at_limDisp = MpcAttributeMetaData()
	at_limDisp.type = MpcAttributeType.Real
	at_limDisp.name = 'limDisp'
	at_limDisp.group = '-limDisp'
	at_limDisp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('limDisp')+'<br/>') +
		html_par('minimum deformation to calculate equivalent coefficient of MSS (see note 1)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# nMNS
	at_nMNS = MpcAttributeMetaData()
	at_nMNS.type = MpcAttributeType.Integer
	at_nMNS.name = 'nMNS'
	at_nMNS.group = '-nMNS'
	at_nMNS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nMNS')+'<br/>') +
		html_par('number of springs in MNS = nMNS*nMNS (for round and square shape)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# -lambda
	at_use_lambda = MpcAttributeMetaData()
	at_use_lambda.type = MpcAttributeType.Boolean
	at_use_lambda.name = '-lambda'
	at_use_lambda.group = 'Optional parameters'
	at_use_lambda.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-lambda')+'<br/>') +
		html_par('parameter to calculate compression modulus distribution on MNS (see note 2)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# lambda
	at_lambda = MpcAttributeMetaData()
	at_lambda.type = MpcAttributeType.Real
	at_lambda.name = 'lambda'
	at_lambda.group = '-lambda'
	at_lambda.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('lambda')+'<br/>') +
		html_par('parameter to calculate compression modulus distribution on MNS (see note 2)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# -orient
	at_orient = MpcAttributeMetaData()
	at_orient.type = MpcAttributeType.Boolean
	at_orient.name = '-orient'
	at_orient.group = 'Optional parameters'
	at_orient.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-orient')+'<br/>') +
		html_par('activate vector components in global coordinates') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# -mass
	at_mass = MpcAttributeMetaData()
	at_mass.type = MpcAttributeType.Boolean
	at_mass.name = '-mass'
	at_mass.group = 'Optional parameters'
	at_mass.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-mass')+'<br/>') +
		html_par('element mass') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.QuantityScalar
	at_m.name = 'm'
	at_m.group = '-mass'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') +
		html_par('element mass') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	# at_m.dimension = u.M
	
	# -noPDInput
	at_noPDInput = MpcAttributeMetaData()
	at_noPDInput.type = MpcAttributeType.Boolean
	at_noPDInput.name = '-noPDInput'
	at_noPDInput.group = 'Optional parameters'
	at_noPDInput.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-noPDInput')+'<br/>') +
		html_par('not consider P-Delta moment') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# -noTilt
	at_noTilt = MpcAttributeMetaData()
	at_noTilt.type = MpcAttributeType.Boolean
	at_noTilt.name = '-noTilt'
	at_noTilt.group = 'Optional parameters'
	at_noTilt.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-noTilt')+'<br/>') +
		html_par('not consider tilt of rigid link') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# -adjustPDOutput
	at_adjustPDOutput = MpcAttributeMetaData()
	at_adjustPDOutput.type = MpcAttributeType.Boolean
	at_adjustPDOutput.name = '-adjustPDOutput'
	at_adjustPDOutput.group = 'Optional parameters'
	at_adjustPDOutput.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-adjustPDOutput')+'<br/>') +
		html_par('P-Delta moment adjustment for reaction force (default: ci=0.5, cj=0.5)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# ci
	at_ci = MpcAttributeMetaData()
	at_ci.type = MpcAttributeType.Real
	at_ci.name = 'ci'
	at_ci.group = '-adjustPDOutput'
	at_ci.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ci')+'<br/>') +
		html_par('P-Delta moment adjustment for reaction force (default: ci=0.5)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	at_ci.setDefault(0.5)
	
	# cj
	at_cj = MpcAttributeMetaData()
	at_cj.type = MpcAttributeType.Real
	at_cj.name = 'cj'
	at_cj.group = '-adjustPDOutput'
	at_cj.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cj')+'<br/>') +
		html_par('P-Delta moment adjustment for reaction force (default: cj=0.5)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	at_cj.setDefault(0.5)
	
	# -doBalance
	at_doBalance = MpcAttributeMetaData()
	at_doBalance.type = MpcAttributeType.Boolean
	at_doBalance.name = '-doBalance'
	at_doBalance.group = 'Optional parameters'
	at_doBalance.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-doBalance')+'<br/>') +
		html_par('to activate limFo, limFi and nIter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# limFo
	at_limFo = MpcAttributeMetaData()
	at_limFo.type = MpcAttributeType.Real
	at_limFo.name = 'limFo'
	at_limFo.group = '-doBalance'
	at_limFo.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('limFo')+'<br/>') +
		html_par('tolerance of external unbalanced force') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# limFi
	at_limFi = MpcAttributeMetaData()
	at_limFi.type = MpcAttributeType.Real
	at_limFi.name = 'limFi'
	at_limFi.group = '-doBalance'
	at_limFi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('limFi')+'<br/>') +
		html_par('tolorance of internal unbalanced force') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	# nIter
	at_nIter = MpcAttributeMetaData()
	at_nIter.type = MpcAttributeType.Integer
	at_nIter.name = 'nIter'
	at_nIter.group = '-doBalance'
	at_nIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nIter')+'<br/>') +
		html_par('number of iterations to get rid of internal unbalanced force') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/KikuchiBearing_Element','KikuchiBearing Element')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'KikuchiBearing'
	xom.addAttribute(at_shape)
	xom.addAttribute(at_size)
	xom.addAttribute(at_totalRubber)
	xom.addAttribute(at_use_totalHeight)
	xom.addAttribute(at_totalHeight)
	xom.addAttribute(at_nMSS)
	xom.addAttribute(at_use_limDisp)
	xom.addAttribute(at_limDisp)
	xom.addAttribute(at_nMNS)
	xom.addAttribute(at_use_lambda)
	xom.addAttribute(at_lambda)
	xom.addAttribute(at_orient)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_m)
	xom.addAttribute(at_noPDInput)
	xom.addAttribute(at_noTilt)
	xom.addAttribute(at_adjustPDOutput)
	xom.addAttribute(at_ci)
	xom.addAttribute(at_cj)
	xom.addAttribute(at_doBalance)
	xom.addAttribute(at_limFo)
	xom.addAttribute(at_limFi)
	xom.addAttribute(at_nIter)
	
	
	# visibility dependencies
	
	# totalHeight-dep
	xom.setVisibilityDependency(at_use_totalHeight, at_totalHeight)
	
	# limDisp-dep
	xom.setVisibilityDependency(at_use_limDisp, at_limDisp)
	
	# lambda-dep
	xom.setVisibilityDependency(at_use_lambda, at_lambda)
	
	# m-dep
	xom.setVisibilityDependency(at_mass, at_m)
	
	# ci, cj-dep
	xom.setVisibilityDependency(at_adjustPDOutput, at_ci)
	xom.setVisibilityDependency(at_adjustPDOutput, at_cj)
	
	# limFo, limFi, nIter-dep
	xom.setVisibilityDependency(at_doBalance, at_limFo)
	xom.setVisibilityDependency(at_doBalance, at_limFi)
	xom.setVisibilityDependency(at_doBalance, at_nIter)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)]	#(ndm,ndf)

def writeTcl(pinfo):
	
	# element KikuchiBearing $eleTag $iNode $jNode -shape $shape -size $size $totalRubber <-totalHeight $totalHeight>
	# -nMSS $nMSS -matMSS $matMSSTag <-limDisp $limDisp> -nMNS $nMNS -matMNS $matMNSTag <-lambda $lambda>
	# <-orient <$x1 $x2 $x3> $yp1 $yp2 $yp3> <-mass $m> <-noPDInput> <-noTilt> <-adjustPDOutput $ci $cj> <-doBalance $limFo $limFi $nIter>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	pinfo.updateModelBuilder(3,6)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# ***special_purpose***
	if phys_prop.XObject.name != 'KikuchiBearingMaterial':
		raise Exception('Wrong material type for KikuchiBearing element. Expected: KikuchiBearingMaterial, given: {}'.format(phys_prop.XObject.name))
	
	matMSSTag_at = phys_prop.XObject.getAttribute('matMSSTag')
	if(matMSSTag_at is None):
		raise Exception('Error: cannot find "matMSSTag" attribute')
	matMSSTag = matMSSTag_at.index
	
	matMNSTag_at = phys_prop.XObject.getAttribute('matMNSTag')
	if(matMNSTag_at is None):
		raise Exception('Error: cannot find "matMNSTag" attribute')
	matMNSTag = matMNSTag_at.index
	#***end special_purpose***
	
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=2):
		raise Exception('Error: invalid number of nodes')
	
	
	# mandatory parameters
	shape_at = xobj.getAttribute('shape')
	if(shape_at is None):
		raise Exception('Error: cannot find "shape" attribute')
	shape = shape_at.string
	
	size_at = xobj.getAttribute('size')
	if(size_at is None):
		raise Exception('Error: cannot find "size" attribute')
	size = size_at.quantityScalar.value
	
	totalRubber_at = xobj.getAttribute('totalRubber')
	if(totalRubber_at is None):
		raise Exception('Error: cannot find "totalRubber" attribute')
	totalRubber = totalRubber_at.quantityScalar.value
	
	
	# optional paramters 1
	sopt = ''
	use_totalHeight_at = xobj.getAttribute('-totalHeight')
	if(use_totalHeight_at is None):
		raise Exception('Error: cannot find "use_totalHeight" attribute')
	if use_totalHeight_at.boolean:
		
		totalHeight_at = xobj.getAttribute('totalHeight')
		if(totalHeight_at is None):
			raise Exception('Error: cannot find "totalHeight" attribute')
		totalHeight = totalHeight_at.quantityScalar
		
		sopt = ' -totalHeight {}'.format(totalHeight.value)
	
	
	nMSS_at = xobj.getAttribute('nMSS')
	if(nMSS_at is None):
		raise Exception('Error: cannot find "nMSS" attribute')
	nMSS = nMSS_at.integer
	
	
	# optional paramters 2
	sopt2 = ''
	use_limDisp_at = xobj.getAttribute('-limDisp')
	if(use_limDisp_at is None):
		raise Exception('Error: cannot find "use_limDisp" attribute')
	if use_limDisp_at.boolean:
		
		limDisp_at = xobj.getAttribute('limDisp')
		if(limDisp_at is None):
			raise Exception('Error: cannot find "limDisp" attribute')
		limDisp = limDisp_at.real
		
		sopt2 = ' -limDisp {}'.format(limDisp)
	
	nMNS_at = xobj.getAttribute('nMNS')
	if(nMNS_at is None):
		raise Exception('Error: cannot find "nMNS" attribute')
	nMNS = nMNS_at.integer
	
	
	# optional paramters 2
	sopt3 = ''
	use_lambda_at = xobj.getAttribute('-lambda')
	if(use_lambda_at is None):
		raise Exception('Error: cannot find "-lambda" attribute')
	if use_lambda_at.boolean:
		
		lambda_at = xobj.getAttribute('lambda')
		if(lambda_at is None):
			raise Exception('Error: cannot find "lambda" attribute')
		lambd = lambda_at.real
		
		sopt3 += '-lambda {}'.format(lambd)
	
	orient_at = xobj.getAttribute('-orient')
	if(orient_at is None):
		raise Exception('Error: cannot find "-orient" attribute')
	if orient_at.boolean:
		vect_x=elem.orientation.computeOrientation().col(0)
		vect_y=elem.orientation.computeOrientation().col(1)
		
		sopt3 += ' -orient {} {} {} {} {} {}'.format (vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
	
	
	mass_at = xobj.getAttribute('-mass')
	if(mass_at is None):
		raise Exception('Error: cannot find "-mass" attribute')
	if mass_at.boolean:
		
		m_at = xobj.getAttribute('m')
		if(m_at is None):
			raise Exception('Error: cannot find "m" attribute')
		m = m_at.quantityScalar
		
		sopt3 += ' -mass {}'.format(m.value)
	
	noPDInput_at = xobj.getAttribute('-noPDInput')
	if(noPDInput_at is None):
		raise Exception('Error: cannot find "-noPDInput" attribute')
	if noPDInput_at.boolean:
		
		sopt3 += ' -noPDInput'
	
	noTilt_at = xobj.getAttribute('-noTilt')
	if(noTilt_at is None):
		raise Exception('Error: cannot find "-noTilt" attribute')
	if noTilt_at.boolean:
		
		sopt3 += ' -noTilt'
	
	adjustPDOutput_at = xobj.getAttribute('-adjustPDOutput')
	if(adjustPDOutput_at is None):
		raise Exception('Error: cannot find "-adjustPDOutput" attribute')
	if adjustPDOutput_at.boolean:
		
		ci_at = xobj.getAttribute('ci')
		if(ci_at is None):
			raise Exception('Error: cannot find "ci" attribute')
		ci = ci_at.real
		
		cj_at = xobj.getAttribute('cj')
		if(cj_at is None):
			raise Exception('Error: cannot find "cj" attribute')
		cj = cj_at.real
		
		sopt3 += ' -adjustPDOutput {} {}'.format(ci, cj)
	
	doBalance_at = xobj.getAttribute('-doBalance')
	if(doBalance_at is None):
		raise Exception('Error: cannot find "-doBalance" attribute')
	if doBalance_at.boolean:
		
		limFo_at = xobj.getAttribute('limFo')
		if(limFo_at is None):
			raise Exception('Error: cannot find "limFo" attribute')
		limFo = limFo_at.real
		
		limFi_at = xobj.getAttribute('limFi')
		if(limFi_at is None):
			raise Exception('Error: cannot find "limFi" attribute')
		limFi = limFi_at.real
		
		nIter_at = xobj.getAttribute('nIter')
		if(nIter_at is None):
			raise Exception('Error: cannot find "nIter" attribute')
		nIter = nIter_at.integer
		
		sopt3 += ' -doBalance {} {} {}'.format(limFo, limFi, nIter)
	
	str_tcl = '{}element KikuchiBearing {}{} -shape {} -size {} {}{} -nMSS {} -matMSS {}{} -nMNS {} -matMNS {} {}\n'.format(
	pinfo.indent, tag, nstr, shape, size, totalRubber, sopt, nMSS, matMSSTag, sopt2, nMNS, matMNSTag, sopt3)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
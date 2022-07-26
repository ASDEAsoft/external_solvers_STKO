import PyMpc.IO
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.element_properties.utils.geomTransf as gtran

class my_data:
	def __init__(self):
		# attributes will be set in the __control method
		pass

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

	# Dimension
	at_Dimension = mka('Dimension', MpcAttributeType.String, 'Group', 'choose between 2D and 3D')
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('3D')

	# 2D
	at_2D = mka('2D', MpcAttributeType.Boolean, 'Group', '')
	at_2D.editable = False

	# 3D
	at_3D = mka('3D', MpcAttributeType.Boolean, 'Group', '')
	at_3D.editable = False
	
	# lambda1
	at_lambda1 = mka('lambda1', MpcAttributeType.QuantityScalar, 'Group', 'fraction of beam length (L) at near end represented by $endSecTag1')
	
	# lambda2
	at_lambda2 = mka('lambda2', MpcAttributeType.QuantityScalar, 'Group', 'fraction of beam length (L) at far end represented by $endSecTag2. Note that $lambda1 + $lambda2 should be smaller than unity')

	# transType
	at_transfType = gtran.makeAttribute('Group', name = 'transfType')

	# -iter
	at_iter = mka('-iter', MpcAttributeType.Boolean, 'Optional', 'to set iterative solution algorithm parameters')
	
	# maxIter
	at_maxIter = mka('maxIter', MpcAttributeType.Integer, 'Optional', 'maximum number of iterations (default: 50)')
	at_maxIter.setDefault(50)
	
	# minTol
	at_minTol = mka('minTol', MpcAttributeType.QuantityScalar, 'Optional', 'minimum tolerance (default: 1E-10)')
	at_minTol.setDefault(1e-10)

	# maxTol
	at_maxTol = mka('maxTol', MpcAttributeType.QuantityScalar, 'Optional', 'maximum tolerance (default: 1E-8)')
	at_maxTol.setDefault(1e-8)


	xom = MpcXObjectMetaData()
	xom.name = 'gradientInelasticBeamColumn'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_lambda1)
	xom.addAttribute(at_lambda2)
	xom.addAttribute(at_transfType)
	xom.addAttribute(at_iter)
	xom.addAttribute(at_maxIter)
	xom.addAttribute(at_minTol)
	xom.addAttribute(at_maxTol)
	xom.setVisibilityDependency(at_iter, at_maxIter)
	xom.setVisibilityDependency(at_iter, at_minTol)
	xom.setVisibilityDependency(at_iter, at_maxTol)

	# auto-exclusive dependencies
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	return xom

def __control(xobj):
	d = my_data()
	
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	d.Dimension2 = Dimension2_at.boolean
	
	Dimension3_at = xobj.getAttribute('3D')
	if(Dimension3_at is None):
		raise Exception('Error: cannot find "3D" attribute')
	d.Dimension3 = Dimension3_at.boolean
	
	return d

def getNodalSpatialDim(xobj, xobj_phys_prop):
	d = __control(xobj)
	
	if d.Dimension2:
		ndm = 2
		ndf = 3
	
	else:
		ndm = 3
		ndf = 6

	return [(ndm,ndf),(ndm,ndf)]


def writeTcl(pinfo):
	# TODO: add check in $numIntgrPts: if Simpson's rule is used (in $integrType), $numIntgrPts should be an odd number

	import opensees.element_properties.shell.shell_utils as shelu
	
	# element gradientInelasticBeamColumn $eleTag $iNode $jNode $numIntgrPts $endSecTag1 $intSecTag $endSecTag2 $lambda1 $lambda2 $lc $transfTag
	#										<-integration integrType> <-iter $maxIter $minTol $maxTol>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	def geta(name):
		at = xobj.getAttribute(name)
		if(at is None):
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	d = __control(xobj)

	# check compatibility between element and material
	if phys_prop.XObject.name != 'gradientInelasticProperty':
		raise Exception('Error: wrong physical property ({}) assigned to "gradientInelasticBeamColumn" element. Use "gradientInelasticProperty"'.format(phys_prop.XObject.name))
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Line or len(node_vect)!=2):
		raise Exception('Error: invalid type of element or number of nodes')
	
	# mandatory parameters
	numIntgrPts = phys_prop.XObject.getAttribute('numIntgrPts').integer
	endSecTag1 = phys_prop.XObject.getAttribute('endSecTag1').index
	intSecTag = phys_prop.XObject.getAttribute('intSecTag').index
	endSecTag2 = phys_prop.XObject.getAttribute('endSecTag2').index
	
	lambda1 = geta('lambda1').quantityScalar.value
	lambda2 = geta('lambda2').quantityScalar.value
	if (lambda1 + lambda2) > 1:
		PyMpc.IO.write_cerr('Warning: $lambda1 + $lambda2 should be smaller than unity\n')

	lc = phys_prop.XObject.getAttribute('lc').quantityScalar.value

	# optional parameters
	sopt = ''
	
	#if geta('-integration').boolean:
	if phys_prop.XObject.getAttribute('-integration').boolean:
		#sopt += ' -integration {}'.format(geta('integrType').string)
		sopt += ' -integration {}'.format(phys_prop.XObject.getAttribute('integrType').string)
	
	if geta('-iter').boolean:
		sopt += ' -iter {} {} {}'.format(geta('maxIter').integer, geta('minTol').quantityScalar.value, geta('maxTol').quantityScalar.value)

	# geometric transformation command
	pinfo.out_file.write(gtran.writeGeomTransf(pinfo, (not d.Dimension2), name = 'transfType'))

	# element gradientInelasticBeamColumn $eleTag $iNode $jNode $numIntgrPts $endSecTag1 $intSecTag $endSecTag2 $lambda1 $lambda2 $lc $transfTag <-integration integrType> <-iter $maxIter $minTol $maxTol>
	str_tcl = '{}element gradientInelasticBeamColumn {}{} {} {} {} {} {} {} {} {}{}\n'.format(pinfo.indent, tag, nstr, numIntgrPts, endSecTag1, intSecTag, endSecTag2, lambda1, lambda2, lc, tag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)

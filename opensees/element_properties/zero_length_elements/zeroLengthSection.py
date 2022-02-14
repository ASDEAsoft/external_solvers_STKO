import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Dimension
	at_Dimension = MpcAttributeMetaData()
	at_Dimension.type = MpcAttributeType.String
	at_Dimension.name = 'Dimension'
	at_Dimension.group = 'Group'
	at_Dimension.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthSection_Element','ZeroLengthSection Element')+'<br/>') +
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
		html_par('Dx Constraint') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthSection_Element','ZeroLengthSection Element')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthSection_Element','ZeroLengthSection Element')+'<br/>') +
		html_end()
		)
	at_3D.editable = False
	
	#-doRayleigh
	at_doRayleigh = MpcAttributeMetaData()
	at_doRayleigh.type = MpcAttributeType.Boolean
	at_doRayleigh.name = '-doRayleigh'
	at_doRayleigh.group = 'Group'
	at_doRayleigh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-doRayleigh')+'<br/>') +
		html_par('optional, default = 0') +
		html_par('rFlag = 0 NO RAYLEIGH DAMPING (default)') +
		html_par('rFlag = 1 include rayleigh damping') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthSection_Element','ZeroLengthSection Element')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'zeroLengthSection'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_doRayleigh)
	
	# visibility dependencies
	
	# 2D or 3D
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
	
	# element zeroLengthSection $Tag $iNode $jNode $secTag <-orient $x1 $x2 $x3 $yp1 $yp2 $yp3> <-doRayleigh $rFlag>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	secTag = phys_prop.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	Dimension2_at = xobj.getAttribute('2D')
	if(Dimension2_at is None):
		raise Exception('Error: cannot find "2D" attribute')
	if Dimension2_at.boolean:
		ndm = 2
		ndf = 3
	else:
		ndm = 3
		ndf = 6
	
	pinfo.updateModelBuilder(ndm, ndf)
	
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
		raise Exception('Error: number of nodes')
	
	vect_x=elem.orientation.computeOrientation().col(0)
	vect_y=elem.orientation.computeOrientation().col(1)
	
	
	# optional paramters
	sopt = ''
	
	doRayleigh_at = xobj.getAttribute('-doRayleigh')
	if(doRayleigh_at is None):
		raise Exception('Error: cannot find "-doRayleigh" attribute')
	doRayleigh = doRayleigh_at.boolean
	if doRayleigh:
		
		sopt += ' -doRayleigh 1'
	
	str_tcl = '{}element zeroLengthSection {}{} {} -orient {} {} {} {} {} {}{}\n'.format(
			pinfo.indent, tag, nstr, secTag, vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
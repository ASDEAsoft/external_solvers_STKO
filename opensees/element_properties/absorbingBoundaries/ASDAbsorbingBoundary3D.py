import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import importlib
import opensees.utils.tcl_input as tclin
import math
import os

def makeXObjectMetaData():
	
	dp = 'file:///{}/ASDAbsorbingBoundaryElement.pdf'.format(os.path.dirname(os.path.realpath(__file__)))
	def mka(name, type, description, group, dimension = None, default = None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(description) +
			html_par(html_href(dp,'ASDAbsorbingBoundary3D')+'<br/>') +
			html_end()
			)
		if dimension:
			a.dimension = dimension
		if default:
			a.setDefault(default)
		return a
	
	boundary = mka('boundary', MpcAttributeType.String, 'The boundary type', 'Default', default = 'Bottom')
	boundary.sourceType = MpcAttributeSourceType.List
	boundary.setSourceList([
		'Bottom', 'Left', 'Right', 'Front', 'Back',
		'Bottom-Left', 'Bottom-Right', 'Bottom-Front', 'Bottom-Back',
		'Left-Front', 'Right-Front', 'Left-Back', 'Right-Back',
		'Bottom-Left-Front', 'Bottom-Right-Front', 'Bottom-Left-Back', 'Bottom-Right-Back'
		])
	
	fx = mka('Base Action X', MpcAttributeType.Index,
		('The time series used as velocity input at the bottom boundary along the X direction.\n'
		'It will be automatically multipled by:\n'
		'1) The Vs wave velocity\n'
		'2) 2, to compensate the half portion absorbed by the dashpots'),
		'Input', default = 0)
	fy = mka('Base Action Y', MpcAttributeType.Index,
		('The time series used as velocity input at the bottom boundary along the Y direction.\n'
		'It will be automatically multipled by:\n'
		'1) The Vs wave velocity\n'
		'2) 2, to compensate the half portion absorbed by the dashpots'),
		'Input', default = 0)
	fz = mka('Base Action Z', MpcAttributeType.Index,
		('The time series used as velocity input at the bottom boundary along the Z direction.\n'
		'It will be automatically multipled by:\n'
		'1) The Vp wave velocity\n'
		'2) 2, to compensate the half portion absorbed by the dashpots'),
		'Input', default = 0)
	fx.indexSource.type = MpcAttributeIndexSourceType.Definition
	fx.indexSource.addAllowedNamespace('timeSeries')
	fy.indexSource.type = MpcAttributeIndexSourceType.Definition
	fy.indexSource.addAllowedNamespace('timeSeries')
	fz.indexSource.type = MpcAttributeIndexSourceType.Definition
	fz.indexSource.addAllowedNamespace('timeSeries')
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDAbsorbingBoundary3D'
	xom.addAttribute(boundary)
	xom.addAttribute(fx)
	xom.addAttribute(fy)
	xom.addAttribute(fz)
	
	return xom

def _geta(xobj, name):
	at = xobj.getAttribute(name)
	if(at is None):
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	return at

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,[3,4,6]),(3,[3,4,6]),(3,[3,4,6]),(3,[3,4,6]),(3,[3,4,6]),(3,[3,4,6]),(3,[3,4,6]),(3,[3,4,6])]	#(ndm, ndf)

def _updateVisibility(xobj):
	vis = 'Bottom' in _geta(xobj, 'boundary').string
	_geta(xobj, 'Base Action X').visible = vis
	_geta(xobj, 'Base Action Y').visible = vis
	_geta(xobj, 'Base Action Z').visible = vis

def onEditBegin(editor, xobj):
	_updateVisibility(xobj)

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name == 'boundary':
		_updateVisibility(xobj)

class __utility:
	btype = {
		'Bottom'              : 'B'  ,
		'Left'                : 'L'  ,
		'Right'               : 'R'  ,
		'Front'               : 'F'  ,
		'Back'                : 'K'  ,
		'Bottom-Left'         : 'BL' ,
		'Bottom-Right'        : 'BR' ,
		'Bottom-Front'        : 'BF' ,
		'Bottom-Back'         : 'BK' ,
		'Left-Front'          : 'LF' ,
		'Right-Front'         : 'RF' ,
		'Left-Back'           : 'LK' ,
		'Right-Back'          : 'RK' ,
		'Bottom-Left-Front'   : 'BLF',
		'Bottom-Right-Front'  : 'BRF',
		'Bottom-Left-Back'    : 'BLK',
		'Bottom-Right-Back'   : 'BRK'
	}

def writeTcl(pinfo):
	
	# element ASDAbsorbingBoundary3D $Tag  $n1 $n2 $n3 $n4 $n5 $n6 $n7 $n8 $G $rho $btype <-fx $fx> <-fy $fy> <-fz $fz>
	
	# standardized error
	def err(msg):
		return 'Error in "ASDAbsorbingBoundary3D" :\n{}'.format(msg)
	
	elem = pinfo.elem
	elem_prop = pinfo.elem_prop
	mat_prop = pinfo.phys_prop
	if mat_prop is None:
		raise Exception(err('Physical Property of type ASDAbsorbingBoundary3DMaterial must be provided'))
	
	tag = elem.id
	xobj = elem_prop.XObject
	xobjm = mat_prop.XObject
	if xobjm.name != 'ASDAbsorbingBoundary3DMaterial':
		raise Exception(err('Physical Property of type ASDAbsorbingBoundary3DMaterial must be provided'))
	
	# info
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# get parameters
	G = _geta(xobjm, 'G').quantityScalar.value
	v = _geta(xobjm, 'v').real
	rho = _geta(xobjm, 'rho').quantityScalar.value
	btype = __utility.btype[_geta(xobj, 'boundary').string]
	opt = ''
	if 'B' in btype:
		fx = _geta(xobj, 'Base Action X').index
		fy = _geta(xobj, 'Base Action Y').index
		fz = _geta(xobj, 'Base Action Z').index
		if fx != 0:
			opt += ' -fx {}'.format(fx)
		if fy != 0:
			opt += ' -fy {}'.format(fy)
		if fz != 0:
			opt += ' -fz {}'.format(fz)
	nlmat_tag = _geta(xobjm, 'material').index # optional, it can be 0
	if nlmat_tag > 0:
		opt += ' -mat {}'.format(nlmat_tag)
	
	# check element type
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Hexahedron or len(elem.nodes)!=8:
		raise Exception(err('invalid type of element or number of nodes, It should be a Hexahedron with 8 nodes, not a {} with {} nodes'
			.format(elem.geometryFamilyType(), len(elem.nodes))))
	
	# get connectivity
	N1 = [elem.nodes[i].id for i in range(8)]
	
	# now write the string into the file
	pinfo.out_file.write(
		'{}element ASDAbsorbingBoundary3D {}   {} {} {} {} {} {} {} {}   {} {} {} {}{}\n'.format(pinfo.indent, tag, *N1, G, v, rho, btype, opt)
		)
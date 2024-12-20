import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import PyMpc
import PyMpc.App

def makeXObjectMetaData():
	
	def mka(type, name, group, descr, default = None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(descr) +
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/FSIFluidBoundaryElement2D.html','FSIFluidBoundaryElement2D')+'<br/>') +
			html_end()
			)
		if default:
			a.setDefault(default)
		return a
	
	# create all atributes
	boundary = mka(MpcAttributeType.String, 'boundary', 'Default', 'The boundary type', default = 'Radiation Side')
	boundary.sourceType = MpcAttributeSourceType.List
	boundary.setSourceList(['Radiation Side', 'Reservoir Bottom', 'Free Surface'])

	cc = mka(MpcAttributeType.Real, 'cc', 'Default', 'speed of pressure waves in water')
	alpha = mka(MpcAttributeType.Real, 'alpha', 'Default', 'reservoir bottom reflection coefficient')
	g = mka(MpcAttributeType.Real, 'g', 'Default', 'acceleration due to gravity')
	thickness = mka(MpcAttributeType.Real, 'thickness', 'Default', 'element thickness')
	thickness.setDefault(1.0)
	
	# metadata
	xom = MpcXObjectMetaData()
	xom.name = 'FSIFluidBoundaryElement2D'
	xom.addAttribute(boundary)
	xom.addAttribute(cc)
	xom.addAttribute(alpha)
	xom.addAttribute(g)
	xom.addAttribute(thickness)
	
	return xom

def _geta(xobj, name):
	at = xobj.getAttribute(name)
	if(at is None):
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	return at

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,1),(2,1)]	#[(ndm, ndf)...]

def _updateVisibility(xobj): 
	boundary = _geta(xobj, 'boundary').string

	# cc is visible for 'Radiation Side' and 'Reservoir Bottom'
	cc_visible = boundary in ['Radiation Side', 'Reservoir Bottom']
	_geta(xobj, 'cc').visible = cc_visible

	# alpha is visible only for 'Reservoir Bottom'
	alpha_visible = boundary == 'Reservoir Bottom'
	_geta(xobj, 'alpha').visible = alpha_visible

	# g is visible only for 'Free Surface'
	g_visible = boundary == 'Free Surface'
	_geta(xobj, 'g').visible = g_visible

	# thickness is always visible
	_geta(xobj, 'thickness').visible = True

def onEditBegin(editor, xobj):
	_updateVisibility(xobj)

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name == 'boundary':
		_updateVisibility(xobj)

def writeTcl(pinfo):
	
	# get the mesh element and check it
	elem = pinfo.elem
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Line) or (len(elem.nodes) !=2):
		raise Exception('Error: invalid type of element or number of nodes. It should be a line element')

	# get the xobj
	elem_prop = pinfo.elem_prop
	xobj = elem_prop.XObject
	
	# get all attributes
	boundary = _geta(xobj, 'boundary').string
	cc = xobj.getAttribute('cc').real
	alpha = xobj.getAttribute('alpha').real
	g = xobj.getAttribute('g').real
	thickness = xobj.getAttribute('thickness').real

	# write a comment with the name of this element only once
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName

	# generate Tcl command based on boundary type
	if boundary == 'Radiation Side':
		if cc <= 0.0:
			raise Exception('Error in FSIFluidBoundaryElement2D: cc must be strictly positive')
		pinfo.out_file.write('{}element FSIFluidBoundaryElement2D {} {} {} {} 0.0 0.0 -thickness {}\n'.format(
			pinfo.indent, elem.id, *[node.id for node in elem.nodes], cc, thickness))
	elif boundary == 'Reservoir Bottom':
		if cc <= 0.0:
			raise Exception('Error in FSIFluidBoundaryElement2D: cc must be strictly positive')
		if not (0.0 <= alpha <= 1.0):
			raise Exception('Error in FSIFluidBoundaryElement2D: alpha must take values between 0 and 1')
		pinfo.out_file.write('{}element FSIFluidBoundaryElement2D {} {} {} {} {} 0.0 -thickness {}\n'.format(
			pinfo.indent, elem.id, *[node.id for node in elem.nodes], cc, alpha, thickness))
	elif boundary == 'Free Surface':
		if g <= 0.0:
			raise Exception('Error in FSIFluidBoundaryElement2D: g must be strictly positive')
		pinfo.out_file.write('{}element FSIFluidBoundaryElement2D {} {} {} 0.0 0.0 {} -thickness {}\n'.format(
			pinfo.indent, elem.id, *[node.id for node in elem.nodes], g, thickness))
	else:
		# Raise an error if the boundary type is not recognized
		raise Exception('Error in FSIFluidBoundaryElement2D: unrecognized boundary type "{}".'.format(boundary))

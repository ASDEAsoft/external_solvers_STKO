import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import PyMpc
import PyMpc.App

def makeXObjectMetaData():
	
	def mka(type, name, group, descr):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(descr) +
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/FSIFluidElement2D.html','FSIFluidElement2D')+'<br/>') +
			html_end()
			)
		return a
	
	# -thickness $thickess
	
	# create all attributes
	cc = mka(MpcAttributeType.Real, 'cc', 'Default', 'speed of pressure waves in water')
	thickness = mka(MpcAttributeType.Real, 'thickness', 'Default', 'element thickness')
	thickness.setDefault(1.0)
	
	# metadata
	xom = MpcXObjectMetaData()
	xom.name = 'FSIFluidElement2D'
	xom.addAttribute(cc)
	xom.addAttribute(thickness)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,1),(2,1),(2,1),(2,1)]

def writeTcl(pinfo):
	
	# get the mesh element and check it
	elem = pinfo.elem
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Quadrilateral) or (len(elem.nodes) != 4):
		raise Exception('Error in FSIFluidElement2D: invalid type of element or number of nodes. It should be a linear quadrilateral element')
	
	# get the xobj
	elem_prop = pinfo.elem_prop
	xobj = elem_prop.XObject
	
	# get all attributes
	cc = xobj.getAttribute('cc').real
	thickness = xobj.getAttribute('thickness').real
	if cc <= 0.0:
		raise Exception('Error in FSIFluidElement2D: cc must be strictly positive')
	# todo: do all checks
	
	# write a comment with the name of this element only once
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# write the tcl command
	pinfo.out_file.write('{}element FSIFluidElement2D {} {} {} {} {} {} -thickess {}\n'.format(
		pinfo.indent, elem.id, *[node.id for node in elem.nodes], cc, thickness))
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
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/FSIInterfaceElement2D.html','FSIInterfaceElement2D')+'<br/>') +
			html_end()
			)
		return a
	
	# create all atributes
	rho = mka(MpcAttributeType.Real, 'rho', 'Default', 'the mass density of the fluid domain (acoustic medium)')
	thickness = mka(MpcAttributeType.Real, 'thickness', 'Default', 'element thickness')
	thickness.setDefault(1.0)
	
	# metadata
	xom = MpcXObjectMetaData()
	xom.name = 'FSIInterfaceElement2D'
	xom.addAttribute(rho)
	xom.addAttribute(thickness)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3)]	#[(ndm, ndf)...]

def writeTcl(pinfo):
	
	# get the mesh element and check it
	elem = pinfo.elem
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Line) or (len(elem.nodes) !=2):
		raise Exception('Error: invalid type of element or number of nodes. It should be a line element')

	# get the xobj
	elem_prop = pinfo.elem_prop
	xobj = elem_prop.XObject

	# get all attributes
	rho = xobj.getAttribute('rho').real
	thickness = xobj.getAttribute('thickness').real
	if rho <= 0.0:
		raise Exception('Error in FSIInterfaceElement2D: rho must be strictly positive')
	# todo: add checks if needed

	# write a comment with the name of this element only once
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName

	# write the tcl command
	pinfo.out_file.write('{}element FSIInterfaceElement2D {} {} {} {} -thickness {}\n'.format(
		pinfo.indent, elem.id, *[node.id for node in elem.nodes], rho, thickness))

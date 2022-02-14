import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# linear
	at_linear = MpcAttributeMetaData()
	at_linear.type = MpcAttributeType.Boolean
	at_linear.name = 'linear'
	at_linear.group = 'Group'
	at_linear.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('linear')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	# at_linear.sourceType = MpcAttributeSourceType.List
	# at_linear.setSourceList([0, 1])
	# at_linear.setDefault(0)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'element2dGNL'
	xom.addAttribute(at_linear)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3)]	#[(ndm, ndf)...]

def writeTcl(pinfo):
	
	# element element2dGNL tag Nd1 Nd2 A E Iz <linear>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	xelem=phys_prop.XObject
	
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
	
	
	if ( len(node_vect)!=2):
		raise Exception('Error: invalid type of element or number of nodes')
	
	at_Dimension_Section = phys_prop.XObject.getAttribute('Dimension')
	if(at_Dimension_Section is None):
		raise Exception('Error: cannot find "Dimension" attribute')
	if(at_Dimension_Section.string != '2D'):
		raise Exception('Error: dimension of physical property must be "2D"')
	
	at_Section = phys_prop.XObject.getAttribute('Section')
	if(at_Section is None):
		raise Exception('Error: cannot find "Section" attribute')
	Section = at_Section.customObject
	
	if Section is None:
		raise Exception('Error: Section is None')
	
	A = Section.properties.area
	
	at_E = phys_prop.XObject.getAttribute('E')
	if(at_E is None):
		raise Exception('Error: cannot find "E" attribute')
	E = at_E.quantityScalar.value
	
	Iz = Section.properties.Izz
	
	# optional paramters
	linear_at = xobj.getAttribute('linear')
	if(linear_at is None):
		raise Exception('Error: cannot find "linear" attribute')
	if linear_at.boolean:
		linear = 1
	else:
		linear = 0
	
	str_tcl = '{}element element2dGNL {}{} {} {} {} {}\n'.format(pinfo.indent, tag, nstr, A, E, Iz, linear)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
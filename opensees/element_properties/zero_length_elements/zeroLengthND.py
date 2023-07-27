import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	xom = MpcXObjectMetaData()
	xom.name = 'zeroLengthND'
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)]	# [(ndm, ndf), (ndm, ndf)]

def writeTcl(pinfo):
	
	# element zeroLengthND eleTag? iNode? jNode? NDTag? <1DTag?> <-orient x1? x2? x3? y1? y2? y3?>
	
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
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += '{} '.format(node.id)
	
	if (len(node_vect)!=2):
		raise Exception('Error: invalid type of element or number of nodes')
	
	# special_purpose
	if phys_prop.XObject.name != 'zeroLengthNDMaterial':
		raise Exception('Wrong material type for ZeroLength element. Expected: zeroLengthNDMaterial, given: {}'.format(phys_prop.XObject.name))
	
	matTag_at = phys_prop.XObject.getAttribute('matTag')
	matTag=matTag_at.index
	uniTag_at = phys_prop.XObject.getAttribute('uniTag')
	uniTag=uniTag_at.index if uniTag_at.index != 0 else ''
	
	# end special_purpose
	
	vect_x=elem.orientation.computeOrientation().col(0)
	vect_y=elem.orientation.computeOrientation().col(1)
	
	
	str_tcl = '{}element zeroLengthND {} {} {} {} -orient {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, nstr, matTag, uniTag, vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
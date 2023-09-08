import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	def mka(name, type, group, descr, dval=None, dim=None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(descr) +
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/TenNodeTetrahedron.html','TenNodeTetrahedron')+'<br/>') +
			html_end()
			)
		if dval:
			a.setDefault(dval)
		if dim:
			a.dimension = dim
		return a
	
	body_forces = mka('Body forces', MpcAttributeType.Boolean, 'Default', 'Optional: defines body forces in global X,Y and Z directions', dval = False)
	b1 = mka('b1', MpcAttributeType.QuantityScalar, 'Default', 'Body force in X direction', dval = 0.0, dim = u.F/u.L**3)
	b2 = mka('b2', MpcAttributeType.QuantityScalar, 'Default', 'Body force in Y direction', dval = 0.0, dim = u.F/u.L**3)
	b3 = mka('b3', MpcAttributeType.QuantityScalar, 'Default', 'Body force in Z direction', dval = 0.0, dim = u.F/u.L**3)
	
	xom = MpcXObjectMetaData()
	xom.name = 'TenNodeTetrahedron'
	xom.addAttribute(body_forces)
	xom.addAttribute(b1)
	xom.addAttribute(b2)
	xom.addAttribute(b3)
	
	# Optional-dep
	xom.setVisibilityDependency(body_forces, b1)
	xom.setVisibilityDependency(body_forces, b2)
	xom.setVisibilityDependency(body_forces, b3)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,3) for i in range(10)]#(ndm, ndf)

def writeTcl(pinfo):
	
	# element TenNodeTetrahedron eleTag? Node1? Node2? Node3? Node4? Node5? Node6? Node7? Node8? Node9? Node10? matTag? <$b1 $b2 $b3>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	matTag = phys_prop.id
	xobj = elem_prop.XObject
	
	def geta(name):
		a = xobj.getAttribute(name)
		if a is None:
			raise Exception('Error in TenNodeTetrahedron: cannot find "{}" attribute'.format(name))
		return a
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh = phys_prop.XObject.Xnamespace
	if not namePh.startswith('materials.nD'):
		raise Exception('Error: physical property must be "materials.nD" and not: "{}"'.format(namePh))
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Tetrahedron or len(elem.nodes)!=10:
		raise Exception('Error: invalid type of element or number of nodes')
	
	# node string
	elem_ = [e for e in elem.nodes]
	elem_[8], elem_[9] = elem_[9], elem_[8]
	#nstr = ' '.join(str(node.id) for node in elem.nodes)
	nstr = ' '.join(str(node.id) for node in elem_)

	# optional paramters
	sopt = ''
	if geta('Body forces').boolean:
		b1 = geta('b1').quantityScalar.value
		b2 = geta('b2').quantityScalar.value
		b3 = geta('b3').quantityScalar.value
		sopt = '{} {} {}'.format(b1, b2, b3)
	
	# command
	str_tcl = '{}element TenNodeTetrahedron {} {} {} {}\n'.format(pinfo.indent, tag, nstr, matTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)

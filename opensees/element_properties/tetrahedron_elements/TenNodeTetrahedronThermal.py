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
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/TenNodeTetrahedronThermal.html','TenNodeTetrahedronThermal')+'<br/>') +
			html_end()
			)
		if dval:
			a.setDefault(dval)
		if dim:
			a.dimension = dim
		return a
	
	kxx = mka('kxx', MpcAttributeType.QuantityScalar, 'Default', 'Coefficient of thermal conductivity for X direction', dval = 0.0, dim = u.F/u.L**3)
	kyy = mka('kyy', MpcAttributeType.QuantityScalar, 'Default', 'Coefficient of thermal conductivity for Y direction', dval = 0.0, dim = u.F/u.L**3)
	kzz = mka('kzz', MpcAttributeType.QuantityScalar, 'Default', 'Coefficient of thermal conductivity for Z direction', dval = 0.0, dim = u.F/u.L**3)
	
	rho = mka('rho', MpcAttributeType.QuantityScalar, 'Default', 'Density', dval = 0.0, dim = u.F/u.L**3)
	cp  = mka('cp', MpcAttributeType.QuantityScalar, 'Default', 'Specific heat', dval = 0.0, dim = u.F/u.L**3)
	Q  = mka('Q', MpcAttributeType.QuantityScalar, 'Default', 'Initial temperature', dval = 0.0, dim = u.F/u.L**3)
	
	xom = MpcXObjectMetaData()
	xom.name = 'TenNodeTetrahedronThermal'
	xom.addAttribute(kxx)
	xom.addAttribute(kyy)
	xom.addAttribute(kzz)
	xom.addAttribute(rho)
	xom.addAttribute(cp)
	xom.addAttribute(Q)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,1) for i in range(10)]#(ndm, ndf)

def writeTcl(pinfo):
	
	# element TenNodeTetrahedronThermal eleTag? Node1? Node2? Node3? Node4? Node5? Node6? Node7? Node8? Node9? Node10? <$kxx $kyy $kzz $rho $cp>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	def geta(name):
		a = xobj.getAttribute(name)
		if a is None:
			raise Exception('Error in TenNodeTetrahedronThermal: cannot find "{}" attribute'.format(name))
		return a
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Tetrahedron or len(elem.nodes)!=10:
		raise Exception('Error: invalid type of element or number of nodes')
	
	# node string
	elem_ = [e for e in elem.nodes]
	elem_[8], elem_[9] = elem_[9], elem_[8]
	#nstr = ' '.join(str(node.id) for node in elem.nodes)
	nstr = ' '.join(str(node.id) for node in elem_)

	# paramters
	kxx = geta('kxx').quantityScalar.value
	kyy = geta('kyy').quantityScalar.value
	kzz = geta('kzz').quantityScalar.value
	rho = geta('rho').quantityScalar.value
	cp  = geta('cp').quantityScalar.value
	Q   = geta('Q').quantityScalar.value
	sopt = '{} {} {} {} {} {}'.format(kxx, kyy, kzz, rho, cp, Q)
	
	# command
	str_tcl = '{}element TenNodeTetrahedronThermal {} {} {}\n'.format(pinfo.indent, tag, nstr, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
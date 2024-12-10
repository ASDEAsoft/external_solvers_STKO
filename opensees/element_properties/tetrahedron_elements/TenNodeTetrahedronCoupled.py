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
    
    #PARAMETERS RELATED TO MECHANICAL
    body_forces = mka('Body forces', MpcAttributeType.Boolean, 'Default', 'Optional: defines body forces in global X,Y and Z directions', dval = False)
    b1 = mka('b1', MpcAttributeType.QuantityScalar, 'Default', 'Body force in X direction', dval = 0.0, dim = u.F/u.L**3)
    b2 = mka('b2', MpcAttributeType.QuantityScalar, 'Default', 'Body force in Y direction', dval = 0.0, dim = u.F/u.L**3)
    b3 = mka('b3', MpcAttributeType.QuantityScalar, 'Default', 'Body force in Z direction', dval = 0.0, dim = u.F/u.L**3)

    #PARAMETERS RELATED TO THERMAL
    kxx = mka('kxx', MpcAttributeType.QuantityScalar, 'Default', 'Coefficient of thermal conductivity for X direction', dval = 0.0, dim = u.F/u.L**3)
    kyy = mka('kyy', MpcAttributeType.QuantityScalar, 'Default', 'Coefficient of thermal conductivity for Y direction', dval = 0.0, dim = u.F/u.L**3)
    kzz = mka('kzz', MpcAttributeType.QuantityScalar, 'Default', 'Coefficient of thermal conductivity for Z direction', dval = 0.0, dim = u.F/u.L**3)

    rho = mka('rho', MpcAttributeType.QuantityScalar, 'Default', 'Density', dval = 0.0, dim = u.F/u.L**3)
    cp  = mka('cp', MpcAttributeType.QuantityScalar, 'Default', 'Specific heat', dval = 0.0, dim = u.F/u.L**3)
    Q  = mka('Q', MpcAttributeType.QuantityScalar, 'Default', 'Initial temperature', dval = 0.0, dim = u.F/u.L**3)

    xom = MpcXObjectMetaData()
    xom.name = 'TenNodeTetrahedronCoupled'
    xom.addAttribute(body_forces)
    xom.addAttribute(b1)
    xom.addAttribute(b2)
    xom.addAttribute(b3)
    xom.addAttribute(kxx)
    xom.addAttribute(kyy)
    xom.addAttribute(kzz)
    xom.addAttribute(rho)
    xom.addAttribute(cp)
    xom.addAttribute(Q)

    #OPTIONAL PARAMETERS MECHANICAL
    xom.setVisibilityDependency(body_forces, b1)
    xom.setVisibilityDependency(body_forces, b2)
    xom.setVisibilityDependency(body_forces, b3)

    return xom


def getNodalSpatialDimExtended(xobj, xobj_phys_prop):
    return [(3,1) for i in range(10)]

def getNodalSpatialDim(xobj, xobj_phys_prop):
    return [(3,3) for i in range(10)]


def writeTcl(pinfo):
    
    # element TenNodeTetrahedron eleTag? Node1? Node2? Node3? Node4? Node5? Node6? Node7? Node8? Node9? Node10? matTag? <$b1 $b2 $b3 $kxx $kyy $kzz $rho $cp $Q>
    
    elem = pinfo.elem
    phys_prop = pinfo.phys_prop
    elem_prop = pinfo.elem_prop
    
    tag = elem.id
    matTag = phys_prop.id
    xobj = elem_prop.XObject
    
    def geta(name):
        a = xobj.getAttribute(name)
        if a is None:
            raise Exception('Error in TenNodeTetrahedronCoupled: cannot find "{}" attribute'.format(name))
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
	
    if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Tetrahedron or len(elem.nodes)!=10:
        raise Exception('Error: invalid type of element or number of nodes')
	
	# node string
    nodes_ = [e for e in elem.nodes]
    nodes_[8], nodes_[9] = nodes_[9], nodes_[8]
    #nstr = ' '.join(str(node.id) for node in elem.nodes)
    nstr = ' '.join(str(node.id) for node in nodes_)


    sopt = ''
    if geta('Body forces').boolean:
        b1 = geta('b1').quantityScalar.value
        b2 = geta('b2').quantityScalar.value
        b3 = geta('b3').quantityScalar.value
    kxx = geta('kxx').quantityScalar.value
    kyy = geta('kyy').quantityScalar.value
    kzz = geta('kzz').quantityScalar.value
    rho = geta('rho').quantityScalar.value
    cp  = geta('cp').quantityScalar.value
    Q   = geta('Q').quantityScalar.value

    sopt = ''
    if geta('Body forces').boolean:
        b1 = geta('b1').quantityScalar.value
        b2 = geta('b2').quantityScalar.value
        b3 = geta('b3').quantityScalar.value
        sopt = '{} {} {}'.format(b1, b2, b3)
    sopt_thermal = sopt = '{} {} {} {} {} {}'.format(kxx, kyy, kzz, rho, cp, Q)  
    # command
    if pinfo.is_thermo_mechanical_analysis:
        full_string = 'element TenNodeTetrahedronThermal {} {} {}\n'.format(tag, nstr, sopt_thermal)
    else:
        full_string = 'element TenNodeTetrahedron {} {} {} {}\n'.format(tag, nstr, matTag, sopt)

    # now write the string into the file
    pinfo.out_file.write(full_string)
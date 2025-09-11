import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import math
import os
from typing import List, Tuple

# TODO: use a "once" initialization in the getNodalSpatialDim function instead of preprocessing elements!

def _err(msg):
	return 'Error in "PML" :\n{}'.format(msg)

# The PMLInfo class stores information about all PML elements in the model
# It is created once and stored in the global process info
class PMLInfo:
    def __init__(self):
        self.dimension : int = 0 # 2 or 3
        self.elements : List[MpcElement] = []
        self.bbox : FxBndBox = FxBndBox()
        self.properties : List[int] = []
        self._process()
        
    def _find_properties(self):
        print('PML: Finding element properties ...')
        doc = App.caeDocument()
        for _, prop in doc.elementProperties.items():
            if prop.XObject.name == 'PML':
                self.properties.append(prop.id)
        print('PML: Found {} element properties.'.format(len(self.properties)))

    def _find_elements(self):
        print('PML: Finding elements ...')
        '''
        Finds all the elements that use the given PML element property.
        Process edges for 2D and faces for 3D.
        Note: only one of the 2 lists can be non-empty, depending on the dimension of the model.
        '''
        doc = App.caeDocument()
        ele_2d = []
        ele_3d = []
        bbox = FxBndBox()
        for geom_id, geom in doc.geometries.items():
            # get the mesh of this geometry
            mesh_of_geom = doc.mesh.meshedGeometries[geom_id]
            # get element property assignments
            asn_3d = geom.elementPropertyAssignment.onSolids
            asn_2d = geom.elementPropertyAssignment.onFaces
            # process all mesh domains
            all_solids = mesh_of_geom.solids
            all_faces = mesh_of_geom.faces
            # process solids
            for solid_id in range(len(all_solids)):
                solid = all_solids[solid_id]
                # get element property assigned to this face
                elem_prop = asn_3d[solid_id]
                if elem_prop is None or elem_prop.id not in self.properties:
                    continue
                # process all elements
                for elem in solid.elements:
                    # check element
                    if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Hexahedron or len(elem.nodes)!=8:
                        raise Exception(_err('invalid type of element or number of nodes, It should be a Hexahedron with 8 nodes, not a {} with {} nodes'
                            .format(elem.geometryFamilyType(), len(elem.nodes))))
                    # collect element
                    ele_3d.append(elem)
                    # update bbox
                    for node in elem.nodes:
                        bbox.add(node.position)
            # process faces
            for face_id in range(len(all_faces)):
                face = all_faces[face_id]
                # get element property assigned to this edge
                elem_prop = asn_2d[face_id]
                if elem_prop is None or elem_prop.id not in self.properties:
                    continue
                # process all elements
                for elem in face.elements:
                    # check element
                    if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Quadrilateral or len(elem.nodes)!=4:
                        raise Exception(_err('invalid type of element or number of nodes, It should be a Quadrilateral with 4 nodes, not a {} with {} nodes'
                            .format(elem.geometryFamilyType(), len(elem.nodes))))
                    # collect element
                    ele_2d.append(elem)
                    # update bbox
                    for node in elem.nodes:
                        bbox.add(node.position)
        # check if we have elements
        if len(ele_2d) == 0 and len(ele_3d) == 0:
            raise Exception(_err('No PML elements found in the model.'))
        elif len(ele_2d) > 0 and len(ele_3d) > 0:
            raise Exception(_err('PML elements cannot be mixed in the model. Found both 2D and 3D elements.'))
        # done
        self.bbox = bbox
        self.dimension = 2 if len(ele_2d)>0 else 3
        self.elements = ele_2d if len(ele_2d)>0 else ele_3d
        print('PML: Found {} elements in {}D.'.format(len(self.elements), self.dimension))
        
    def _process(self):
        self._find_properties()
        self._find_elements()
    

def _setup_once():
    pinfo = tclin.process_info.current_process_info
    if pinfo is None:
        raise Exception(_err('global process info is not set.'))
    # make sure not already setup
    if 'PMLInfo' in pinfo.custom_data:
        return
    print('PML: Setting up global process info ...')
    # create a new PMLInfo
    pml_info = PMLInfo()
    pinfo.custom_data['PMLInfo'] = pml_info

def getNodalSpatialDim(xobj, xobj_phys_prop):
    _setup_once()
    dim = tclin.process_info.current_process_info.custom_data['PMLInfo'].dimension
    if dim == 2:
        return [(2,5) for i in range(4)] # For 2D PML each node has 5 DOFs (2 translations and Sx, Sy, Sxy)
    elif dim == 3:
        return [(3,9) for i in range(8)] # For 3D PML each node has 9 DOFs (3 translations and Sxx, Syy, Szz, Sxy, Sxz, Syz)

def makeXObjectMetaData():

    def mka(name, type, description, group, dimension = None, default = None):
        a = MpcAttributeMetaData()
        a.type = type
        a.name = name
        a.group = group
        a.description = (
            html_par(html_begin()) +
            html_par(html_boldtext(name)+'<br/>') + 
            html_par(description) +
            html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/PML.html','PML Element')+'<br/>') +
            html_end()
            )
        if dimension:
            a.dimension = dimension
        if default:
            a.setDefault(default)
        return a

    E = mka('E', MpcAttributeType.QuantityScalar,
            'Young\'s modulus of the PML material',
            'Material Properties',
            dimension=u.F/u.L**2, default=0.0)
    nu = mka('nu', MpcAttributeType.Real,
            'Poisson\'s ratio of the PML material',
            'Material Properties',
            default=0.0)
    rho = mka('rho', MpcAttributeType.QuantityScalar,
            'Density of the PML material',
            'Material Properties',
            dimension=u.F*u.t**2/u.L**4, default=0.0)
    
    m = mka('m', MpcAttributeType.Real,
            'PML parameter m (2 is recommended)',
            'Miscellaneous',
            default=2.0)
    R = mka('R', MpcAttributeType.Real,
            'PML parameter R (1.0e-8 is recommended)',
            'Miscellaneous',
            default=1.0e-8)
    
    alpha = mka('alpha', MpcAttributeType.Real,
            'Rayleigh damping parameter for PML (alpha will be 0 even if you input a value)',
            'Damping',
            default=0.0)
    beta = mka('beta', MpcAttributeType.Real,
            'Rayleigh damping parameter for PML (beta will be 0 even if you input a value)',
            'Damping',
            default=0.0)
    
    n_gamma = mka('γ', MpcAttributeType.Real,
                'Newmark integration parameter',
                'Integration',
                default=0.5)
    n_beta = mka('β', MpcAttributeType.Real,
                'Newmark integration parameter',
                'Integration',
                default=0.25)
    n_eta = mka('η', MpcAttributeType.Real,
                'Newmark integration parameter',
                'Integration',
                default=0.0833333333333333)
    
    xom = MpcXObjectMetaData()
    xom.name = 'PML'
    xom.addAttribute(E)
    xom.addAttribute(nu)
    xom.addAttribute(rho)
    xom.addAttribute(m)
    xom.addAttribute(R)
    xom.addAttribute(alpha)
    xom.addAttribute(beta)
    xom.addAttribute(n_gamma)
    xom.addAttribute(n_beta)
    xom.addAttribute(n_eta)

    return xom
    
def writeTcl(pinfo):
    _setup_once()
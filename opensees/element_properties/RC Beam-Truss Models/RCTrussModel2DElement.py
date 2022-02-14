import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.physical_properties.materials.uniaxial.ConcretewBeta as cwb
import math

####################################################################################
# Utilities
####################################################################################

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

def _description(title, body):
	return (
		html_par(html_begin()) +
		html_par(html_boldtext(title)+'<br/>') + 
		html_par(body) +
		html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Truss2_Element','RCTrussModel2DElement')) +
		html_end()
		)

# return [0,1,2,3] (the standard connectivity) if the angle between the local x axis and the 0-1 axis 
# is < then the angle between the local x axis and the 2-1 axis (in this case we return [1, 2, 3, 0])
def _get_oriented_ids(elem):
	elem_dir_x = elem.nodes[1].position - elem.nodes[0].position
	elem_dir_y = elem.nodes[2].position - elem.nodes[1].position
	elem_dir_y.normalize()
	elem_dir_x.normalize()
	# get orientation matrix and local x direction
	orientation_matrix = elem.orientation.quaternion.toRotationMatrix()
	dir_x = orientation_matrix.col(0)
	if abs(dir_x.dot(elem_dir_x)) > abs(dir_x.dot(elem_dir_y)):
		return [0,1,2,3]
	else:
		return [1,2,3,0]

# return command parameters and options
def _get_command_params(xobj):
	if _get_xobj_attribute(xobj, '-rho').boolean:
		rho = _get_xobj_attribute(xobj, 'rho').real
		rho = ' -rho {}'.format(rho)
	else:
		rho = ''
	kin = _get_xobj_attribute(xobj, 'Kinematics').string
	use_rayleigh = _get_xobj_attribute(xobj, '-rayleigh').boolean
	if kin == 'Linear':
		truss = 'truss'
		truss2 = 'Truss2'
		if use_rayleigh:
			rayleigh = ' -doRayleigh 1'
			rayleigh2 = ' -rayleigh 1'
		else:
			rayleigh = ''
			rayleigh2 = ''
	else:
		truss = 'corotTruss'
		truss2 = 'CorotTruss2'
		if use_rayleigh:
			rayleigh = ' -doRayleigh 1'
		else:
			rayleigh = ''
		rayleigh2 = ''
	return (truss, truss2, rayleigh, rayleigh2, rho)

# obtains a material from an instance of RCTrussModel2D physica property
def _get_material(doc, phys_prop, name):
	mat_id = _get_xobj_attribute(phys_prop.XObject, name).index
	if mat_id == 0:
		raise Exception('Error: no physical property provided in the "{}" field of RCTrussModel2D'.format(name))
	prop = doc.getPhysicalProperty(mat_id)
	if prop is None:
		raise Exception('Error: the material specified in "{}" of RCTrussModel2D with index = {} is not in the document'.format(name, mat_id))
	return prop

# process the steel model
# steel is not modified so the source ID will be returned
def _process_steel(doc, phys_prop):
	prop = _get_material(doc, phys_prop, 'Rebars Material')
	return prop.id

# process one of the concrete models,
# applies the fracture energy regularization,
# writes a new regularized material in the tcl file
# and returns the ID of the material
def _process_concrete(pinfo, doc, phys_prop, name, L):
	# get physical property
	prop = _get_material(doc, phys_prop, name)
	# get parameters
	p = cwb.ConcretewBetaParameters(prop.XObject)
	# regularize tensile behavior
	# TODO: ask Rodolfo, he told me not to regularize it, but in the MassoneWall_TrussModel.tcl there is this...
	p.etint = 3.0*(p.ft/p.Ec)*(p.LR/L)
	if p.etres <= p.etint:
		p.etres = p.etint*1.1 # make sure res > int
	# regularize compressive behavior
	# TODO: ask Rodolfo, in the MassoneWall_TrussModel the regularization is different from paper of 2013
	# and Eu is used instead of Ec
	# and I fear residual stress should be always set to a small value otherwise this might not work...
	if p.conf is not None:
		A = p.conf.fcc/(0.5*(p.Ec*p.conf.ecc + p.conf.fcc))
		p.ecint = (1.0-A)*p.conf.ecc + (p.LR/L)*(-0.002 + A*p.conf.ecc)
	else:
		# Paper version:
		#A = p.fpc/(0.5*(p.Ec*p.ec0 + p.fpc))
		#p.ecint = (1.0-A)*p.ec0 + (p.LR/L)*(-0.002 + A*p.ec0)
		# MassoneWall_TrussModel.tcl version
		lambda_ = 0.5
		if p.lambda_ is not None:
			lambda_ = p.lambda_
		Eu = lambda_*(p.fpc/p.ec0) + (1.0-lambda_)*p.Ec
		p.ecint = (-0.002 + p.fpc/Eu)*(p.LR/L) + (-0.002 - p.fpc/Eu)
	if p.ecres >= p.ecint:
		p.ecres = p.ecint*1.1 # make sure res > int
	# regularize biaxial behavior
	# TODO: ask Rodolfo, he told me to look at paper of 2014 but I couldn't find it, so I took it from
	# the MassoneWall_TrussModel.tcl example
	if p.beta is not None:
		p.beta.ebint *= (p.LR/L)
		p.beta.ebres *= (p.LR/L)
	# get the new ID
	p.tag = pinfo.next_physicalProperties_id
	pinfo.next_physicalProperties_id += 1
	# write it to file
	pinfo.out_file.write('{}# {}\n'.format(pinfo.indent, name))
	cwb.writeTclInternal(pinfo, p)
	# done
	return p.tag

# Truss elements used here are in 2D and support both 2 or 3 dofs,
# but both nodes of the same truss must have the same number of dofs.
# When a truss is connected with a beam only at one end, this is not true,
# so in those cases we need to duplicate the node with 3 dofs,
# create an auxiliary node with 2 dofs on the fly, and use that auxiliary
# as the end node of a truss with 2 dofs, and of course we use an equal dof
# to merge the disp dofs.
# This function takes care of producing and writing extra nodes if necessary
# and return a list with 4 indices of the 4 nodes, either the source ones
# or the extra ones. It also takes care of update the model builder accordingly.
def _process_nodes(pinfo, nodes):
	nid = [inode.id for inode in nodes] # start with given nodes
	ndof = [2, 2, 2, 2] # assume they all have 2 dofs
	num_3 = 0 # count how many nodes have 3 dofs
	for i in range(4):
		indf = pinfo.node_to_model_map[nid[i]][1]
		ndof[i] = indf
		if indf == 3:
			num_3 += 1
	# if all are equal (2 or 3 dofs)
	if num_3 == 0:
		# all nodes with 2 dofs, just update the model builder accordingly
		pinfo.updateModelBuilder(2, 2)
	elif num_3 == 4:
		# all nodes with 3 dofs, just update the model builder accordingly
		pinfo.updateModelBuilder(2, 3)
	else:
		# needed to correctly format nodal coordinates
		FMT = pinfo.get_double_formatter()
		# some nodes have 3 dofs, other just 2.
		# here we duplicate nodes with 3 dofs, giving the new nodes 2 dofs
		# and linking old 3-dof nodes with new 2-dof nodes with equal dofs.
		# the new nodes will be used for trusses
		pinfo.out_file.write('{}# auxiliary nodes\n'.format(pinfo.indent))
		# duplicate nodes with 3 dofs and give them 2 dofs
		pinfo.updateModelBuilder(2, 2)
		for i in range(4):
			if ndof[i] == 3:
				inode = nodes[i]
				pinfo.out_file.write('{}node {}   {} {} {}\n'.format(pinfo.indent, pinfo.next_node_id, FMT(inode.x), FMT(inode.y), FMT(inode.z)))
				pinfo.out_file.write('{}equalDOF {} {}   1 2\n'.format(pinfo.indent, inode.id, pinfo.next_node_id))
				nid[i] = pinfo.next_node_id
				pinfo.next_node_id += 1
	# done, return a tuple with the modified list of node ids
	return (nid[0], nid[1], nid[2], nid[3])

####################################################################################
# Main methods
####################################################################################

def makeXObjectMetaData():
	
	# Kinematics
	at_Kinematics = MpcAttributeMetaData()
	at_Kinematics.type = MpcAttributeType.String
	at_Kinematics.name = 'Kinematics'
	at_Kinematics.group = 'General'
	at_Kinematics.description = _description('Kinematics', 'It can be Linear (Truss2 element) or Corotational (CorotTruss2 element).')
	at_Kinematics.sourceType = MpcAttributeSourceType.List
	at_Kinematics.setSourceList(['Linear', 'Corotational'])
	at_Kinematics.setDefault('Linear')
	
	# -rho
	at_use_rho = MpcAttributeMetaData()
	at_use_rho.type = MpcAttributeType.Boolean
	at_use_rho.name = '-rho'
	at_use_rho.group = 'Optional'
	at_use_rho.description = _description('-rho', 'input optional parameter: rho')
	
	# rho
	at_rho = MpcAttributeMetaData()
	at_rho.type = MpcAttributeType.Real
	at_rho.name = 'rho'
	at_rho.group = 'Optional'
	at_rho.description = _description('rho', 'mass per unit area (default = 0.0)')
	at_rho.setDefault(0.0)
	
	# -rayleigh
	at_rayleigh = MpcAttributeMetaData()
	at_rayleigh.type = MpcAttributeType.Boolean
	at_rayleigh.name = '-rayleigh'
	at_rayleigh.group = 'Optional'
	at_rayleigh.description = _description('-rayleigh', 'check it to activate rayleigh damping (note that if Kinematics = Corotational, rayleigh is activated by default)')
	
	xom = MpcXObjectMetaData()
	xom.name = 'RCTrussModel2DElement'
	xom.addAttribute(at_Kinematics)
	xom.addAttribute(at_use_rho)
	xom.addAttribute(at_rho)
	xom.addAttribute(at_rayleigh)
	
	# boolean dependencies
	xom.setVisibilityDependency(at_use_rho, at_rho)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	# This is an assembly of 4 truss2 elements
	# in 2D, they support both 2 or 3 dofs.
	return [(2, [2,3]), (2, [2,3]), (2, [2,3]), (2, [2,3])]

def writeTcl(pinfo):
	
	# This is a macro-element, a 4 node quad in STKO, that generates an assembly of truss/truss2 elements in TCL.
	# The expected physical property assigned to this material is a RCTrussModel2D (special_purpose) material.
	# The element orientation will be used to orient the trusses
	
	# get document
	# we need it to obtain concrete and steel materials from the RCTrussModel2D container
	doc = App.caeDocument()
	if(doc is None):
		raise Exception('Error: No cae document')
	
	# check mesh element
	elem = pinfo.elem
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Quadrilateral or len(elem.nodes)!=4):
		raise Exception('Error: Invalid Element type ({}) or number of nodes ({}). Expected: element type = {}, number of nodes = 4'.format(
			elem.geometryFamilyType(), len(elem.nodes), MpcElementGeometryFamilyType.Quadrilateral))
	
	# get physical property and check it
	phys_prop = pinfo.phys_prop
	if phys_prop is None:
		raise Exception('Error: No physical property provided for "RCTrussModel2DElement" element {}'.format(elem.id))
	if phys_prop.XObject.name != 'RCTrussModel2D':
		raise Exception('Error: Wrong physical property ({}) assigned to "RCTrussModel2DElement" element {}. Use "RCTrussModel2D"'.format(phys_prop.XObject.name, elem.id))
	
	# get element property
	elem_prop = pinfo.elem_prop
	xobj = elem_prop.XObject
	
	# get nodal permutation
	perm = _get_oriented_ids(elem)
	
	# get nodes
	n1 = elem.nodes[perm[0]]
	n2 = elem.nodes[perm[1]]
	n3 = elem.nodes[perm[2]]
	n4 = elem.nodes[perm[3]]
	
	# compute vectors
	vbot = n2.position - n1.position
	vtop = n3.position - n4.position
	vlef = n4.position - n1.position
	vrig = n3.position - n2.position
	vdia = n3.position - n1.position
	
	# compute characteristic dimensions
	thickness = _get_xobj_attribute(phys_prop.XObject, 'Thickness').quantityScalar.value
	len_bot = vbot.norm()
	len_top = vtop.norm()
	len_lef = vlef.norm()
	len_rig = vrig.norm()
	len_hori = (len_top + len_bot) / 2.0
	len_vert = (len_lef + len_rig) / 2.0
	len_diag = vdia.norm()
	# TODO: as Rodolfo if we need to restrict the usage to square or rectangular geometries without distorsion
	# if so, keep the following exception
	dist_tolerance = max(1.0e-12, 1.0e-4*(len_bot+len_top+len_lef+len_rig)/4.0)
	if (abs(len_bot - len_top) > dist_tolerance) or (abs(len_lef - len_rig) > dist_tolerance):
		raise Exception('Error: the quadritaral base mesh for the RCTrussModel2DElement is distorted, please build a non-distorted mesh.')
	
	# compute the diagonal angle
	angle = math.acos(vbot.normalized().dot(vdia.normalized()))
	
	# compute concrete areas
	area_concr_hori = thickness * len_vert / 2.0
	area_concr_vert = thickness * len_hori / 2.0
	area_concr_diag = thickness * len_hori * math.sin(angle)
	
	# compute steel areas
	reb_diam_hori = _get_xobj_attribute(phys_prop.XObject, 'Horizontal Diameter').quantityScalar.value
	reb_diam_vert = _get_xobj_attribute(phys_prop.XObject, 'Vertical Diameter').quantityScalar.value
	reb_spac_hori = _get_xobj_attribute(phys_prop.XObject, 'Horizontal Spacing').quantityScalar.value
	reb_spac_vert = _get_xobj_attribute(phys_prop.XObject, 'Vertical Spacing').quantityScalar.value
	area_steel_hori = (math.pi * (reb_diam_hori/2.0)**2) * len_vert / reb_spac_hori / 2.0
	area_steel_vert = (math.pi * (reb_diam_vert/2.0)**2) * len_hori / reb_spac_vert / 2.0
	
	# write a comment
	pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.name, elem.id))
	
	# process materials
	mat_id_steel = _process_steel(doc, phys_prop)
	mat_id_concr_vert = _process_concrete(pinfo, doc, phys_prop, 'Vertical Concrete Material', len_vert)
	mat_id_concr_hori = _process_concrete(pinfo, doc, phys_prop, 'Horizontal Concrete Material', len_hori)
	mat_id_concr_diag = _process_concrete(pinfo, doc, phys_prop, 'Diagonal Concrete Material', len_diag)
	
	# get command parameters
	truss, truss2, rayleigh, rayleigh2, rho = _get_command_params(xobj)
	
	# define new element ids. we generate 10 elements from this macro-element
	# TODO: possible improvement, for vertical and horizontal elements
	# create just 1 element with a Parallel material (1*concr + 1*steel)
	base_id = pinfo.next_elem_id
	concr_ele_id_bot = base_id
	concr_ele_id_top = base_id + 1
	concr_ele_id_lef = base_id + 2
	concr_ele_id_rig = base_id + 3
	steel_ele_id_bot = base_id + 4
	steel_ele_id_top = base_id + 5
	steel_ele_id_lef = base_id + 6
	steel_ele_id_rig = base_id + 7
	concr_ele_id_d1 = base_id + 8
	concr_ele_id_d2 = base_id + 9
	pinfo.next_elem_id += 10
	
	# check dof size, if incompatible (mixing 2 and 3 dofs)
	# create extra nodes and connect with equal dofs
	i1, i2, i3, i4 = _process_nodes(pinfo, [n1, n2, n3, n4])
	
	# write elements
	# vertical and horizontal concrete
	pinfo.out_file.write('{}element {} {}   {} {}   {} {}{}{}; # bottom concrete (1->2)\n'.format(pinfo.indent, truss, concr_ele_id_bot, i1, i2, area_concr_hori, mat_id_concr_hori, rho, rayleigh))
	pinfo.out_file.write('{}element {} {}   {} {}   {} {}{}{}; # top concrete (4->3)\n'.format(pinfo.indent, truss, concr_ele_id_top, i4, i3, area_concr_hori, mat_id_concr_hori, rho, rayleigh))
	pinfo.out_file.write('{}element {} {}   {} {}   {} {}{}{}; # left concrete (1->4)\n'.format(pinfo.indent, truss, concr_ele_id_lef, i1, i4, area_concr_vert, mat_id_concr_vert, rho, rayleigh))
	pinfo.out_file.write('{}element {} {}   {} {}   {} {}{}{}; # right concrete (2->3)\n'.format(pinfo.indent, truss, concr_ele_id_rig, i2, i3, area_concr_vert, mat_id_concr_vert, rho, rayleigh))
	# vertical and horizontal steel
	pinfo.out_file.write('{}element {} {}   {} {}   {} {}{}{}; # bottom steel (1->2)\n'.format(pinfo.indent, truss, steel_ele_id_bot, i1, i2, area_steel_hori, mat_id_steel, rho, rayleigh))
	pinfo.out_file.write('{}element {} {}   {} {}   {} {}{}{}; # top steel (4->3)\n'.format(pinfo.indent, truss, steel_ele_id_top, i4, i3, area_steel_hori, mat_id_steel, rho, rayleigh))
	pinfo.out_file.write('{}element {} {}   {} {}   {} {}{}{}; # left steel (1->4)\n'.format(pinfo.indent, truss, steel_ele_id_lef, i1, i4, area_steel_vert, mat_id_steel, rho, rayleigh))
	pinfo.out_file.write('{}element {} {}   {} {}   {} {}{}{}; # right steel (2->3)\n'.format(pinfo.indent, truss, steel_ele_id_rig, i2, i3, area_steel_vert, mat_id_steel, rho, rayleigh))
	# diagonal concrete
	pinfo.out_file.write('{}element {} {}   {} {} {} {}   {} {}{}{}; # diagonal concrete (1->3)\n'.format(pinfo.indent, truss2, concr_ele_id_d1, i1, i3, i2, i4, area_concr_diag, mat_id_concr_diag, rho, rayleigh2))
	pinfo.out_file.write('{}element {} {}   {} {} {} {}   {} {}{}{}; # diagonal concrete (2->4)\n'.format(pinfo.indent, truss2, concr_ele_id_d2, i2, i4, i1, i3, area_concr_diag, mat_id_concr_diag, rho, rayleigh2))
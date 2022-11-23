import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.physical_properties.materials.uniaxial.ConcretewBeta as cwb
from math import *
import numpy as np
from scipy.optimize import fsolve
import os
import shutil
import glob

def makeXObjectMetaData():
	
	# utilties
	def mka(name, group, description, type, dim = None, default = None, slist = None):
		at = MpcAttributeMetaData()
		at.type = type
		at.name = name
		at.group = group
		at.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(description) +
			html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Infill_Wall_Model_and_Element_Removal','MasonryInfillWallMaterial')+'<br/>') +
			html_end()
			)
		if dim is not None:
			at.dim = dim
		if slist is not None:
			at.sourceType = MpcAttributeSourceType.List
			at.setSourceList(slist)
		if default is not None:
			at.setDefault(default)
		return at
	
	# RC Frame parameters
	Efe = mka('Efe', 'RC Frame parameters', 'Expected elastic modulus of frame concrete', MpcAttributeType.QuantityScalar, dim = u.F/u.L**2, default = 3122.0)
	Ig = mka('Ig', 'RC Frame parameters', 'Gross moment of inertia of the concrete columns', MpcAttributeType.QuantityScalar, dim = u.L**4, default = 8856.0)
	# Misc
	Pce = mka('Pce', 'Misc', 'Expected gravity compressive force applied to infill panel', MpcAttributeType.QuantityScalar, dim = u.F, default = 41.4)
	Ninteraction = mka('Ninteraction', 'Misc', 'Number of points on the interaction curve to be used for calculating fiber properties (should be an even number).', MpcAttributeType.Integer, default = 6)
	
	# Xom
	xom = MpcXObjectMetaData()
	xom.name = 'MasonryInfillWallElement'
	xom.addAttribute(Efe)
	xom.addAttribute(Ig)
	xom.addAttribute(Pce)
	xom.addAttribute(Ninteraction)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	# This is an assembly of beams in 3D space
	return [(3, 6), (3, 6), (3, 6), (3, 6)]

def writeTcl(pinfo):
	
	# This is a macro-element, a 4 node quad in STKO, 
	# that generates an assembly of 2 beam elements + 1 central node.
	# It also generate a collapse recorder
	
	#############################################################################
	# utilities
	#############################################################################
	
	# get attribute from xobject
	def geta(xobj, at_name):
		attribute = xobj.getAttribute(at_name)
		if attribute is None:
			raise Exception('Error: cannot find "{}" attribute'.format(at_name))
		return attribute
	
	# get order of magnitute
	def OM(x):
		if x == 0.0:
			return 0.0
		return round(log10(abs(x)))
	
	# return [0,1,2,3] (the standard connectivity) if the angle between the local x axis and the 0-1 axis 
	# is < then the angle between the local x axis and the 2-1 axis (in this case we return [1, 2, 3, 0])
	def get_oriented_ids(elem):
		elem_dir_x = elem.nodes[1].position - elem.nodes[0].position
		elem_dir_y = elem.nodes[2].position - elem.nodes[1].position
		elem_dir_y.normalize()
		elem_dir_x.normalize()
		# get orientation matrix and local x direction
		orientation_matrix = elem.orientation.quaternion.toRotationMatrix()
		dir_x = orientation_matrix.col(0)
		if abs(dir_x.dot(elem_dir_x)) > abs(dir_x.dot(elem_dir_y)):
			if dir_x.dot(elem_dir_x) > 0.0:
				return [0,1,2,3]
			else:
				return [2,3,0,1]
		else:
			if dir_x.dot(elem_dir_y) > 0.0:
				return [3,0,1,2]
			else:
				return [1,2,3,0]
	
	#############################################################################
	# initial checks
	#############################################################################
	
	# get document
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
		raise Exception('Error: No physical property provided for "MasonryInfillWallElement" element {}'.format(elem.id))
	if phys_prop.XObject.name != 'MasonryInfillWallMaterial':
		raise Exception('Error: Wrong physical property ({}) assigned to "MasonryInfillWallElement" element {}. Use "MasonryInfillWallMaterial"'.format(phys_prop.XObject.name, elem.id))
	
	# get element property
	elem_prop = pinfo.elem_prop
	
	# get nodal permutation
	perm = get_oriented_ids(elem)
	
	# get nodes
	n1 = elem.nodes[perm[0]]
	n2 = elem.nodes[perm[1]]
	n3 = elem.nodes[perm[2]]
	n4 = elem.nodes[perm[3]]
	
	#############################################################################
	# some formula here assume kip/inches... 
	# so we need the follwing unit system tools
	#############################################################################
	
	kip = 1.0
	inc = 1.0
	sec = 1.0
	
	m = inc/0.0254
	dm = 0.1*m
	cm = 0.01*m
	mm = 0.001*m
	foot = 0.3048*m
	
	kN  = 0.224808943*kip
	hN  = 0.1*kN
	daN = 0.01*kN
	N   = 0.001*kN
	
	MPa = 1000.0*kN/m/m
	psi = MPa/145.037738
	
	lbf = psi*inc*inc
	ksi = 1000.0*psi
	
	g = 9.81*m/sec/sec
	
	# map by string
	UFMap = ({
		'kip': kip,
		'N'  : N,
		'daN': daN,
		'hN' : hN,
		'kN' : kN,
		})
	ULMap = ({
		'in' : inc,
		'm'  : m,
		'dm' : dm,
		'cm' : cm,
		'mm' : mm,
		'ft' : foot,
		})
	
	# User units
	UF = geta(phys_prop.XObject, 'Force unit').string
	UL = geta(phys_prop.XObject, 'Length unit').string

	# scale factors from user input to base system
	F = UFMap[UF] # force
	L = ULMap[UL] # length
	P = F/L/L # pressure
	t = 1# seconds
	Acc = L/t**2
	M = F/Acc # mass
	
	#############################################################################
	# get input from physical property
	#############################################################################
	
	fme = geta(phys_prop.XObject, 'fme').quantityScalar.value * P # Masonry expected compressive strength
	tinf = geta(phys_prop.XObject, 'tinf').quantityScalar.value * L # Thickness of masonry infill wall
	Em = geta(phys_prop.XObject, 'Em').quantityScalar.value * P # Elastic modulus of masonry infill
	vte = geta(phys_prop.XObject, 'vte').quantityScalar.value * P # Average bed joint strength
	fvie = geta(phys_prop.XObject, 'fvie').quantityScalar.value * P # see FEMA356, Section 7.5.2.2
	gamma_inf = geta(phys_prop.XObject, 'gamma_inf').quantityScalar.value * F/L**3 # Weight density of the infill bricks.
	
	#############################################################################
	# get input from element property
	#############################################################################
	
	Efe = geta(elem_prop.XObject, 'Efe').quantityScalar.value * P # Expected elastic modulus of frame concrete
	Ig = geta(elem_prop.XObject, 'Ig').quantityScalar.value * L**4 # Gross moment of inertia of the concrete columns
	Pce = geta(elem_prop.XObject, 'Pce').quantityScalar.value * F # Expected gravity compressive force applied to infill panel
	Ninteraction = geta(elem_prop.XObject, 'Ninteraction').integer # Number of points on the interaction curve to be used for calculating fiber properties (should be an even number).
	
	#############################################################################
	# get input from element geometry
	#############################################################################
	
	L_bottom = (n2.position - n1.position).norm()
	L_top = (n3.position - n4.position).norm()
	H_left = (n4.position - n1.position).norm()
	H_right = (n3.position - n2.position).norm()
	
	hinf = (H_left + H_right)/2.0 * L # Height of masonry infill wall
	Linf = (L_bottom + L_top)/2.0 * L # Length of masonry infill wall
	hcol = hinf # assumed equal
	Lcol = Linf # assumed equal
	
	#############################################################################
	# Perform all calculations for the infill assembly
	#############################################################################
	
	# Calculate infill properties
	Icol = 0.5*Ig # Effective cracked moment of inertia of the concrete columns
	rinf = sqrt(hinf**2 + Linf**2) # Diagonal length of the infill
	theta_inf = atan(hinf/Linf) # Angle of the diagonal for the infill
	Ldiag = sqrt(hcol**2 + Lcol**2) # Diagonal length between column centerlines and floor centerlines
	theta_diag = atan(hcol/Lcol) # Angle of the diagonal between beam-column workpoints

	# Calculate the axial stiffness of the infill strut
	# Calculate the width of the compression strut which represents the infill, based on the method
	# given in FEMA 356, Section 7.5.2
	lam1 = ((Em*tinf*sin(2*theta_inf))/(4.0*Efe*Icol*hinf))**(1.0/4.0)
	a = rinf*0.175*(lam1*hcol)**(-0.4)
	kinf = a*tinf*Em/rinf

	# Calculate the required area of the equivalent element, which will span between
	# workpoints and will have an elastic modulus equal to Em
	Aelem = kinf*Ldiag/Em

	# Calculate the axial strength of the infill strut (Based on FEMA356, Section 7.5.2.2)
	An = tinf*Linf # Net bedded area of the infill
	vme = 0.75*(vte+Pce/An)/1.5 # Expected masonry shear strength
	vshear = min(vme, fvie)
	Qce = vshear*An # Expected horizontal shear capacity of infill
	Pn0 = Qce/cos(theta_diag) # Axial capacity of the equivalent compression strut

	# Calculate the in-plane displacement properties of the infill strut:
	# Calculate the "yield point", i.e., the axial deformation in the equivalent strut at the point where
	# the initial tangent stiffness line intersects the element capacity:
	dAy0 = Pn0/kinf #assumes no OOP load
	# Calculate the IP horizontal deflection of the panel at the yield point
	# Note : assumes that the vertical deflections of the endpoints are zero
	uHy0 = dAy0/cos(theta_diag)

	# Calculate the lateral deflection of the panel at the collpase prevention (CP) limit state:
	# Based on FEMA 356, Section 7.5.3.2.4, including Table 7-9.
	# Interpolated in Table 7-9. It is assumed that the CP limit state is
	# reached when the element drift reaches point "d" as shown in Figure 7.1 of FEMA356
	table79x = [0.5, 1.0, 2.0]
	table79y = [0.01, 0.008, 0.006]
	beta = Linf/hinf
	d = np.interp(beta, table79x, table79y)
	uHcp0 = d*hinf # Displacement of the panel at the limit state
	uH0 = uHcp0/uHy0 # Implied ductility at the collapse prevention level

	# Calculate the Out-of-Plane (OOP) parameters of the infill:
	# Calculate the OOP frequency of the infill, assuming that it spans vertically, with
	# simply-supported ends:
	Iinf_g = (Linf*tinf**3)/12.0 # Moment of inertia of the uncracked infill (gross moment)
	Iinf = 0.5*Iinf_g # Estimated moment of inertia of the cracked infill
	winf = Linf*tinf*gamma_inf # Weight per unit of length (measured vertically) of the infill
	# First natural frequency of the infill, spanning in the vertical
	# direction, with top and bottom ends simply supported.
	# (Blevins, 1979, Table 8-1).
	fss = pi/(2.0*hinf**2)*sqrt(Em*Iinf*g/winf)
	per = 1.0/fss

	# Calculate the OOP effective weight:
	# The OOP effective weight is based on the modal effective mass of the vertically spanning,
	# simply supported (assumed) infill wall. For simple-simple conditions, the modal effective
	# weight is equal to 81% of the total infill weight. See Appendix D for a derivation of this value.
	Winf = gamma_inf*tinf*hinf*Linf # Total weight of the infill.
	MASSinf = Winf/g # Total mass of the infill
	# Modal effective weight, assuming that the wall
	# spans vertically, is simply supported top and bottom.
	# (First mode). See Appendix D.
	# This value divide by g is the OOP mass value that
	# should be assigned to the center node
	MEW = 0.81*Winf
	# Calculate the equivalent OOP spring which will provide the identical frequency.
	keq_N = ((2.0*pi*fss)**2) * MEW/g

	# Calculate the moment of inertia of the equivalent beam element, such that it will provide the
	# correct value of keq_N:
	Ieq = keq_N*(Ldiag**3)/(48.0*Em)
	Ielem = Ieq

	# Calculate the OOP Capacity of the infill:
	# The OOP capacity is based on FEMA 356, Section 7.5.3.2.
	# Since this value is outside the range used in FEMA 356, Table 7-11, for determining l,
	# perform an extrapolation:
	# Array of values from Table 7-11:
	table711x = [5.0, 10.0, 15.0, 25.0]
	table711y = [0.129, 0.06, 0.034, 0.013]
	lambda2 = np.interp(hinf/tinf, table711x, table711y)

	# Note: the expected, rather than the lower bound value, of masonry
	# compressive strength is used here, since the expected OOP
	# strength will be used in later calculations.
	qin = 0.7*fme*lambda2/(hinf/tinf)

	# Calculate the moment in the infill wall at the time that it reaches its capacity:
	# Assumes simple support at the top and bottom.
	My = (qin*Linf*hinf**2)/8.0

	# Calculate the required yield moment for the equivalent element, such that the same base
	# motion will bring it and the original wall to incipient yield:
	Meq_y = 1.57*Ldiag/hinf*My # Note: for derivation of this equation, see Appendix D.
	# Defines the OOP "yield" moment for the equivalent
	# member when the IP axial force is zero.
	Mn0 = Meq_y

	# Determine the OOP point force, applied at the midspan of the equivalent element, to cause
	# yielding:
	FNy0 = 4.0*Meq_y/Ldiag

	# Calculate the displacement of the equivalent element at first yield and at the collapse
	# prevention limit state, assuming no IP axial force:
	UNy0 = FNy0/keq_N

	# The displacement at collapse prevention limit state:
	# FEMA 356, Section 7.5.3.3 gives a maximum OOP deflection based on an OOP story drift
	# ratio of 5%.
	UNcp0 = 0.05*hinf

	# This value seems too high, since it's larger than the thickness of the infill itself. Instead, define the
	# CP displacement as equal to one half the thickness of the infill.
	UNcp0 = min(UNcp0, tinf/2.0)

	# The implied ductility ratio is:
	muNcp0 = UNcp0/UNy0

	# This ductility still seems too high. Based on judgment, use a (conservative) ductility of 5:
	muNcp0 = min(muNcp0, 5.0)
	UNcp0 = UNy0*muNcp0

	# Calculating the axial force - moment interaction curve for specific values of Pn0 and Mn0:
	# Ninteraction should be an even number
	if Ninteraction % 2 != 0:
		Ninteraction += 1
	Mn = [0.0]*Ninteraction
	Pn = [0.0]*Ninteraction
	for q in range(Ninteraction):
		Mnq = float(q)*Mn0/float(Ninteraction-1)
		Pnq = Pn0*max(0.0, (1.0-((Mnq/Mn0)**(3.0/2.0))))**(2.0/3.0)
		Mn[q] = Mnq
		Pn[q] = Pnq

	# Calculate the required strength and location of the various fibers:
	Nfiber = 2*(Ninteraction-1)
	Fy = [0.0]*Nfiber
	z = [0.0]*Nfiber
	for p in range(Ninteraction-1):
		Fy[p] = (Pn[p] - Pn[p+1]) / 2.0
		Fy[-p-1] = Fy[p]
		z[p] = (Mn[p+1] - Mn[p])/(2.0*Fy[p])
		z[-p-1] = -z[p]

	# Solve block for the determining the values of the parameters gamma and eta:
	# Estimate the values of the parameters:
	def target_function(x):
		gamma = x[0]
		eta = x[1]
		R1 = 0.0
		R2 = 0.0
		for i in range(Nfiber):
			R1 += gamma*(abs(z[i])**eta)
			R2 += ((gamma*(abs(z[i])**eta))*(z[i]**2))
		R1 -= Aelem
		R2 -= Ielem
		R = np.empty((2))
		R[0] = R1
		R[1] = R2
		return R

	guess = np.array([1.0, 1.0])
	[gamma, eta] = fsolve(target_function, guess)
	A = [gamma*(abs(z[i])**eta) for i in range(Nfiber)]

	# Determine the stress at yield:
	Sy = [Fy[i]/A[i] for i in range(Nfiber)]
	# Calculate the strain at first yield:
	Ey = [Sy[i]/Em for i in range(Nfiber)]
	# Ratio
	Ratio = [Ey[i]/z[i] for i in range(Nfiber)]
	# GJ as a penalty parameter relative to the Em value
	GJ = 10.0**(OM(Em)+8)
	
	# Calculating the IP disp - OOP disp curve for specific values of OOP disp
	OOPv = [0.0]*Ninteraction
	IIPv = [0.0]*Ninteraction
	for i in range(Ninteraction):
		OOPi = float(i)*UNcp0/float(Ninteraction-1)
		IIPi = uHcp0*((1.0-(OOPi/UNcp0)**(3.0/2.0))**(2.0/3.0))
		OOPv[i] = OOPi
		IIPv[i] = IIPi
	
	#############################################################################
	# initialize IDs for dynamically created items
	#############################################################################
	
	# get references to the next available IDs, since here we need
	# to dynamically allocate extra materials/sections/elements that are not in STKO
	node_id = pinfo.next_node_id
	elem_id = pinfo.next_elem_id
	mat_id = pinfo.next_physicalProperties_id
	
	#############################################################################
	# Prepare the assembly model
	#############################################################################
	
	# a utility to write to the current output file using the current indentation
	def write(x):
		pinfo.out_file.write('\n{}{}'.format(pinfo.indent, x))
	
	# make sure the current model builder is for 3D 6DOFs
	pinfo.updateModelBuilder(3, 6)
	# reference to a formatter for double precision numbers
	FMT = pinfo.get_double_formatter()
	
	# write a comment
	write('')
	write('# MasonryInfillWallElement Assembly : generated from STKO quad element {}'.format(elem.id))
	
	# write the section fiber
	fiber_section_id = mat_id # save it for later
	write('section fiberSec {} -GJ {:.2e} {{'.format(mat_id, GJ/(F*L**2))) # open the fiber loop
	# write nonlinear fibers in local Y direction (for OOP bending)
	mat_id += 1
	for i in range(Nfiber):
		write('\t# Fiber {}'.format(i+1))
		write('\tuniaxialMaterial Steel01 {} {} {} 0.02;'.format(mat_id, Sy[i]/P, Em/P))
		write('\tfiber {} 0.0 {} {};'.format(z[i]/L, A[i]/(L**2), mat_id))
		mat_id += 1
	# write 2 dummy (small) fibers in the local Z direction to provide non-zero IP bending stiffness
	write('\t# Add 2 dummy Fibers in Z direction')
	write('\tuniaxialMaterial Elastic {} {};'.format(mat_id, Em/P))
	write('\tlayer straight {0} 2 {1:.2e} 0.0 {2:.2e} 0.0 -{2:.2e};'.format(mat_id, 10.0**(OM(Aelem/(L**2))-6), 10.0**(OM(z[0]/L)-2)))
	mat_id += 1
	write('}') # close the fiber loop
	
	# write elastic section
	write('#elastic section')
	elastic_section_id = mat_id # save it for later
	write('section Elastic {0} {1} {2} {3:.2e} {3:.2e} [expr {1}/2.5] {3:.2e}'.format(mat_id, Em/P, Aelem/(L**2), 10.0**(OM(Aelem/(L**2))-5)))
	mat_id += 1
	
	# write midspan node
	write('# midspan node with OOP mass')
	mnP = (n1.position + n3.position)/2.0 # mid-span node Position
	wallNormal = (n3.position - n1.position).cross(n4.position - n2.position).normalized()
	# we assume the vertical axis is the global Z
	if abs(wallNormal.z) > 1.0e-6:
		raise Exception('MasonryInfillWallElement Error: The infill wall can be customly oriented, but the vertical direction should coincide with the global Z axis')
	mpM = wallNormal * MASSinf
	mpM.x = abs(mpM.x)
	mpM.y = abs(mpM.y)
	mpM.z = abs(mpM.z)
	center_node_id = node_id # save it for later
	write('node {} {} {} {} -mass {} {} {} 0.0 0.0 0.0'.format(node_id, 
		FMT(mnP.x), FMT(mnP.y), FMT(mnP.z), 
		FMT(mpM.x/M), FMT(mpM.y/M), FMT(mpM.z/M)))
	node_id += 1
	
	# write diagonal elements
	ele_id_1 = elem_id
	ele_id_2 = elem_id+1
	elem_id += 2
	write('# transformations')
	write('geomTransf Linear {}  0.0 0.0 1.0'.format(ele_id_1))
	write('geomTransf Linear {}  0.0 0.0 1.0'.format(ele_id_2))
	write('# elements')
	write('element beamWithHinges {0} {1}  {2} {3} [expr {4}*0.1] {10} [expr {4}*0.05] {5} {6} {8} {9}   [expr {5}/2.5] {7} {0}'.format(
		ele_id_1, center_node_id, n1.id, fiber_section_id, rinf/L, Em/P, Aelem/(L**2), GJ/(F*L**2), Ieq/(L**4), 10.0**(OM(Ieq/(L**4))-8), elastic_section_id))
	write('element beamWithHinges {0} {1}  {2} {3} [expr {4}*0.1] {10} [expr {4}*0.05] {5} {6} {8} {9}   [expr {5}/2.5] {7} {0}'.format(
		ele_id_2, center_node_id, n3.id, fiber_section_id, rinf/L, Em/P, Aelem/(L**2), GJ/(F*L**2), Ieq/(L**4), 10.0**(OM(Ieq/(L**4))-8), elastic_section_id))
	
	# write recorders for removal
	# first create a directory for storing the collapse recorders outputs. remove it first, if it already exists.
	# we want to do it only once, so use the pinfo.custom_map to check whether it has been done already
	removal_dir = 'MasonryInfillWallElementRemovalOutput'
	if not 'MasonryInfillWallElement' in pinfo.custom_data:
		# just a value to fill the map
		pinfo.custom_data['MasonryInfillWallElement'] = 1
		# create the removal output directory
		removal_dir_abs = '{}/{}'.format(pinfo.out_dir, removal_dir)
		if os.path.exists(removal_dir_abs):
			shutil.rmtree(removal_dir_abs)
		os.mkdir(removal_dir_abs)
		# only once, remove all previously created files starting with OOP_IIP_curve_wall_*
		for filename in glob.glob('{}/OOP_IIP_curve_wall_*'.format(pinfo.out_dir)):
			print('removing OOP-IIP file: {}'.format(filename))
			os.remove(filename)
	# create the OOP-IIP tcl file needed by the recorder
	OOP_IIP_filename = 'OOP_IIP_curve_wall_{}.tcl'.format(elem.id) # we use the quad element id for this wall file
	with open('{}/{}'.format(pinfo.out_dir, OOP_IIP_filename), 'w', encoding='utf-8') as OOP_IIP_file:
		for i in range(Ninteraction):
			OOP_IIP_file.write('{}\t{}\n'.format(OOPv[i]/L, IIPv[i]/L))
	# write recorders for removal
	write('# recorders for removal')
	write('recorder Collapse -ele {}   -time  -crit INFILLWALL  -file "{}/CollapseSequence.out"  -file_infill "{}" -global_gravaxis 3 -checknodes {} {} {}'.format(
		ele_id_1, removal_dir, OOP_IIP_filename, n1.id, center_node_id, n3.id))
	write('recorder Collapse -ele {}   -time  -crit INFILLWALL  -file_infill "{}" -global_gravaxis 3 -checknodes {} {} {}'.format(
		ele_id_2, OOP_IIP_filename, n1.id, center_node_id, n3.id))
	write('recorder Collapse -ele {} {} -node {}'.format(ele_id_1, ele_id_2, center_node_id))
	
	#############################################################################
	# update IDs for dynamically created items
	#############################################################################
	
	pinfo.next_node_id = node_id
	pinfo.next_elem_id = elem_id
	pinfo.next_physicalProperties_id = mat_id
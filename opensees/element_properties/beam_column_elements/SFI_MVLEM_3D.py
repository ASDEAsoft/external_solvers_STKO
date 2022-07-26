from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def __fillVector(new_size, vect):

	backup_vector = Math.vec(new_size)

	if (len(vect) > 0):
		# store the last value of indexVect in backup_vector
		backup_vector = [vect.valueAt(len(vect)-1)] * new_size
	else:
		# fill the backup_vector with a default value
		backup_vector = [0.0] * new_size

	for i in range(min(len(vect), new_size)):
		backup_vector[i] = vect.valueAt(i)

	vect.resize(new_size, 1)
	vect.referenceValue = backup_vector


def __fillIndexVector(new_size, indexVect):

	if (len(indexVect) > new_size):
		indexVect[:] = indexVect[:new_size]
	else:
		backup_vector = Math.int_array(new_size)

		if (len(indexVect) > 0):
			# store the last value of indexVect in backup_vector
			backup_vector = [indexVect[-1]] * new_size
		else:
			# fill the backup_vector with a default value
			backup_vector = [0] * new_size

		for i in range(min(len(indexVect), new_size)):
			backup_vector[i] = indexVect[i]

		backup_vector[:len(indexVect)] = indexVect[:]
		indexVect[:] = backup_vector[:]


def makeXObjectMetaData():
	
	def mka(name, type, group, body=''):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(body) +
			html_par(html_href("https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/SFI_MVLEM_3D.html?highlight=sfi_mvlem_3d", 'SFI_MVLEM_3D Element')+'<br/>') +
			html_end()
			)
		return a
	
	# m
	at_m = mka('m', MpcAttributeType.Integer, 'Group', 'number of element fibers')
	
	# Thicknesses
	at_Thicknesses = mka('Thicknesses', MpcAttributeType.QuantityVector, 'Group', 'array of m fiber thicknesses')
	
	# Widths
	at_Widths = mka('Widths', MpcAttributeType.QuantityVector, 'Group', 'array of m macro-fiber widths')

	# Material_tags
	at_Material_tags = mka('Material_tags', MpcAttributeType.IndexVector, 'Group', 'array of m macro-fiber nDMaterial (' + html_href('https://opensees.berkeley.edu/wiki/index.php/FSAM_-_2D_RC_Panel_Constitutive_Behavior','FSAM') + ') tags')
	at_Material_tags.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_Material_tags.indexSource.addAllowedNamespace("materials.nD")
	at_Material_tags.indexSource.addAllowedClass("FSAM")
	
	# -CoR
	at_CoR = mka('-CoR', MpcAttributeType.Boolean, 'Optional', 'to activate location of center of rotation from the base')
	
	# c
	at_c = mka('c', MpcAttributeType.QuantityScalar, 'Optional', 'location of center of rotation from the base (optional; default = 0.4 (recommended))')
	at_c.setDefault(0.4)
	
	# -ThickMod
	at_ThickMod = mka('-ThickMod', MpcAttributeType.Boolean, 'Optional', 'to activate thickness multiplier')
	
	# tMod
	at_tMod = mka('tMod', MpcAttributeType.QuantityScalar, 'Optional', 'thickness multiplier (optional; default = 0.63 equivalent to 0.25Ig for out-of-plane bending)')
	at_tMod.setDefault(0.63)
	
	# -Poisson 
	at_Poisson = mka('-Poisson', MpcAttributeType.Boolean, 'Optional', 'to activate Poisson ratio for out-of-plane bending')
	
	# Nu
	at_Nu = mka('Nu', MpcAttributeType.QuantityScalar, 'Optional', 'Poisson ratio for out-of-plane bending (optional; default = 0.25)')
	at_Nu.setDefault(0.25)

	# -Density 
	at_Density = mka('-Density', MpcAttributeType.Boolean, 'Optional', 'to activate Density')
	
	# Dens
	at_Dens = mka('Dens', MpcAttributeType.QuantityScalar, 'Optional', 'Density (optional; default = 0.0)')
	at_Dens.setDefault(0.0)


	xom = MpcXObjectMetaData()
	xom.name = 'SFI_MVLEM_3D'
	xom.addAttribute(at_m)
	xom.addAttribute(at_Thicknesses)
	xom.addAttribute(at_Widths)
	xom.addAttribute(at_Material_tags)
	xom.addAttribute(at_CoR)
	xom.addAttribute(at_c)
	xom.addAttribute(at_ThickMod)
	xom.addAttribute(at_tMod)
	xom.addAttribute(at_Poisson)
	xom.addAttribute(at_Nu)
	xom.addAttribute(at_Density)
	xom.addAttribute(at_Dens)

	xom.setVisibilityDependency(at_CoR, at_c)
	xom.setVisibilityDependency(at_ThickMod, at_tMod)
	xom.setVisibilityDependency(at_Poisson, at_Nu)
	xom.setVisibilityDependency(at_Density, at_Dens)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6),(3,6),(3,6)]	#(ndm, ndf)

def onEditBegin(editor, xobj):
	def geta(name):
		at = xobj.getAttribute(name)
		if(at is None):
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	m = geta('m').integer
	if m < 3:
		m = 3
	onAttributeChanged(editor, xobj, 'm')

def onAttributeChanged(editor, xobj, attribute_name):

	'''
	This method is called everytime the value of an attribute is changed.
	The xobject containing the modified attribute and the attribute name
	are passed as input arguments to this function.
	'''
	def geta(name):
		at = xobj.getAttribute(name)
		if(at is None):
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	attribute = geta(attribute_name)
	new_size = 0
	if attribute_name == 'm':
		new_size = attribute.integer
	elif attribute_name in ('Thicknesses','Widths'):
		new_size = len(attribute.quantityVector.referenceValue)
	elif attribute_name in ('Material_tags'):
		new_size = len(attribute.indexVector)
	else:
		return

	new_size = max(3, new_size)
	geta('m').integer = new_size

	Thicknesses = geta('Thicknesses').quantityVector
	__fillVector(new_size, Thicknesses)

	Widths = geta('Widths').quantityVector
	__fillVector(new_size, Widths)

	Material_tags = geta('Material_tags').indexVector
	__fillIndexVector(new_size, Material_tags)


def writeTcl(pinfo):
	import opensees.element_properties.shell.shell_utils as shelu
	
	# element SFI_MVLEM_3D eleTag iNode jNode kNode lNode m -thick {Thicknesses} -width {Widths} -mat {Material_tags} <-CoR c> <-ThickMod tMod> <-Poisson Nu> <-Density Dens>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	def geta(name):
		at = xobj.getAttribute(name)
		if(at is None):
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	# NODE
	nstr = shelu.getNodeString(elem)
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Quadrilateral or len(elem.nodes)!=4:
		raise Exception('Error: invalid type of element or number of nodes')
	
	# mandatory parameters
	m = geta('m').integer
	
	Thicknesses = geta('Thicknesses').quantityVector
	if len(Thicknesses)!= m:
		raise Exception('Error: different length between Thicknesses vector and number of element fibers')

	Widths = geta('Widths').quantityVector
	if len(Widths)!= m:
		raise Exception('Error: different length between Widths vector and number of element fibers')
	
	Material_tags = geta('Material_tags').indexVector
	if len(Material_tags)!= m:
		raise Exception('Error: different length between Material_tags vector and number of element fibers')

	Thicknesses_str = ''
	Widths_str = ''
	Material_tags_str = ''
	for i in range(m):
		Thicknesses_str += ' {}'.format(Thicknesses.valueAt(i))
		Widths_str += ' {}'.format(Widths.valueAt(i))
		Material_tags_str += ' {}'.format(Material_tags[i])


	# optional paramters
	sopt = ''
	
	if geta('-CoR').boolean:
		sopt += ' -CoR {}'.format(geta('c').quantityScalar)
	
	if geta('-ThickMod').boolean:
		sopt += ' -ThickMod {}'.format(geta('tMod').quantityScalar)
	
	if geta('-Poisson').boolean:
		sopt += ' -Poisson {}'.format(geta('Nu').quantityScalar)
	
	if geta('-Density').boolean:
		sopt += ' -Density {}'.format(geta('Dens').quantityScalar)


	# element SFI_MVLEM_3D eleTag iNode jNode kNode lNode m -thick {Thicknesses} -width {Widths} -mat {Material_tags} <-CoR c> <-ThickMod tMod> <-Poisson Nu> <-Density Dens>
	str_tcl = '{}element SFI_MVLEM_3D {} {} {} -thick{} -width{} -mat{}{}\n'.format(pinfo.indent, tag, nstr, m, Thicknesses_str, Widths_str, Material_tags_str, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.element_properties.utils.geomTransf as gtran

def makeXObjectMetaData():
	
	def mka(name, type, descr):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = 'Default'
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(descr) +
			html_par(html_href('https://opensees.berkeley.edu/wiki/index.php/Elastic_Timoshenko_Beam_Column_Element','Elastic Timoshenko Beam Column Element')+'<br/>') +
			html_end()
		)
		return a
	
	# Dimension
	at_Dimension = mka('Dimension', MpcAttributeType.String, 'choose between 2D and 3D')
	at_Dimension.sourceType = MpcAttributeSourceType.List
	at_Dimension.setSourceList(['2D', '3D'])
	at_Dimension.setDefault('3D')
	
	# 2D
	at_2D = mka('2D', MpcAttributeType.Boolean, '')
	at_2D.editable = False
	
	# 3D
	at_3D = mka('3D', MpcAttributeType.Boolean, '')
	at_3D.editable = False
	
	# transType
	at_transfType = gtran.makeAttribute('Default', name = 'transfType')
	
	# -mass
	at_mass = mka('-mass', MpcAttributeType.Boolean, 'Use element mass density')
	
	# massDens
	at_massDens = mka('massDens', MpcAttributeType.QuantityScalar, 'element mass per unit length (optional, default = 0.0)')
	at_massDens.setDefault(0.0)
	
	# -cMass
	at_cMass = mka('-cMass', MpcAttributeType.Boolean, 'to form consistent mass matrix (optional, default = lumped mass matrix)')
	
	xom = MpcXObjectMetaData()
	xom.name = 'ElasticTimoshenkoBeam'
	xom.addAttribute(at_Dimension)
	xom.addAttribute(at_2D)
	xom.addAttribute(at_3D)
	xom.addAttribute(at_transfType)
	xom.addAttribute(at_mass)
	xom.addAttribute(at_massDens)
	xom.addAttribute(at_cMass)
	
	# visibility dependencies
	
	# massDens-dep
	xom.setVisibilityDependency(at_mass, at_massDens)
	
	# auto-exclusive dependencies
	# 2D or 3D
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_2D)
	xom.setBooleanAutoExclusiveDependency(at_Dimension, at_3D)
	
	# done
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	d = xobj.getAttribute('Dimension').string
	if d == '2D':
		ndm = 2
		ndf = 3
	else:
		ndm = 3
		ndf = 6
	return [(ndm,ndf),(ndm,ndf)]

def writeTcl(pinfo):
	
	#2D
	#element ElasticTimoshenkoBeam $eleTag $iNode $jNode $E $G $A $Iz $Avy $transfTag <-mass $massDens> <-cMass>
	#3D
	#element ElasticTimoshenkoBeam $eleTag $iNode $jNode $E $G $A $Jx $Iy $Iz $Avy $Avz $transfTag <-mass $massDens> <-cMass>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	if (phys_prop.XObject.Xnamespace != 'sections'):
		raise Exception('Error: physical property must be "sections" and not: "{}"'.format(phys_prop.XObject.Xnamespace))
	
	if(phys_prop.XObject.name != 'Elastic'):
		raise Exception('Error: section must be "Elastic" and not "{}"'.format(phys_prop.XObject.name))
	
	if (elem.geometryFamilyType() != MpcElementGeometryFamilyType.Line or len(elem.nodes)!=2):
		raise Exception('Error: invalid type of element or number of nodes')
	
	def geta(xobj, name):
		a = xobj.getAttribute(name)
		if a is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return a
	
	Dimension = geta(xobj, 'Dimension').string
	Dimension_Section = geta(phys_prop.XObject, 'Dimension').string
	if(Dimension != Dimension_Section):
		raise Exception('Error: different dimension between physical property and "Element Property"')
	is_2d = Dimension == '2D'
	Section = geta(phys_prop.XObject, 'Section').customObject
	if Section is None:
		raise Exception('Error: No Elastic Section provided')
	Izz_modifier = geta(phys_prop.XObject, 'Izz_modifier').real
	Iyy_modifier = geta(phys_prop.XObject, 'Iyy_modifier').real
	A = Section.properties.area
	E = geta(phys_prop.XObject, 'E').quantityScalar.value
	G = geta(phys_prop.XObject, 'G/2D' if is_2d else 'G/3D').quantityScalar.value
	J = Section.properties.J
	Avy = Section.properties.alphaY*A
	Avz = Section.properties.alphaZ*A
	Iy = Section.properties.Iyy * Iyy_modifier
	Iz = Section.properties.Izz * Izz_modifier
	if geta(xobj, '-mass').boolean:
		massDens = geta(xobj, 'massDens').quantityScalar.value
		cMass = ' -cMass' if geta(xobj, '-cMass').boolean else ''
		mass = '-mass {}{}'.format(massDens, cMass)
	else:
		mass = ''
	
	if is_2d:
		ndm = 2
		ndf = 3
	else:
		ndm = 3
		ndf = 6
	pinfo.updateModelBuilder(ndm, ndf)
	
	# geometric transformation command
	pinfo.out_file.write(gtran.writeGeomTransf(pinfo, (not is_2d), name = 'transfType'))
	
	# now write the string into the file
	if is_2d:
		pinfo.out_file.write('{}element ElasticTimoshenkoBeam {}   {} {}   {} {} {} {} {}   {}   {}\n'.format(
			pinfo.indent, tag, elem.nodes[0].id, elem.nodes[1].id,
			E, G, A, Iz, Avy, tag, mass))
	else:
		pinfo.out_file.write('{}element ElasticTimoshenkoBeam {}   {} {}   {} {} {} {} {} {} {} {}   {}   {}\n'.format(
			pinfo.indent, tag, elem.nodes[0].id, elem.nodes[1].id,
			E, G, A, J, Iy, Iz, Avy, Avz, tag, mass))
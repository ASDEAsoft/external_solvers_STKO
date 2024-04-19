from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	def mka(name, type, group, description):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(description+'<br/>') +
			html_par(html_href("https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/ASDShellQ4.html", 'ASDShellQ4 Element')+'<br/>') +
			html_end()
			)
		return a
	
	# kinematics
	at_kin = mka('Kinematics', MpcAttributeType.String, 'Group',
		'Linear: small displacement/rotations<br/>Corotational: large displacement/rotations (Geometric Nonlinearity)')
	at_kin.sourceType = MpcAttributeSourceType.List
	at_kin.setSourceList(['Linear', 'Corotational'])
	at_kin.setDefault('Linear')
	
	# eas
	at_eas = mka('Use EAS', MpcAttributeType.Boolean, 'Group',
		'If True (Default) the membrane behavior is enhanced using an Enhanced Assumed Strain filed (EAS)')
	at_eas.setDefault(True)
	
	# drilling stab
	at_dr_type = mka('Drilling DOF Type', MpcAttributeType.String, 'Group',
		'Specify how the Drilling DOF should be treated:Elastic (Default) or Non-Linear (Good for when using strain-softening materials)')
	at_dr_type.sourceType = MpcAttributeSourceType.List
	at_dr_type.setSourceList(['Elastic Drilling DOF', 'Non-Linear Drilling DOF'])
	at_dr_type.setDefault('Elastic Drilling DOF')
	at_dr_elastic = mka('Elastic Drilling DOF', MpcAttributeType.Boolean, 'Group','')
	at_dr_elastic.setDefault(True)
	at_dr_elastic.editable = False
	at_dr = mka('Drilling Stabilization', MpcAttributeType.Real, 'Group',
		'The stabilization parameter (default = 0.01) for the reduced integration of the drilling stiffness (0 <= drillingStab <= 1)')
	at_dr.setDefault(0.01)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDShellQ4'
	xom.addAttribute(at_kin)
	xom.addAttribute(at_eas)
	xom.addAttribute(at_dr_type)
	xom.addAttribute(at_dr_elastic)
	xom.addAttribute(at_dr)
	
	xom.setBooleanAutoExclusiveDependency(at_dr_type, at_dr_elastic)
	xom.setVisibilityDependency(at_dr_elastic, at_dr)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6),(3,6),(3,6)]	#(ndm, ndf)

def writeTcl(pinfo):
	import opensees.element_properties.shell.shell_utils as shelu
	
	# element ASDShellQ4 $tag $iNode $jNoe $kNode $lNode $secTag <-corotational> 
	# <-noeas> <-drillingStab $drillingStab> <-drillingNL> <-local $x1 $x2 $x3>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	secTag = phys_prop.id
	xobj = elem_prop.XObject
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Quadrilateral or len(elem.nodes)!=4:
		raise Exception('Error: invalid type of element or number of nodes')
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh = phys_prop.XObject.Xnamespace
	if namePh != 'sections':
		raise Exception('Error: physical property must be "sections" and not: "{}"'.format(namePh))
	
	def geta(name):
		at = xobj.getAttribute(name)
		if(at is None):
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	# NODE
	nstr = shelu.getNodeString(elem)
	
	# optional paramters
	sopt = ''
	
	if geta('Kinematics').string == 'Corotational':
		sopt += ' -corotational'
	if not geta('Use EAS').boolean:
		sopt += ' -noeas'
	if geta('Drilling DOF Type').string == 'Elastic Drilling DOF':
		sopt += ' -drillingStab {:.6g}'.format(geta('Drilling Stabilization').real)
	else:
		sopt += ' -drillingNL'
	
	# local axes
	uvx = elem.orientation.quaternion.toRotationMatrix().col(0)
	sopt += ' -local {:.6g} {:.6g} {:.6g}'.format(uvx.x, uvx.y, uvx.z)
	
	str_tcl = '{}element ASDShellQ4 {} {} {}{}\n'.format(pinfo.indent, tag, nstr, secTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
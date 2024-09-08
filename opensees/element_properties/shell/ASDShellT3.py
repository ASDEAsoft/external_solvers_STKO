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
			html_par(html_href("https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/ASDShellT3.html", 'ASDShellT3 Element')+'<br/>') +
			html_end()
			)
		return a
	
	# kinematics
	at_kin = mka('Kinematics', MpcAttributeType.String, 'Group',
		'Linear: small displacement/rotations<br/>Corotational: large displacement/rotations (Geometric Nonlinearity)')
	at_kin.sourceType = MpcAttributeSourceType.List
	at_kin.setSourceList(['Linear', 'Corotational'])
	at_kin.setDefault('Linear')
	
	# integration scheme
	at_int = mka('Integration', MpcAttributeType.String, 'Group',
		'<p>The integration scheme:</p>'
		'<ul>'
		'<li><strong>Full (<em>Default</em>)</strong>: 3 integration points in the middle of each edge.</li>'
		'<li><strong>Reduced</strong>: 1 integration point at the centroid. When using this integration scheme, '
		'a drilling stabilization is used to suppress the 2 spurious drilling zero-energy modes. '
		'There will be also 1 spurious zero-energy mode in bending but it is not transmittable. Use with care.</li>'
		'</ul>')
	at_int.sourceType = MpcAttributeSourceType.List
	at_int.setSourceList(['Full', 'Reduced'])
	at_int.setDefault('Full')
	
	# drilling type
	at_dr_type = mka('Drilling DOF Type', MpcAttributeType.String, 'Group',
		'Specify how the Drilling DOF should be treated:Elastic (Default) or Non-Linear (Good when using strain-softening materials)')
	at_dr_type.sourceType = MpcAttributeSourceType.List
	at_dr_type.setSourceList(['Elastic Drilling DOF', 'Non-Linear Drilling DOF'])
	at_dr_type.setDefault('Elastic Drilling DOF')
	
	xom = MpcXObjectMetaData()
	xom.name = 'ASDShellT3'
	xom.addAttribute(at_kin)
	xom.addAttribute(at_int)
	xom.addAttribute(at_dr_type)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6),(3,6)]	#(ndm, ndf)

def _consistency_check(xobj):
	itype = xobj.getAttribute('Integration').string
	reduced = itype == 'Reduced'
	xobj.getAttribute('Drilling DOF Type').visible = reduced

def onEditBegin(editor, xobj):
	_consistency_check(xobj)

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name == 'Integration':
		_consistency_check(xobj)

def writeTcl(pinfo):
	import opensees.element_properties.shell.shell_utils as shelu
	
	# element ASDShellT3 $tag $iNode $jNoe $kNode $secTag <-corotational> 
	# <-reducedIntegration> <-drillingNL> <-local $x1 $x2 $x3>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	secTag = phys_prop.id
	xobj = elem_prop.XObject
	
	if (elem.geometryFamilyType()) != MpcElementGeometryFamilyType.Triangle or len(elem.nodes)!=3:
		raise Exception('ASDShellT3 Error: invalid type of element or number of nodes ({} with {} nodes)'.format(elem.geometryFamilyType(), len(elem.nodes)))
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	namePh = phys_prop.XObject.Xnamespace
	if namePh != 'sections':
		raise Exception('ASDShellT3 Error: physical property must be "sections" and not: "{}"'.format(namePh))
	
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
	if geta('Integration').string == 'Reduced':
		sopt += ' -reducedIntegration'
		if geta('Drilling DOF Type').string == 'Non-Linear Drilling DOF':
			sopt += ' -drillingNL'
	
	# local axes
	uvx = elem.orientation.quaternion.toRotationMatrix().col(0)
	sopt += ' -local {:.6g} {:.6g} {:.6g}'.format(uvx.x, uvx.y, uvx.z)
	
	str_tcl = '{}element ASDShellT3 {} {} {}{}\n'.format(pinfo.indent, tag, nstr, secTag, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	def mka(type, name, group, descr):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href("https://opensees.berkeley.edu/wiki/index.php/Limit_Curve", 'Limit Curve')+'<br/>') +
			html_end()
			)
		return a
	
	eleTag = mka(MpcAttributeType.Index, 'eleTag', 'Reference', 'Tag of zero-length element associated with hinge')
	eleTag.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	
	iNodeTag = mka(MpcAttributeType.Index, 'iNodeTag', 'Reference', 'Tag of node "i" of hinge (used to determine total hinge rotation)')
	iNodeTag.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	
	jNodeTag = mka(MpcAttributeType.Index, 'jNodeTag', 'Reference', 'Tag of node "j" of hinge (used to determine total hinge rotation)')
	jNodeTag.indexSource.type = MpcAttributeIndexSourceType.SelectionSet
	
	dofl = mka(MpcAttributeType.Integer, 'dofl', 'Reference', 'Lateral degree of freedom (used to determine shear demand)')
	dofv = mka(MpcAttributeType.Integer, 'dofv', 'Reference', 'Vertical degree of freedom (used to determine shear demand)')
	
	thetay = mka(MpcAttributeType.Real, 'thetay', 'Material', 'Yield rotation of hinge (rad)')
	a = mka(MpcAttributeType.Real, 'a', 'Material', 'Rotation limit a')
	b = mka(MpcAttributeType.Real, 'b', 'Material', 'Rotation limit b')
	
	xom = MpcXObjectMetaData()
	xom.name = 'RotationStatic'
	
	xom.addAttribute(eleTag)
	xom.addAttribute(iNodeTag)
	xom.addAttribute(jNodeTag)
	xom.addAttribute(dofl)
	xom.addAttribute(dofv)
	
	xom.addAttribute(thetay)
	xom.addAttribute(a)
	xom.addAttribute(b)
	
	return xom

def writeTcl(pinfo):
	
	# limitCurve RotationStatic $curveTag $eleTag $dofl $dofv $iNodeTag $jNodeTag $thetay $a $b
	xobj = pinfo.definition.XObject
	tag = xobj.parent.componentId
	doc = App.caeDocument()
	
	# description
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	def geta(name):
		a = xobj.getAttribute(name)
		if a is None:
			raise Exception('Cannot find "{}" attribute'.format(name))
		return a
	
	def getnode(sset_id, name):
		selection_set = doc.getSelectionSet(sset_id)
		if selection_set is None:
			raise Exception('Error: No selection set specified for the "{}" attribute'.format(name))
		if len(selection_set.geometries) != 1:
			raise Exception('Error: the selection set for the "{}" attribute must contain 1 vertex (found {} geometries)'.format(name, len(selection_set.geometries)))
		for geometry_id, geometry_subset in selection_set.geometries.items():
			mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
			if len(geometry_subset.vertices) != 1: 
				raise Exception('Error: the selection set for the "{}" attribute must contain 1 vertex (found {} vertices)'.format(name, len(geometry_subset.vertices)))
			for domain_id in geometry_subset.vertices:
				node = mesh_of_geom.vertices[domain_id].id
				return node
	
	def getelem(sset_id, name):
		selection_set = doc.getSelectionSet(sset_id)
		if selection_set is None:
			raise Exception('Error: No selection set specified for the "{}" attribute'.format(name))
		if (len(selection_set.geometries) + len(selection_set.interactions)) != 1:
			raise Exception('Error: the selection set for the "{}" attribute must contain 1 element (found {} geometries and {} interactions)'.format(name, len(selection_set.geometries), len(selection_set.interactions)))
		element = None
		for geometry_id, geometry_subset in selection_set.geometries.items():
			mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
			for domain_id in geometry_subset.edges:
				domain = mesh_of_geom.edges[domain_id]
				for ele in domain.elements:
					if element is not None:
						raise Exception('Error: Multiple elements found in the selection set for the "{}" attribute. It must contain only 1 element'.format(name))
					element = ele.id
		for interaction_id in selection_set.interactions:
			mesh_of_inter = doc.mesh.meshedInteractions[interaction_id]
			for ele in mesh_of_inter.elements:
				if element is not None:
					raise Exception('Error: Multiple elements found in the selection set for the "{}" attribute. It must contain only 1 element'.format(name))
				element = ele.id
		return element
	
	eleTag = getelem(geta('eleTag').index, 'eleTag')
	iNodeTag = getnode(geta('iNodeTag').index, 'iNodeTag')
	jNodeTag = getnode(geta('jNodeTag').index, 'jNodeTag')
	dofl = geta('dofl').integer
	dofv = geta('dofv').integer
	thetay = geta('thetay').real
	a = geta('a').real
	b = geta('b').real
	
	# now write the string into the file
	pinfo.out_file.write(
		'{}limitCurve RotationStatic {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, eleTag, dofl, dofv, iNodeTag, jNodeTag,
			thetay, a, b
			)
	)
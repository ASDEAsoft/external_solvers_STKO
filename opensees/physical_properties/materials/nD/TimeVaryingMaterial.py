import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

class _globals:
	targets = ['Time', 'E', 'K', 'A']

def _check_consistency(xobj, at, targets):
	if at is None:
		at = xobj.getAttribute(targets[0])
		for i in range(1, len(targets)):
			iat = xobj.getAttribute(targets[i])
			if len(iat.quantityVector.referenceValue) > len(at.quantityVector.referenceValue):
				at = iat
	n = len(at.quantityVector.referenceValue)
	for i in targets:
		iat = xobj.getAttribute(i)
		ival = iat.quantityVector.referenceValue
		if len(ival) != n:
			new_ival = Math.vec(n)
			nmin = min(n, len(ival))
			for j in range(nmin):
				new_ival[j] = ival[j]
			iat.quantityVector.referenceValue = new_ival

def onEditBegin(editor, xobj):
	_check_consistency(xobj, None, _globals.targets)

def onAttributeChanged(editor, xobj, attribute_name):
	if attribute_name in _globals.targets:
		_check_consistency(xobj, xobj.getAttribute(attribute_name), _globals.targets)

def makeXObjectMetaData():
	
	def mka(name, type, group, description, dval=None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext('TimeVaryingMaterial')+'<br/>') + 
			html_par(description) +
			html_par(html_href('https://opensees.github.io/OpenSeesDocumentation/user/manual/material/ndMaterials/ASDConcrete3D.html','ASDConcrete3D')+'<br/>') + #TODO: change
			html_end()
			)
		if dval:
			a.setDefault(dval)
		return a
	
	source = mka('Source', MpcAttributeType.Index, 'Default', 'The source wrapped material')
	source.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	source.indexSource.addAllowedNamespace('materials.nD')
	T = mka("Time", MpcAttributeType.QuantityVector, 'Default', 'List of time values')
	E = mka("E", MpcAttributeType.QuantityVector, 'Default', "List of time Young's modulus values")
	K = mka("K", MpcAttributeType.QuantityVector, 'Default', "List of time Bulk modulus values")
	A = mka("A", MpcAttributeType.QuantityVector, 'Default', "List of time strength ratio values")
	
	xom = MpcXObjectMetaData()
	xom.name = 'TimeVaryingMaterial'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(source)
	xom.addAttribute(T)
	xom.addAttribute(E)
	xom.addAttribute(K)
	xom.addAttribute(A)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial TimeVarying $tag $otherTag $N $list_T $list_E $list_K $list_A
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
		
	# mandatory parameters
	source = geta('Source').index
	T = geta('Time').quantityVector.value
	K = geta('K').quantityVector.value
	E = geta('E').quantityVector.value
	A = geta('A').quantityVector.value
	n = len(T)
	
	# TODO: do checks
	str_tcl = '{0}nDMaterial TimeVarying {2} {3}    {4} \\\n{0}{1}{5}  \\\n{0}{1}{6}  \\\n{0}{1}{7}  \\\n{0}{1}{8}\n'.format(
		pinfo.indent, pinfo.tabIndent, tag, source, n,
		' '.join(str(i) for i in T),
		' '.join(str(i) for i in E),
		' '.join(str(i) for i in K),
		' '.join(str(i) for i in A)
		)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
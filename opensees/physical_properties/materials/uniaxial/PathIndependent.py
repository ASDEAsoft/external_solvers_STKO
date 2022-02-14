import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
    
	def mka(name, group, descr, atype, adim = None, dval = None):
		a = MpcAttributeMetaData()
		a.type = atype
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('','PathIndependent')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a

	matTag = mka("matTag", "Group", "Material tag for uniaxial materials", MpcAttributeType.Index)
	matTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	matTag.indexSource.addAllowedNamespace('materials.uniaxial')

	xom = MpcXObjectMetaData()
	xom.name = 'PathIndependent'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(matTag)

	return xom

def writeTcl(pinfo):
	# uniaxialMaterial PathIndependent tag? matTag?
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# utils
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at

	# uniaxialMaterial PathIndependent tag? matTag?
	str_tcl = '{}uniaxialMaterial PathIndependent {} {}\n'.format(
		pinfo.indent,
		tag,
		geta('matTag').index)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
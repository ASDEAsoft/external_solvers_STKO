import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin


def makeXObjectMetaData():
	
	# nDMatTag
	at_nDMatTag = MpcAttributeMetaData()
	at_nDMatTag.type = MpcAttributeType.Index
	at_nDMatTag.name = 'nDMatTag'
	at_nDMatTag.group = 'Non linear'
	at_nDMatTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nDMatTag')+'<br/>') + 
		html_par('the tag of the associated nDMaterial object') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/InitialStateAnalysisWrapper','InitialStateAnalysisWrapper')+'<br/>') +
		html_end()
		)
	at_nDMatTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_nDMatTag.indexSource.addAllowedNamespace('materials.nD')
	
	# nDim
	at_nDim = MpcAttributeMetaData()
	at_nDim.type = MpcAttributeType.Integer
	at_nDim.name = 'nDim'
	at_nDim.group = 'Non linear'
	at_nDim.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nDim')+'<br/>') + 
		html_par('number of dimensions (2 for 2D, 3 for 3D)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/InitialStateAnalysisWrapper','InitialStateAnalysisWrapper')+'<br/>') +
		html_end()
		)
	at_nDim.sourceType = MpcAttributeSourceType.List
	at_nDim.setSourceList([2, 3])
	at_nDim.setDefault(2)
	
	xom = MpcXObjectMetaData()
	xom.name = 'InitialStateAnalysisWrapper'
	xom.Xgroup = 'Wrapper material for Initial State Analysis'
	xom.addAttribute(at_nDMatTag)
	xom.addAttribute(at_nDim)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial InitialStateAnalysisWrapper $matTag $nDMatTag $nDim
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	nDMatTag_at = xobj.getAttribute('nDMatTag')
	if(nDMatTag_at is None):
		raise Exception('Error: cannot find "nDMatTag" attribute')
	nDMatTag = nDMatTag_at.index
	
	nDim_at = xobj.getAttribute('nDim')
	if(nDim_at is None):
		raise Exception('Error: cannot find "nDim" attribute')
	ndm = nDim_at.integer
	
	str_tcl = '{}nDMaterial InitialStateAnalysisWrapper {} {} {}\n'.format(pinfo.indent, tag, nDMatTag, ndm)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
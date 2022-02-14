import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# nd
	at_nd = MpcAttributeMetaData()
	at_nd.type = MpcAttributeType.Integer
	at_nd.name = 'nd'
	at_nd.group = 'Non-linear'
	at_nd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nd')+'<br/>') + 
		html_par('Number of dimensions, 2 for plane-strain, and 3 for general 3D analysis.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FluidSolidPorousMaterial','FluidSolidPorousMaterial')+'<br/>') +
		html_end()
		)
	at_nd.sourceType = MpcAttributeSourceType.List
	at_nd.setSourceList([2, 3])
	at_nd.setDefault(2)
	
	# soilMatTag
	at_soilMatTag = MpcAttributeMetaData()
	at_soilMatTag.type = MpcAttributeType.Index
	at_soilMatTag.name = 'soilMatTag'
	at_soilMatTag.group = 'Non-linear'
	at_soilMatTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('soilMatTag')+'<br/>') + 
		html_par('The material number for the solid phase material (previously defined).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FluidSolidPorousMaterial','FluidSolidPorousMaterial')+'<br/>') +
		html_end()
		)
	at_soilMatTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_soilMatTag.indexSource.addAllowedNamespace('materials.nD')
	
	# combinedBulkModul
	at_combinedBulkModul = MpcAttributeMetaData()
	at_combinedBulkModul.type = MpcAttributeType.QuantityScalar
	at_combinedBulkModul.name = 'combinedBulkModul'
	at_combinedBulkModul.group = 'Non-linear'
	at_combinedBulkModul.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('combinedBulkModul')+'<br/>') + 
		html_par('Combined undrained bulk modulus Bc relating changes in pore pressure and volumetric strain, may be approximated by:') +
		html_par('Bc ≈ Bf /n') +
		html_par('where Bf is the bulk modulus of fluid phase (2.2x106 kPa (or 3.191x105 psi) for water), and n the initial porosity.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FluidSolidPorousMaterial','FluidSolidPorousMaterial')+'<br/>') +
		html_end()
		)
	at_combinedBulkModul.dimension = u.F/u.L**2
	
	# use_pa
	at_use_pa = MpcAttributeMetaData()
	at_use_pa.type = MpcAttributeType.Boolean
	at_use_pa.name = 'use_pa'
	at_use_pa.group = 'Non-linear'
	at_use_pa.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_pa')+'<br/>') + 
		html_par('Optional atmospheric pressure for normalization (typically 101 kPa in SI units, or 14.65 psi in English units)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FluidSolidPorousMaterial','FluidSolidPorousMaterial')+'<br/>') +
		html_end()
		)
	
	# pa
	at_pa = MpcAttributeMetaData()
	at_pa.type = MpcAttributeType.QuantityScalar
	at_pa.name = 'pa'
	at_pa.group = 'Optional parameter'
	at_pa.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('pa')+'<br/>') + 
		html_par('Optional atmospheric pressure for normalization (typically 101 kPa in SI units, or 14.65 psi in English units)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/FluidSolidPorousMaterial','FluidSolidPorousMaterial')+'<br/>') +
		html_end()
		)
	at_pa.setDefault(101)
	at_pa.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'FluidSolidPorousMaterial'
	xom.Xgroup = 'UC San Diego Saturated Undrained soil'
	xom.addAttribute(at_nd)
	xom.addAttribute(at_soilMatTag)
	xom.addAttribute(at_combinedBulkModul)
	xom.addAttribute(at_use_pa)
	xom.addAttribute(at_pa)
	
	# use_pa-dep
	xom.setVisibilityDependency(at_use_pa, at_pa)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial FluidSolidPorousMaterial $tag $nd $soilMatTag $combinedBulkModul <$pa=101>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	nd_at = xobj.getAttribute('nd')
	if(nd_at is None):
		raise Exception('Error: cannot find "nd" attribute')
	nd = nd_at.integer
	
	soilMatTag_at = xobj.getAttribute('soilMatTag')
	if(soilMatTag_at is None):
		raise Exception('Error: cannot find "soilMatTag" attribute')
	soilMatTag = soilMatTag_at.index
	
	combinedBulkModul_at = xobj.getAttribute('combinedBulkModul')
	if(combinedBulkModul_at is None):
		raise Exception('Error: cannot find "combinedBulkModul" attribute')
	combinedBulkModul = combinedBulkModul_at.quantityScalar
	
	# optional paramters
	sopt = ''
	
	use_pa_at = xobj.getAttribute('use_pa')
	if(use_pa_at is None):
		raise Exception('Error: cannot find "use_pa" attribute')
	use_pa = use_pa_at.boolean
	if use_pa:
		pa_at = xobj.getAttribute('pa')
		if(pa_at is None):
			raise Exception('Error: cannot find "pa" attribute')
		pa = pa_at.quantityScalar
		
		sopt += '{}'.format(pa.value)
	
	str_tcl = '{}nDMaterial FluidSolidPorous {} {} {} {} {}\n'.format(
			pinfo.indent, tag, nd, soilMatTag, combinedBulkModul.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
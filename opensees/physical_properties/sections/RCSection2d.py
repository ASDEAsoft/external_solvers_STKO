import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# coreTag
	at_coreTag = MpcAttributeMetaData()
	at_coreTag.type = MpcAttributeType.Index
	at_coreTag.name = 'coreTag'
	at_coreTag.group = 'Group'
	at_coreTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('coreTag')+'<br/>') + 
		html_par('tag of uniaxialMaterial assigned to each fiber in the core region') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	at_coreTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_coreTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# coverTag
	at_coverTag = MpcAttributeMetaData()
	at_coverTag.type = MpcAttributeType.Index
	at_coverTag.name = 'coverTag'
	at_coverTag.group = 'Group'
	at_coverTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('coverTag')+'<br/>') + 
		html_par('tag of uniaxialMaterial assigned to each fiber in the cover region') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	at_coverTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_coverTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# steelTag
	at_steelTag = MpcAttributeMetaData()
	at_steelTag.type = MpcAttributeType.Index
	at_steelTag.name = 'steelTag'
	at_steelTag.group = 'Group'
	at_steelTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('steelTag')+'<br/>') + 
		html_par('tag of uniaxialMaterial assigned to each reinforcing bar') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	at_steelTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_steelTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# d
	at_d = MpcAttributeMetaData()
	at_d.type = MpcAttributeType.QuantityScalar
	at_d.name = 'd'
	at_d.group = 'Group'
	at_d.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('d')+'<br/>') + 
		html_par('section depth') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	at_d.dimension = u.L
	
	# b
	at_b = MpcAttributeMetaData()
	at_b.type = MpcAttributeType.QuantityScalar
	at_b.name = 'b'
	at_b.group = 'Group'
	at_b.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b')+'<br/>') + 
		html_par('section width') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	at_b.dimension = u.L
	
	# cover
	at_cover = MpcAttributeMetaData()
	at_cover.type = MpcAttributeType.QuantityScalar
	at_cover.name = 'cover'
	at_cover.group = 'Group'
	at_cover.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cover')+'<br/>') + 
		html_par('cover depth (assumed uniform around perimeter)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	at_cover.dimension = u.L
	
	# Atop
	at_Atop = MpcAttributeMetaData()
	at_Atop.type = MpcAttributeType.QuantityScalar
	at_Atop.name = 'Atop'
	at_Atop.group = 'Group'
	at_Atop.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Atop')+'<br/>') + 
		html_par('area of reinforcing bars in top layer') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	at_Atop.dimension = u.L**2
	
	# Abot
	at_Abot = MpcAttributeMetaData()
	at_Abot.type = MpcAttributeType.QuantityScalar
	at_Abot.name = 'Abot'
	at_Abot.group = 'Group'
	at_Abot.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Abot')+'<br/>') + 
		html_par('area of reinforcing bars in bottom layer') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	at_Abot.dimension = u.L**2
	
	# Aside
	at_Aside = MpcAttributeMetaData()
	at_Aside.type = MpcAttributeType.QuantityScalar
	at_Aside.name = 'Aside'
	at_Aside.group = 'Group'
	at_Aside.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Aside')+'<br/>') + 
		html_par('area of reinforcing bars on intermediate layers') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	at_Aside.dimension = u.L**2
	
	# Nfcore
	at_Nfcore = MpcAttributeMetaData()
	at_Nfcore.type = MpcAttributeType.Integer
	at_Nfcore.name = 'Nfcore'
	at_Nfcore.group = 'Group'
	at_Nfcore.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Nfcore')+'<br/>') + 
		html_par('number of fibers through the core depth') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	
	# Nfcover
	at_Nfcover = MpcAttributeMetaData()
	at_Nfcover.type = MpcAttributeType.Integer
	at_Nfcover.name = 'Nfcover'
	at_Nfcover.group = 'Group'
	at_Nfcover.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Nfcover')+'<br/>') + 
		html_par('number of fibers through the cover depth') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	
	# Nfs
	at_Nfs = MpcAttributeMetaData()
	at_Nfs.type = MpcAttributeType.Integer
	at_Nfs.name = 'Nfs'
	at_Nfs.group = 'Group'
	at_Nfs.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Nfs')+'<br/>') + 
		html_par('number of bars on the top and bottom rows of reinforcement (Nfs-2 bars will be placed on the side rows)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/RC_Section','RC Section')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'RCSection2d'
	xom.addAttribute(at_coreTag)
	xom.addAttribute(at_coverTag)
	xom.addAttribute(at_steelTag)
	xom.addAttribute(at_d)
	xom.addAttribute(at_b)
	xom.addAttribute(at_cover)
	xom.addAttribute(at_Atop)
	xom.addAttribute(at_Abot)
	xom.addAttribute(at_Aside)
	xom.addAttribute(at_Nfcore)
	xom.addAttribute(at_Nfcover)
	xom.addAttribute(at_Nfs)
	
	return xom

def writeTcl(pinfo):
	
	#section RCSection2d $secTag $coreTag $coverTag $steelTag $d $b $cover $Atop $Abot $Aside $Nfcore $Nfcover $Nfs
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	coreTag_at = xobj.getAttribute('coreTag')
	if(coreTag_at is None):
		raise Exception('Error: cannot find "coreTag" attribute')
	coreTag = coreTag_at.index
	
	coverTag_at = xobj.getAttribute('coverTag')
	if(coverTag_at is None):
		raise Exception('Error: cannot find "coverTag" attribute')
	coverTag = coverTag_at.index
	
	steelTag_at = xobj.getAttribute('steelTag')
	if(steelTag_at is None):
		raise Exception('Error: cannot find "steelTag" attribute')
	steelTag = steelTag_at.index
	
	d_at = xobj.getAttribute('d')
	if(d_at is None):
		raise Exception('Error: cannot find "d" attribute')
	d = d_at.quantityScalar
	
	b_at = xobj.getAttribute('b')
	if(b_at is None):
		raise Exception('Error: cannot find "b" attribute')
	b = b_at.quantityScalar
	
	cover_at = xobj.getAttribute('cover')
	if(cover_at is None):
		raise Exception('Error: cannot find "cover" attribute')
	cover = cover_at.quantityScalar
	
	Atop_at = xobj.getAttribute('Atop')
	if(Atop_at is None):
		raise Exception('Error: cannot find "Atop" attribute')
	Atop = Atop_at.quantityScalar
	
	Abot_at = xobj.getAttribute('Abot')
	if(Abot_at is None):
		raise Exception('Error: cannot find "Abot" attribute')
	Abot = Abot_at.quantityScalar
	
	Aside_at = xobj.getAttribute('Aside')
	if(Aside_at is None):
		raise Exception('Error: cannot find "Aside" attribute')
	Aside = Aside_at.quantityScalar
	
	Nfcore_at = xobj.getAttribute('Nfcore')
	if(Nfcore_at is None):
		raise Exception('Error: cannot find "Nfcore" attribute')
	Nfcore = Nfcore_at.integer
	
	Nfcover_at = xobj.getAttribute('Nfcover')
	if(Nfcover_at is None):
		raise Exception('Error: cannot find "Nfcover" attribute')
	Nfcover = Nfcover_at.integer
	
	Nfs_at = xobj.getAttribute('Nfs')
	if(Nfs_at is None):
		raise Exception('Error: cannot find "Nfs" attribute')
	Nfs = Nfs_at.integer
	
	
	
	str_tcl = '{}section RCSection2d {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, coreTag, coverTag, steelTag, d.value, b.value, cover.value,
			Atop.value, Abot.value, Aside.value, Nfcore, Nfcover, Nfs)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
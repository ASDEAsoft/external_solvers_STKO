import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# matTag
	at_matTag = MpcAttributeMetaData()
	at_matTag.type = MpcAttributeType.Index
	at_matTag.name = 'matTag'
	at_matTag.group = 'Group'
	at_matTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('matTag')+'<br/>') + 
		html_par('tag of uniaxialMaterial assigned to each fiber') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Wide_Flange_Section','Wide Flange Section')+'<br/>') +
		html_end()
		)
	at_matTag.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_matTag.indexSource.addAllowedNamespace('materials.uniaxial')
	
	# d
	at_d = MpcAttributeMetaData()
	at_d.type = MpcAttributeType.QuantityScalar
	at_d.name = 'd'
	at_d.group = 'Group'
	at_d.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('d')+'<br/>') + 
		html_par('section depth') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Wide_Flange_Section','Wide Flange Section')+'<br/>') +
		html_end()
		)
	at_d.dimension = u.L
	
	# tw
	at_tw = MpcAttributeMetaData()
	at_tw.type = MpcAttributeType.QuantityScalar
	at_tw.name = 'tw'
	at_tw.group = 'Group'
	at_tw.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tw')+"<br/>") + 
		html_par('web thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Wide_Flange_Section','Wide Flange Section')+'<br/>') +
		html_end()
		)
	at_tw.dimension = u.L
	
	# bf
	at_bf = MpcAttributeMetaData()
	at_bf.type = MpcAttributeType.QuantityScalar
	at_bf.name = 'bf'
	at_bf.group = 'Group'
	at_bf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('bf')+'<br/>') + 
		html_par('flange width') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Wide_Flange_Section','Wide Flange Section')+'<br/>') +
		html_end()
		)
	at_bf.dimension = u.L
	
	# tf
	at_tf = MpcAttributeMetaData()
	at_tf.type = MpcAttributeType.QuantityScalar
	at_tf.name = 'tf'
	at_tf.group = 'Group'
	at_tf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tf')+'<br/>') + 
		html_par('flange thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Wide_Flange_Section','Wide Flange Section')+'<br/>') +
		html_end()
		)
	at_tf.dimension = u.L
	
	# Nfw
	at_Nfw = MpcAttributeMetaData()
	at_Nfw.type = MpcAttributeType.Integer
	at_Nfw.name = 'Nfw'
	at_Nfw.group = 'Group'
	at_Nfw.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Nfw')+'<br/>') + 
		html_par('number of fibers in the web') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Wide_Flange_Section','Wide Flange Section')+'<br/>') +
		html_end()
		)
	
	# Nff
	at_Nff = MpcAttributeMetaData()
	at_Nff.type = MpcAttributeType.Integer
	at_Nff.name = 'Nff'
	at_Nff.group = 'Group'
	at_Nff.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Nff')+'<br/>') + 
		html_par('number of fibers in each flange') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Wide_Flange_Section','Wide Flange Section')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'WFSection2d'
	xom.addAttribute(at_matTag)
	xom.addAttribute(at_d)
	xom.addAttribute(at_tw)
	xom.addAttribute(at_bf)
	xom.addAttribute(at_tf)
	xom.addAttribute(at_Nfw)
	xom.addAttribute(at_Nff)
	
	return xom

def writeTcl(pinfo):
	
	#section WFSection2d $secTag $matTag $d $tw $bf $tf $Nfw $Nff
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	matTag_at = xobj.getAttribute('matTag')
	if(matTag_at is None):
		raise Exception('Error: cannot find "matTag" attribute')
	matTag = matTag_at.index
	
	d_at = xobj.getAttribute('d')
	if(d_at is None):
		raise Exception('Error: cannot find "d" attribute')
	d = d_at.quantityScalar
	
	tw_at = xobj.getAttribute('tw')
	if(tw_at is None):
		raise Exception('Error: cannot find "tw" attribute')
	tw = tw_at.quantityScalar
	
	bf_at = xobj.getAttribute('bf')
	if(bf_at is None):
		raise Exception('Error: cannot find "bf" attribute')
	bf = bf_at.quantityScalar
	
	tf_at = xobj.getAttribute('tf')
	if(tf_at is None):
		raise Exception('Error: cannot find "tf" attribute')
	tf = tf_at.quantityScalar
	
	Nfw_at = xobj.getAttribute('Nfw')
	if(Nfw_at is None):
		raise Exception('Error: cannot find "Nfw" attribute')
	Nfw = Nfw_at.integer
	
	Nff_at = xobj.getAttribute('Nff')
	if(Nff_at is None):
		raise Exception('Error: cannot find "Nff" attribute')
	Nff = Nff_at.integer
	
	
	str_tcl = '{}section WFSection2d {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, matTag, d.value, tw.value, bf.value, tf.value, Nfw, Nff)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
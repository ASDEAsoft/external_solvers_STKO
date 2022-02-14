# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# height
	at_height = MpcAttributeMetaData()
	at_height.type = MpcAttributeType.QuantityScalar
	at_height.name = 'height'
	at_height.group = 'Non-linear'
	at_height.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('height')+'<br/>') + 
		html_par('SWP’s height') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_height.dimension = u.L
	
	# width
	at_width = MpcAttributeMetaData()
	at_width.type = MpcAttributeType.QuantityScalar
	at_width.name = 'width'
	at_width.group = 'Non-linear'
	at_width.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('width')+'<br/>') + 
		html_par('SWP’s width') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_width.dimension = u.L
	
	# fuf
	at_fuf = MpcAttributeMetaData()
	at_fuf.type = MpcAttributeType.QuantityScalar
	at_fuf.name = 'fuf'
	at_fuf.group = 'Non-linear'
	at_fuf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fuf')+'<br/>') + 
		html_par('Tensile strength of framing members') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_fuf.dimension = u.F/u.L**2
	
	# tf
	at_tf = MpcAttributeMetaData()
	at_tf.type = MpcAttributeType.QuantityScalar
	at_tf.name = 'tf'
	at_tf.group = 'Non-linear'
	at_tf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tf')+'<br/>') + 
		html_par('Framing thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_tf.dimension = u.L
	
	# Ife
	at_Ife = MpcAttributeMetaData()
	at_Ife.type = MpcAttributeType.QuantityScalar
	at_Ife.name = 'Ife'
	at_Ife.group = 'Non-linear'
	at_Ife.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ife')+'<br/>') + 
		html_par('Moment of inertia of the double end-stud') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_Ife.dimension = u.L**4
	
	# Ifi
	at_Ifi = MpcAttributeMetaData()
	at_Ifi.type = MpcAttributeType.QuantityScalar
	at_Ifi.name = 'Ifi'
	at_Ifi.group = 'Non-linear'
	at_Ifi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ifi')+'<br/>') + 
		html_par('Moment of inertia of the intermediate stud') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_Ifi.dimension = u.L**4
	
	# ts
	at_ts = MpcAttributeMetaData()
	at_ts.type = MpcAttributeType.QuantityScalar
	at_ts.name = 'ts'
	at_ts.group = 'Non-linear'
	at_ts.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ts')+'<br/>') + 
		html_par('Sheathing thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_ts.dimension = u.L
	
	# np
	at_np = MpcAttributeMetaData()
	at_np.type = MpcAttributeType.Integer
	at_np.name = 'np'
	at_np.group = 'Non-linear'
	at_np.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('np')+'<br/>') + 
		html_par('Sheathing number (one or two sides sheathed)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	
	# ds
	at_ds = MpcAttributeMetaData()
	at_ds.type = MpcAttributeType.QuantityScalar
	at_ds.name = 'ds'
	at_ds.group = 'Non-linear'
	at_ds.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ds')+'<br/>') + 
		html_par('Screws diameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_ts.dimension = u.L
	
	# Vs
	at_Vs = MpcAttributeMetaData()
	at_Vs.type = MpcAttributeType.QuantityScalar
	at_Vs.name = 'Vs'
	at_Vs.group = 'Non-linear'
	at_Vs.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Vs')+'<br/>') + 
		html_par('Screws shear strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_Vs.dimension = u.F
	
	# sc
	at_sc = MpcAttributeMetaData()
	at_sc.type = MpcAttributeType.QuantityScalar
	at_sc.name = 'sc'
	at_sc.group = 'Non-linear'
	at_sc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sc')+'<br/>') + 
		html_par('Screw spacing on the SWP perimeter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_sc.dimension = u.L
	
	# nc
	at_nc = MpcAttributeMetaData()
	at_nc.type = MpcAttributeType.Integer
	at_nc.name = 'nc'
	at_nc.group = 'Non-linear'
	at_nc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nc')+'<br/>') + 
		html_par('Total number of screws located on the SWP perimeter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	
	# type
	at_type = MpcAttributeMetaData()
	at_type.type = MpcAttributeType.Integer
	at_type.name = 'type'
	at_type.group = 'Non-linear'
	at_type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('type')+'<br/>') + 
		html_par('Integer identifier used to define wood sheathing type (DFP=1, OSB=2, CSP=3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_type.sourceType = MpcAttributeSourceType.List
	at_type.setSourceList([1, 2, 3])
	at_type.setDefault(1)
	
	# openingArea
	at_openingArea = MpcAttributeMetaData()
	at_openingArea.type = MpcAttributeType.QuantityScalar
	at_openingArea.name = 'openingArea'
	at_openingArea.group = 'Non-linear'
	at_openingArea.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('openingArea')+'<br/>') + 
		html_par('Total area of openings') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_openingArea.dimension = u.L**2
	
	# openingLength
	at_openingLength = MpcAttributeMetaData()
	at_openingLength.type = MpcAttributeType.QuantityScalar
	at_openingLength.name = 'openingLength'
	at_openingLength.group = 'Non-linear'
	at_openingLength.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('openingLength')+'<br/>') + 
		html_par('Cumulative length of openings') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSWSWP','CFSWSWP')+'<br/>') +
		html_end()
		)
	at_openingLength.dimension = u.L
	
	xom = MpcXObjectMetaData()
	xom.name = 'CFSWSWP'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_height)
	xom.addAttribute(at_width)
	xom.addAttribute(at_fuf)
	xom.addAttribute(at_tf)
	xom.addAttribute(at_Ife)
	xom.addAttribute(at_Ifi)
	xom.addAttribute(at_ts)
	xom.addAttribute(at_np)
	xom.addAttribute(at_ds)
	xom.addAttribute(at_Vs)
	xom.addAttribute(at_sc)
	xom.addAttribute(at_nc)
	xom.addAttribute(at_type)
	xom.addAttribute(at_openingArea)
	xom.addAttribute(at_openingLength)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial CFSWSWP $tag $height $width $fut $tf $Ife $Ifi $ts $np $ds $Vs $sc $nc $type $openingArea $openingLength
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	height_at = xobj.getAttribute('height')
	if(height_at is None):
		raise Exception('Error: cannot find "height" attribute')
	height = height_at.quantityScalar
	
	width_at = xobj.getAttribute('width')
	if(width_at is None):
		raise Exception('Error: cannot find "width" attribute')
	width = width_at.quantityScalar
	
	fut_at = xobj.getAttribute('fuf')
	if(fut_at is None):
		raise Exception('Error: cannot find "fuf" attribute')
	fut = fut_at.quantityScalar
	
	tf_at = xobj.getAttribute('tf')
	if(tf_at is None):
		raise Exception('Error: cannot find "tf" attribute')
	tf = tf_at.quantityScalar
	
	Ife_at = xobj.getAttribute('Ife')
	if(Ife_at is None):
		raise Exception('Error: cannot find "Ife" attribute')
	Ife = Ife_at.quantityScalar
	
	Ifi_at = xobj.getAttribute('Ifi')
	if(Ifi_at is None):
		raise Exception('Error: cannot find "Ifi" attribute')
	Ifi = Ifi_at.quantityScalar
	
	ts_at = xobj.getAttribute('ts')
	if(ts_at is None):
		raise Exception('Error: cannot find "ts" attribute')
	ts = ts_at.quantityScalar
	
	np_at = xobj.getAttribute('np')
	if(np_at is None):
		raise Exception('Error: cannot find "np" attribute')
	np = np_at.integer
	
	ds_at = xobj.getAttribute('ds')
	if(ds_at is None):
		raise Exception('Error: cannot find "ds" attribute')
	ds = ds_at.quantityScalar
	
	Vs_at = xobj.getAttribute('Vs')
	if(Vs_at is None):
		raise Exception('Error: cannot find "Vs" attribute')
	Vs = Vs_at.quantityScalar
	
	sc_at = xobj.getAttribute('sc')
	if(sc_at is None):
		raise Exception('Error: cannot find "sc" attribute')
	sc = sc_at.quantityScalar
	
	nc_at = xobj.getAttribute('nc')
	if(nc_at is None):
		raise Exception('Error: cannot find "nc" attribute')
	nc = nc_at.integer
	
	type_at = xobj.getAttribute('type')
	if(type_at is None):
		raise Exception('Error: cannot find "type" attribute')
	type = type_at.integer
	
	openingArea_at = xobj.getAttribute('openingArea')
	if(openingArea_at is None):
		raise Exception('Error: cannot find "openingArea" attribute')
	openingArea = openingArea_at.quantityScalar
	
	openingLength_at = xobj.getAttribute('openingLength')
	if(openingLength_at is None):
		raise Exception('Error: cannot find "openingLength" attribute')
	openingLength = openingLength_at.quantityScalar
	
	
	str_tcl = '{}uniaxialMaterial CFSWSWP {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, height.value, width.value, fut.value, tf.value, Ife.value, Ifi.value,
			ts.value, np, ds.value, Vs.value, sc.value, nc, type, openingArea.value, openingLength.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
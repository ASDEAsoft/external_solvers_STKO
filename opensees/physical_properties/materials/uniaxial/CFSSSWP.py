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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
		html_end()
		)
	at_fuf.dimension = u.F/u.L**2
	
	# fyf
	at_fyf = MpcAttributeMetaData()
	at_fyf.type = MpcAttributeType.QuantityScalar
	at_fyf.name = 'fyf'
	at_fyf.group = 'Non-linear'
	at_fyf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fyf')+'<br/>') + 
		html_par('Yield strength of framing members') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
		html_end()
		)
	at_fyf.dimension = u.F/u.L**2
	
	# tf
	at_tf = MpcAttributeMetaData()
	at_tf.type = MpcAttributeType.QuantityScalar
	at_tf.name = 'tf'
	at_tf.group = 'Non-linear'
	at_tf.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tf')+'<br/>') + 
		html_par('Framing thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
		html_end()
		)
	at_tf.dimension = u.L
	
	# Af
	at_Af = MpcAttributeMetaData()
	at_Af.type = MpcAttributeType.QuantityScalar
	at_Af.name = 'Af'
	at_Af.group = 'Non-linear'
	at_Af.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Af')+'<br/>') + 
		html_par('Framing cross section area') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
		html_end()
		)
	at_Af.dimension = u.L**2
	
	# fus
	at_fus = MpcAttributeMetaData()
	at_fus.type = MpcAttributeType.QuantityScalar
	at_fus.name = 'fus'
	at_fus.group = 'Non-linear'
	at_fus.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fus')+'<br/>') + 
		html_par('Tensile strength of steel sheet sheathing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
		html_end()
		)
	at_fus.dimension = u.F/u.L**2
	
	# fys
	at_fys = MpcAttributeMetaData()
	at_fys.type = MpcAttributeType.QuantityScalar
	at_fys.name = 'fys'
	at_fys.group = 'Non-linear'
	at_fys.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fys')+'<br/>') + 
		html_par('Yield strength of steel sheet sheathing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
		html_end()
		)
	at_fys.dimension = u.F/u.L**2
	
	# ts
	at_ts = MpcAttributeMetaData()
	at_ts.type = MpcAttributeType.QuantityScalar
	at_ts.name = 'ts'
	at_ts.group = 'Non-linear'
	at_ts.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ts')+'<br/>') + 
		html_par('Sheathing thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
		html_end()
		)
	at_ds.dimension = u.L
	
	# Vs
	at_Vs = MpcAttributeMetaData()
	at_Vs.type = MpcAttributeType.QuantityScalar
	at_Vs.name = 'Vs'
	at_Vs.group = 'Non-linear'
	at_Vs.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Vs')+'<br/>') + 
		html_par('Screws shear strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
		html_end()
		)
	at_sc.dimension = u.L
	
	# dt
	at_dt = MpcAttributeMetaData()
	at_dt.type = MpcAttributeType.QuantityScalar
	at_dt.name = 'dt'
	at_dt.group = 'Non-linear'
	at_dt.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dt')+'<br/>') + 
		html_par('Anchor bolt’s diameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
		html_end()
		)
	at_dt.dimension = u.L
	
	# openingArea
	at_openingArea = MpcAttributeMetaData()
	at_openingArea.type = MpcAttributeType.QuantityScalar
	at_openingArea.name = 'openingArea'
	at_openingArea.group = 'Non-linear'
	at_openingArea.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('openingArea')+'<br/>') + 
		html_par('Total area of openings') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/CFSSSWP','CFSSSWP')+'<br/>') +
		html_end()
		)
	at_openingLength.dimension = u.L
	
	xom = MpcXObjectMetaData()
	xom.name = 'CFSSSWP'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_height)
	xom.addAttribute(at_width)
	xom.addAttribute(at_fuf)
	xom.addAttribute(at_fyf)
	xom.addAttribute(at_tf)
	xom.addAttribute(at_Af)
	xom.addAttribute(at_fus)
	xom.addAttribute(at_fys)
	xom.addAttribute(at_ts)
	xom.addAttribute(at_np)
	xom.addAttribute(at_ds)
	xom.addAttribute(at_Vs)
	xom.addAttribute(at_sc)
	xom.addAttribute(at_dt)
	xom.addAttribute(at_openingArea)
	xom.addAttribute(at_openingLength)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial CFSSSWP $tag $height $width $fuf $fyf $tf $Af $fus $fys $ts $np $ds $Vs $sc $dt $openingArea $openingLength
	
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
	
	fuf_at = xobj.getAttribute('fuf')
	if(fuf_at is None):
		raise Exception('Error: cannot find "fuf" attribute')
	fuf = fuf_at.quantityScalar
	
	fyf_at = xobj.getAttribute('fyf')
	if(fyf_at is None):
		raise Exception('Error: cannot find "fyf" attribute')
	fyf = fyf_at.quantityScalar
	
	tf_at = xobj.getAttribute('tf')
	if(tf_at is None):
		raise Exception('Error: cannot find "tf" attribute')
	tf = tf_at.quantityScalar
	
	Af_at = xobj.getAttribute('Af')
	if(Af_at is None):
		raise Exception('Error: cannot find "Af" attribute')
	Af = Af_at.quantityScalar
	
	fus_at = xobj.getAttribute('fus')
	if(fus_at is None):
		raise Exception('Error: cannot find "fus" attribute')
	fus = fus_at.quantityScalar
	
	fys_at = xobj.getAttribute('fys')
	if(fys_at is None):
		raise Exception('Error: cannot find "fys" attribute')
	fys = fys_at.quantityScalar
	
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
	
	dt_at = xobj.getAttribute('dt')
	if(dt_at is None):
		raise Exception('Error: cannot find "dt" attribute')
	dt = dt_at.quantityScalar
	
	openingArea_at = xobj.getAttribute('openingArea')
	if(openingArea_at is None):
		raise Exception('Error: cannot find "openingArea" attribute')
	openingArea = openingArea_at.quantityScalar
	
	openingLength_at = xobj.getAttribute('openingLength')
	if(openingLength_at is None):
		raise Exception('Error: cannot find "openingLength" attribute')
	openingLength = openingLength_at.quantityScalar
	
	
	str_tcl = '{}uniaxialMaterial CFSSSWP {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, height.value, width.value, fuf.value, fyf.value, tf.value, Af.value, fus.value,
			fys.value, ts.value, np, ds.value, Vs.value, sc.value, dt.value, openingArea.value, openingLength.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
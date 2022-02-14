import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Gr
	at_Gr = MpcAttributeMetaData()
	at_Gr.type = MpcAttributeType.QuantityScalar
	at_Gr.name = 'Gr'
	at_Gr.group = 'Group'
	at_Gr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Gr')+'<br/>') +
		html_par('shear modulus of elastomeric bearing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_Gr.dimension = u.F/u.L**2
	
	# Kbulk
	at_Kbulk = MpcAttributeMetaData()
	at_Kbulk.type = MpcAttributeType.QuantityScalar
	at_Kbulk.name = 'Kbulk'
	at_Kbulk.group = 'Group'
	at_Kbulk.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kbulk')+'<br/>') +
		html_par('bulk modulus of rubber') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_Kbulk.dimension = u.F/u.L**2
	
	# D1
	at_D1 = MpcAttributeMetaData()
	at_D1.type = MpcAttributeType.QuantityScalar
	at_D1.name = 'D1'
	at_D1.group = 'Group'
	at_D1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D1')+'<br/>') +
		html_par('internal diameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_D1.dimension = u.L
	
	# D2
	at_D2 = MpcAttributeMetaData()
	at_D2.type = MpcAttributeType.QuantityScalar
	at_D2.name = 'D2'
	at_D2.group = 'Group'
	at_D2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D2')+'<br/>') +
		html_par('outer diameter (excluding cover thickness)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_D2.dimension = u.L
	
	# ts
	at_ts = MpcAttributeMetaData()
	at_ts.type = MpcAttributeType.QuantityScalar
	at_ts.name = 'ts'
	at_ts.group = 'Group'
	at_ts.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ts')+'<br/>') +
		html_par('single steel shim layer thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_ts.dimension = u.L
	
	# tr
	at_tr = MpcAttributeMetaData()
	at_tr.type = MpcAttributeType.QuantityScalar
	at_tr.name = 'tr'
	at_tr.group = 'Group'
	at_tr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tr')+'<br/>') +
		html_par('single rubber layer thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_tr.dimension = u.L
	
	# n
	at_n = MpcAttributeMetaData()
	at_n.type = MpcAttributeType.Integer
	at_n.name = 'n'
	at_n.group = 'Group'
	at_n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('n')+'<br/>') +
		html_par('number of rubber layers') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# a1
	at_a1 = MpcAttributeMetaData()
	at_a1.type = MpcAttributeType.Real
	at_a1.name = 'a1'
	at_a1.group = 'Grant model'
	at_a1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a1')+'<br/>') +
		html_par('parameter of the Grant model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# a2
	at_a2 = MpcAttributeMetaData()
	at_a2.type = MpcAttributeType.Real
	at_a2.name = 'a2'
	at_a2.group = 'Grant model'
	at_a2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a2')+'<br/>') +
		html_par('parameter of the Grant model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# a3
	at_a3 = MpcAttributeMetaData()
	at_a3.type = MpcAttributeType.Real
	at_a3.name = 'a3'
	at_a3.group = 'Grant model'
	at_a3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a3')+'<br/>') +
		html_par('parameter of the Grant model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# b1
	at_b1 = MpcAttributeMetaData()
	at_b1.type = MpcAttributeType.Real
	at_b1.name = 'b1'
	at_b1.group = 'Grant model'
	at_b1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b1')+'<br/>') +
		html_par('parameter of the Grant model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# b2
	at_b2 = MpcAttributeMetaData()
	at_b2.type = MpcAttributeType.Real
	at_b2.name = 'b2'
	at_b2.group = 'Grant model'
	at_b2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b2')+'<br/>') +
		html_par('parameter of the Grant model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# b3
	at_b3 = MpcAttributeMetaData()
	at_b3.type = MpcAttributeType.Real
	at_b3.name = 'b3'
	at_b3.group = 'Grant model'
	at_b3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b3')+'<br/>') +
		html_par('parameter of the Grant model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# c1
	at_c1 = MpcAttributeMetaData()
	at_c1.type = MpcAttributeType.Real
	at_c1.name = 'c1'
	at_c1.group = 'Grant model'
	at_c1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c1')+'<br/>') +
		html_par('parameter of the Grant model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# c2
	at_c2 = MpcAttributeMetaData()
	at_c2.type = MpcAttributeType.Real
	at_c2.name = 'c2'
	at_c2.group = 'Grant model'
	at_c2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c2')+'<br/>') +
		html_par('parameter of the Grant model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# c3
	at_c3 = MpcAttributeMetaData()
	at_c3.type = MpcAttributeType.Real
	at_c3.name = 'c3'
	at_c3.group = 'Grant model'
	at_c3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c3')+'<br/>') +
		html_par('parameter of the Grant model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# c4
	at_c4 = MpcAttributeMetaData()
	at_c4.type = MpcAttributeType.Real
	at_c4.name = 'c4'
	at_c4.group = 'Grant model'
	at_c4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c4')+'<br/>') +
		html_par('parameter of the Grant model') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# -orient
	at_orient = MpcAttributeMetaData()
	at_orient.type = MpcAttributeType.Boolean
	at_orient.name = '-orient'
	at_orient.group = 'Optional parameters'
	at_orient.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-orient')+'<br/>') +
		html_par('activate vector components in global coordinates') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# use_kc
	at_use_kc = MpcAttributeMetaData()
	at_use_kc.type = MpcAttributeType.Boolean
	at_use_kc.name = 'use_kc'
	at_use_kc.group = 'Group'
	at_use_kc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_kc')+'<br/>') +
		html_par('cavitation parameter (optional, default = 10.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# kc
	at_kc = MpcAttributeMetaData()
	at_kc.type = MpcAttributeType.Real
	at_kc.name = 'kc'
	at_kc.group = 'Optional parameters'
	at_kc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kc')+'<br/>') +
		html_par('cavitation parameter (optional, default = 10.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_kc.setDefault(10.0)
	
	# use_PhiM
	at_use_PhiM = MpcAttributeMetaData()
	at_use_PhiM.type = MpcAttributeType.Boolean
	at_use_PhiM.name = 'use_PhiM'
	at_use_PhiM.group = 'Group'
	at_use_PhiM.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_PhiM')+'<br/>') +
		html_par('damage parameter (optional, default = 0.5)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# PhiM
	at_PhiM = MpcAttributeMetaData()
	at_PhiM.type = MpcAttributeType.Real
	at_PhiM.name = 'PhiM'
	at_PhiM.group = 'Optional parameters'
	at_PhiM.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('PhiM')+'<br/>') +
		html_par('damage parameter (optional, default = 0.5)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_PhiM.setDefault(0.5)
	
	# use_ac
	at_use_ac = MpcAttributeMetaData()
	at_use_ac.type = MpcAttributeType.Boolean
	at_use_ac.name = 'use_ac'
	at_use_ac.group = 'Group'
	at_use_ac.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_ac')+'<br/>') +
		html_par('strength reduction parameter (optional, default = 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# ac
	at_ac = MpcAttributeMetaData()
	at_ac.type = MpcAttributeType.Real
	at_ac.name = 'ac'
	at_ac.group = 'Optional parameters'
	at_ac.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ac')+'<br/>') +
		html_par('strength reduction parameter (optional, default = 1.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_ac.setDefault(1.0)
	
	# use_sDratio
	at_use_sDratio = MpcAttributeMetaData()
	at_use_sDratio.type = MpcAttributeType.Boolean
	at_use_sDratio.name = 'use_sDratio'
	at_use_sDratio.group = 'Group'
	at_use_sDratio.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_sDratio')+'<br/>') +
		html_par('shear distance from iNode as a fraction of the element length (optional, default = 0.5)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# sDratio
	at_sDratio = MpcAttributeMetaData()
	at_sDratio.type = MpcAttributeType.QuantityScalar
	at_sDratio.name = 'sDratio'
	at_sDratio.group = 'Optional parameters'
	at_sDratio.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sDratio')+'<br/>') +
		html_par('shear distance from iNode as a fraction of the element length (optional, default = 0.5)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_sDratio.setDefault(0.5)
	at_sDratio.dimension = u.L
	
	# use_m
	at_use_m = MpcAttributeMetaData()
	at_use_m.type = MpcAttributeType.Boolean
	at_use_m.name = 'use_m'
	at_use_m.group = 'Group'
	at_use_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_m')+'<br/>') +
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.Real
	at_m.name = 'm'
	at_m.group = 'Optional parameters'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') +
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_m.setDefault(0.0)
	# at_m.dimension = u.M
	
	# use_tc
	at_use_tc = MpcAttributeMetaData()
	at_use_tc.type = MpcAttributeType.Boolean
	at_use_tc.name = 'use_tc'
	at_use_tc.group = 'Group'
	at_use_tc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_tc')+'<br/>') +
		html_par('cover thickness (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	
	# tc
	at_tc = MpcAttributeMetaData()
	at_tc.type = MpcAttributeType.QuantityScalar
	at_tc.name = 'tc'
	at_tc.group = 'Optional parameters'
	at_tc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tc')+'<br/>') +
		html_par('cover thickness (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/HDR','HDR')+'<br/>') +
		html_end()
		)
	at_tc.setDefault(0.0)
	at_tc.dimension = u.L
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'HDR'
	xom.addAttribute(at_Gr)
	xom.addAttribute(at_Kbulk)
	xom.addAttribute(at_D1)
	xom.addAttribute(at_D2)
	xom.addAttribute(at_ts)
	xom.addAttribute(at_tr)
	xom.addAttribute(at_n)
	xom.addAttribute(at_a1)
	xom.addAttribute(at_a2)
	xom.addAttribute(at_a3)
	xom.addAttribute(at_b1)
	xom.addAttribute(at_b2)
	xom.addAttribute(at_b3)
	xom.addAttribute(at_c1)
	xom.addAttribute(at_c2)
	xom.addAttribute(at_c3)
	xom.addAttribute(at_c4)
	xom.addAttribute(at_orient)
	xom.addAttribute(at_use_kc)
	xom.addAttribute(at_kc)
	xom.addAttribute(at_use_PhiM)
	xom.addAttribute(at_PhiM)
	xom.addAttribute(at_use_ac)
	xom.addAttribute(at_ac)
	xom.addAttribute(at_use_sDratio)
	xom.addAttribute(at_sDratio)
	xom.addAttribute(at_use_m)
	xom.addAttribute(at_m)
	xom.addAttribute(at_use_tc)
	xom.addAttribute(at_tc)
	
	
	# visibility dependencies
	
	# kc-dep
	xom.setVisibilityDependency(at_use_kc, at_kc)
	
	# PhiM-dep
	xom.setVisibilityDependency(at_use_PhiM, at_PhiM)
	
	# -dep
	xom.setVisibilityDependency(at_use_ac, at_ac)
	
	# sDratio-dep
	xom.setVisibilityDependency(at_use_sDratio, at_sDratio)
	
	# m-dep
	xom.setVisibilityDependency(at_use_m, at_m)
	
	# tc-dep
	xom.setVisibilityDependency(at_use_tc, at_tc)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	#element HDR $eleTag $Nd1 $Nd2 $Gr $Kbulk $D1 $D2 $ts $tr $n $a1 $a2 $a3 $b1 $b2 $b3 $c1 $c2 $c3 $c4
	#<<$x1 $x2 $x3> $y1 $y2 $y3> <$kc> <$PhiM> <$ac> <$sDratio> <$m> <$tc>
	
	elem = pinfo.elem
	phys_prop = pinfo.phys_prop
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	# getSpatialDim
	pinfo.updateModelBuilder(3,6)
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# NODE
	nstr = ''	#node string
	node_vect = []
	for node in elem.nodes:
		node_vect.append(node.id)
		nstr += ' {}'.format(node.id)
	
	if (len(node_vect)!=2):														#CONTROLLARE: elem.geometryFamilyType() != MpcElementGeometryFamilyType.Quadrilateral or
		raise Exception('Error: invalid type of element or number of nodes')	#CONTROLLARE IL FamilyType
	
	
	# mandatory parameters
	Gr_at = xobj.getAttribute('Gr')
	if(Gr_at is None):
		raise Exception('Error: cannot find "Gr" attribute')
	Gr = Gr_at.quantityScalar.value
	
	Kbulk_at = xobj.getAttribute('Kbulk')
	if(Kbulk_at is None):
		raise Exception('Error: cannot find "Kbulk" attribute')
	Kbulk = Kbulk_at.quantityScalar.value
	
	D1_at = xobj.getAttribute('D1')
	if(D1_at is None):
		raise Exception('Error: cannot find "D1" attribute')
	D1 = D1_at.quantityScalar.value
	
	D2_at = xobj.getAttribute('D2')
	if(D2_at is None):
		raise Exception('Error: cannot find "D2" attribute')
	D2 = D2_at.quantityScalar.value
	
	ts_at = xobj.getAttribute('ts')
	if(ts_at is None):
		raise Exception('Error: cannot find "ts" attribute')
	ts = ts_at.quantityScalar.value
	
	tr_at = xobj.getAttribute('tr')
	if(tr_at is None):
		raise Exception('Error: cannot find "tr" attribute')
	tr = tr_at.quantityScalar.value
	
	n_at = xobj.getAttribute('n')
	if(n_at is None):
		raise Exception('Error: cannot find "n" attribute')
	n = n_at.integer
	
	a1_at = xobj.getAttribute('a1')
	if(a1_at is None):
		raise Exception('Error: cannot find "a1" attribute')
	a1 = a1_at.real
	
	a2_at = xobj.getAttribute('a2')
	if(a2_at is None):
		raise Exception('Error: cannot find "a2" attribute')
	a2 = a2_at.real
	
	a3_at = xobj.getAttribute('a3')
	if(a3_at is None):
		raise Exception('Error: cannot find "a3" attribute')
	a3 = a3_at.real
	
	b1_at = xobj.getAttribute('b1')
	if(b1_at is None):
		raise Exception('Error: cannot find "b1" attribute')
	b1 = b1_at.real
	
	b2_at = xobj.getAttribute('b2')
	if(b2_at is None):
		raise Exception('Error: cannot find "b2" attribute')
	b2 = b2_at.real
	
	b3_at = xobj.getAttribute('b3')
	if(b3_at is None):
		raise Exception('Error: cannot find "b3" attribute')
	b3 = b3_at.real
	
	c1_at = xobj.getAttribute('c1')
	if(c1_at is None):
		raise Exception('Error: cannot find "c1" attribute')
	c1 = c1_at.real
	
	c2_at = xobj.getAttribute('c2')
	if(c2_at is None):
		raise Exception('Error: cannot find "c2" attribute')
	c2 = c2_at.real
	
	c3_at = xobj.getAttribute('c3')
	if(c3_at is None):
		raise Exception('Error: cannot find "c3" attribute')
	c3 = c3_at.real
	
	c4_at = xobj.getAttribute('c4')
	if(c4_at is None):
		raise Exception('Error: cannot find "c4" attribute')
	c4 = c4_at.real
	
	
	# optional paramters
	sopt = ''
	
	'''
	-orient SARA' INSERITO ATTRAVERSO UNA FUNZIONE
	'''
	orient_at = xobj.getAttribute('-orient')
	if(orient_at is None):
		raise Exception('Error: cannot find "-orient" attribute')
	if orient_at.boolean:
		vect_x=elem.orientation.computeOrientation().col(0)
		vect_y=elem.orientation.computeOrientation().col(1)
		
		sopt += ' {} {} {} {} {} {}'.format (vect_x.x, vect_x.y, vect_x.z, vect_y.x, vect_y.y, vect_y.z)
	
	
	use_kc_at = xobj.getAttribute('use_kc')
	if(use_kc_at is None):
		raise Exception('Error: cannot find "use_kc" attribute')
	use_kc = use_kc_at.boolean
	if use_kc:
		kc_at = xobj.getAttribute('kc')
		if(kc_at is None):
			raise Exception('Error: cannot find "kc" attribute')
		kc = kc_at.real
		
		sopt += ' {}'.format(kc)
	
	
	use_PhiM_at = xobj.getAttribute('use_PhiM')
	if(use_PhiM_at is None):
		raise Exception('Error: cannot find "use_PhiM" attribute')
	use_PhiM = use_PhiM_at.boolean
	if use_PhiM:
		PhiM_at = xobj.getAttribute('PhiM')
		if(PhiM_at is None):
			raise Exception('Error: cannot find "PhiM" attribute')
		PhiM = PhiM_at.real
		
		sopt += ' {}'.format(PhiM)
	
	
	use_ac_at = xobj.getAttribute('use_ac')
	if(use_ac_at is None):
		raise Exception('Error: cannot find "use_ac" attribute')
	use_ac = use_ac_at.boolean
	if use_ac:
		ac_at = xobj.getAttribute('ac')
		if(ac_at is None):
			raise Exception('Error: cannot find "ac" attribute')
		ac = ac_at.real
		
		sopt += ' {}'.format(ac)
	
	
	use_sDratio_at = xobj.getAttribute('use_sDratio')
	if(use_sDratio_at is None):
		raise Exception('Error: cannot find "use_sDratio" attribute')
	use_sDratio = use_sDratio_at.boolean
	if use_sDratio:
		sDratio_at = xobj.getAttribute('sDratio')
		if(sDratio_at is None):
			raise Exception('Error: cannot find "sDratio" attribute')
		sDratio = sDratio_at.quantityScalar
		
		sopt += ' {}'.format(sDratio.value)
	
	
	use_m_at = xobj.getAttribute('use_m')
	if(use_m_at is None):
		raise Exception('Error: cannot find "use_m" attribute')
	use_m = use_m_at.boolean
	if use_m:
		m_at = xobj.getAttribute('m')
		if(m_at is None):
			raise Exception('Error: cannot find "m" attribute')
		m = m_at.quantityScalar
		
		sopt += ' {}'.format(m.value)
	
	
	use_tc_at = xobj.getAttribute('use_tc')
	if(use_tc_at is None):
		raise Exception('Error: cannot find "use_tc" attribute')
	use_tc = use_tc_at.boolean
	if use_tc:
		tc_at = xobj.getAttribute('tc')
		if(tc_at is None):
			raise Exception('Error: cannot find "tc" attribute')
		tc = tc_at.quantityScalar
		
		sopt += ' {}'.format(tc.value)
	
	
	str_tcl = '{}element HDR {}{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}{}\n'.format(
				pinfo.indent, tag, nstr, Gr, Kbulk, D1, D2,
				ts, tr, n, a1, a2, a3, b1, b2, b3, c1, c2, c3, c4, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
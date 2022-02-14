import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Fy
	at_Fy = MpcAttributeMetaData()
	at_Fy.type = MpcAttributeType.QuantityScalar
	at_Fy.name = 'Fy'
	at_Fy.group = 'Group'
	at_Fy.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Fy')+'<br/>') +
		html_par('yield strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_Fy.dimension = u.F
	
	# alpha
	at_alpha = MpcAttributeMetaData()
	at_alpha.type = MpcAttributeType.Real
	at_alpha.name = 'alpha'
	at_alpha.group = 'Group'
	at_alpha.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('alpha')+'<br/>') +
		html_par('post-yield stiffness ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	# Gr
	at_Gr = MpcAttributeMetaData()
	at_Gr.type = MpcAttributeType.QuantityScalar
	at_Gr.name = 'Gr'
	at_Gr.group = 'Group'
	at_Gr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Gr')+'<br/>') +
		html_par('shear modulus of elastomeric bearing') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_D1.dimension = u.F
	
	# D2
	at_D2 = MpcAttributeMetaData()
	at_D2.type = MpcAttributeType.QuantityScalar
	at_D2.name = 'D2'
	at_D2.group = 'Group'
	at_D2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('D2')+'<br/>') +
		html_par('outer diameter (excluding cover thickness)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_D2.dimension = u.F
	
	# ts
	at_ts = MpcAttributeMetaData()
	at_ts.type = MpcAttributeType.QuantityScalar
	at_ts.name = 'ts'
	at_ts.group = 'Group'
	at_ts.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ts')+'<br/>') +
		html_par('single steel shim layer thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_ts.dimension = u.F
	
	# tr
	at_tr = MpcAttributeMetaData()
	at_tr.type = MpcAttributeType.QuantityScalar
	at_tr.name = 'tr'
	at_tr.group = 'Group'
	at_tr.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tr')+'<br/>') +
		html_par('single rubber layer thickness') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_tr.dimension = u.F
	
	# n
	at_n = MpcAttributeMetaData()
	at_n.type = MpcAttributeType.Integer
	at_n.name = 'n'
	at_n.group = 'Group'
	at_n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('n')+'<br/>') +
		html_par('number of rubber layers') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	# -orient
	at_orient = MpcAttributeMetaData()
	at_orient.type = MpcAttributeType.Boolean
	at_orient.name = '-orient'
	at_orient.group = 'Group'
	at_orient.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-orient')+'<br/>') +
		html_par('activate vector components in global coordinates') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	# m
	at_m = MpcAttributeMetaData()
	at_m.type = MpcAttributeType.QuantityScalar
	at_m.name = 'm'
	at_m.group = 'Optional parameters'
	at_m.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('m')+'<br/>') +
		html_par('element mass (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_m.setDefault(0.0)
	# at_m.dimension = u.M
	
	# use_cd
	at_use_cd = MpcAttributeMetaData()
	at_use_cd.type = MpcAttributeType.Boolean
	at_use_cd.name = 'use_cd'
	at_use_cd.group = 'Group'
	at_use_cd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_cd')+'<br/>') +
		html_par('viscous damping parameter (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	# cd
	at_cd = MpcAttributeMetaData()
	at_cd.type = MpcAttributeType.QuantityScalar
	at_cd.name = 'cd'
	at_cd.group = 'Optional parameters'
	at_cd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cd')+'<br/>') +
		html_par('viscous damping parameter (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_cd.setDefault(0.0)
	at_cd.dimension = u.F*u.t/u.L
	
	# use_tc
	at_use_tc = MpcAttributeMetaData()
	at_use_tc.type = MpcAttributeType.Boolean
	at_use_tc.name = 'use_tc'
	at_use_tc.group = 'Group'
	at_use_tc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_tc')+'<br/>') +
		html_par('cover thickness (optional, default = 0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
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
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_tc.setDefault(0.0)
	at_tc.dimension = u.L
	
	# use_qL
	at_use_qL = MpcAttributeMetaData()
	at_use_qL.type = MpcAttributeType.Boolean
	at_use_qL.name = 'use_qL'
	at_use_qL.group = 'Group'
	at_use_qL.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_qL')+'<br/>') +
		html_par('density of lead (optional, default = 11200 kg/m3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	# qL
	at_qL = MpcAttributeMetaData()
	at_qL.type = MpcAttributeType.QuantityScalar
	at_qL.name = 'qL'
	at_qL.group = 'Optional parameters'
	at_qL.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('qL')+'<br/>') +
		html_par('density of lead (optional, default = 11200 kg/m3)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_qL.setDefault(11200)
	
	# use_cL
	at_use_cL = MpcAttributeMetaData()
	at_use_cL.type = MpcAttributeType.Boolean
	at_use_cL.name = 'use_cL'
	at_use_cL.group = 'Group'
	at_use_cL.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_cL')+'<br/>') +
		html_par('specific heat of lead (optional, default = 130 (N m)/(kg oC))') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	# cL
	at_cL = MpcAttributeMetaData()
	at_cL.type = MpcAttributeType.QuantityScalar
	at_cL.name = 'cL'
	at_cL.group = 'Optional parameters'
	at_cL.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cL')+'<br/>') +
		html_par('specific heat of lead (optional, default = 130 (N m)/(kg oC))') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_cL.setDefault(130)
	
	# use_kS
	at_use_kS = MpcAttributeMetaData()
	at_use_kS.type = MpcAttributeType.Boolean
	at_use_kS.name = 'use_kS'
	at_use_kS.group = 'Group'
	at_use_kS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_kS')+'<br/>') +
		html_par('thermal conductivity of steel (optional, default = 50 W/(m oC))') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	# kS
	at_kS = MpcAttributeMetaData()
	at_kS.type = MpcAttributeType.QuantityScalar
	at_kS.name = 'kS'
	at_kS.group = 'Optional parameters'
	at_kS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('kS')+'<br/>') +
		html_par('thermal conductivity of steel (optional, default = 50 W/(m oC))') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_kS.setDefault(50)
	
	# use_aS
	at_use_aS = MpcAttributeMetaData()
	at_use_aS.type = MpcAttributeType.Boolean
	at_use_aS.name = 'use_aS'
	at_use_aS.group = 'Group'
	at_use_aS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_aS')+'<br/>') +
		html_par('thermal diffusivity of steel (optional, default = 1.41e-05 m2/s)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	# aS
	at_aS = MpcAttributeMetaData()
	at_aS.type = MpcAttributeType.QuantityScalar
	at_aS.name = 'aS'
	at_aS.group = 'Optional parameters'
	at_aS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('aS')+'<br/>') +
		html_par('thermal diffusivity of steel (optional, default = 1.41e-05 m2/s)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	at_aS.setDefault(1.41e-05)
	
	
	# tag1
	at_tag1 = MpcAttributeMetaData()
	at_tag1.type = MpcAttributeType.Boolean
	at_tag1.name = 'tag1'
	at_tag1.group = 'Optional parameters'
	at_tag1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tag1')+'<br/>') +
		html_par('Tag to include cavitation and post-cavitation (optional, default = 0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	
	# tag2
	at_tag2 = MpcAttributeMetaData()
	at_tag2.type = MpcAttributeType.Boolean
	at_tag2.name = 'tag2'
	at_tag2.group = 'Optional parameters'
	at_tag2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tag2')+'<br/>') +
		html_par('Tag to include buckling load variation (optional, default = 0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	
	# tag3
	at_tag3 = MpcAttributeMetaData()
	at_tag3.type = MpcAttributeType.Boolean
	at_tag3.name = 'tag3'
	at_tag3.group = 'Optional parameters'
	at_tag3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tag3')+'<br/>') +
		html_par('Tag to include horizontal stiffness variation (optional, default = 0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	
	# tag4
	at_tag4 = MpcAttributeMetaData()
	at_tag4.type = MpcAttributeType.Index
	at_tag4.name = 'tag4'
	at_tag4.group = 'Optional parameters'
	at_tag4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tag4')+'<br/>') +
		html_par('Tag to include vertical stiffness variation (optional, default = 0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	
	# tag5
	at_tag5 = MpcAttributeMetaData()
	at_tag5.type = MpcAttributeType.Boolean
	at_tag5.name = 'tag5'
	at_tag5.group = 'Optional parameters'
	at_tag5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('tag5')+'<br/>') +
		html_par('Tag to include strength degradation in shear due to heating of lead core (optional, default = 0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/LeadRubberX','LeadRubberX')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'LeadRubberX'
	xom.addAttribute(at_Fy)
	xom.addAttribute(at_alpha)
	xom.addAttribute(at_Gr)
	xom.addAttribute(at_Kbulk)
	xom.addAttribute(at_D1)
	xom.addAttribute(at_D2)
	xom.addAttribute(at_ts)
	xom.addAttribute(at_tr)
	xom.addAttribute(at_n)
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
	xom.addAttribute(at_use_cd)
	xom.addAttribute(at_cd)
	xom.addAttribute(at_use_tc)
	xom.addAttribute(at_tc)
	xom.addAttribute(at_use_qL)
	xom.addAttribute(at_qL)
	xom.addAttribute(at_use_cL)
	xom.addAttribute(at_cL)
	xom.addAttribute(at_use_kS)
	xom.addAttribute(at_kS)
	xom.addAttribute(at_use_aS)
	xom.addAttribute(at_aS)
	xom.addAttribute(at_tag1)
	xom.addAttribute(at_tag2)
	xom.addAttribute(at_tag3)
	xom.addAttribute(at_tag4)
	xom.addAttribute(at_tag5)
	
	
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
	
	# cd-dep
	xom.setVisibilityDependency(at_use_cd, at_cd)
	
	# tc-dep
	xom.setVisibilityDependency(at_use_tc, at_tc)
	
	# qL-dep
	xom.setVisibilityDependency(at_use_qL, at_qL)
	
	# cL-dep
	xom.setVisibilityDependency(at_use_cL, at_cL)
	
	# kS-dep
	xom.setVisibilityDependency(at_use_kS, at_kS)
	
	# aS-dep
	xom.setVisibilityDependency(at_use_aS, at_aS)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(3,6),(3,6)]	#(ndm, ndf)

def writeTcl(pinfo):
	
	#element LeadRubberX $eleTag $Nd1 $Nd2 $Fy $alpha $Gr $Kbulk $D1 $D2 $ts $tr $n
	#<<$x1 $x2 $x3> $y1 $y2 $y3> <$kc> <$PhiM> <$ac> <$sDratio> <$m> <$cd> <$tc>
	#<$qL> <$cL> <$kS> <$aS> <$tag1> <$tag2> <$tag3> <$tag4> <$tag5>
	
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
	Fy_at = xobj.getAttribute('Fy')
	if(Fy_at is None):
		raise Exception('Error: cannot find "Fy" attribute')
	Fy = Fy_at.quantityScalar.value
	
	alpha_at = xobj.getAttribute('alpha')
	if(alpha_at is None):
		raise Exception('Error: cannot find "alpha" attribute')
	alpha = alpha_at.real
	
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
	
	
	# optional paramters
	sopt = ''
	
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
	
	
	use_cd_at = xobj.getAttribute('use_cd')
	if(use_cd_at is None):
		raise Exception('Error: cannot find "use_cd" attribute')
	use_cd = use_cd_at.boolean
	if use_cd:
		cd_at = xobj.getAttribute('cd')
		if(cd_at is None):
			raise Exception('Error: cannot find "cd" attribute')
		cd = cd_at.quantityScalar
		
		sopt += ' {}'.format(cd.value)
	
	
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
	
	
	use_qL_at = xobj.getAttribute('use_qL')
	if(use_qL_at is None):
		raise Exception('Error: cannot find "use_qL" attribute')
	use_qL = use_qL_at.boolean
	if use_qL:
		qL_at = xobj.getAttribute('qL')
		if(qL_at is None):
			raise Exception('Error: cannot find "qL" attribute')
		qL = qL_at.quantityScalar
		
		sopt += ' {}'.format(qL.value)
	
	
	use_cL_at = xobj.getAttribute('use_cL')
	if(use_cL_at is None):
		raise Exception('Error: cannot find "use_cL" attribute')
	use_cL = use_cL_at.boolean
	if use_cL:
		cL_at = xobj.getAttribute('cL')
		if(cL_at is None):
			raise Exception('Error: cannot find "cL" attribute')
		cL = cL_at.quantityScalar
		
		sopt += ' {}'.format(cL.value)
	
	
	use_kS_at = xobj.getAttribute('use_kS')
	if(use_kS_at is None):
		raise Exception('Error: cannot find "use_kS" attribute')
	use_kS = use_kS_at.boolean
	if use_kS:
		kS_at = xobj.getAttribute('kS')
		if(kS_at is None):
			raise Exception('Error: cannot find "kS" attribute')
		kS = kS_at.quantityScalar
		
		sopt += ' {}'.format(kS.value)
	
	
	use_aS_at = xobj.getAttribute('use_aS')
	if(use_aS_at is None):
		raise Exception('Error: cannot find "use_aS" attribute')
	use_aS = use_aS_at.boolean
	if use_aS:
		aS_at = xobj.getAttribute('aS')
		if(aS_at is None):
			raise Exception('Error: cannot find "aS" attribute')
		aS = aS_at.quantityScalar
		
		sopt += ' {}'.format(aS.value)
	
	
	tag1_at = xobj.getAttribute('tag1')
	if(tag1_at is None):
		raise Exception('Error: cannot find "tag1" attribute')
	if tag1_at.boolean:
		
		sopt += ' 1'
	
	tag2_at = xobj.getAttribute('tag2')
	if(tag2_at is None):
		raise Exception('Error: cannot find "tag2" attribute')
	if tag2_at.boolean:
		
		sopt += ' 1'
	
	tag3_at = xobj.getAttribute('tag3')
	if(tag3_at is None):
		raise Exception('Error: cannot find "tag3" attribute')
	if tag3_at.boolean:
		
		sopt += ' 1'
	
	tag4_at = xobj.getAttribute('tag4')
	if(tag4_at is None):
		raise Exception('Error: cannot find "tag4" attribute')
	if tag4_at.boolean:
		
		sopt += ' 1'
	
	tag5_at = xobj.getAttribute('tag5')
	if(tag5_at is None):
		raise Exception('Error: cannot find "tag5" attribute')
	if tag5_at.boolean:
		sopt += ' 1'
	
	
	str_tcl = '{}element LeadRubberX {}{} {} {} {} {} {} {} {} {} {}{}\n'.format(
				pinfo.indent, tag, nstr, Fy, alpha, Gr, Kbulk, D1, 
				D2, ts, tr, n, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
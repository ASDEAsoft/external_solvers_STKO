import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# mDen
	at_mDen = MpcAttributeMetaData()
	at_mDen.type = MpcAttributeType.QuantityScalar
	at_mDen.name = 'mDen'
	at_mDen.group = 'Non-linear'
	at_mDen.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mDen')+'<br/>') + 
		html_par('mass density') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	#at_mDen.dimension = u.M/u.L**3
	
	# eNot
	at_eNot = MpcAttributeMetaData()
	at_eNot.type = MpcAttributeType.Real
	at_eNot.name = 'eNot'
	at_eNot.group = 'Non-linear'
	at_eNot.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eNot')+'<br/>') + 
		html_par('initial void ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# A
	at_A = MpcAttributeMetaData()
	at_A.type = MpcAttributeType.Real
	at_A.name = 'A'
	at_A.group = 'Non-linear'
	at_A.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('A')+'<br/>') + 
		html_par('constant for elastic shear modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# n
	at_n = MpcAttributeMetaData()
	at_n.type = MpcAttributeType.Real
	at_n.name = 'n'
	at_n.group = 'Non-linear'
	at_n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('n')+'<br/>') + 
		html_par('pressure dependency exponent for elastic shear modulus') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# nu
	at_nu = MpcAttributeMetaData()
	at_nu.type = MpcAttributeType.Real
	at_nu.name = 'nu'
	at_nu.group = 'Non-linear'
	at_nu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nu')+'<br/>') + 
		html_par('Poisson\'s ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# a1
	at_a1 = MpcAttributeMetaData()
	at_a1.type = MpcAttributeType.Real
	at_a1.name = 'a1'
	at_a1.group = 'Non-linear'
	at_a1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a1')+'<br/>') + 
		html_par('peak stress ratio coefficient (etaMax = a1 + b1*Is)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# b1
	at_b1 = MpcAttributeMetaData()
	at_b1.type = MpcAttributeType.Real
	at_b1.name = 'b1'
	at_b1.group = 'Non-linear'
	at_b1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b1')+'<br/>') + 
		html_par('peak stress ratio coefficient (etaMax = a1 + b1*Is)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# a2
	at_a2 = MpcAttributeMetaData()
	at_a2.type = MpcAttributeType.Real
	at_a2.name = 'a2'
	at_a2.group = 'Non-linear'
	at_a2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a2')+'<br/>') + 
		html_par('max shear modulus coefficient (Gn_max = a2 + b2*Is)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# b2
	at_b2 = MpcAttributeMetaData()
	at_b2.type = MpcAttributeType.Real
	at_b2.name = 'b2'
	at_b2.group = 'Non-linear'
	at_b2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b2')+'<br/>') + 
		html_par('max shear modulus coefficient (Gn_max = a2 + b2*Is)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# a3
	at_a3 = MpcAttributeMetaData()
	at_a3.type = MpcAttributeType.Real
	at_a3.name = 'a3'
	at_a3.group = 'Non-linear'
	at_a3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('a3')+'<br/>') + 
		html_par('min shear modulus coefficient (Gn_min = a3 + b3*Is)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# b3
	at_b3 = MpcAttributeMetaData()
	at_b3.type = MpcAttributeType.Real
	at_b3.name = 'b3'
	at_b3.group = 'Non-linear'
	at_b3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b3')+'<br/>') + 
		html_par('min shear modulus coefficient (Gn_min = a3 + b3*Is)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# fd
	at_fd = MpcAttributeMetaData()
	at_fd.type = MpcAttributeType.Real
	at_fd.name = 'fd'
	at_fd.group = 'Non-linear'
	at_fd.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fd')+'<br/>') + 
		html_par('degradation constant') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# muNot
	at_muNot = MpcAttributeMetaData()
	at_muNot.type = MpcAttributeType.Real
	at_muNot.name = 'muNot'
	at_muNot.group = 'Non-linear'
	at_muNot.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('muNot')+'<br/>') + 
		html_par('dilatancy coefficient (monotonic loading)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# muCyc
	at_muCyc = MpcAttributeMetaData()
	at_muCyc.type = MpcAttributeType.Real
	at_muCyc.name = 'muCyc'
	at_muCyc.group = 'Non-linear'
	at_muCyc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('muCyc')+'<br/>') + 
		html_par('dilatancy coefficient (cyclic loading)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# sc
	at_sc = MpcAttributeMetaData()
	at_sc.type = MpcAttributeType.QuantityScalar
	at_sc.name = 'sc'
	at_sc.group = 'Non-linear'
	at_sc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sc')+'<br/>') + 
		html_par('dilatancy strain') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_sc.dimension = u.F/u.L**2
	
	# M
	at_M = MpcAttributeMetaData()
	at_M.type = MpcAttributeType.Real
	at_M.name = 'M'
	at_M.group = 'Non-linear'
	at_M.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('M')+'<br/>') + 
		html_par('critical state stress ratio') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# patm
	at_patm = MpcAttributeMetaData()
	at_patm.type = MpcAttributeType.QuantityScalar
	at_patm.name = 'patm'
	at_patm.group = 'Non-linear'
	at_patm.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('patm')+'<br/>') + 
		html_par('atmospheric pressure (in appropriate units)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_patm.dimension = u.F/u.L**2
	
	# Optional
	at_Optional = MpcAttributeMetaData()
	at_Optional.type = MpcAttributeType.Boolean
	at_Optional.name = 'Optional'
	at_Optional.group = 'Non-linear'
	at_Optional.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Optional')+'<br/>') + 
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# ssl1
	at_ssl1 = MpcAttributeMetaData()
	at_ssl1.type = MpcAttributeType.Real
	at_ssl1.name = 'ssl1'
	at_ssl1.group = 'Optional parameters'
	at_ssl1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ssl1')+'<br/>') + 
		html_par('void ratio of quasi steady state (QSS-line) at pressure p1 (default = 0.877)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_ssl1.setDefault(0.877)
	
	# ssl2
	at_ssl2 = MpcAttributeMetaData()
	at_ssl2.type = MpcAttributeType.Real
	at_ssl2.name = 'ssl2'
	at_ssl2.group = 'Optional parameters'
	at_ssl2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ssl2')+'<br/>') + 
		html_par('void ratio of quasi steady state (QSS-line) at pressure p2 (default = 0.877)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_ssl2.setDefault(0.877)
	
	# ssl3
	at_ssl3 = MpcAttributeMetaData()
	at_ssl3.type = MpcAttributeType.Real
	at_ssl3.name = 'ssl3'
	at_ssl3.group = 'Optional parameters'
	at_ssl3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ssl3')+'<br/>') + 
		html_par('void ratio of quasi steady state (QSS-line) at pressure p3 (default = 0.873)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_ssl3.setDefault(0.873)
	
	# ssl4
	at_ssl4 = MpcAttributeMetaData()
	at_ssl4.type = MpcAttributeType.Real
	at_ssl4.name = 'ssl4'
	at_ssl4.group = 'Optional parameters'
	at_ssl4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ssl4')+'<br/>') + 
		html_par('void ratio of quasi steady state (QSS-line) at pressure p4 (default = 0.870)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_ssl4.setDefault(0.870)
	
	# ssl5
	at_ssl5 = MpcAttributeMetaData()
	at_ssl5.type = MpcAttributeType.Real
	at_ssl5.name = 'ssl5'
	at_ssl5.group = 'Optional parameters'
	at_ssl5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ssl5')+'<br/>') + 
		html_par('void ratio of quasi steady state (QSS-line) at pressure p5 (default = 0.860)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_ssl5.setDefault(0.860)
	
	# ssl6
	at_ssl6 = MpcAttributeMetaData()
	at_ssl6.type = MpcAttributeType.Real
	at_ssl6.name = 'ssl6'
	at_ssl6.group = 'Optional parameters'
	at_ssl6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ssl6')+'<br/>') + 
		html_par('void ratio of quasi steady state (QSS-line) at pressure p6 (default = 0.850)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_ssl6.setDefault(0.850)
	
	# ssl7
	at_ssl7 = MpcAttributeMetaData()
	at_ssl7.type = MpcAttributeType.Real
	at_ssl7.name = 'ssl7'
	at_ssl7.group = 'Optional parameters'
	at_ssl7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ssl7')+'<br/>') + 
		html_par('void ratio of quasi steady state (QSS-line) at pressure p7 (default = 0.833)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_ssl7.setDefault(0.833)
	
	# ssl8
	at_ssl8 = MpcAttributeMetaData()
	at_ssl8.type = MpcAttributeType.Real
	at_ssl8.name = 'ssl8'
	at_ssl8.group = 'Optional parameters'
	at_ssl8.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ssl8')+'<br/>') + 
		html_par('void ratio of quasi steady state (QSS-line) at pressure p8 (default = 0.833)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_ssl8.setDefault(0.833)
	
	# ssl9
	at_ssl9 = MpcAttributeMetaData()
	at_ssl9.type = MpcAttributeType.Real
	at_ssl9.name = 'ssl9'
	at_ssl9.group = 'Optional parameters'
	at_ssl9.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ssl9')+'<br/>') + 
		html_par('void ratio of quasi steady state (QSS-line) at pressure $p9 (default = 0.833)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_ssl9.setDefault(0.833)
	
	# ssl10
	at_ssl10 = MpcAttributeMetaData()
	at_ssl10.type = MpcAttributeType.Real
	at_ssl10.name = 'ssl10'
	at_ssl10.group = 'Optional parameters'
	at_ssl10.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ssl10')+'<br/>') + 
		html_par('void ratio of quasi steady state (QSS-line) at pressure p10 (default = 0.833)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	
	# hsl
	at_hsl = MpcAttributeMetaData()
	at_hsl.type = MpcAttributeType.Real
	at_hsl.name = 'hsl'
	at_hsl.group = 'Optional parameters'
	at_hsl.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('hsl')+'<br/>') + 
		html_par('void ratio of upper reference state (UR-line) for all pressures (default = 0.895)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_hsl.setDefault(0.895)
	
	# p1
	at_p1 = MpcAttributeMetaData()
	at_p1.type = MpcAttributeType.QuantityScalar
	at_p1.name = 'p1'
	at_p1.group = 'Optional parameters'
	at_p1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p1')+'<br/>') + 
		html_par('pressure corresponding to ssl1 (default = 1.0 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_p1.setDefault(1.0)#kPa
	at_p1.dimension = u.F/u.L**2
	
	# p2
	at_p2 = MpcAttributeMetaData()
	at_p2.type = MpcAttributeType.QuantityScalar
	at_p2.name = 'p2'
	at_p2.group = 'Optional parameters'
	at_p2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p2')+'<br/>') + 
		html_par('pressure corresponding to ssl1 (default = 10.0 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_p2.setDefault(10.0)#kPa
	at_p2.dimension = u.F/u.L**2
	
	# p3
	at_p3 = MpcAttributeMetaData()
	at_p3.type = MpcAttributeType.QuantityScalar
	at_p3.name = 'p3'
	at_p3.group = 'Optional parameters'
	at_p3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p3')+'<br/>') + 
		html_par('pressure corresponding to ssl1 (default = 30.0 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_p3.setDefault(30.0)#kPa
	at_p3.dimension = u.F/u.L**2
	
	# p4
	at_p4 = MpcAttributeMetaData()
	at_p4.type = MpcAttributeType.QuantityScalar
	at_p4.name = 'p4'
	at_p4.group = 'Optional parameters'
	at_p4.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p4')+'<br/>') + 
		html_par('pressure corresponding to ssl1 (default = 50.0 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_p4.setDefault(50.0)#kPa
	at_p4.dimension = u.F/u.L**2
	
	# p5
	at_p5 = MpcAttributeMetaData()
	at_p5.type = MpcAttributeType.QuantityScalar
	at_p5.name = 'p5'
	at_p5.group = 'Optional parameters'
	at_p5.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p5')+'<br/>') + 
		html_par('pressure corresponding to ssl1 (default = 100.0 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_p5.setDefault(100.0)#kPa
	at_p5.dimension = u.F/u.L**2
	
	# p6
	at_p6 = MpcAttributeMetaData()
	at_p6.type = MpcAttributeType.QuantityScalar
	at_p6.name = 'p6'
	at_p6.group = 'Optional parameters'
	at_p6.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p6')+'<br/>') + 
		html_par('pressure corresponding to ssl1 (default = 200.0 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_p6.setDefault(200.0)#kPa
	at_p6.dimension = u.F/u.L**2
	
	# p7
	at_p7 = MpcAttributeMetaData()
	at_p7.type = MpcAttributeType.QuantityScalar
	at_p7.name = 'p7'
	at_p7.group = 'Optional parameters'
	at_p7.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p7')+'<br/>') + 
		html_par('pressure corresponding to ssl1 (default = 400.0 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_p7.setDefault(400.0)#kPa
	at_p7.dimension = u.F/u.L**2
	
	# p8
	at_p8 = MpcAttributeMetaData()
	at_p8.type = MpcAttributeType.QuantityScalar
	at_p8.name = 'p8'
	at_p8.group = 'Optional parameters'
	at_p8.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p8')+'<br/>') + 
		html_par('pressure corresponding to ssl1 (default = 400.0 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_p8.setDefault(400.0)#kPa
	at_p8.dimension = u.F/u.L**2
	
	# p9
	at_p9 = MpcAttributeMetaData()
	at_p9.type = MpcAttributeType.QuantityScalar
	at_p9.name = 'p9'
	at_p9.group = 'Optional parameters'
	at_p9.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p9')+'<br/>') + 
		html_par('pressure corresponding to ssl1 (default = 400.0 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_p9.setDefault(400.0)#kPa
	at_p9.dimension = u.F/u.L**2
	
	# p10
	at_p10 = MpcAttributeMetaData()
	at_p10.type = MpcAttributeType.QuantityScalar
	at_p10.name = 'p10'
	at_p10.group = 'Optional parameters'
	at_p10.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('p10')+'<br/>') + 
		html_par('pressure corresponding to ssl1 (default = 400.0 kPa)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Stress_Density_Material','Stress Density Material')+'<br/>') +
		html_end()
		)
	at_p10.setDefault(400.0)#kPa
	at_p10.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'StressDensityModel'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_mDen)
	xom.addAttribute(at_eNot)
	xom.addAttribute(at_A)
	xom.addAttribute(at_n)
	xom.addAttribute(at_nu)
	xom.addAttribute(at_a1)
	xom.addAttribute(at_b1)
	xom.addAttribute(at_a2)
	xom.addAttribute(at_b2)
	xom.addAttribute(at_a3)
	xom.addAttribute(at_b3)
	xom.addAttribute(at_fd)
	xom.addAttribute(at_muNot)
	xom.addAttribute(at_muCyc)
	xom.addAttribute(at_sc)
	xom.addAttribute(at_M)
	xom.addAttribute(at_patm)
	xom.addAttribute(at_Optional)
	xom.addAttribute(at_ssl1)
	xom.addAttribute(at_ssl2)
	xom.addAttribute(at_ssl3)
	xom.addAttribute(at_ssl4)
	xom.addAttribute(at_ssl5)
	xom.addAttribute(at_ssl6)
	xom.addAttribute(at_ssl7)
	xom.addAttribute(at_ssl8)
	xom.addAttribute(at_ssl9)
	xom.addAttribute(at_ssl10)
	xom.addAttribute(at_hsl)
	xom.addAttribute(at_p1)
	xom.addAttribute(at_p2)
	xom.addAttribute(at_p3)
	xom.addAttribute(at_p4)
	xom.addAttribute(at_p5)
	xom.addAttribute(at_p6)
	xom.addAttribute(at_p7)
	xom.addAttribute(at_p8)
	xom.addAttribute(at_p9)
	xom.addAttribute(at_p10)
	
	# use_Optional-dep
	xom.setVisibilityDependency(at_Optional, at_ssl1)
	xom.setVisibilityDependency(at_Optional, at_ssl2)
	xom.setVisibilityDependency(at_Optional, at_ssl3)
	xom.setVisibilityDependency(at_Optional, at_ssl4)
	xom.setVisibilityDependency(at_Optional, at_ssl5)
	xom.setVisibilityDependency(at_Optional, at_ssl6)
	xom.setVisibilityDependency(at_Optional, at_ssl7)
	xom.setVisibilityDependency(at_Optional, at_ssl8)
	xom.setVisibilityDependency(at_Optional, at_ssl9)
	xom.setVisibilityDependency(at_Optional, at_ssl10)
	xom.setVisibilityDependency(at_Optional, at_hsl)
	xom.setVisibilityDependency(at_Optional, at_p1)
	xom.setVisibilityDependency(at_Optional, at_p2)
	xom.setVisibilityDependency(at_Optional, at_p3)
	xom.setVisibilityDependency(at_Optional, at_p4)
	xom.setVisibilityDependency(at_Optional, at_p5)
	xom.setVisibilityDependency(at_Optional, at_p6)
	xom.setVisibilityDependency(at_Optional, at_p7)
	xom.setVisibilityDependency(at_Optional, at_p8)
	xom.setVisibilityDependency(at_Optional, at_p9)
	xom.setVisibilityDependency(at_Optional, at_p10)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial StressDensityModel $matTag $mDen $eNot $A $n $nu $a1 $b1 $a2 $b2
	# $a3 $b3 $fd $muNot $muCyc $sc $M $patm <$ssl1 $ssl2 $ssl3 $ssl4 $ssl5 $ssl6
	# $ssl7 $ssl8 $ssl9 $ssl10 $hsl $p1 $p2 $p3 $p4 $p5 $p6 $p7 $p8 $p9 $p10>
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	mDen_at = xobj.getAttribute('mDen')
	if(mDen_at is None):
		raise Exception('Error: cannot find "mDen" attribute')
	mDen = mDen_at.quantityScalar
	
	eNot_at = xobj.getAttribute('eNot')
	if(eNot_at is None):
		raise Exception('Error: cannot find "eNot" attribute')
	eNot = eNot_at.real
	
	A_at = xobj.getAttribute('A')
	if(A_at is None):
		raise Exception('Error: cannot find "A" attribute')
	A = A_at.real
	
	n_at = xobj.getAttribute('n')
	if(n_at is None):
		raise Exception('Error: cannot find "n" attribute')
	n = n_at.real
	
	nu_at = xobj.getAttribute('nu')
	if(nu_at is None):
		raise Exception('Error: cannot find "nu" attribute')
	nu = nu_at.real
	
	a1_at = xobj.getAttribute('a1')
	if(a1_at is None):
		raise Exception('Error: cannot find "a1" attribute')
	a1 = a1_at.real
	
	b1_at = xobj.getAttribute('b1')
	if(b1_at is None):
		raise Exception('Error: cannot find "b1" attribute')
	b1 = b1_at.real
	
	a2_at = xobj.getAttribute('a2')
	if(a2_at is None):
		raise Exception('Error: cannot find "a2" attribute')
	a2 = a2_at.real
	
	b2_at = xobj.getAttribute('b2')
	if(b2_at is None):
		raise Exception('Error: cannot find "b2" attribute')
	b2 = b2_at.real
	
	a3_at = xobj.getAttribute('a3')
	if(a3_at is None):
		raise Exception('Error: cannot find "a3" attribute')
	a3 = a3_at.real
	
	b3_at = xobj.getAttribute('b3')
	if(b3_at is None):
		raise Exception('Error: cannot find "b3" attribute')
	b3 = b3_at.real
	
	fd_at = xobj.getAttribute('fd')
	if(fd_at is None):
		raise Exception('Error: cannot find "fd" attribute')
	fd = fd_at.real
	
	muNot_at = xobj.getAttribute('muNot')
	if(muNot_at is None):
		raise Exception('Error: cannot find "muNot" attribute')
	muNot = muNot_at.real
	
	muCyc_at = xobj.getAttribute('muCyc')
	if(muCyc_at is None):
		raise Exception('Error: cannot find "muCyc" attribute')
	muCyc = muCyc_at.real
	
	sc_at = xobj.getAttribute('sc')
	if(sc_at is None):
		raise Exception('Error: cannot find "sc" attribute')
	sc = sc_at.quantityScalar
	
	M_at = xobj.getAttribute('M')
	if(M_at is None):
		raise Exception('Error: cannot find "M" attribute')
	M = M_at.real
	
	patm_at = xobj.getAttribute('patm')
	if(patm_at is None):
		raise Exception('Error: cannot find "patm" attribute')
	patm = patm_at.quantityScalar
	
	# optional paramters
	sopt = ''
	
	Optional_at = xobj.getAttribute('Optional')
	if(Optional_at is None):
		raise Exception('Error: cannot find "Optional" attribute')
	Optional = Optional_at.boolean
	if Optional:
		ssl1_at = xobj.getAttribute('ssl1')
		if(ssl1_at is None):
			raise Exception('Error: cannot find "ssl1" attribute')
		ssl1 = ssl1_at.real
		
		ssl2_at = xobj.getAttribute('ssl2')
		if(ssl2_at is None):
			raise Exception('Error: cannot find "ssl2" attribute')
		ssl2 = ssl2_at.real
		
		ssl3_at = xobj.getAttribute('ssl3')
		if(ssl3_at is None):
			raise Exception('Error: cannot find "ssl3" attribute')
		ssl3 = ssl3_at.real
		
		ssl4_at = xobj.getAttribute('ssl4')
		if(ssl4_at is None):
			raise Exception('Error: cannot find "ssl4" attribute')
		ssl4 = ssl4_at.real
		
		ssl5_at = xobj.getAttribute('ssl5')
		if(ssl5_at is None):
			raise Exception('Error: cannot find "ssl5" attribute')
		ssl5 = ssl5_at.real
		
		ssl6_at = xobj.getAttribute('ssl6')
		if(ssl6_at is None):
			raise Exception('Error: cannot find "ssl6" attribute')
		ssl6 = ssl6_at.real
		
		ssl7_at = xobj.getAttribute('ssl7')
		if(ssl7_at is None):
			raise Exception('Error: cannot find "ssl7" attribute')
		ssl7 = ssl7_at.real
		
		ssl8_at = xobj.getAttribute('ssl8')
		if(ssl8_at is None):
			raise Exception('Error: cannot find "ssl8" attribute')
		ssl8 = ssl8_at.real
		
		ssl9_at = xobj.getAttribute('ssl9')
		if(ssl9_at is None):
			raise Exception('Error: cannot find "ssl9" attribute')
		ssl9 = ssl9_at.real
		
		ssl10_at = xobj.getAttribute('ssl10')
		if(ssl10_at is None):
			raise Exception('Error: cannot find "ssl10" attribute')
		ssl10 = ssl10_at.real
		
		hsl_at = xobj.getAttribute('hsl')
		if(hsl_at is None):
			raise Exception('Error: cannot find "hsl" attribute')
		hsl = hsl_at.real
		
		p1_at = xobj.getAttribute('p1')
		if(p1_at is None):
			raise Exception('Error: cannot find "p1" attribute')
		p1 = p1_at.quantityScalar
		
		p2_at = xobj.getAttribute('p2')
		if(p2_at is None):
			raise Exception('Error: cannot find "p2" attribute')
		p2 = p2_at.quantityScalar
		
		p3_at = xobj.getAttribute('p3')
		if(p3_at is None):
			raise Exception('Error: cannot find "p3" attribute')
		p3 = p3_at.quantityScalar
		
		p4_at = xobj.getAttribute('p4')
		if(p4_at is None):
			raise Exception('Error: cannot find "p4" attribute')
		p4 = p4_at.quantityScalar
		
		p5_at = xobj.getAttribute('p5')
		if(p5_at is None):
			raise Exception('Error: cannot find "p5" attribute')
		p5 = p5_at.quantityScalar
		
		p6_at = xobj.getAttribute('p6')
		if(p6_at is None):
			raise Exception('Error: cannot find "p6" attribute')
		p6 = p6_at.quantityScalar
		
		p7_at = xobj.getAttribute('p7')
		if(p7_at is None):
			raise Exception('Error: cannot find "p7" attribute')
		p7 = p7_at.quantityScalar
		
		p8_at = xobj.getAttribute('p8')
		if(p8_at is None):
			raise Exception('Error: cannot find "p8" attribute')
		p8 = p8_at.quantityScalar
		
		p9_at = xobj.getAttribute('p9')
		if(p9_at is None):
			raise Exception('Error: cannot find "p9" attribute')
		p9 = p9_at.quantityScalar
		
		p10_at = xobj.getAttribute('p10')
		if(p10_at is None):
			raise Exception('Error: cannot find "p10" attribute')
		p10 = p10_at.quantityScalar
		
		sopt += '{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
			ssl1, ssl2, ssl3, ssl4, ssl5, ssl6, ssl7, ssl8, ssl9, ssl10, hsl, p1.value,
			p2.value, p3.value, p4.value, p5.value, p6.value, p7.value, p8.value, p9.value, p10.value)
	
	str_tcl = '{}nDMaterial StressDensityModel {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag, mDen.value, eNot, A, n, nu, a1, b1, a2, b2, a3, b3, fd, muNot, muCyc, sc.value, M, patm.value, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
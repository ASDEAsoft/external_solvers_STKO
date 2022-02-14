# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# secType
	at_secType = MpcAttributeMetaData()
	at_secType.type = MpcAttributeType.String
	at_secType.name = 'secType'
	at_secType.group = 'Non-linear'
	at_secType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('secType')+'<br/>') + 
		html_par('tag for the transverse reinforcement configuration. See NOTE 1.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_secType.sourceType = MpcAttributeSourceType.List
	at_secType.setSourceList(['S1', 'S2', 'S3', 'S4a', 'S4b', 'S5', 'C', 'R'])
	at_secType.setDefault('S1')
	
	# fpc
	at_fpc = MpcAttributeMetaData()
	at_fpc.type = MpcAttributeType.QuantityScalar
	at_fpc.name = 'fpc'
	at_fpc.group = 'Non-linear'
	at_fpc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fpc')+'<br/>') + 
		html_par('unconfined cylindrical strength of concrete specimen.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_fpc.dimension = u.F/u.L**2
	
	# Ec
	at_Ec = MpcAttributeMetaData()
	at_Ec.type = MpcAttributeType.QuantityScalar
	at_Ec.name = 'Ec'
	at_Ec.group = 'Non-linear'
	at_Ec.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ec')+'<br/>') + 
		html_par('initial elastic modulus of unconfined concrete.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_Ec.dimension = u.F/u.L**2
	
	#Optional parameters
	#Option_1	###<-epscu $epscu> OR <-gamma $gamma>###
	#-epscu
	at_use_epscu = MpcAttributeMetaData()
	at_use_epscu.type = MpcAttributeType.Boolean
	at_use_epscu.name = '-epscu'
	at_use_epscu.group = 'Optional parameters'
	at_use_epscu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-epscu')+'<br/>') + 
		html_par('confined concrete ultimate strain. See NOTE 2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_use_epscu.editable = False
	
	#epscu
	at_epscu = MpcAttributeMetaData()
	at_epscu.type = MpcAttributeType.Real
	at_epscu.name = 'epscu'
	at_epscu.group = '-epscu'
	at_epscu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epscu')+'<br/>') + 
		html_par('confined concrete ultimate strain. See NOTE 2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	#-gamma
	at_use_gamma = MpcAttributeMetaData()
	at_use_gamma.type = MpcAttributeType.Boolean
	at_use_gamma.name = '-gamma'
	at_use_gamma.group = 'Optional parameters'
	at_use_gamma.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-gamma')+'<br/>') + 
		html_par('confined concrete ultimate strain. See NOTE 2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_use_gamma.editable = False
	
	#gamma
	at_gamma = MpcAttributeMetaData()
	at_gamma.type = MpcAttributeType.Real
	at_gamma.name = 'gamma'
	at_gamma.group = '-gamma'
	at_gamma.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('gamma')+'<br/>') + 
		html_par('confined concrete ultimate strain. See NOTE 2') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	#aex_option_1
	at_aex_option_1 = MpcAttributeMetaData()
	at_aex_option_1.type = MpcAttributeType.String
	at_aex_option_1.name = 'Option 1'
	at_aex_option_1.group = 'Optional parameters'
	at_aex_option_1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Option 1')+'<br/>') + 
		html_par('Choose between -epscu and -gamma options') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_aex_option_1.sourceType = MpcAttributeSourceType.List
	at_aex_option_1.setSourceList(['-epscu', '-gamma'])
	at_aex_option_1.setDefault('-epscu')
	
	#Optional parameters
	#Option_2	###<-nu $nu> OR <-varub> OR <-varnoub>###
	#-nu
	at_use_nu = MpcAttributeMetaData()
	at_use_nu.type = MpcAttributeType.Boolean
	at_use_nu.name = '-nu'
	at_use_nu.group = 'Optional parameters'
	at_use_nu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-nu')+'<br/>') + 
		html_par('Poisson\'s Ratio. See NOTE 3.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_use_nu.editable = False
	
	#nu
	at_nu = MpcAttributeMetaData()
	at_nu.type = MpcAttributeType.Real
	at_nu.name = 'nu'
	at_nu.group = '-nu'
	at_nu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nu')+'<br/>') + 
		html_par('Poisson\'s Ratio. See NOTE 3.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	#-varub
	at_use_varub = MpcAttributeMetaData()
	at_use_varub.type = MpcAttributeType.Boolean
	at_use_varub.name = '-varub'
	at_use_varub.group = 'Optional parameters'
	at_use_varub.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-varub')+'<br/>') + 
		html_par('Poisson\'s Ratio. See NOTE 3.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_use_varub.editable = False
	
	#-varnoub
	at_use_varnoub = MpcAttributeMetaData()
	at_use_varnoub.type = MpcAttributeType.Boolean
	at_use_varnoub.name = '-varnoub'
	at_use_varnoub.group = 'Optional parameters'
	at_use_varnoub.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-varnoub')+'<br/>') + 
		html_par('Poisson\'s Ratio. See NOTE 3.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_use_varnoub.editable = False
	
	#aex_option_2
	at_aex_option_2 = MpcAttributeMetaData()
	at_aex_option_2.type = MpcAttributeType.String
	at_aex_option_2.name = 'Option 2'
	at_aex_option_2.group = 'Optional parameters'
	at_aex_option_2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Option 2')+'<br/>') + 
		html_par('Choose between -nu, -varub and -varnoub options') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_aex_option_2.sourceType = MpcAttributeSourceType.List
	at_aex_option_2.setSourceList(['-nu', '-varub', '-varnoub'])
	at_aex_option_2.setDefault('-nu')
	
	# L1
	at_L1 = MpcAttributeMetaData()
	at_L1.type = MpcAttributeType.QuantityScalar
	at_L1.name = 'L1'
	at_L1.group = 'Non-linear'
	at_L1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('L1')+'<br/>') + 
		html_par('length/diameter of square/circular core section measured respect to the hoop center line.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_L1.dimension = u.L
	
	# L2
	at_L2 = MpcAttributeMetaData()
	at_L2.type = MpcAttributeType.QuantityScalar
	at_L2.name = 'L2'
	at_L2.group = 'Non-linear'
	at_L2.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('L2')+'<br/>') + 
		html_par('additional dimension when multiple hoops are being used. See NOTE 4.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_L2.dimension = u.L
	
	# L3
	at_L3 = MpcAttributeMetaData()
	at_L3.type = MpcAttributeType.QuantityScalar
	at_L3.name = 'L3'
	at_L3.group = 'Non-linear'
	at_L3.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('L3')+'<br/>') + 
		html_par('additional dimension when multiple hoops are being used. See NOTE 4.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_L3.dimension = u.L
	
	# phis
	at_phis = MpcAttributeMetaData()
	at_phis.type = MpcAttributeType.QuantityScalar
	at_phis.name = 'phis'
	at_phis.group = 'Non-linear'
	at_phis.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('phis')+'<br/>') + 
		html_par('hoop diameter. If section arrangement has multiple hoops it refers to the external hoop.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_phis.dimension = u.L
	
	# S
	at_S = MpcAttributeMetaData()
	at_S.type = MpcAttributeType.QuantityScalar
	at_S.name = 'S'
	at_S.group = 'Non-linear'
	at_S.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('S')+'<br/>') + 
		html_par('hoop spacing.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_S.dimension = u.L
	
	# fyh
	at_fyh = MpcAttributeMetaData()
	at_fyh.type = MpcAttributeType.QuantityScalar
	at_fyh.name = 'fyh'
	at_fyh.group = 'Non-linear'
	at_fyh.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fyh')+'<br/>') + 
		html_par('yielding strength of the hoop steel.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_fyh.dimension = u.F/u.L**2
	
	# Es0
	at_Es0 = MpcAttributeMetaData()
	at_Es0.type = MpcAttributeType.QuantityScalar
	at_Es0.name = 'Es0'
	at_Es0.group = 'Non-linear'
	at_Es0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Es0')+'<br/>') + 
		html_par('elastic modulus of the hoop steel.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_Es0.dimension = u.F/u.L**2
	
	# haRatio
	at_haRatio = MpcAttributeMetaData()
	at_haRatio.type = MpcAttributeType.Real
	at_haRatio.name = 'haRatio'
	at_haRatio.group = 'Non-linear'
	at_haRatio.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('haRatio')+'<br/>') + 
		html_par('hardening ratio of the hoop steel.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	# mu
	at_mu = MpcAttributeMetaData()
	at_mu.type = MpcAttributeType.Real
	at_mu.name = 'mu'
	at_mu.group = 'Non-linear'
	at_mu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu')+'<br/>') + 
		html_par('ductility factor of the hoop steel.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	# phiLon
	at_phiLon = MpcAttributeMetaData()
	at_phiLon.type = MpcAttributeType.QuantityScalar
	at_phiLon.name = 'phiLon'
	at_phiLon.group = 'Non-linear'
	at_phiLon.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('phiLon')+'<br/>') + 
		html_par('diameter of longitudinal bars.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_phiLon.dimension = u.L
	
	#optional parameters
	#-internal
	at_internal = MpcAttributeMetaData()
	at_internal.type = MpcAttributeType.Boolean
	at_internal.name = '-internal'
	at_internal.group = 'Optional parameters'
	at_internal.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-internal')+'<br/>') + 
		html_par('optional parameters for defining the internal transverse reinforcement. If they are not specified they will be assumed equal to the external ones (for S2, S3, S4a, S4b and S5 typed).') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	# phisi
	at_phisi = MpcAttributeMetaData()
	at_phisi.type = MpcAttributeType.QuantityScalar
	at_phisi.name = 'phisi'
	at_phisi.group = '-internal'
	at_phisi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('phisi')+'<br/>') + 
		html_par('hoop diameter. If section arrangement has multiple hoops it refers to the external hoop.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_phisi.dimension = u.L
	
	# Si
	at_Si = MpcAttributeMetaData()
	at_Si.type = MpcAttributeType.QuantityScalar
	at_Si.name = 'Si'
	at_Si.group = '-internal'
	at_Si.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Si')+'<br/>') + 
		html_par('hoop spacing.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_Si.dimension = u.L
	
	# fyhi
	at_fyhi = MpcAttributeMetaData()
	at_fyhi.type = MpcAttributeType.QuantityScalar
	at_fyhi.name = 'fyhi'
	at_fyhi.group = '-internal'
	at_fyhi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fyhi')+'<br/>') + 
		html_par('yielding strength of the hoop steel.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_fyhi.dimension = u.F/u.L**2
	
	# Es0i
	at_Es0i = MpcAttributeMetaData()
	at_Es0i.type = MpcAttributeType.QuantityScalar
	at_Es0i.name = 'Es0i'
	at_Es0i.group = '-internal'
	at_Es0i.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Es0i')+'<br/>') + 
		html_par('elastic modulus of the hoop steel.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_Es0i.dimension = u.F/u.L**2
	
	# haRatioi
	at_haRatioi = MpcAttributeMetaData()
	at_haRatioi.type = MpcAttributeType.Real
	at_haRatioi.name = 'haRatioi'
	at_haRatioi.group = '-internal'
	at_haRatioi.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('haRatioi')+'<br/>') + 
		html_par('hardening ratio of the hoop steel.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	# mui
	at_mui = MpcAttributeMetaData()
	at_mui.type = MpcAttributeType.Real
	at_mui.name = 'mui'
	at_mui.group = '-internal'
	at_mui.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mui')+'<br/>') + 
		html_par('ductility factor of the hoop steel.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	#optional parameters
	#-wrap
	at_wrap = MpcAttributeMetaData()
	at_wrap.type = MpcAttributeType.Boolean
	at_wrap.name = '-wrap'
	at_wrap.group = 'Optional parameters'
	at_wrap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-wrap')+'<br/>') + 
		html_par('cover thickness measured from the outer line of hoop. (optional parameter required when section is strengthened with FRP wraps. See NOTE 5.)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	# cover
	at_cover = MpcAttributeMetaData()
	at_cover.type = MpcAttributeType.QuantityScalar
	at_cover.name = 'cover'
	at_cover.group = '-wrap'
	at_cover.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cover')+'<br/>') + 
		html_par('cover thickness measured from the outer line of hoop. (optional parameter required when section is strengthened with FRP wraps. See NOTE 5.)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_cover.dimension = u.L
	
	# Am
	at_Am = MpcAttributeMetaData()
	at_Am.type = MpcAttributeType.QuantityScalar
	at_Am.name = 'Am'
	at_Am.group = '-wrap'
	at_Am.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Am')+'<br/>') + 
		html_par('total area of FRP wraps (number of layers x wrap thickness x wrap width). (optional parameter required when section is strengthened with FRP wraps. See NOTE 5.)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_Am.dimension = u.L**2
	
	# Sw
	at_Sw = MpcAttributeMetaData()
	at_Sw.type = MpcAttributeType.QuantityScalar
	at_Sw.name = 'Sw'
	at_Sw.group = '-wrap'
	at_Sw.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Sw')+'<br/>') + 
		html_par('spacing of FRP wraps (if continuous wraps are used the spacing is equal to the wrap width). (optional parameter required when section is strengthened with FRP wraps. See NOTE 5.)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_Sw.dimension = u.L
	
	# ful
	at_ful = MpcAttributeMetaData()
	at_ful.type = MpcAttributeType.QuantityScalar
	at_ful.name = 'ful'
	at_ful.group = '-wrap'
	at_ful.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ful')+'<br/>') + 
		html_par('ultimate strength of FRP wraps. (optional parameter required when section is strengthened with FRP wraps. See NOTE 5.)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_ful.dimension = u.F/u.L**2
	
	# Es0w
	at_Es0w = MpcAttributeMetaData()
	at_Es0w.type = MpcAttributeType.QuantityScalar
	at_Es0w.name = 'Es0w'
	at_Es0w.group = '-wrap'
	at_Es0w.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Es0w')+'<br/>') + 
		html_par('elastic modulus of FRP wraps. (optional parameter required when section is strengthened with FRP wraps. See NOTE 5.)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_Es0w.dimension = u.F/u.L**2
	
	#-gravel
	at_gravel = MpcAttributeMetaData()
	at_gravel.type = MpcAttributeType.Boolean
	at_gravel.name = '-gravel'
	at_gravel.group = 'Optional parameters'
	at_gravel.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-gravel')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	#-silica
	at_silica = MpcAttributeMetaData()
	at_silica.type = MpcAttributeType.Boolean
	at_silica.name = '-silica'
	at_silica.group = 'Optional parameters'
	at_silica.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-silica')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	#-tol
	at_use_tol = MpcAttributeMetaData()
	at_use_tol.type = MpcAttributeType.Boolean
	at_use_tol.name = '-tol'
	at_use_tol.group = 'Optional parameters'
	at_use_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-tol')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	# tol
	at_tol = MpcAttributeMetaData()
	at_tol.type = MpcAttributeType.Real
	at_tol.name = 'tol'
	at_tol.group = '-tol'
	at_tol.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-tol')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	#-maxNumIter
	at_use_maxNumIter = MpcAttributeMetaData()
	at_use_maxNumIter.type = MpcAttributeType.Boolean
	at_use_maxNumIter.name = '-maxNumIter'
	at_use_maxNumIter.group = 'Optional parameters'
	at_use_maxNumIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-maxNumIter')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	# maxNumIter
	at_maxNumIter = MpcAttributeMetaData()
	at_maxNumIter.type = MpcAttributeType.Integer
	at_maxNumIter.name = 'maxNumIter'
	at_maxNumIter.group = '-maxNumIter'
	at_maxNumIter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('maxNumIter')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	#-epscuLimit
	at_use_epscuLimit = MpcAttributeMetaData()
	at_use_epscuLimit.type = MpcAttributeType.Boolean
	at_use_epscuLimit.name = '-epscuLimit'
	at_use_epscuLimit.group = 'Optional parameters'
	at_use_epscuLimit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-epscuLimit')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	# epscuLimit
	at_epscuLimit = MpcAttributeMetaData()
	at_epscuLimit.type = MpcAttributeType.Real
	at_epscuLimit.name = 'epscuLimit'
	at_epscuLimit.group = '-epscuLimit'
	at_epscuLimit.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epscuLimit')+'<br/>') +
		html_par('ultimate strain') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	at_epscuLimit.setDefault(0.05)
	
	#-stRatio
	at_use_stRatio = MpcAttributeMetaData()
	at_use_stRatio.type = MpcAttributeType.Boolean
	at_use_stRatio.name = '-stRatio'
	at_use_stRatio.group = 'Optional parameters'
	at_use_stRatio.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-stRatio')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	# stRatio
	at_stRatio = MpcAttributeMetaData()
	at_stRatio.type = MpcAttributeType.Real
	at_stRatio.name = 'stRatio'
	at_stRatio.group = '-stRatio'
	at_stRatio.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('stRatio')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ConfinedConcrete01_Material','ConfinedConcrete01 Material')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'ConfinedConcrete01'
	xom.Xgroup = 'Concrete Materials'
	xom.addAttribute(at_secType)
	xom.addAttribute(at_fpc)
	xom.addAttribute(at_Ec)
	xom.addAttribute(at_aex_option_1)
	xom.addAttribute(at_use_epscu)
	xom.addAttribute(at_epscu)
	xom.addAttribute(at_use_gamma)
	xom.addAttribute(at_gamma)
	xom.addAttribute(at_aex_option_2)
	xom.addAttribute(at_use_nu)
	xom.addAttribute(at_nu)
	xom.addAttribute(at_use_varub)
	xom.addAttribute(at_use_varnoub)
	xom.addAttribute(at_L1)
	xom.addAttribute(at_L2)
	xom.addAttribute(at_L3)
	xom.addAttribute(at_phis)
	xom.addAttribute(at_S)
	xom.addAttribute(at_fyh)
	xom.addAttribute(at_Es0)
	xom.addAttribute(at_haRatio)
	xom.addAttribute(at_mu)
	xom.addAttribute(at_phiLon)
	xom.addAttribute(at_internal)
	xom.addAttribute(at_phisi)
	xom.addAttribute(at_Si)
	xom.addAttribute(at_fyhi)
	xom.addAttribute(at_Es0i)
	xom.addAttribute(at_haRatioi)
	xom.addAttribute(at_mui)
	xom.addAttribute(at_wrap)
	xom.addAttribute(at_cover)
	xom.addAttribute(at_Am)
	xom.addAttribute(at_Sw)
	xom.addAttribute(at_ful)
	xom.addAttribute(at_Es0w)
	xom.addAttribute(at_gravel)
	xom.addAttribute(at_silica)
	xom.addAttribute(at_use_tol)
	xom.addAttribute(at_tol)
	xom.addAttribute(at_use_maxNumIter)
	xom.addAttribute(at_maxNumIter)
	xom.addAttribute(at_use_epscuLimit)
	xom.addAttribute(at_epscuLimit)
	xom.addAttribute(at_use_stRatio)
	xom.addAttribute(at_stRatio)
	
	# visibility dependencies
	
	# epscu-dep
	xom.setVisibilityDependency(at_use_epscu, at_epscu)
	# gamma-dep
	xom.setVisibilityDependency(at_use_gamma, at_gamma)
	
	# nu-dep
	xom.setVisibilityDependency(at_use_nu, at_nu)
	
	# internal-dep
	xom.setVisibilityDependency(at_internal, at_phisi)
	xom.setVisibilityDependency(at_internal, at_Si)
	xom.setVisibilityDependency(at_internal, at_fyhi)
	xom.setVisibilityDependency(at_internal, at_Es0i)
	xom.setVisibilityDependency(at_internal, at_haRatioi)
	xom.setVisibilityDependency(at_internal, at_mui)
	
	# wrap-dep
	xom.setVisibilityDependency(at_wrap, at_cover)
	xom.setVisibilityDependency(at_wrap, at_Am)
	xom.setVisibilityDependency(at_wrap, at_Sw)
	xom.setVisibilityDependency(at_wrap, at_ful)
	xom.setVisibilityDependency(at_wrap, at_Es0w)
	
	# maxNumIter-dep
	xom.setVisibilityDependency(at_use_maxNumIter, at_maxNumIter)
	
	# epscuLimit-dep
	xom.setVisibilityDependency(at_use_epscuLimit, at_epscuLimit)
	
	# stRatio-dep
	xom.setVisibilityDependency(at_use_stRatio, at_stRatio)
	
	# tol-dep
	xom.setVisibilityDependency(at_use_tol, at_tol)
	
	
	# auto-exclusive dependencies
	
	# epscu-or-gamma
	xom.setBooleanAutoExclusiveDependency(at_aex_option_1, at_use_epscu)
	xom.setBooleanAutoExclusiveDependency(at_aex_option_1, at_use_gamma)
	
	# nu-or-varub-or-varnoub
	xom.setBooleanAutoExclusiveDependency(at_aex_option_2, at_use_nu)
	xom.setBooleanAutoExclusiveDependency(at_aex_option_2, at_use_varub)
	xom.setBooleanAutoExclusiveDependency(at_aex_option_2, at_use_varnoub)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ConfinedConcrete01 $tag $secType $fpc $Ec
	#(<-epscu $epscu> OR <-gamma $gamma>) (<-nu $nu> OR <-varub> OR <-varnoub>)
	#$L1 ($L2) ($L3) $phis $S $fyh $Es0 $haRatio $mu $phiLon
	#<-internal $phisi $Si $fyhi $Es0i $haRatioi $mui>
	#<-wrap $cover $Am $Sw $fuil $Es0w> <-gravel>
	#<-silica> <-tol $tol> <-maxNumIter $maxNumIter>
	#<-epscuLimit $epscuLimit> <-stRatio $stRatio>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	secType_at = xobj.getAttribute('secType')
	if(secType_at is None):
		raise Exception('Error: cannot find "secType" attribute')
	secType = secType_at.string
	
	fpc_at = xobj.getAttribute('fpc')
	if(fpc_at is None):
		raise Exception('Error: cannot find "fpc" attribute')
	fpc = fpc_at.quantityScalar
	
	Ec_at = xobj.getAttribute('Ec')
	if(Ec_at is None):
		raise Exception('Error: cannot find "Ec" attribute')
	Ec = Ec_at.quantityScalar
	
	
	str_tcl = '{}uniaxialMaterial ConfinedConcrete01 {} {} {} {}'.format(pinfo.indent, tag, secType, fpc.value, Ec.value)
	
	# optional paramters
	sopt = ''
	
	#(<-epscu $epscu> OR <-gamma $gamma>)
	use_epscu_at = xobj.getAttribute('-epscu')
	if(use_epscu_at is None):
		raise Exception('Error: cannot find "-epscu" attribute')
	use_epscu = use_epscu_at.boolean
	if use_epscu:
		epscu_at = xobj.getAttribute('epscu')
		if(epscu_at is None):
			raise Exception('Error: cannot find "epscu" attribute')
		epscu = epscu_at.real
		sopt += ' -epscu {}'.format(epscu)
	else:
		use_gamma_at = xobj.getAttribute('-gamma')
		if(use_gamma_at is None):
			raise Exception('Error: cannot find "-gamma" attribute')
		use_gamma = use_gamma_at.boolean
		if use_gamma:
			gamma_at = xobj.getAttribute('gamma')
			if(gamma_at is None):
				raise Exception('Error: cannot find "gamma" attribute')
			gamma = gamma_at.real
			sopt += ' -gamma {}'.format(gamma)
	
	#(<-nu $nu> OR <-varub> OR <-varnoub>)
	use_nu_at = xobj.getAttribute('-nu')
	if(use_nu_at is None):
		raise Exception('Error: cannot find "-nu" attribute')
	use_nu = use_nu_at.boolean
	if use_nu:
		nu_at = xobj.getAttribute('nu')
		if(nu_at is None):
			raise Exception('Error: cannot find "nu" attribute')
		nu = nu_at.real
		
		sopt += ' -nu {}'.format(nu)
	else:
		use_varub_at = xobj.getAttribute('-varub')
		if(use_varub_at is None):
			raise Exception('Error: cannot find "-varub" attribute')
		use_varub = use_varub_at.boolean
		if use_varub:
			sopt += ' -varub'
		else:
			use_varnoub_at = xobj.getAttribute('-varnoub')
			if(use_varnoub_at is None):
				raise Exception('Error: cannot find "-varnoub" attribute')
			use_varnoub = use_varnoub_at.boolean
			if use_varnoub:
				sopt += ' -varnoub'
	
	str_tcl += sopt
	sopt = ''
	
	
	#$L1 ($L2) ($L3)
	L1_at = xobj.getAttribute('L1')
	if(L1_at is None):
		raise Exception('Error: cannot find "L1" attribute')
	L1 = L1_at.quantityScalar
	
	str_tcl += ' {}'.format(L1.value)
	
	if (secType=='R' or secType=='S4a' or secType=='S4b'):
		L2_at = xobj.getAttribute('L2')
		if(L2_at is None):
			raise Exception('Error: cannot find "L2" attribute')
		L2 = L2_at.quantityScalar
		
		str_tcl += ' {}'.format(L2.value)
		
		if(secType=='S4a' or secType=='S4b'):
			L3_at = xobj.getAttribute('L3')
			if(L3_at is None):
				raise Exception('Error: cannot find "L3" attribute')
			L3 = L3_at.quantityScalar
			
			str_tcl += ' {}'.format(L3.value)
	
	
	# mandatory parameters
	phis_at = xobj.getAttribute('phis')
	if(phis_at is None):
		raise Exception('Error: cannot find "phis" attribute')
	phis = phis_at.quantityScalar
	
	S_at = xobj.getAttribute('S')
	if(S_at is None):
		raise Exception('Error: cannot find "S" attribute')
	S = S_at.quantityScalar
	
	fyh_at = xobj.getAttribute('fyh')
	if(fyh_at is None):
		raise Exception('Error: cannot find "fyh" attribute')
	fyh = fyh_at.quantityScalar
	
	Es0_at = xobj.getAttribute('Es0')
	if(Es0_at is None):
		raise Exception('Error: cannot find "Es0" attribute')
	Es0 = Es0_at.quantityScalar
	
	haRatio_at = xobj.getAttribute('haRatio')
	if(haRatio_at is None):
		raise Exception('Error: cannot find "haRatio" attribute')
	haRatio = haRatio_at.real
	
	mu_at = xobj.getAttribute('mu')
	if(mu_at is None):
		raise Exception('Error: cannot find "mu" attribute')
	mu = mu_at.real
	
	phiLon_at = xobj.getAttribute('phiLon')
	if(phiLon_at is None):
		raise Exception('Error: cannot find "phiLon" attribute')
	phiLon = phiLon_at.quantityScalar
	
	str_tcl += ' {} {} {} {} {} {} {}'.format(phis.value, S.value, fyh.value, Es0.value, haRatio, mu, phiLon.value)
	
	
	# optional paramters
	#<-internal $phisi $Si $fyhi $Es0i $haRatioi $mui>
	internal_at = xobj.getAttribute('-internal')
	if(internal_at is None):
		raise Exception('Error: cannot find "-internal" attribute')
	internal = internal_at.boolean
	if internal:
		phisi_at = xobj.getAttribute('phisi')
		if(phisi_at is None):
			raise Exception('Error: cannot find "phisi" attribute')
		phisi = phisi_at.quantityScalar
		
		Si_at = xobj.getAttribute('Si')
		if(Si_at is None):
			raise Exception('Error: cannot find "Si" attribute')
		Si = Si_at.quantityScalar
		
		fyhi_at = xobj.getAttribute('fyhi')
		if(fyhi_at is None):
			raise Exception('Error: cannot find "fyhi" attribute')
		fyhi = fyhi_at.quantityScalar
		
		Es0i_at = xobj.getAttribute('Es0i')
		if(Es0i_at is None):
			raise Exception('Error: cannot find "Es0i" attribute')
		Es0i = Es0i_at.quantityScalar
		
		haRatioi_at = xobj.getAttribute('haRatioi')
		if(haRatioi_at is None):
			raise Exception('Error: cannot find "haRatioi" attribute')
		haRatioi = haRatioi_at.real
		
		mui_at = xobj.getAttribute('mui')
		if(mui_at is None):
			raise Exception('Error: cannot find "mui" attribute')
		mui = mui_at.real
		
		sopt += ' -internal {} {} {} {} {} {}'.format(phisi.value, Si.value, fyhi.value, Es0i.value, haRatioi, mui)
	
	#<-wrap $cover $Am $Sw $fuil $Es0w>
	wrap_at = xobj.getAttribute('-wrap')
	if(wrap_at is None):
		raise Exception('Error: cannot find "-wrap" attribute')
	wrap = wrap_at.boolean
	if wrap:
		cover_at = xobj.getAttribute('cover')
		if(cover_at is None):
			raise Exception('Error: cannot find "cover" attribute')
		cover = cover_at.quantityScalar
		
		Am_at = xobj.getAttribute('Am')
		if(Am_at is None):
			raise Exception('Error: cannot find "Am" attribute')
		Am = Am_at.quantityScalar
		
		Sw_at = xobj.getAttribute('Sw')
		if(Sw_at is None):
			raise Exception('Error: cannot find "Sw" attribute')
		Sw = Sw_at.quantityScalar
		
		ful_at = xobj.getAttribute('ful')
		if(ful_at is None):
			raise Exception('Error: cannot find "ful" attribute')
		ful = ful_at.quantityScalar
		
		Es0w_at = xobj.getAttribute('Es0w')
		if(Es0w_at is None):
			raise Exception('Error: cannot find "Es0w" attribute')
		Es0w = Es0w_at.quantityScalar
		
		sopt += ' -wrap {} {} {} {} {}'.format(cover.value, Am.value, Sw.value, ful.value, Es0w.value)
	
	#<-gravel>
	gravel_at = xobj.getAttribute('-gravel')
	if(gravel_at is None):
		raise Exception('Error: cannot find "-gravel" attribute')
	gravel = gravel_at.boolean
	if gravel:
		sopt += ' -gravel'
	
	#<-silica>
	silica_at = xobj.getAttribute('-silica')
	if(silica_at is None):
		raise Exception('Error: cannot find "-silica" attribute')
	silica = silica_at.boolean
	if silica:
		sopt += ' -silica'
	
	#<-tol $tol>
	use_tol_at = xobj.getAttribute('-tol')
	if(use_tol_at is None):
		raise Exception('Error: cannot find "-tol" attribute')
	use_tol = use_tol_at.boolean
	if use_tol:
		tol_at = xobj.getAttribute('tol')
		if(tol_at is None):
			raise Exception('Error: cannot find "tol" attribute')
		tol = tol_at.real
		
		sopt += ' -tol {}'.format(tol)
	
	#<-maxNumIter $maxNumIter>
	use_maxNumIter_at = xobj.getAttribute('-maxNumIter')
	if(use_maxNumIter_at is None):
		raise Exception('Error: cannot find "-maxNumIter" attribute')
	use_maxNumIter = use_maxNumIter_at.boolean
	if use_maxNumIter:
		maxNumIter_at = xobj.getAttribute('maxNumIter')
		if(maxNumIter_at is None):
			raise Exception('Error: cannot find "maxNumIter" attribute')
		maxNumIter = maxNumIter_at.integer
		
		sopt += ' -maxNumIter {}'.format(maxNumIter)
	
	#<-epscuLimit $epscuLimit>
	use_epscuLimit_at = xobj.getAttribute('-epscuLimit')
	if(use_epscuLimit_at is None):
		raise Exception('Error: cannot find "-epscuLimit" attribute')
	use_epscuLimit = use_epscuLimit_at.boolean
	if use_epscuLimit:
		epscuLimit_at = xobj.getAttribute('epscuLimit')
		if(epscuLimit_at is None):
			raise Exception('Error: cannot find "epscuLimit" attribute')
		epscuLimit = epscuLimit_at.real
		
		sopt += ' -epscuLimit {}'.format(epscuLimit)
	
	#<-stRatio $stRatio>
	use_stRatio_at = xobj.getAttribute('-stRatio')
	if(use_stRatio_at is None):
		raise Exception('Error: cannot find "-stRatio" attribute')
	use_stRatio = use_stRatio_at.boolean
	if use_stRatio:
		stRatio_at = xobj.getAttribute('stRatio')
		if(stRatio_at is None):
			raise Exception('Error: cannot find "stRatio" attribute')
		stRatio = stRatio_at.real
		
		sopt += ' -stRatio {}'.format(stRatio)
	
	str_tcl += '{}\n'.format(sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
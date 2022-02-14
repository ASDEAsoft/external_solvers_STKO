# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import PyMpc.IO

def makeXObjectMetaData():

	# fc
	at_fc = MpcAttributeMetaData()
	at_fc.type = MpcAttributeType.QuantityScalar
	at_fc.name = 'fc'
	at_fc.group = 'Non-linear'
	at_fc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fc')+'<br/>') +
		html_par('concrete compressive strength*') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('The value of fc is used for computing default values for other parameters.') +
		html_par('Default value = [TO BE IMPLEMENTED].') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_fc.dimension = u.F/u.L**2
	at_fc.setDefault(-30)

	# Ec
	at_Ec = MpcAttributeMetaData()
	at_Ec.type = MpcAttributeType.QuantityScalar
	at_Ec.name = 'Ec'
	at_Ec.group = 'Non-linear'
	at_Ec.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ec')+'<br/>') +
		html_par('concrete elastic modulus*') +
		html_par('Concrete elastic  modulus should be input as positive value.') +
		html_par('Default value = [TO BE IMPLEMENTED].') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_Ec.dimension = u.F/u.L**2
	at_Ec.setDefault(30000) #DT Da aggiornare con Model Code 2010

	# f0n
	at_f0n = MpcAttributeMetaData()
	at_f0n.type = MpcAttributeType.QuantityScalar
	at_f0n.name = 'f0n'
	at_f0n.group = 'Non-linear'
	at_f0n.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('f0n')+'<br/>') +
		html_par('concrete compressive stress corresponding to elastic threeshold*') +
		html_par('Concrete compressive strengths and the corresponding strains should be input as negative values.') +
		html_par('Default value = 0.6*fc') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_f0n.dimension = u.F/u.L**2
	at_f0n.setDefault(-19.5) #DT Da aggiornare con Model Code 2010

	# ft
	at_ft = MpcAttributeMetaData()
	at_ft.type = MpcAttributeType.QuantityScalar
	at_ft.name = 'ft'
	at_ft.group = 'Non-linear'
	at_ft.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ft')+'<br/>') +
		html_par('concrete tensile strength *') +
		html_par('Concrete tensile strength should be input as negative values.') +
		html_par('Default value = [TO BE IMPLEMENTED]') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_ft.dimension = u.F/u.L**2
	at_ft.setDefault(3.0) #DT Da aggiornare con Model Code 2010

	# beta
	at_beta = MpcAttributeMetaData()
	at_beta.type = MpcAttributeType.Real
	at_beta.name = 'beta'
	at_beta.group = 'Non-linear'
	at_beta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('beta')+'<br/>') +
		html_par('concrete plastic parameter*') +
		html_par('Increment of plastic strain is equal to beta times increment of total strain.') +
		html_par('The typical value for beta is between 0.2 and 0.5.') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_beta.setDefault(0.3)

	# An
	at_An = MpcAttributeMetaData()
	at_An.type = MpcAttributeType.Real
	at_An.name = 'An'
	at_An.group = 'Non-linear'
	at_An.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('An')+'<br/>') +
		html_par('Negative damage parameter*') +
		html_par('Parameter for evolution of negative damage.') +
		html_par('The typical value for An is between 2 and 5.') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_An.setDefault(2.5)

	# Bn
	at_Bn = MpcAttributeMetaData()
	at_Bn.type = MpcAttributeType.Real
	at_Bn.name = 'Bn'
	at_Bn.group = 'Non-linear'
	at_Bn.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Bn')+'<br/>') +
		html_par('Negative damage parameter*') +
		html_par('Parameter for evolution of negative damage.') +
		html_par('The typical value for An is between 0.7 and 0.9.') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_Bn.setDefault(0.8)

	# Ap
	at_Ap = MpcAttributeMetaData()
	at_Ap.type = MpcAttributeType.Real
	at_Ap.name = 'Ap'
	at_Ap.group = 'Non-linear'
	at_Ap.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ap')+'<br/>') +
		html_par('Negative damage parameter*') +
		html_par('Parameter for evolution of positive damage.') +
		html_par('The value is limited to [TO BE IMPLEMENTED]') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_Ap.setDefault(1.0)

	# -epscu
	at_use_epscu = MpcAttributeMetaData()
	at_use_epscu.type = MpcAttributeType.Boolean
	at_use_epscu.name = '-epscu'
	at_use_epscu.group = 'Optional parameters'
	at_use_epscu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_epscu')+'<br/>') +
		html_par('Ultimate compressive strain*') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)

	# epscu
	at_epscu = MpcAttributeMetaData()
	at_epscu.type = MpcAttributeType.Real
	at_epscu.name = 'epscu'
	at_epscu.group = '-epscu'
	at_epscu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('epscu')+'<br/>') +
		html_par('Ultimate compressive strain*') +
		html_par('Concrete compressive strength and the corresponding strain should be input as negative values.') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_epscu.setDefault(-1.0)

	# -dpMax
	at_use_dpMax = MpcAttributeMetaData()
	at_use_dpMax.type = MpcAttributeType.Boolean
	at_use_dpMax.name = '-dpMax'
	at_use_dpMax.group = 'Optional parameters'
	at_use_dpMax.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_dpMax')+'<br/>') +
		html_par('Maximum positive damage parameter*') +
		html_par('Maximum damage parameter that cannot be exceeded') +
		html_par('The value must be in the range 0.0 - 1.0') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)

	# dpMax
	at_dpMax = MpcAttributeMetaData()
	at_dpMax.type = MpcAttributeType.Real
	at_dpMax.name = 'dpMax'
	at_dpMax.group = '-dpMax'
	at_dpMax.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dpMax')+'<br/>') +
		html_par('Maximum positive damage parameter*') +
		html_par('Maximum damage parameter that cannot be exceeded') +
		html_par('The value must be in the range 0.0 - 1.0') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_dpMax.setDefault(0.99999)

	# -dnMax
	at_use_dnMax = MpcAttributeMetaData()
	at_use_dnMax.type = MpcAttributeType.Boolean
	at_use_dnMax.name = '-dnMax'
	at_use_dnMax.group = 'Optional parameters'
	at_use_dnMax.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_dnMax')+'<br/>') +
		html_par('Maximum negative damage parameter*') +
		html_par('Maximum damage parameter that cannot be exceeded') +
		html_par('The value must be in the range 0.0 - 1.0') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)

	# dnMax
	at_dnMax = MpcAttributeMetaData()
	at_dnMax.type = MpcAttributeType.Real
	at_dnMax.name = 'dnMax'
	at_dnMax.group = '-dnMax'
	at_dnMax.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dnMax')+'<br/>') +
		html_par('Maximum negative damage parameter*') +
		html_par('Maximum damage parameter that cannot be exceeded') +
		html_par('The value must be in the range 0.0 - 1.0') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_dnMax.setDefault(0.99999)

	# -denv
	at_use_denv = MpcAttributeMetaData()
	at_use_denv.type = MpcAttributeType.Boolean
	at_use_denv.name = '-denv'
	at_use_denv.group = 'Optional parameters'
	at_use_denv.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_denv')+'<br/>') +
		html_par('Environmental damage parameter*') +
		html_par('Damage parameter due to environmental degradation') +
		html_par('e.g. corrosion, freeze-thaw cycles, sulphate attack, etc.') +
		html_par('The value must be in the range 0.0 - 1.0') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)

	# denv
	at_denv = MpcAttributeMetaData()
	at_denv.type = MpcAttributeType.Real
	at_denv.name = 'denv'
	at_denv.group = '-denv'
	at_denv.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('denv')+'<br/>') +
		html_par('Environmental damage parameter*') +
		html_par('Damage parameter due to environmental degradation') +
		html_par('e.g. corrosion, freeze-thaw cycles, sulphate attack, etc.') +
		html_par('The value must be in the range 0.0 - 1.0') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_denv.setDefault(0.0)

	# -denvp
	at_use_denvp = MpcAttributeMetaData()
	at_use_denvp.type = MpcAttributeType.Boolean
	at_use_denvp.name = '-denvp'
	at_use_denvp.group = 'Optional parameters'
	at_use_denvp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_denvp')+'<br/>') +
		html_par('Environmental positive damage parameter*') +
		html_par('Tensile damage parameter due to environmental degradation') +
		html_par('e.g. corrosion, freeze-thaw cycles, sulphate attack, etc.') +
		html_par('The value must be in the range 0.0 - 1.0') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)

	# denvp
	at_denvp = MpcAttributeMetaData()
	at_denvp.type = MpcAttributeType.Real
	at_denvp.name = 'denvp'
	at_denvp.group = '-denvp'
	at_denvp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('denvp')+'<br/>') +
		html_par('Environmental positive damage parameter*') +
		html_par('Tensile damage parameter due to environmental degradation') +
		html_par('e.g. corrosion, freeze-thaw cycles, sulphate attack, etc.') +
		html_par('The value must be in the range 0.0 - 1.0') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_denvp.setDefault(0.0)
	
	# Utility per calcolo
	at_useExp = MpcAttributeMetaData()
	at_useExp.type = MpcAttributeType.Boolean
	at_useExp.name = '-useExp'
	at_useExp.group = 'UtilsExp'
	at_useExp.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Superimpose experimental data')+'<br/>') +
		html_par('If selected the user will be asked to import experimental data*') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_useExp.setDefault(0)
	
	at_expFileNameC = MpcAttributeMetaData()
	at_expFileNameC.type = MpcAttributeType.String
	at_expFileNameC.name = 'fileNameC'
	at_expFileNameC.group = 'useExpFile'
	at_expFileNameC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('experimental file')+'<br/>') +
		html_par('File name where experimental data in compression are loaded*') +
		html_par('Data is plotted as found in the text file') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_expFileNameC.stringType = 'OpenFilePath Text file (*.txt)'
	
	at_expFileNameT = MpcAttributeMetaData()
	at_expFileNameT.type = MpcAttributeType.String
	at_expFileNameT.name = 'fileNameT'
	at_expFileNameT.group = 'useExpFile'
	at_expFileNameT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('experimental file')+'<br/>') +
		html_par('File name where experimental data in tension are loaded*') +
		html_par('Data is plotted as found in the text file') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_expFileNameT.stringType = 'OpenFilePath Text file (*.txt)'
	
	# Curva sigma epsilon inserita da utente manualmente
	at_expEpsilonC = MpcAttributeMetaData()
	at_expEpsilonC.type = MpcAttributeType.QuantityVector
	at_expEpsilonC.name = 'expEpsilonC'
	at_expEpsilonC.group = 'useExpList'
	at_expEpsilonC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('experimental file')+'<br/>') +
		html_par('List of strains for compression law*') +
		html_par('Sign should be negative in compression') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	
	at_expSigmaC = MpcAttributeMetaData()
	at_expSigmaC.type = MpcAttributeType.QuantityVector
	at_expSigmaC.name = 'expSigmaC'
	at_expSigmaC.group = 'useExpList'
	at_expSigmaC.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('experimental file')+'<br/>') +
		html_par('List of stresses for compression law*') +
		html_par('Sign should be negative in compression') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_expSigmaC.dimension = u.F/u.L**2
	
	at_expEpsilonT = MpcAttributeMetaData()
	at_expEpsilonT.type = MpcAttributeType.QuantityVector
	at_expEpsilonT.name = 'expEpsilonT'
	at_expEpsilonT.group = 'useExpList'
	at_expEpsilonT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('experimental file')+'<br/>') +
		html_par('List of strains for tension law*') +
		html_par('Sign should be positive in tension') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	
	at_expSigmaT = MpcAttributeMetaData()
	at_expSigmaT.type = MpcAttributeType.QuantityVector
	at_expSigmaT.name = 'expSigmaT'
	at_expSigmaT.group = 'useExpList'
	at_expSigmaT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('experimental file')+'<br/>') +
		html_par('List of stresses for tension law*') +
		html_par('Sign should be positive in tension') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_expSigmaT.dimension = u.F/u.L**2
	
	# Fare il calcolo automatico con algoritmo genetico per il fitting della curva
	at_useGenetic = MpcAttributeMetaData()
	at_useGenetic.type = MpcAttributeType.Boolean
	at_useGenetic.name = '-useGenetic'
	at_useGenetic.group = 'UtilsGen'
	at_useGenetic.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Automatically compute material parameters')+'<br/>') +
		html_par('Compute material parameters with a genetic algorithm*') +
		html_par('Written by Diego Talledo - University IUAV of Venice - Italy') +
		html_par('contact: diego.talledo@iuav.it') +
		html_par(html_href('website','ConcreteDamage Material')+'<br/>') +
		html_end()
		)
	at_useGenetic.setDefault(0)
	
	# Vettore con i dati che utente ha inserito da usare come backup
	at_backupParameters = MpcAttributeMetaData()
	at_backupParameters.type = MpcAttributeType.QuantityVector
	at_backupParameters.name = 'backupParameters'
	at_backupParameters.group = 'Backup'
	at_backupParameters.editable = False
	
	# Flag che indica se devo tenermi fissati i parametri di backup o aggiornarli
	at_backedup = MpcAttributeMetaData()
	at_backedup.type = MpcAttributeType.Boolean
	at_backedup.name = 'backupFlag'
	at_backedup.group = 'Backup'
	at_backedup.editable = False
	at_backedup.setDefault(False)

	xom = MpcXObjectMetaData()
	xom.name = 'ConcreteDamage'
	xom.Xgroup = 'Concrete Materials'
	xom.addAttribute(at_fc)
	xom.addAttribute(at_Ec)
	xom.addAttribute(at_f0n)
	xom.addAttribute(at_ft)
	xom.addAttribute(at_beta)
	xom.addAttribute(at_An)
	xom.addAttribute(at_Bn)
	xom.addAttribute(at_Ap)
	xom.addAttribute(at_use_epscu)
	xom.addAttribute(at_epscu)
	xom.addAttribute(at_use_denv)
	xom.addAttribute(at_denv)
	xom.addAttribute(at_use_denvp)
	xom.addAttribute(at_denvp)
	xom.addAttribute(at_use_dpMax)
	xom.addAttribute(at_dpMax)
	xom.addAttribute(at_use_dnMax)
	xom.addAttribute(at_dnMax)
	xom.addAttribute(at_useExp)
	xom.addAttribute(at_useGenetic)
	xom.addAttribute(at_expFileNameC)
	xom.addAttribute(at_expFileNameT)
	xom.addAttribute(at_expEpsilonC)
	xom.addAttribute(at_expSigmaC)
	xom.addAttribute(at_expEpsilonT)
	xom.addAttribute(at_expSigmaT)
	xom.addAttribute(at_backupParameters)
	xom.addAttribute(at_backedup)

	# eps_cu
	xom.setVisibilityDependency(at_use_epscu, at_epscu)

	# denv
	xom.setVisibilityDependency(at_use_denv, at_denv)

	# denvp
	xom.setVisibilityDependency(at_use_denvp, at_denvp)

	# dpMax
	xom.setVisibilityDependency(at_use_dpMax, at_dpMax)

	# dnMax
	xom.setVisibilityDependency(at_use_dnMax, at_dnMax)
	
	# expFileName
	xom.setVisibilityDependency(at_useExp, at_expFileNameC)
	xom.setVisibilityDependency(at_useExp, at_expFileNameT)
	xom.setVisibilityDependency(at_useExp, at_expEpsilonC)
	xom.setVisibilityDependency(at_useExp, at_expSigmaC)
	xom.setVisibilityDependency(at_useExp, at_expEpsilonT)
	xom.setVisibilityDependency(at_useExp, at_expSigmaT)

	return xom

def writeTcl(pinfo):

	#uniaxialMaterial ConcreteDamage tag? E? f0n? f0p? beta? An? Bn? Ap? <-epscu eps_cu?> <-dpMax max?> <-dnMax max?> <-denv denv?> <-denvn denvn?> <-denvp denvp?> <-stiffness stiff?>

	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId

	# mandatory parameters
	Ec_at = xobj.getAttribute('Ec')
	if(Ec_at is None):
		raise Exception('Error: cannot find "Ec" attribute')
	Ec = Ec_at.quantityScalar

	f0n_at = xobj.getAttribute('f0n')
	if(f0n_at is None):
		raise Exception('Error: cannot find "f0n" attribute')
	f0n = f0n_at.quantityScalar

	ft_at = xobj.getAttribute('ft')
	if(ft_at is None):
		raise Exception('Error: cannot find "ft" attribute')
	ft = ft_at.quantityScalar

	beta_at = xobj.getAttribute('beta')
	if(beta_at is None):
		raise Exception('Error: cannot find "beta" attribute')
	beta = beta_at.real

	An_at = xobj.getAttribute('An')
	if(An_at is None):
		raise Exception('Error: cannot find "An" attribute')
	An = An_at.real

	Bn_at = xobj.getAttribute('Bn')
	if(Bn_at is None):
		raise Exception('Error: cannot find "Bn" attribute')
	Bn = Bn_at.real

	Ap_at = xobj.getAttribute('Ap')
	if(Ap_at is None):
		raise Exception('Error: cannot find "Ap" attribute')
	Ap = Ap_at.real


	# optional paramters
	sopt = ''

	use_epscu_at = xobj.getAttribute('-epscu')
	if(use_epscu_at is None):
		raise Exception('Error: cannot find "-epscu" attribute')
	use_epscu = use_epscu_at.boolean
	if use_epscu:
		epscu_at = xobj.getAttribute('epscu')
		if(epscu_at is None):
			raise Exception('Error: cannot find "epscu" attribute')
		epscu = epscu_at.real

		sopt += '-epscu {}'.format(epscu)

	use_denv_at = xobj.getAttribute('-denv')
	if(use_denv_at is None):
		raise Exception('Error: cannot find "-denv" attribute')
	use_denv = use_denv_at.boolean
	if use_denv:
		denv_at = xobj.getAttribute('denv')
		if(denv_at is None):
			raise Exception('Error: cannot find "denv" attribute')
		denv = denv_at.real

		sopt += ' -denv {}'.format(denv)

	use_denvp_at = xobj.getAttribute('-denvp')
	if(use_denvp_at is None):
		raise Exception('Error: cannot find "-denvp" attribute')
	use_denvp = use_denvp_at.boolean
	if use_denvp:
		denvp_at = xobj.getAttribute('denvp')
		if(denvp_at is None):
			raise Exception('Error: cannot find "denvp" attribute')
		denvp = denvp_at.real

		sopt += ' -denvp {}'.format(denvp)

	use_dpMax_at = xobj.getAttribute('-dpMax')
	if(use_dpMax_at is None):
		raise Exception('Error: cannot find "-dpMax" attribute')
	use_dpMax = use_dpMax_at.boolean
	if use_dpMax:
		dpMax_at = xobj.getAttribute('dpMax')
		if(dpMax_at is None):
			raise Exception('Error: cannot find "dpMax" attribute')
		dpMax = dpMax_at.real

		sopt += ' -dpMax {}'.format(dpMax)

	use_dnMax_at = xobj.getAttribute('-dnMax')
	if(use_dnMax_at is None):
		raise Exception('Error: cannot find "-dnMax" attribute')
	use_dnMax = use_dnMax_at.boolean
	if use_dnMax:
		dnMax_at = xobj.getAttribute('dnMax')
		if(dnMax_at is None):
			raise Exception('Error: cannot find "dnMax" attribute')
		dnMax = dnMax_at.real

		sopt += ' -dnMax {}'.format(dnMax)


	str_tcl = '{}uniaxialMaterial ConcreteDamage {} {} {} {} {} {} {} {} {}\n'.format(
			pinfo.indent, tag,  Ec.value, f0n.value, ft.value, beta, An, Bn, Ap, sopt)

	# now write the string into the file
	pinfo.out_file.write(str_tcl)

def __get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

def __set_backup_parameters(xobj,Ec,ft,f0n,beta,An,Bn,Ap,epscu,denv,denvp):
	attribute = __get_xobj_attribute(xobj, 'Ec')
	attribute.quantityScalar.referenceValue = Ec
	attribute = __get_xobj_attribute(xobj, 'ft')
	attribute.quantityScalar.referenceValue = ft
	attribute = __get_xobj_attribute(xobj, 'f0n')
	attribute.quantityScalar.referenceValue = f0n
	attribute = __get_xobj_attribute(xobj, 'beta')
	attribute.real = beta
	attribute = __get_xobj_attribute(xobj, 'An')
	attribute.real = An
	attribute = __get_xobj_attribute(xobj, 'Bn')
	attribute.real = Bn
	attribute = __get_xobj_attribute(xobj, 'Ap')
	attribute.real = Ap
	attribute = __get_xobj_attribute(xobj, 'epscu')
	attribute.real = epscu
	attribute = __get_xobj_attribute(xobj, 'denv')
	attribute.real = denv
	attribute = __get_xobj_attribute(xobj, 'denvp')
	attribute.real = denvp
	
def __get_constitutive_parameters(xobj):
	attribute = __get_xobj_attribute(xobj, 'Ec')
	Ec = attribute.quantityScalar;
	attribute = __get_xobj_attribute(xobj, 'ft')
	ft = attribute.quantityScalar;
	attribute = __get_xobj_attribute(xobj, 'f0n')
	f0n = attribute.quantityScalar;
	attribute = __get_xobj_attribute(xobj, 'beta')
	beta = attribute.real;
	attribute = __get_xobj_attribute(xobj, 'An')
	An = attribute.real;
	attribute = __get_xobj_attribute(xobj, 'Bn')
	Bn = attribute.real;
	attribute = __get_xobj_attribute(xobj, 'Ap')
	Ap = attribute.real;
	attribute = __get_xobj_attribute(xobj, '-epscu')
	use_epscu = attribute.boolean;
	if use_epscu:
		attribute = __get_xobj_attribute(xobj, 'epscu')
		epscu = attribute.real;
	else :
		epscu = -1.0
	attribute = __get_xobj_attribute(xobj, '-denv')
	use_denv = attribute.boolean;
	if use_denv:
		attribute = __get_xobj_attribute(xobj, 'denv')
		denv = attribute.real;
		denvp = denv
	else:
		denv = 0.0
		denvp = denv
	attribute = __get_xobj_attribute(xobj, '-denvp')
	use_denvp = attribute.boolean;
	if use_denvp:
		attribute = __get_xobj_attribute(xobj, 'denvp')
		denvp = attribute.real;
	attribute = __get_xobj_attribute(xobj, '-dnMax')
	use_dnMax = attribute.boolean;
	if use_dnMax:
		attribute = __get_xobj_attribute(xobj, 'dnMax')
		dnMax = attribute.real;
	else:
		dnMax = 1.0
	attribute = __get_xobj_attribute(xobj, '-dpMax')
	use_dpMax = attribute.boolean;
	if use_dpMax:
		attribute = __get_xobj_attribute(xobj, 'dpMax')
		dpMax = attribute.real;
	else:
		dpMax = 1.0
	return Ec.value, ft.value, f0n.value, beta, An, Bn, Ap, epscu, denv, denvp, dnMax, dpMax

def __computeConstitutiveLaw(Ec, ft, f0n, beta, An, Bn, Ap, epscu, denv, denvp, dnMax, dpMax, eps):
	import math
	sig = [0] * len(eps)
	# PyMpc.IO.write_cerr(str(sig) +'\n')
	r0n = abs(f0n)
	eps0n = f0n/Ec
	r0p = ft
	eps0p = ft/Ec
	dn = 0
	dp = 0
	eps_p_n = 0
	sig_eff = 0
	rn = r0n
	rp = r0p
	for i in range(1,len(eps)):
		deps = eps[i] - eps[i-1]
		sig_eff_t = sig_eff + Ec * deps
		# BOX 1
		if beta > 0:
			# Calcolo taun e taup
			if sig_eff_t < 0:
				# Compressione
				taun = abs(sig_eff_t);
				taup = 0.0
			else:
				# Trazione
				taun = 0.0;
				taup = sig_eff_t
			if taun > rn or taup > rp:
				if sig_eff_t < 0:
					# Compressione
					alfa = taun/rn
					depsa = sig_eff_t/Ec*(1-1/alfa)
					lamda = 1 - beta/sig_eff_t * Ec * depsa
					sig_eff_cap = sig_eff_t * lamda
					taun = abs(sig_eff_t)
					if taun > rn:
						sig_eff = sig_eff_cap
					else:
						sig_eff = sig_eff_t
				else:
					# Trazione
					alfa = taup/rp
					depsa = sig_eff_t/Ec*(1-1/alfa)
					lamda = 1 - beta/sig_eff_t*Ec*depsa
					sig_eff_cap = sig_eff_t * lamda
					taup = sig_eff_cap
					if taup > rp:
						sig_eff = sig_eff_cap
					else:
						sig_eff = sig_eff_t
			else:
				sig_eff = sig_eff_t
		else:
			sig_eff = sig_eff_t
		# END OF BOX 1
		# BOX 2
		if sig_eff < 0:
			# Compressione
			taun = abs(sig_eff);
			taup = 0.0
		else:
			# Trazione
			taun = 0.0;
			taup = sig_eff
		if taun > rn:
			rn = taun
		if taup > rp:
			rp = taup
		dn = 1 - math.sqrt(r0n/rn) * (1-An) - An* math.exp(Bn*(1-math.sqrt(rn/r0n)))
		if eps[i] <= epscu:
			dn = 1
		if dn < 0:
			dn = 0.0
		if dn > dnMax:
			dn = dnMax
		dp = 1 - r0p/rp * math.exp(Ap*(1-(rp/r0p)))
		if dp < 0:
			dp = 0.0
		if dp > dpMax:
			dp = dpMax

		if sig_eff < 0:
			# Compressione
			sig_i = (1-denv)*(1-dn)*sig_eff
		else:
			# Trazione
			sig_i = (1-denvp)*(1-dp)*sig_eff
		sig[i] = sig_i

	return sig

def __compute_Tensile_Law(xobj):
	# Take default parameters
	Ec, ft, f0n, beta, An, Bn, Ap, epscu, denv, denvp, dnMax, dpMax = __get_constitutive_parameters(xobj)
	# Compute law
	eps_t = ft / Ec
	# PyMpc.IO.write_cerr('eps_t = {} / {} = {} \n'.format(ft,Ec,eps_t))
	eps = [x * eps_t/2.0 for x in range(0, 20)]
	sig = [0] * len(eps)
	# PyMpc.IO.write_cerr(str(eps) +'\n')
	sig = __computeConstitutiveLaw(Ec, ft, f0n, beta, An, Bn, Ap, epscu, denv, denvp, dnMax, dpMax, eps)
	# PyMpc.IO.write_cerr(str(sig) +'\n')
	# 1) create the chart data
	data = MpcChartData(1)
	data.name = "Envelope"
	data.xLabel = "Strain"
	data.yLabel = "Stress"
	# Create tension envelope
	data.x = Math.double_array(eps)
	data.y = Math.double_array(sig)
	return data

def __compute_Compressive_Law(xobj):

	def compute_MaxEps(Ec, f0n, beta, An, Bn, epscu, dnMax):
		def compute_Stress_Given_Strain(Ec, f0n, beta, An, Bn, epscu, dnMax, eps):
			import math
			r0n = abs(f0n)
			eps0n = f0n/Ec
			dn = 0
			eps_p_n = 0
			sig_eff = 0
			rn = r0n
			sig_eff_t = Ec * eps
			# BOX 1
			if beta > 0:
				# Calcolo taun
				taun = abs(sig_eff_t);
				if taun > rn:
					epsp = beta * (eps - eps0n)
					sig_eff = Ec * (eps-epsp)
				else:
					sig_eff = sig_eff_t
			else:
				sig_eff = sig_eff_t
			# END OF BOX 1
			# BOX 2
			taun = abs(sig_eff);
			if taun > rn:
				rn = taun
			dn = 1 - math.sqrt(r0n/rn) * (1-An) - An* math.exp(Bn*(1-math.sqrt(rn/r0n)))
			if dn < 0:
				dn = 0.0
			if dn > dnMax:
				dn = dnMax
			sig = (1-denv)*(1-dn)*sig_eff

			return sig

		# Tentativo: parto da 100 volte eps_0n
		a = f0n / Ec
		sig_a = f0n
		b = f0n / Ec * 100
		sig_b = compute_Stress_Given_Strain(Ec, f0n, beta, An, Bn, epscu, dnMax, b)
		it = 0
		IT_MAX = 100
		TOL = 1e-7
		# PyMpc.IO.write_cerr('a = {} / sig(a) = {} \n'.format(a,sig_a))
		# PyMpc.IO.write_cerr('b = {} / sig(b) = {} \n'.format(b,sig_b))
		while abs(a-b) > TOL and it < IT_MAX:
			it = it+1
			# PyMpc.IO.write_cerr('Iteration {}\n'.format(it))
			# PyMpc.IO.write_cerr('a = {} / sig(a) = {} \n'.format(a,sig_a))
			# PyMpc.IO.write_cerr('b = {} / sig(b) = {} \n'.format(b,sig_b))
			m = (a+b) / 2.0
			sig_m = compute_Stress_Given_Strain(Ec, f0n, beta, An, Bn, epscu, dnMax, m)
			# PyMpc.IO.write_cerr('m = {} / sig(m) = {} \n'.format(m,sig_m))
			if sig_m <= -0.01:
				a = m
				sig_a = sig_m
			else:
				b = m
				sig_b = sig_m
		if it >= IT_MAX:
			PyMpc.IO.write_cerr('Impossibile to find solution within {} iteration \n'.format(IT_MAX))
			m = 100 * f0n / Ec
		m = max(m,epscu)
		return m


	# Take default parameters
	Ec, ft, f0n, beta, An, Bn, Ap, epscu, denv, denvp, dnMax, dpMax = __get_constitutive_parameters(xobj)
	# Compute law
	eps_0n = f0n / Ec
	# PyMpc.IO.write_cerr('eps_0n = {} / {} = {} \n'.format(f0n,Ec,eps_0n))
	maxEps = compute_MaxEps(Ec, f0n, beta, An, Bn, epscu, dnMax)
	# PyMpc.IO.write_cerr(str(maxEps) +'\n')
	n = int((maxEps*1.1) // eps_0n + 1)
	# PyMpc.IO.write_cerr(str(n) +'\n')
	eps = [x * eps_0n/3.0 for x in range(0, n*3)]
	sig = [0] * len(eps)
	# PyMpc.IO.write_cerr(str(eps) +'\n')
	sig = __computeConstitutiveLaw(Ec, ft, f0n, beta, An, Bn, Ap, epscu, denv, denvp, dnMax, dpMax, eps)
	# PyMpc.IO.write_cerr(str(sig) +'\n')
	# 1) create the chart data
	data = MpcChartData(2)
	data.name = "Envelope"
	data.xLabel = "Strain"
	data.yLabel = "Stress"
	# Create tension envelope
	data.x = Math.double_array(eps)
	data.y = Math.double_array(sig)
	return data

def onEditBegin(editor, xobj):

	# a utility lambda to create a label
	def make_label(text):
		label = MpcLabelWidget()
		label.text = text
		label.alignCenter()
		return label

	# how to create a chart and plot it
	data = __compute_Tensile_Law(xobj)
	# 2) create the chart data graphic item
	item = MpcChartDataGraphicItem(data)
	item.color = QColor(255, 0, 0, 255)
	item.thickness = 2.0
	item.penStype = QPenStyle.SolidLine
	# 3) create the chart, and add all chart data graphic items you want
	chart = MpcChart(1)
	chart.addItem(item)
	# 4) make the chart widget and set the chart to plot
	chart_widget = MpcChartWidget()
	chart_widget.setMinimumWidth(200)
	chart_widget.setMinimumHeight(200)
	chart_widget.chart = chart
	# 5) add chart widget to editor
	editor.requestAddCustomWidget(
		make_label(
			html_par(html_begin()) +
			html_par(html_boldtext('Concrete Damage - Tension')) +
			html_par('The uniaxial response of the concrete damage model in tension') +
			html_end()),
		"ChartWidgetLabelT")
	editor.requestAddCustomWidget(chart_widget, "ChartWidgetT")
	editor.requestAddCustomWidget(MpcHorizontalSeparatorWidget(), "ChartWidgetSeparatorT")

	# how to create a chart and plot it
	data = __compute_Compressive_Law(xobj)
	# 2) create the chart data graphic item
	item = MpcChartDataGraphicItem(data)
	item.color = QColor(255, 0, 0, 255)
	item.thickness = 2.0
	item.penStype = QPenStyle.SolidLine
	# 3) create the chart, and add all chart data graphic items you want
	chart = MpcChart(2)
	chart.addItem(item)
	# 4) make the chart widget and set the chart to plot
	chart_widget = MpcChartWidget()
	chart_widget.setMinimumWidth(200)
	chart_widget.setMinimumHeight(200)
	chart_widget.chart = chart
	# 5) add chart widget to editor
	editor.requestAddCustomWidget(
		make_label(
			html_par(html_begin()) +
			html_par(html_boldtext('Concrete Damage - Compression')) +
			html_par('The uniaxial response of the concrete damage model in compression') +
			html_end()),
		"ChartWidgetLabelC")
	editor.requestAddCustomWidget(chart_widget, "ChartWidgetC")
	editor.requestAddCustomWidget(MpcHorizontalSeparatorWidget(), "ChartWidgetSeparatorC")

class __constants:
	groups_for_section_update = ([
		'Non-linear',
		'Optional parameters',
		'-epscu',
		'-denv',
		'-denvp',
		'-dpMax',
		'-dnMax'])
		
def __updateCharts(editor, xobj):
	# chart 1: change color
	chart_widget = editor.getCustomWidget("ChartWidgetT")
	chart = chart_widget.chart
	item = chart.items[0]
	# item.color = QColor(0, 0, 255, 255)
	data = __compute_Tensile_Law(xobj)
	item.data = data
	chart_widget.chart = chart
	# chart 2: change data
	chart_widget = editor.getCustomWidget("ChartWidgetC")
	chart = chart_widget.chart
	item = chart.items[0]
	data = __compute_Compressive_Law(xobj)
	item.data = data
	chart_widget.chart = chart

def onAttributeChanged(editor, xobj, attribute_name):

	'''
	This method is called everytime the value of an attribute is changed.
	The xobject containing the modified attribute and the attribute name
	are passed as input arguments to this function.
	'''
	attribute = __get_xobj_attribute(xobj, attribute_name)
	# print('Called onAttribute Changed')
	
	if attribute.group == 'UtilsExp':
		# PyMpc.IO.write_cerr('Plot experimental/Reference points \n')
		useExp_at = __get_xobj_attribute(xobj, '-useExp')
		useExp = useExp_at.boolean
		if not useExp:
			chart_widget = editor.getCustomWidget("ChartWidgetC")
			chart = chart_widget.chart
			if len(chart.items) > 1:
				chart.removeItem(1)
			chart_widget.chart = chart
			
			chart_widget = editor.getCustomWidget("ChartWidgetT")
			chart = chart_widget.chart
			if len(chart.items) > 1:
				chart.removeItem(1)
			chart_widget.chart = chart
	if attribute.group == 'UtilsGen':
		PyMpc.IO.write_cerr('Modified selection Genetic \n')
		# Verificare se dobbiamo fare calcolo automatico
		useGenetic_at = __get_xobj_attribute(xobj, '-useGenetic')
		useGenetic = useGenetic_at.boolean
		if useGenetic:
			# Salvo i dati attuali come backup se il flag è falso
			# Take default parameters
			# print('use Genetic: Calcolo dei parametri in automatico. Prima salvo backup')
			backedup_at = __get_xobj_attribute(xobj, 'backupFlag')
			if not backedup_at.boolean:
				PyMpc.IO.write_cerr('Use Genetic - Salvo valori di backup\n')
				Ec, ft, f0n, beta, An, Bn, Ap, epscu, denv, denvp, dnMax, dpMax = __get_constitutive_parameters(xobj)
				backupParameters_at = __get_xobj_attribute(xobj, 'backupParameters')
				backup_list = [Ec, ft, f0n, beta, An, Bn, Ap, epscu, denv, denvp]
				PyMpc.IO.write_cerr('Ec, ft, f0n, beta, An, Bn, Ap, epscu, denv, denvp\n{}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n'.format(Ec, ft, f0n, beta, An, Bn, Ap, epscu, denv, denvp))
				backup_vec = PyMpc.Math.vec(len(backup_list))
				for i in range(len(backup_list)):
					backup_vec[i] = backup_list[i]
				backupParameters_at.quantityVector.referenceValue = backup_vec
				backedup_at.boolean = True
				# print('Backed up attribute: {}'.format(backedup_at.boolean))
			# print('Salvati valori di backup. Sscrivo i nuovi automatici')
			attr = __get_xobj_attribute(xobj, 'Ec')
			attr.quantityScalar.referenceValue = 22087
			attr = __get_xobj_attribute(xobj, 'f0n')
			attr.quantityScalar.referenceValue = -36.17
			attr = __get_xobj_attribute(xobj, 'An')
			attr.real = 5.88903
			attr = __get_xobj_attribute(xobj, 'Bn')
			attr.real = 0.63546
			# Aggiorna il grafico con questi dati
			__updateCharts(editor, xobj)
			# print('Scritti gli attributi automatici')
			# Algoritmo genetico da avviare su un processo separata. Questo mi darà i parametri della legge calibrati sugli sperimentali
			# Calibro solo compressione perché trazione è una semplice esponenziale. Gioco con un solo parametro finché torna
			# Compressione
		else:
			# Ripristina i valori di default
			backupParameters_at = __get_xobj_attribute(xobj, 'backupParameters')
			backup_vec = backupParameters_at.quantityVector
			Ec = backup_vec.valueAt(0)
			ft = backup_vec.valueAt(1)
			f0n = backup_vec.valueAt(2)
			beta = backup_vec.valueAt(3)
			An = backup_vec.valueAt(4)
			Bn = backup_vec.valueAt(5)
			Ap = backup_vec.valueAt(6)
			eps_cu = backup_vec.valueAt(7)
			denv = backup_vec.valueAt(8)
			denvp = backup_vec.valueAt(9)
			__set_backup_parameters(xobj,Ec,ft,f0n,beta,An,Bn,Ap,eps_cu,denv,denvp)
			backedup_at = __get_xobj_attribute(xobj, 'backupFlag')
			backedup_at.boolean = True
			__updateCharts(editor, xobj)
			PyMpc.IO.write_cerr('Ritorna ai valori di default\n')
			print('Flag backedup {}\n'.format(backedup_at.boolean))
			
			
	if attribute.group == 'useExpList':
		# Usa una lista specificata dall'utente
		# compressione
		epsC_at = __get_xobj_attribute(xobj, 'expEpsilonC')
		sigC_at = __get_xobj_attribute(xobj, 'expSigmaC')
		epsC = epsC_at.quantityVector
		sigC = sigC_at.quantityVector
		
		if len(epsC) != len(sigC):
			# hanno lunghezze diverse
			n = min(len(epsC),len(sigC))
		else:
			n = len(epsC)
		if n > 0:
			eps, sig = [], []
			for i in range(n):
				eps.append(-abs(epsC.valueAt(i)))
				sig.append(-abs(sigC.valueAt(i)))
				
			chart_widget = editor.getCustomWidget("ChartWidgetC")
			chart = chart_widget.chart
			data = MpcChartData(3)
			data.name = "Reference"
			# Create tension envelope
			data.x = Math.double_array(eps)
			data.y = Math.double_array(sig)
			if len(chart.items) == 1:
				# item.data = data
				item = MpcChartDataGraphicItem(data)
				item.color = QColor(0, 0, 255, 255)
				item.thickness = 1.5
				item.penStype = QPenStyle.DashLine # SolidLine
				chart.addItem(item)
			else:
				item = chart.items[1]
				item.data = data
			chart_widget.chart = chart
		
		# trazione
		epsT_at = __get_xobj_attribute(xobj, 'expEpsilonT')
		sigT_at = __get_xobj_attribute(xobj, 'expSigmaT')
		epsT = epsT_at.quantityVector
		sigT = sigT_at.quantityVector
		
		if len(epsT) != len(sigT):
			# hanno lunghezze diverse
			n = min(len(epsT),len(sigT))
		else:
			n = len(epsC)
		if n > 0:
			eps, sig = [], []
			for i in range(n):
				eps.append(abs(epsT.valueAt(i)))
				sig.append(abs(sigT.valueAt(i)))
				
			chart_widget = editor.getCustomWidget("ChartWidgetT")
			chart = chart_widget.chart
			data = MpcChartData(3)
			data.name = "Reference"
			# Create tension envelope
			data.x = Math.double_array(eps)
			data.y = Math.double_array(sig)
			if len(chart.items) == 1:
				# item.data = data
				item = MpcChartDataGraphicItem(data)
				item.color = QColor(0, 0, 255, 255)
				item.thickness = 1.5
				item.penStype = QPenStyle.DashLine # SolidLine
				chart.addItem(item)
			else:
				item = chart.items[1]
				item.data = data
			chart_widget.chart = chart
	
	if attribute.group == 'useExpFile':
		# PyMpc.IO.write_cerr('Changed and attribute in Utils \n')
		# Load in chart experimental-reference data
		# Load file data
		# Prendi li nome del file dall'attributo corrispondente -> non sono riuscito a fare aprire titolo file
		fileName_at = __get_xobj_attribute(xobj, 'fileNameC')
		if (fileName_at is None):
			raise Exception('Error: cannor find "fileNameC" attribute')
		else:
			fileName = fileName_at.string
			chart_widget = editor.getCustomWidget("ChartWidgetC")
			chart = chart_widget.chart
			if not fileName:
				if len(chart.items) > 1:
					chart.removeItem(1)
			else:
				try:
					fileObj = open(fileName, 'r')
				except (OSError, IOError):
					PyMpc.IO.write_cerr('File "{}" not found \n'.format(fileName))
					if len(chart.items) > 1:
						chart.removeItem(1)
					chart_widget.chart = chart
				else:
					# Lettura dei dati e salvataggio sulle liste
					eps, sig = [], []
					for line in fileObj:
						values = [float(s) for s in line.split()]
						if values[0] > 0:
							eps.append(-values[0])
						else:
							eps.append(values[0])
						if values[1] > 0:
							sig.append(-values[1])
						else:
							sig.append(values[1])
					fileObj.close()
					# item = chart.items[0]
					# item.color = QColor(0, 0, 255, 255)
					# PyMpc.IO.write_cerr('Creation of a new item \n')
					data = MpcChartData(3)
					data.name = "Reference"
					# Create tension envelope
					data.x = Math.double_array(eps)
					data.y = Math.double_array(sig)
					if len(chart.items) == 1:
						# item.data = data
						item = MpcChartDataGraphicItem(data)
						item.color = QColor(0, 0, 255, 255)
						item.thickness = 1.5
						item.penStype = QPenStyle.DashLine # SolidLine
						chart.addItem(item)
					else:
						item = chart.items[1]
						item.data = data
			chart_widget.chart = chart
			
		fileName_at = __get_xobj_attribute(xobj, 'fileNameT')
		if (fileName_at is None):
			raise Exception('Error: cannor find "fileNameT" attribute')
		else:
			fileName = fileName_at.string
			chart_widget = editor.getCustomWidget("ChartWidgetT")
			chart = chart_widget.chart
			if not fileName:
				if len(chart.items) > 1:
					chart.removeItem(1)
			else:
				try:
					fileObj = open(fileName, 'r')
				except (OSError, IOError):
					PyMpc.IO.write_cerr('File "{}" not found \n'.format(fileName))
					if len(chart.items) > 1:
						chart.removeItem(1)
					chart_widget.chart = chart
				else:
					# Lettura dei dati e salvataggio sulle liste
					eps, sig = [], []
					for line in fileObj:
						values = [float(s) for s in line.split()]
						if values[0] < 0:
							eps.append(-values[0])
						else:
							eps.append(values[0])
						if values[1] < 0:
							sig.append(-values[1])
						else:
							sig.append(values[1])
					fileObj.close()
					# item = chart.items[0]
					# item.color = QColor(0, 0, 255, 255)
					# PyMpc.IO.write_cerr('Creation of a new item \n')
					data = MpcChartData(3)
					data.name = "Reference"
					# Create tension envelope
					data.x = Math.double_array(eps)
					data.y = Math.double_array(sig)
					if len(chart.items) == 1:
						# item.data = data
						item = MpcChartDataGraphicItem(data)
						item.color = QColor(0, 0, 255, 255)
						item.thickness = 1.5
						item.penStype = QPenStyle.DashLine # SolidLine
						chart.addItem(item)
					else:
						item = chart.items[1]
						item.data = data
			chart_widget.chart = chart
		
	# if attribute.group in __constants.groups_for_section_update:
		# print('L\'attributo fa parte del gruppo per aggiornamento curva')
		# print(attribute.group)
		# print(attribute.name)
	if attribute.group in __constants.groups_for_section_update:
		PyMpc.IO.write_cerr('Changed an attribute of constitutive law \n')
		backedup_at = __get_xobj_attribute(xobj, 'backupFlag')
		backedup_at.boolean = False
		useGenetic_at = __get_xobj_attribute(xobj, '-useGenetic')
		if useGenetic_at.boolean:	
			useGenetic_at.boolean = False
			# print('Manual change of parameters, disabled Genetic option')
		# print('Backedup: {}\nuseGenetic: {}\n'.format(backedup_at.boolean, useGenetic_at.boolean))
			
		# update charts
		__updateCharts(editor, xobj)

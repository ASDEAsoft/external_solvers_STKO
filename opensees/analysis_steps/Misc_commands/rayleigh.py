# enable default distribution tester for this module
from opensees.analysis_steps.Misc_commands.utils.tester.RayleighDampingTester import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from itertools import groupby, count
import PyMpc
import PyMpc.Math
from math import exp, pi
import opensees.utils.tcl_input as tclin

class _internals:
	version = 1 # the current version

def makeXObjectMetaData():
	
	def mka(type, name, group, descr, default=None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.descr = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(descr + '<br/>') +
			html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Rayleigh_Damping_Command','rayleigh')+'<br/>') +
			html_end()
			)
		if default:
			a.setDefault(default)
		return a
	
	type = mka(MpcAttributeType.String, 'Input Type', 'Input Type', 
		('Choose how to input your values:<br/>'
		'"Automatic" (Default): you can input the 2 frequencies of interest and the 2 damping ratios. The damping coefficients will be computed automatically.<br/>'
		'"Manual": you can directly input the 2 damping coefficients.'))
	type.sourceType = MpcAttributeSourceType.List
	type.setSourceList(['Automatic', 'Manual'])
	type.setDefault('Automatic')
	
	f1 = mka(MpcAttributeType.Real, 'f1/Rayleigh', 'Rayleigh Input Parameters', 'First frequency', default = 1.0)
	f2 = mka(MpcAttributeType.Real, 'f2/Rayleigh', 'Rayleigh Input Parameters', 'Second frequency', default = 2.0)
	csi1 = mka(MpcAttributeType.Real, 'damp_1/Rayleigh', 'Rayleigh Input Parameters', 'First damping ratio', default = 0.05)
	csi2 = mka(MpcAttributeType.Real, 'damp_2/Rayleigh', 'Rayleigh Input Parameters', 'Second damping ratio', default = 0.05)
	
	alphaM = mka(MpcAttributeType.Real, 'alphaM/Rayleigh', 'Calculated Rayleigh Damping Parameters', 'Mass propotional damping coefficient')
	Betak = mka(MpcAttributeType.Real, 'Betak/Rayleigh', 'Calculated Rayleigh Damping Parameters', 'Stiffness propotional damping coefficient')
	
	alphaM_user = mka(MpcAttributeType.Real, 'alphaM/RayleighUser', 'Rayleigh Damping Parameters', 'Mass propotional damping coefficient')
	Betak_user = mka(MpcAttributeType.Real, 'Betak/RayleighUser', 'Rayleigh Damping Parameters', 'Stiffness propotional damping coefficient')
	
	Kcurr = mka(MpcAttributeType.Boolean, 'Kcurr/Rayleigh', 'Stiffness Beta Type', 'Propotional to current stiffness', default = True)
	Kinit = mka(MpcAttributeType.Boolean, 'Kinit/Rayleigh', 'Stiffness Beta Type', 'Propotional to initial stiffness', default = False)
	Kcomm = mka(MpcAttributeType.Boolean, 'Kcomm/Rayleigh', 'Stiffness Beta Type', 'Propotional to committed stiffness', default = False)
	
	xom = MpcXObjectMetaData()
	xom.name = 'rayleigh'
	xom.addAttribute(type)
	xom.addAttribute(f1)
	xom.addAttribute(f2)
	xom.addAttribute(csi1)
	xom.addAttribute(csi2)
	xom.addAttribute(alphaM)
	xom.addAttribute(Betak)
	xom.addAttribute(alphaM_user)
	xom.addAttribute(Betak_user)
	xom.addAttribute(Kcurr)
	xom.addAttribute(Kinit)
	xom.addAttribute(Kcomm)
	
	# add a last attribute for versioning
	av = MpcAttributeMetaData()
	av.type = MpcAttributeType.Integer
	av.name = 'version'
	av.setDefault(_internals.version)
	av.editable = False
	xom.addAttribute(av)
	
	return xom

def _onAttributeChangedInternal(xobj, attribute_name):
	if attribute_name == 'Input Type':
		def geta(name):
			at = xobj.getAttribute(name)
			if at is None:
				raise Exception('Error: cannot find "{}" attribute'.format(name))
			return at
		type = geta('Input Type').string
		automatic = (type == "Automatic")
		geta('f1/Rayleigh').visible = automatic
		geta('f2/Rayleigh').visible = automatic
		geta('damp_1/Rayleigh').visible = automatic
		geta('damp_2/Rayleigh').visible = automatic
		geta('alphaM/Rayleigh').visible = automatic
		geta('Betak/Rayleigh').visible = automatic
		geta('alphaM/RayleighUser').visible = not automatic
		geta('Betak/RayleighUser').visible = not automatic
		
def onAttributeChanged(editor, xobj, attribute_name):
	onAttributeChanged_Tester(editor, xobj, attribute_name)
	_onAttributeChangedInternal(xobj, attribute_name)

def onEditBegin(editor, xobj):
	onEditBegin_Tester(editor, xobj)
	onAttributeChanged(editor, xobj, 'Input Type')

def onConvertOldVersion(xobj, old_xobj):
	
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	'''
	try to convert objects from old versions to the current one.
	current version: 1
	'''
	
	version = 0 # default one
	av = old_xobj.getAttribute('version')
	if av:
		version = av.integer
	
	# just a safety check
	cav = xobj.getAttribute('version')
	if cav is None:
		IO.write_cerr('Cannot find "version" attribute in rayleigh\n')
		return
	cav.integer = _internals.version
	
	if version == 0:
		# Note: in version 1, betaK keeps the same value and by default the Kcurr flag is on
		geta('Betak/RayleighUser').real = geta('Betak/Rayleigh').real
		geta('alphaM/RayleighUser').real = geta('alphaM/Rayleigh').real
		geta('Input Type').string = 'Manual'
		bkinit = old_xobj.getAttribute('betaKinit/Rayleigh')
		if (bkinit is not None) and (bkinit.real > 0.0):
			geta('Betak/RayleighUser').real = bkinit.real
			geta('Kcurr/Rayleigh').boolean = False
			geta('Kinit/Rayleigh').boolean = True
			print('rayleigh: convert from old: betaKinit')
		else:
			bkcommit = old_xobj.getAttribute('betaKcomm/Rayleigh')
			if (bkcommit is not None) and (bkcommit.real > 0.0):
				geta('Betak/RayleighUser').real = bkcommit.real
				geta('Kcurr/Rayleigh').boolean = False
				geta('Kcomm/Rayleigh').boolean = True
				print('rayleigh: convert from old: betaKcomm')
		_onAttributeChangedInternal( xobj, 'Input Type')
		
		
def writeTcl(pinfo):
	
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	# rayleigh $ alphaM $ betaK $ betaKinit $ betaKcomm
	
	xobj = pinfo.analysis_step.XObject
	regTag = xobj.parent.componentId
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# default
	betaK = 0.0
	betaKinit = 0.0
	betaKcomm = 0.0
	
	if geta('Input Type').string == 'Manual':
		alphaM = geta('alphaM/RayleighUser').real
		beta = geta('Betak/RayleighUser').real
	else:
		alphaM = geta('alphaM/Rayleigh').real
		beta = geta('Betak/Rayleigh').real
	
	if geta('Kcurr/Rayleigh').boolean:
		betaK = beta
	if geta('Kinit/Rayleigh').boolean:
		betaKinit = beta
	if geta('Kcomm/Rayleigh').boolean:
		betaKcomm = beta
	
	pinfo.out_file.write('{}rayleigh {} {} {} {}\n'.format(pinfo.indent, alphaM, betaK, betaKinit, betaKcomm))
# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *
from opensees.utils.override_utils import get_function_from_module

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import math
import json
import os
import io

####################################################################################
# Utilities
####################################################################################

def _geta(xobj, name):
	at = xobj.getAttribute(name)
	if at is None:
		raise Exception('Error: cannot find "{}" attribute'.format(name))
	return at

class _globals:
	_js_storage = None
	def js():
		if _globals._js_storage is None:
			with open(os.path.join(os.path.dirname(__file__), 'ASDPlasticMaterial.json'), 'r') as fo:
				_globals._js_storage = json.load(fo)
		return _globals._js_storage

####################################################################################
# CHECKS for user-interaction
####################################################################################

def _check(xobj):
	# todo: all checks and hide/show policy here.
	# for optimization it can be done selectively
	#
	# get the structure
	js = _globals.js()
	EL = js['EL']
	YF = js['YF']
	PF = js['PF']
	HL = js['HL']
	HL_tensor = HL['tensor']
	HL_scalar = HL['scalar']
	#
	# visibilty
	# set everything to hidden
	for _, item in xobj.attributes.items():
		if item.group == 'Parameters' or item.group == 'Variables':
			item.visible = False
	# selectively show necessary ones
	el = xobj.getAttribute('Elasticity').string
	yf = xobj.getAttribute('Yeld Function').string
	pf = xobj.getAttribute('Plastic Flow').string
	# elasticity
	for item in EL[el].get('parameters', {}):
		xobj.getAttribute(item).visible = True
	# yf
	for setting in (YF[yf], PF[pf]):
		for param_name in setting.get('parameters', {}):
			xobj.getAttribute(param_name).visible = True
		for var_name, var_type in setting.get('variables', {}).items():
			source_hl = HL_scalar if var_type == 'scalar' else HL_tensor
			for trial_name in (var_name, '{}-Value'.format(var_name)):
				attr = xobj.getAttribute(trial_name)
				if attr: attr.visible = True
			attr = xobj.getAttribute(var_name)
			curr_hl = attr.string
			hl = source_hl[curr_hl]
			for param_name in hl.get('parameters', {}):
				xobj.getAttribute(param_name).visible = True
	# make sure all tensors are with 6-components
	for _, attr in xobj.attributes.items():
		if attr.type == MpcAttributeType.QuantityVector:
			source = attr.quantityVector.referenceValue
			if len(source) != 6:
				new_value = Math.vec(6)
				for i in range(min(len(source), 6)):
					new_value[i] = source[i]
				attr.quantityVector.referenceValue = new_value
				#IO.write_cerr('ASDPlasticMaterial Warning: attribute "{}" changed to 6-components'.format(attr.name))

_onEditBegin = get_function_from_module(__name__, 'onEditBegin')
def onEditBegin(editor, xobj):
	if _onEditBegin: _onEditBegin(editor, xobj)
	_check(xobj)

_onAttributeChanged = get_function_from_module(__name__, 'onAttributeChanged')
def onAttributeChanged(editor, xobj, attribute_name):
	if _onAttributeChanged: _onAttributeChanged(editor, xobj, attribute_name)
	_check(xobj)

def makeXObjectMetaData():
	
	# get the structure
	js = _globals.js()
	
	def mka(name, group, descr, atype, adim = None, dval = None):
		a = MpcAttributeMetaData()
		a.type = atype
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			# todo: change with compiled doc asap
			html_par(html_href('https://github.com/OpenSees/OpenSeesDocumentation/blob/master/source/user/manual/material/ndMaterials/ASDPlasticMaterial.rst','ASDPlasticMaterial')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	
	# EL
	EL = js['EL']
	EL_values = list(EL.keys())
	el = mka('Elasticity', 'Template', 'The Elasticity Type', MpcAttributeType.String, dval = EL_values[0])
	el.sourceType = MpcAttributeSourceType.List
	el.setSourceList(EL_values)
	
	# YF
	YF = js['YF']
	YF_values = list(YF.keys())
	yf = mka('Yeld Function', 'Template', 'The Yield Function Type', MpcAttributeType.String, dval = YF_values[0])
	yf.sourceType = MpcAttributeSourceType.List
	yf.setSourceList(YF_values)
	
	# PF
	PF = js['PF']
	PF_values = list(PF.keys())
	pf = mka('Plastic Flow', 'Template', 'Plastic Flow Type', MpcAttributeType.String, dval = PF_values[0])
	pf.sourceType = MpcAttributeSourceType.List
	pf.setSourceList(PF_values)
	
	# collect all hardening laws
	HL = js['HL']
	# scalar
	HL_scalar = HL['scalar']
	HL_scalar_values = list(HL_scalar.keys())
	# tensor
	HL_tensor = HL['tensor']
	HL_tensor_values = list(HL_tensor.keys())
	
	# variables
	variable_dict = {}
	for setting in (YF, PF):
		for _, item in setting.items():
			vars = item.get('variables', {})
			for key, value in vars.items():
				attr = variable_dict.get(key)
				if attr is None:
					# make the attribute and add it
					source = HL_scalar_values if value == 'scalar' else HL_tensor_values
					if len(source) > 0:
						attr = mka(key, 'Variables', '',  MpcAttributeType.String, dval=source[0])
						attr.sourceType = MpcAttributeSourceType.List
						attr.setSourceList(source)
						# the variable
						variable_dict[key] = attr
						# and its initialization value
						val_key = '{}-Value'.format(key)
						if value == 'scalar':
							attr_val = mka(val_key, 'Variables', '',  MpcAttributeType.Real, dval=0.0)
						else:
							attr_val = mka(val_key, 'Variables', '',  MpcAttributeType.QuantityVector)
						variable_dict[val_key] = attr_val
	
	# parameters
	param_dict = {}
	for setting in (EL, YF, PF, HL_scalar, HL_tensor):
		for _, item in setting.items():
			param = item.get('parameters', {})
			for key, value in param.items():
				attr = param_dict.get(key)
				if attr is None:
					# make the attribute and add it
					attr = mka(key, 'Parameters', '',  MpcAttributeType.Real, dval=0.0)
					# done
					param_dict[key] = attr
	
	# xom
	xom = MpcXObjectMetaData()
	xom.name = 'ASDPlasticMaterial'
	xom.Xgroup = 'ASDEASoftware'
	
	# Template
	xom.addAttribute(el)
	xom.addAttribute(yf)
	xom.addAttribute(pf)
	# Variables
	for _, attr in variable_dict.items():
		xom.addAttribute(attr)
	# Parameters
	for _, attr in param_dict.items():
		xom.addAttribute(attr)
	
	# done
	return xom

def writeTcl(pinfo):
	
	# the stream
	ss = io.StringIO()
	
	# xobj and tag
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# get the structure
	js = _globals.js()
	
	# get basic parameters
	el = _geta(xobj, 'Elasticity').string
	yf = _geta(xobj, 'Yeld Function').string
	pf = _geta(xobj, 'Plastic Flow').string
	ss.write('{0}nDMaterial ASDPlasticMaterial {1} \\\n{0}{5}{2} \\\n{0}{5}{3} \\\n{0}{5}{4} \\\n'.format(pinfo.indent, tag, yf, pf, el, pinfo.tabIndent))
	
	# build the IV_TYPE string
	YF = js['YF']
	current_YF = YF[yf]
	PF = js['PF']
	current_PF = PF[pf]
	processed = {}
	for item in (current_YF, current_PF):
		vars = list(item.get('variables', {}).keys())
		for var in vars:
			if not var in processed:
				processed[var] = xobj.getAttribute(var).string
	IV_TYPE = ''.join('{}({}):'.format(var_name, har_type) for var_name,har_type in processed.items())
	ss.write('{0}{1}{2} \\\n'.format(pinfo.indent, pinfo.tabIndent, IV_TYPE))
	
	# internal variables
	ss.write('{0}{1}Begin_Internal_Variables \\\n'.format(pinfo.indent, pinfo.tabIndent))
	var_val_postfix = '-Value'
	for _, attr in xobj.attributes.items():
		if attr.visible and attr.group == 'Variables' and attr.name.endswith(var_val_postfix):
			ss.write('{0}{1}{1}{2}'.format(pinfo.indent, pinfo.tabIndent, attr.name[:-len(var_val_postfix)]))
			if attr.type == MpcAttributeType.QuantityVector:
				for i in range(6):
					ss.write(' {:.8g}'.format(attr.quantityVector.valueAt(i)))
			elif attr.type == MpcAttributeType.Real:
				ss.write(' {:.8g}'.format(attr.real))
			else:
				raise Exception('ASDPlasticMaterial Error: unexpected variable type {} {}'.format(attr.name, attr.type))
			ss.write(' \\\n')
	ss.write('{0}{1}End_Internal_Variables \\\n'.format(pinfo.indent, pinfo.tabIndent))
	
	# parameters
	ss.write('{0}{1}Begin_Model_Parameters \\\n'.format(pinfo.indent, pinfo.tabIndent))
	for _, attr in xobj.attributes.items():
		if attr.visible and attr.group == 'Parameters':
			ss.write('{0}{1}{1}{2}'.format(pinfo.indent, pinfo.tabIndent, attr.name))
			if attr.type == MpcAttributeType.Real:
				ss.write(' {:.8g} \\\n'.format(attr.real))
			else:
				raise Exception('ASDPlasticMaterial Error: unexpected parameter type {} {}'.format(attr.name, attr.type))
	ss.write('{0}{1}End_Model_Parameters \\\n'.format(pinfo.indent, pinfo.tabIndent))
	
	# integration options
	
	print(ss.getvalue())
	1/0
	
	
	# obtain the hardening points
	hl_fun = _globals.presets[_geta(xobj, 'Preset').string][0]
	Te,Ts,Td,Ce,Cs,Cd,auto_reg,lch_ref = hl_fun(xobj)
	def to_tcl(x):
		return ' '.join(str(i) for i in x)
	
	# command format
	command = ("{0}nDMaterial ASDConcrete3D {1} {2} {3} \\\n"
		"{0}\t-Te {6} \\\n"
		"{0}\t-Ts {7} \\\n"
		"{0}\t-Td {8} \\\n"
		"{0}\t-Ce {9} \\\n"
		"{0}\t-Cs {10} \\\n"
		"{0}\t-Cd {11} \\\n"
		"{0}\t-rho {4} -eta {5} -Kc {12} -cdf {13}").format(pinfo.indent, tag, E, v, rho, eta, 
			to_tcl(Te), to_tcl(Ts), to_tcl(Td), to_tcl(Ce), to_tcl(Cs), to_tcl(Cd), Kc, cdf)
	
	if _geta(xobj, 'integration').string == 'IMPL-EX':
		#if _geta(xobj, 'implexCheckError').boolean:
		#	command += ' \\\n{}\t-implex -implexAlpha {} -implexControl {} {}'.format(
		#		pinfo.indent,
		#		_geta(xobj, 'implexAlpha').real,
		#		_geta(xobj, 'implexErrorTolerance').real,
		#		_geta(xobj, 'implexErrorTimeReductionLimit').real)
		#else:
		#	command += ' \\\n{}\t-implex -implexAlpha {}'.format(pinfo.indent, _geta(xobj, 'implexAlpha').real)
		#
		# Note 1
		command += ' \\\n{}\t-implex -implexAlpha {}'.format(pinfo.indent, _geta(xobj, 'implexAlpha').real)
	
	if _geta(xobj, '-crackPlanes').boolean:
		command += ' \\\n{}\t-crackPlanes {} {} {}'.format(pinfo.indent, 
			_geta(xobj, 'nct').integer,
			_geta(xobj, 'ncc').integer,
			_geta(xobj, 'smoothingAngle').real)
	
	if _geta(xobj, 'constitutiveTensorType').string == 'Tangent':
		command += ' \\\n{}\t-tangent'.format(pinfo.indent)
	
	if auto_reg:
		command += ' \\\n{}\t-autoRegularization {}'.format(pinfo.indent, lch_ref)
	
	command += '\n'
	
	# now write the string into the file
	pinfo.out_file.write(command)

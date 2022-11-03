from PyMpc import *
from mpc_utils_html import *
import os

def makeXObjectMetaData():
	
	'''
	responseSpectrum $tsTag $direction <-scale $scale> <-mode $mode>
	'''
	
	def mka(type, name, descr):
		at = MpcAttributeMetaData()
		at.type = type
		at.name = name
		at.group = 'Default'
		at.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(descr) +
			html_par(html_href("https://opensees.github.io/OpenSeesDocumentation/user/manual/analysis/responseSpectrumAnalysis.html",'responseSpectrumAnalysis Command')+'<br/>') +
			html_end()
			)
		return at
	
	at_tsTag = mka(
		MpcAttributeType.Index,
		'tsTag',
		'The tag of the time series to be used as the response spectrum function'
		)
	at_tsTag.indexSource.type = MpcAttributeIndexSourceType.Definition
	at_tsTag.indexSource.addAllowedNamespace("timeSeries")
	
	at_direction = mka(
		MpcAttributeType.Integer, 
		'direction', 
		'The 1-based index of the excited DOF (1 to 3 for 2D problems, or 1 to 6 for 3D problems).'
		)
	at_direction.setDefault(1)
	
	at_mode_flag = mka(
		MpcAttributeType.Boolean, 
		'-mode', 
		'Optional. Tells the command to compute the modal displacements for just 1 specified mode (by default all modes are processed).'
		)
	
	at_mode = mka(
		MpcAttributeType.Integer, 
		'mode', 
		'Optional. Mandatory if -mode option is used. The 1-based index of the unique mode to process.'
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'responseSpectrum'
	xom.addAttribute(at_tsTag)
	xom.addAttribute(at_direction)
	xom.addAttribute(at_mode_flag)
	xom.addAttribute(at_mode)
	
	# visibility dependencies
	xom.setVisibilityDependency(at_mode_flag, at_mode)
	
	return xom

def writeTcl(pinfo):
	
	'''
	responseSpectrumAnalysis $tsTag $direction <-scale $scale> <-mode $mode>
	'''
	
	xobj = pinfo.analysis_step.XObject
	
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	at_tsTag = geta('tsTag').index
	at_direction = geta('direction').integer
	at_mode_flag = geta('-mode').boolean
	at_mode = geta('mode').integer
	
	str_tcl = '{}responseSpectrumAnalysis {} {}'.format(pinfo.indent, at_tsTag, at_direction)
	if at_mode_flag:
		str_tcl += ' -mode {}'.format(at_mode)
	str_tcl += '\n'
	
	# now write the string into the file
	pinfo.out_file.write('\n{}# responseSpectrumAnalysis $tsTag $direction <-scale $scale> <-mode $mode>\n'.format(pinfo.indent))
	pinfo.out_file.write(str_tcl)
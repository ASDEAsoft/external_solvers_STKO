from PyMpc import *
from mpc_utils_html import *
import os

def makeXObjectMetaData():
	
	'''
	modalProperties <-print> <-file $reportFileName> <-unorm>
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
			html_par(html_href("https://opensees.github.io/OpenSeesDocumentation/user/manual/analysis/modalProperties.html",'modalProperties Command')+'<br/>') +
			html_end()
			)
		return at
	
	at_print = mka(
		MpcAttributeType.Boolean, 
		'-print', 
		'Optional. If included, a report of the modal properties is printed to the console.'
		)
	
	at_file = mka(
		MpcAttributeType.Boolean, 
		'-file', 
		'Optional. If included, a report of the modal properties is printed to the file $reportFileName.'
		)
	
	at_reportFileName = mka(
		MpcAttributeType.String, 
		'reportFileName', 
		'Optional, but mandatory if the -file option is included. Indicates the filename for the report. If the file does not exist, it will be created. If the file exists, it will be overwritten.'
		)
	at_reportFileName.stringType = 'SaveFilePath Text file (*.txt);;All files (*.*)'
	
	at_unorm = mka(
		MpcAttributeType.Boolean, 
		'-unorm', 
		'Optional. If included, the computation of the modal properties will be carried out using a displacement-normalized version of the eigenvectors.'
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'modalProperties'
	xom.addAttribute(at_print)
	xom.addAttribute(at_file)
	xom.addAttribute(at_reportFileName)
	xom.addAttribute(at_unorm)
	
	# visibility dependencies
	xom.setVisibilityDependency(at_file, at_reportFileName)
	
	return xom

def writeTcl(pinfo):
	
	'''
	modalProperties <-print> <-file $reportFileName> <-unorm>
	'''
	
	xobj = pinfo.analysis_step.XObject
	
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	at_print = geta('-print').boolean
	at_file = geta('-file').boolean
	at_reportFileName = geta('reportFileName').string
	at_unorm = geta('-unorm').boolean
	
	str_tcl = '{}modalProperties'.format(pinfo.indent)
	if at_print:
		str_tcl += ' -print'
	if at_file:
		str_tcl += ' -file "{}"'.format(at_reportFileName)
	if at_unorm:
		str_tcl += ' -unorm'
	str_tcl += '\n'
	
	# now write the string into the file
	pinfo.out_file.write('\n{}# modalProperties <-print> <-file $reportFileName> <-unorm>\n'.format(pinfo.indent))
	pinfo.out_file.write(str_tcl)
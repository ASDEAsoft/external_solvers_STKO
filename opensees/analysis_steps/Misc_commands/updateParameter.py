import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# parameter
	at_parameter = MpcAttributeMetaData()
	at_parameter.type = MpcAttributeType.IndexVector
	at_parameter.name = 'parameter'
	at_parameter.group = 'Data'
	at_parameter.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('sp')+'<br/>') + 
		html_par('command to generate sp constraint')+
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_parameter.indexSource.type = MpcAttributeIndexSourceType.AnalysisStep
	at_parameter.indexSource.addAllowedNamespace("Misc_commands")
	at_parameter.indexSource.addAllowedClassList(["parameter"])
	
	# newVal
	at_newVal = MpcAttributeMetaData()
	at_newVal.type = MpcAttributeType.String
	at_newVal.name = 'newVal'
	at_newVal.group = 'updateParameter'
	at_newVal.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('New parameter value')+'<br/>') + 
		html_par('e.g.:') +
		html_par('100') +
		html_end()
		)
	at_newVal.setDefault('')
	
	xom = MpcXObjectMetaData()
	xom.name = 'updateParameter'
	xom.addAttribute(at_parameter)
	xom.addAttribute(at_newVal)
	
	return xom

def writeTcl(pinfo):
	
	# updateParameter $tag $newValue
	
	xobj = pinfo.analysis_step.XObject
	
	FileName = xobj.name
	if pinfo.currentDescription != FileName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, FileName))
		pinfo.currentDescription = FileName
	doc = App.caeDocument()
	
	
	parameter_at = xobj.getAttribute('parameter')
	if(parameter_at is None):
		raise Exception('Error: cannot find "parameter" attribute')
	parameter = parameter_at.indexVector
	
	NewVal_at = xobj.getAttribute('newVal')
	if(NewVal_at is None):
		raise Exception('Error: cannot find "newVal" attribute')
	NewVal = NewVal_at.string
	
	str_updateParameter = []
	
	for id_addToParameter in parameter:
		if id_addToParameter == 0: continue
		if len(pinfo.map_tag_add_to_parameter_id_partition) == 0: continue
		str_updateParameter.append('{}updateParameter {} {}\n'.format(pinfo.indent, pinfo.map_tag_add_to_parameter_id_partition[id_addToParameter], NewVal))
	pinfo.out_file.write('\n{}# updateParameter\n'.format(pinfo.indent))
	pinfo.out_file.write(''.join(str_updateParameter))
	str_updateParameter = []
import os
from PyMpc import *
from mpc_utils_html import *


def makeXObjectMetaData():
	
	at_SelectionSets = MpcAttributeMetaData()
	at_SelectionSets.type = MpcAttributeType.IndexVector
	at_SelectionSets.name = 'SelectionSets'
	at_SelectionSets.group = 'Data'
	at_SelectionSets.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Enable ThermoMechanical Analysis')+'<br/>') + 
		html_par(
			'Enable the ThermoMechanical Analysis for the selected components. ')+
   
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'StartThermoMechanicalAnalysis'

	
	return xom



def writeTcl(pinfo):
	
	# get xobject and its parent component id
	xobj = pinfo.analysis_step.XObject
	id = xobj.parent.componentId
	
	# write a comment
	pinfo.out_file.write('\n{}# StartThermoMechanicalAnalysis [{}] {}\n'.format(pinfo.indent, id, xobj.parent.componentName))
	
	# write de dir folder for results txt
	pinfo.out_file.write('{}set dir "STKO_THERMAL_RESULTS_FOR_MECHANICAL_ANALYSIS"\n'.format(pinfo.indent))
	
	pinfo.out_file.write('\n')
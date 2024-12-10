import PyMpc.Units as u
import PyMpc.App
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin


def makeXObjectMetaData():
	at_cte_value = MpcAttributeMetaData()
	at_cte_value.type = MpcAttributeType.QuantityScalar
	at_cte_value.name = 'cte_value'
	at_cte_value.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('cte_value')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'ThermalVolumetricLoadingPattern'
	xom.addAttribute(at_cte_value)
	
	return xom

def writeTcl(pinfo):
	
	'''
	pattern ThermalVolumetricLoadingPattern tag cte_value "STKO_THERMAL_RESULTS_FOR_MECHANICAL_ANALYSIS/eleTags.txt" "STKO_THERMAL_RESULTS_FOR_MECHANICAL_ANALYSIS/gaussTemperatures.txt"

	'''
	
	
	xobj = pinfo.analysis_step.XObject
	tag = pinfo.analysis_step.id
	
	
	cte_value = xobj.getAttribute('cte_value').quantityScalar.value

	pinfo.out_file.write('#ThermalVolumetricLoadingPattern and read previous data\n')
	pinfo.out_file.write('\n{}# ThermalVolumetricLoadingPattern\n'.format(pinfo.indent))
	pinfo.out_file.write('{}pattern ThermalVolumetricLoadingPattern {} {} "STKO_THERMAL_RESULTS_FOR_MECHANICAL_ANALYSIS/eleTags.txt" "STKO_THERMAL_RESULTS_FOR_MECHANICAL_ANALYSIS/gaussTemperatures.txt"\n'.format(
		pinfo.indent, 
  		tag, 
  		cte_value,
		))
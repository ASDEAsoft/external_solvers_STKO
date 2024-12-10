import PyMpc.Units as u
import PyMpc.App
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import PyMpc

def makeXObjectMetaData():
    
	def mka(type, name, group, descr):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('','')+'<br/>') +
			html_end()
		)
		return a

	at_regions = mka(MpcAttributeType.IndexVector, 'Regions', 'Regions', 
			('Select the region that have the thermal data, in order to delete that.'))
	at_regions.indexSource.type = MpcAttributeIndexSourceType.AnalysisStep
	at_regions.indexSource.addAllowedNamespace("Misc_commands")
	at_regions.indexSource.addAllowedClass("region")

 
	xom = MpcXObjectMetaData()
	xom.name = 'switchToMechanicalAnalysis'
	xom.addAttribute(at_regions)
	
	return xom

def writeTcl(pinfo):
	
	# write a comment
	pinfo.out_file.write('\n{}# switchToMechanicalAnalysis\n'.format(pinfo.indent))

	# Remove thermal recorder
	pinfo.out_file.write('{}remove recorders\n'.format(pinfo.indent))

	doc = PyMpc.App.caeDocument()
	region = pinfo.analysis_step.XObject.getAttribute('Regions').indexVector[0]
	region_name = doc.analysisSteps[int(region)].XObject.getAttribute('List Name').string
 
	# foreach ele_id $BCtags { remove element $ele_id }
	pinfo.out_file.write('\n{}# Remove thermal elements\n'.format(pinfo.indent))
	pinfo.out_file.write('{}foreach ele_id ${} {{ remove element $ele_id }}\n'.format(pinfo.indent, region_name))
	
	pinfo.inv_map[(3,3)] = pinfo.inv_map.pop((3,1))

	pinfo.is_thermo_mechanical_analysis = False
	
 
	# print(pinfo.node_to_model_map)
	for item in pinfo.node_to_model_map:
		pinfo.node_to_model_map[item] = (3,3)
	
	pinfo.out_file.write('\n')
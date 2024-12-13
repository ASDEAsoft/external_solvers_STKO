import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import PyMpc

def _err(msg):
	return 'Error in "SetInitialTemperature" :\n{}'.format(msg)

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
			('Select the region that have the thermal data.'))
	at_regions.indexSource.type = MpcAttributeIndexSourceType.AnalysisStep
	at_regions.indexSource.addAllowedNamespace("Misc_commands")
	at_regions.indexSource.addAllowedClass("region")
	

	t0 = MpcAttributeMetaData()
	t0.type = MpcAttributeType.QuantityScalar
	t0.name = 't0'
	t0.group = 'Data'
	t0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('t0')+'<br/>') + 
		html_par('The initial temperature') +
		html_end()
		)
	t0.setDefault(0.0)
 
 
	xom = MpcXObjectMetaData()
	xom.name = 'SetInitialTemperature'
	xom.Xgroup = 'Thermal'
	xom.addAttribute(t0)
	xom.addAttribute(at_regions)
	
	return xom

def writeTcl(pinfo):
	
	# a global value
	t0 = pinfo.analysis_step.XObject.getAttribute('t0').quantityScalar.value
	pinfo.out_file.write('\n{}# Define initial temperature on all DOFs\n'.format(pinfo.indent))
	pinfo.out_file.write('{}foreach node [getNodeTags] {{\n'.format(pinfo.indent))
	pinfo.out_file.write('{}{}setNodeDisp $node 1 {} -commit\n'.format(pinfo.indent, pinfo.tabIndent, t0))
	pinfo.out_file.write('{}}}\n'.format(pinfo.indent))

	doc = PyMpc.App.caeDocument()
	region = pinfo.analysis_step.XObject.getAttribute('Regions').indexVector[0]
	region_name = doc.analysisSteps[int(region)].XObject.getAttribute('List Name').string

	# save thermal data
	pinfo.out_file.write('\n{}# Save thermal data\n'.format(pinfo.indent))
	pinfo.out_file.write('{}file mkdir $dir\n'.format(pinfo.indent))
	pinfo.out_file.write('{}set recorderCommand "recorder Element -time -file ${{dir}}/gaussTemperatures.txt -ele ${} gaussTemperature"\n'.format(pinfo.indent, region_name))
	pinfo.out_file.write('{}set outputFile [open "${{dir}}/eleTags.txt" "w"]\n'.format(pinfo.indent))
	pinfo.out_file.write('{}puts $outputFile ${}\n'.format(pinfo.indent, region_name))
	pinfo.out_file.write('{}close $outputFile\n'.format(pinfo.indent))
	pinfo.out_file.write('{}eval $recorderCommand\n'.format(pinfo.indent))
	pinfo.out_file.write('{}puts "Saving element tags and gauss temperatures to folder"\n'.format(pinfo.indent))
	pinfo.out_file.write('{}record\n'.format(pinfo.indent))
 
 


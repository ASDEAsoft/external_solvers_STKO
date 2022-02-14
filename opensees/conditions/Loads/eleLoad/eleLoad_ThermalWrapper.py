import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# node_tag
	at_node_tag = MpcAttributeMetaData()
	at_node_tag.type = MpcAttributeType.String
	at_node_tag.name = 'node_tag'
	at_node_tag.group = 'Group'
	at_node_tag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('node_tag')+'<br/>') +
		html_par('choose between "-nodeLoc" end "-node"') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper','ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	at_node_tag.sourceType = MpcAttributeSourceType.List
	at_node_tag.setSourceList(['-nodeLoc', '-node'])
	at_node_tag.setDefault('-nodeLoc')
	
	# -nodeLoc
	at_nodeLoc = MpcAttributeMetaData()
	at_nodeLoc.type = MpcAttributeType.Boolean
	at_nodeLoc.name = '-nodeLoc'
	at_nodeLoc.group = 'Group'
	at_nodeLoc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-nodeLoc')+'<br/>') +
		html_par('') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper','ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	at_nodeLoc.editable = False
	
	# -node
	at_node = MpcAttributeMetaData()
	at_node.type = MpcAttributeType.Boolean
	at_node.name = '-node'
	at_node.group = 'Group'
	at_node.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-node')+'<br/>') +
		html_par('') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper','ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	at_node.editable = False
	
	# NodeTag
	at_NodeTag = MpcAttributeMetaData()
	at_NodeTag.type = MpcAttributeType.IndexVector
	at_NodeTag.name = 'NodeTag'
	at_NodeTag.group = '-nodeLoc'
	at_NodeTag.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('NodeTag')+'<br/>') +
		html_par('') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper','ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	
	# loc
	at_loc = MpcAttributeMetaData()
	at_loc.type = MpcAttributeType.QuantityVector
	at_loc.name = 'loc'
	at_loc.group = '-nodeLoc'
	at_loc.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('loc')+'<br/>') +
		html_par('') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper','ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	
	# ctype
	at_ctype = MpcAttributeMetaData()
	at_ctype.type = MpcAttributeType.Integer
	at_ctype.editable = False;
	at_ctype.name = 'ctype_constraint'
	at_ctype.group = 'Group'
	at_ctype.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ctype')+'<br/>') +
		html_par('ctype') +
		html_par(html_href('http://openseesforfire.github.io/Subpages/ThermalActionCmds.html#TAWrapper','ThermalActionWrapper')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'eleLoad_ThermalWrapper'
	xom.addAttribute(at_node_tag)
	xom.addAttribute(at_nodeLoc)
	xom.addAttribute(at_node)
	xom.addAttribute(at_NodeTag)
	xom.addAttribute(at_loc)
	xom.addAttribute(at_ctype)
	
	
	# loc-dep
	xom.setVisibilityDependency(at_nodeLoc, at_loc)
	
	
	# auto-exclusive dependencies
	# nodeLoc or node
	xom.setBooleanAutoExclusiveDependency(at_node_tag, at_nodeLoc)
	xom.setBooleanAutoExclusiveDependency(at_node_tag, at_node)
	
	
	return xom

def writeTcl_eleLoad(pinfo, xobj):
	
	#eleLoad -ele $eleTag1 $eleTag2.. -type -ThermalWrapper -nodeLoc $NodeTag1 $loc1 $NodeTag2 $loc2 <$NodeTag3 $loc3..>
	#eleLoad -ele $eleTag1 $eleTag2.. -type -ThermalWrapper -node $NodeTag1 $NodeTag2 <$NodeTag3..>
	
	DefinitionName = 'eleLoad_ThermalWrapper'
	if pinfo.currentDescription != DefinitionName:
		pinfo.out_file.write('\n{}# eleLoad {}\n'.format(pinfo.indent, DefinitionName))
		pinfo.currentDescription = DefinitionName
	
	
	# tag = xobj.parent.componentId
	
	# mandatory parameters
	nodeLoc_at = xobj.getAttribute('-nodeLoc')
	if(nodeLoc_at is None):
		raise Exception('Error: cannot find "-nodeLoc" attribute')
	nodeLoc = nodeLoc_at.boolean
	
	node_at = xobj.getAttribute('-node')
	if(node_at is None):
		raise Exception('Error: cannot find "-node" attribute')
	node = node_at.boolean
	
	
	if nodeLoc:
		loc_at = xobj.getAttribute('loc')
		if(loc_at is None):
			raise Exception('Error: cannot find "loc" attribute')
		loc = loc_at.quantityVector
		
		str_tcl = '{}eleLoad -type -ThermalWrapper -nodeLoc \n'.format(pinfo.indent)
	
	else:
		str_tcl = '{}eleLoad -type -ThermalWrapper -node \n'.format(pinfo.indent)
	
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
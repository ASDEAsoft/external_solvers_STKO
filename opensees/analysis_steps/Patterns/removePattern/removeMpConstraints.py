import PyMpc.Units as u
import PyMpc.App
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# remove MpConstraints
	at_removeMpConstraints = MpcAttributeMetaData()
	at_removeMpConstraints.type = MpcAttributeType.IndexVector
	at_removeMpConstraints.name = 'remove MpConstraints'
	at_removeMpConstraints.group = 'Group'
	at_removeMpConstraints.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('MpConstraints')+'<br/>') + 
		html_par('command to remove fix')+
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Remove_Command','Remove Command')+'<br/>') +
		html_end()
		)
	at_removeMpConstraints.indexSource.type = MpcAttributeIndexSourceType.Condition
	at_removeMpConstraints.indexSource.addAllowedNamespace("Constraints.mp")
	at_removeMpConstraints.indexSource.addAllowedClassList(["equalDOF", "rigidDiaphragm", "rigidLink"])
	
	xom = MpcXObjectMetaData()
	xom.name = 'removeMpConstraints'
	xom.addAttribute(at_removeMpConstraints)
	
	return xom

def writeTcl(pinfo):
	
	# remove sp $nodeTag $dof
	
	xobj = pinfo.analysis_step.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	removeMpConstraints_at = xobj.getAttribute('remove MpConstraints')
	if(removeMpConstraints_at is None):
		raise Exception('Error: cannot find "remove MpConstraints" attribute')
	removeMpConstraints = removeMpConstraints_at.indexVector
	
	doc = App.caeDocument()
	
	
	for condition_id in removeMpConstraints:
		pinfo.condition = doc.conditions.get(condition_id)
		all_inter = pinfo.condition.assignment.interactions
		for inter in all_inter:
			moi = doc.mesh.getMeshedInteraction(inter.id)
			for elem in moi.elements:
				num_master = elem.numberOfMasterNodes()
				if num_master == 0 : continue
				for i in range(num_master, elem.numberOfNodes()):
					slave_id = elem.nodes[i].id
					pinfo.out_file.write('{}remove mp {}\n'.format(pinfo.indent, slave_id))
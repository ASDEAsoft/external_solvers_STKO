import PyMpc.Units as u
import PyMpc.App
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.conditions.Constraints.sp.fix as fix

def makeXObjectMetaData():
	
	# remove SpConstraints
	at_removeSpConstraints = MpcAttributeMetaData()
	at_removeSpConstraints.type = MpcAttributeType.IndexVector
	at_removeSpConstraints.name = 'remove SpConstraints'
	at_removeSpConstraints.group = 'Group'
	at_removeSpConstraints.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('SpConstraints')+'<br/>') + 
		html_par('command to remove fix')+
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Remove_Command','Remove Command')+'<br/>') +
		html_end()
		)
	at_removeSpConstraints.indexSource.type = MpcAttributeIndexSourceType.Condition
	at_removeSpConstraints.indexSource.addAllowedNamespace("Constraints.sp")
	at_removeSpConstraints.indexSource.addAllowedClassList(["fix"])
	
	xom = MpcXObjectMetaData()
	xom.name = 'removeSpConstraints'
	xom.addAttribute(at_removeSpConstraints)
	
	return xom

def writeTcl(pinfo):
	
	# remove sp $nodeTag $dof
	
	xobj = pinfo.analysis_step.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	removeSpConstraints_at = xobj.getAttribute('remove SpConstraints')
	if(removeSpConstraints_at is None):
		raise Exception('Error: cannot find "remove SpConstraints" attribute')
	removeSpConstraints = removeSpConstraints_at.indexVector
	
	doc = App.caeDocument()
	
	for condition_id in removeSpConstraints:
		pinfo.condition = doc.conditions.get(condition_id)
		nodes, dofs = fix.SP_getNodesAndDofs(pinfo)
		for node in nodes:
			for dof in dofs:
				pinfo.out_file.write('{}remove sp {} {}\n'.format(pinfo.indent, node, dof))
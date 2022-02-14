import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# mu
	at_mu = MpcAttributeMetaData()
	at_mu.type = MpcAttributeType.Real
	at_mu.name = 'mu'
	at_mu.group = 'Group'
	at_mu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu')+'<br/>') + 
		html_par('coefficient of friction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Coulomb_Friction','Coulomb Friction')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'Coulomb'
	xom.addAttribute(at_mu)
	
	
	return xom

def writeTcl(pinfo):
	
	#frictionModel Coulomb $frnTag $mu
	xobj = pinfo.definition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	frnTag = xobj.parent.componentId
	
	# mandatory parameters
	mu_at = xobj.getAttribute('mu')
	if(mu_at is None):
		raise Exception('Error: cannot find "mu" attribute')
	mu = mu_at.real
	
	
	str_tcl = '{}frictionModel Coulomb {} {}\n'.format(pinfo.indent, frnTag, mu)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
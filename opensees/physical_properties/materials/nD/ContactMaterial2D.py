import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# mu
	at_mu = MpcAttributeMetaData()
	at_mu.type = MpcAttributeType.Real
	at_mu.name = 'mu'
	at_mu.group = 'Non linear'
	at_mu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu')+'<br/>') + 
		html_par('interface frictional coefficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ContactMaterial2D','ContactMaterial2D')+'<br/>') +
		html_end()
		)
	
	# G
	at_G = MpcAttributeMetaData()
	at_G.type = MpcAttributeType.QuantityScalar
	at_G.name = 'G'
	at_G.group = 'Non linear'
	at_G.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('G')+'<br/>') + 
		html_par('interface stiffness parameter') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ContactMaterial2D','ContactMaterial2D')+'<br/>') +
		html_end()
		)
	at_G.dimension = u.F/u.L**2
	
	# c
	at_c = MpcAttributeMetaData()
	at_c.type = MpcAttributeType.Real
	at_c.name = 'c'
	at_c.group = 'Non linear'
	at_c.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('c')+'<br/>') + 
		html_par('interface cohesive intercept') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ContactMaterial2D','ContactMaterial2D')+'<br/>') +
		html_end()
		)
	
	# t
	at_t = MpcAttributeMetaData()
	at_t.type = MpcAttributeType.QuantityScalar
	at_t.name = 't'
	at_t.group = 'Non linear'
	at_t.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('t')+'<br/>') + 
		html_par('interface tensile strength') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ContactMaterial2D','ContactMaterial2D')+'<br/>') +
		html_end()
		)
	at_t.dimension = u.F/u.L**2
	
	xom = MpcXObjectMetaData()
	xom.name = 'ContactMaterial2D'
	xom.Xgroup = 'Contact Materials for 2D and 3D'
	xom.addAttribute(at_mu)
	xom.addAttribute(at_G)
	xom.addAttribute(at_c)
	xom.addAttribute(at_t)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial ContactMaterial2D $matTag $mu $G $c $t
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	mu_at = xobj.getAttribute('mu')
	if(mu_at is None):
		raise Exception('Error: cannot find "mu" attribute')
	mu = mu_at.real
	
	G_at = xobj.getAttribute('G')
	if(G_at is None):
		raise Exception('Error: cannot find "G" attribute')
	G = G_at.quantityScalar
	
	c_at = xobj.getAttribute('c')
	if(c_at is None):
		raise Exception('Error: cannot find "c" attribute')
	c = c_at.real
	
	t_at = xobj.getAttribute('t')
	if(t_at is None):
		raise Exception('Error: cannot find "t" attribute')
	t = t_at.quantityScalar
	
	str_tcl = '{}nDMaterial ContactMaterial2D {} {} {} {} {}\n'.format(pinfo.indent, tag, mu, G.value, c, t.value)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
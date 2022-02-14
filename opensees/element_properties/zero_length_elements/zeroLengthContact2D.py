import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# Kn
	at_Kn = MpcAttributeMetaData()
	at_Kn.type = MpcAttributeType.Real
	at_Kn.name = 'Kn'
	at_Kn.group = 'Group'
	at_Kn.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kn')+'<br/>') +
		html_par('Penalty in normal direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	# Kt
	at_Kt = MpcAttributeMetaData()
	at_Kt.type = MpcAttributeType.Real
	at_Kt.name = 'Kt'
	at_Kt.group = 'Group'
	at_Kt.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Kt')+'<br/>') +
		html_par('Penalty in tangential direction') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	# mu
	at_mu = MpcAttributeMetaData()
	at_mu.type = MpcAttributeType.Real
	at_mu.name = 'mu'
	at_mu.group = 'Group'
	at_mu.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('mu')+'<br/>') +
		html_par('friction coefficient') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	# Nx
	at_Nx = MpcAttributeMetaData()
	at_Nx.type = MpcAttributeType.Real
	at_Nx.name = 'Nx'
	at_Nx.group = '-normal'
	at_Nx.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Nx')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	# Ny
	at_Ny = MpcAttributeMetaData()
	at_Ny.type = MpcAttributeType.Real
	at_Ny.name = 'Ny'
	at_Ny.group = '-normal'
	at_Ny.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Ny')+'<br/>') +
		html_par('') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	# distributed
	at_distributed = MpcAttributeMetaData()
	at_distributed.type = MpcAttributeType.Boolean
	at_distributed.name = 'distributed'
	at_distributed.group = 'Group'
	at_distributed.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('distributed')+'<br/>') +
		html_par('se this flag if you are using distributed springs on edges or surfaces.') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLengthContact_Element','ZeroLengthContact Element')+'<br/>') +
		html_end()
		)
	
	xom = MpcXObjectMetaData()
	xom.name = 'zeroLengthContact2D'
	xom.addAttribute(at_Kn)
	xom.addAttribute(at_Kt)
	xom.addAttribute(at_mu)
	xom.addAttribute(at_Nx)
	xom.addAttribute(at_Ny)
	xom.addAttribute(at_distributed)
	
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):

	return [(2,2),(2,2)]	# [(ndm, ndf),...]


def writeTcl(pinfo):
	
	# element ZeroLengthContact2D eleTag? iNode? jNode? Kn? Kt? fs? -normal Nx? Ny?
	
	elem = pinfo.elem
	elem_prop = pinfo.elem_prop
	
	tag = elem.id
	xobj = elem_prop.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# NODE
	if (len(elem.nodes)!=2):
		raise Exception('Error: invalid number of nodes')
	# use reverse iterator because in stko the first is the master node
	# while this command wants the slave node first
	nstr = ' '.join([str(node.id) for node in reversed(elem.nodes)])
	
	# optional paramters
	sopt = ''
	
	Kn_at = xobj.getAttribute('Kn')
	if(Kn_at is None):
		raise Exception('Error: cannot find "Kn" attribute')
	Kn = Kn_at.real
	
	Kt_at = xobj.getAttribute('Kt')
	if(Kt_at is None):
		raise Exception('Error: cannot find "Kt" attribute')
	Kt = Kt_at.real
	
	mu_at = xobj.getAttribute('mu')
	if(mu_at is None):
		raise Exception('Error: cannot find "mu" attribute')
	mu = mu_at.real	
	
	Nx_at = xobj.getAttribute('Nx')
	if(Nx_at is None):
		raise Exception('Error: cannot find "Nx" attribute')
	Nx = Nx_at.real
	
	Ny_at = xobj.getAttribute('Ny')
	if(Ny_at is None):
		raise Exception('Error: cannot find "Ny" attribute')
	Ny = Ny_at.real
	
	distributed_at = xobj.getAttribute('distributed')
	if(distributed_at is None):
		raise Exception('Error: cannot find "distributed" attribute')
	distributed = distributed_at.boolean
	if distributed:
		Kn *= elem.lumpingFactor
		Kt *= elem.lumpingFactor
	
	str_tcl = '{}element zeroLengthContact2D {} {} {} {} {} -normal {} {} \n'.format(pinfo.indent, tag, nstr, Kn, Kt, mu, Nx, Ny)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
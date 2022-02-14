import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import PyMpc
import PyMpc.Math
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# eqMotion
	at_eqMotion = MpcAttributeMetaData()
	at_eqMotion.type = MpcAttributeType.String
	at_eqMotion.name = 'eqMotion'
	at_eqMotion.group = 'Group'
	at_eqMotion.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eqMotion')+'<br/>') + 
		html_par('the PEER NGA name of the motion (a string containing the earthquake name, station & dirn)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PeerNGAMotion','PeerNGAMotion')+'<br/>') +
		html_end()
		)
	
	# factor
	at_factor = MpcAttributeMetaData()
	at_factor.type = MpcAttributeType.Real
	at_factor.name = 'factor'
	at_factor.group = 'Group'
	at_factor.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('factor')+'<br/>') + 
		html_par('factor to be applied to the data points, if accel record type you want to specify G') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PeerNGAMotion','PeerNGAMotion')+'<br/>') +
		html_end()
		)
	
	# -NPTS
	at_NPTS = MpcAttributeMetaData()
	at_NPTS.type = MpcAttributeType.Boolean
	at_NPTS.name = '-NPTS'
	at_NPTS.group = 'Group'
	at_NPTS.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-NPTS')+'<br/>') + 
		html_par('optional, if provided will set the variable nPts equal to number of data points found in record') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PeerNGAMotion','PeerNGAMotion')+'<br/>') +
		html_end()
		)
	
	# nPts
	at_nPts = MpcAttributeMetaData()
	at_nPts.type = MpcAttributeType.String
	at_nPts.name = 'nPts'
	at_nPts.group = '-NPTS'
	at_nPts.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('nPts')+'<br/>') + 
		html_par('optional, if provided will set the variable nPts equal to number of data points found in record') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PeerNGAMotion','PeerNGAMotion')+'<br/>') +
		html_end()
		)
	
	# -dT
	at_use_dT = MpcAttributeMetaData()
	at_use_dT.type = MpcAttributeType.Boolean
	at_use_dT.name = '-dT'
	at_use_dT.group = 'Group'
	at_use_dT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('-dT')+'<br/>') + 
		html_par('optional, if provided will set the variable dT equal to time interval between points in the record') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PeerNGAMotion','PeerNGAMotion')+'<br/>') +
		html_end()
		)
	
	# dT
	at_dT = MpcAttributeMetaData()
	at_dT.type = MpcAttributeType.String
	at_dT.name = 'dT'
	at_dT.group = '-dT'
	at_dT.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('dT')+'<br/>') + 
		html_par('optional, if provided will set the variable dT equal to time interval between points in the record') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/PeerNGAMotion','PeerNGAMotion')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'PeerNGAMotion'
	xom.addAttribute(at_eqMotion)
	xom.addAttribute(at_factor)
	xom.addAttribute(at_NPTS)
	xom.addAttribute(at_nPts)
	xom.addAttribute(at_use_dT)
	xom.addAttribute(at_dT)
	
	
	# nPts-dep
	xom.setVisibilityDependency(at_NPTS, at_nPts)
	
	# dt-dep
	xom.setVisibilityDependency(at_use_dT, at_dT)
	
	return xom

def evaluateFunctionAttribute(xobj):
	if(xobj is None):
		print('Error: xobj is null\n')
		return PyMpc.Math.mat()
	
	if(xobj.name != 'PeerNGAMotion'):
		print('Error: invalid xobj type, expected "PeerNGAMotion", given "{}"'.format(xobj.name))
		return PyMpc.Math.mat()
	
	func_at = xobj.getAttribute('__mpc_function__')
	if(func_at is None):
		print('Error: cannot find "__mpc_function__" attribute\n')
		return PyMpc.Math.mat()
	
	eqMotion_at = xobj.getAttribute('eqMotion')
	if(eqMotion_at is None):
		print('Error: cannot find "eqMotion" attribute\n')
		return PyMpc.Math.mat()
	
	factor_at = xobj.getAttribute('factor')
	if(factor_at is None):
		print('Error: cannot find "factor" attribute\n')
		return PyMpc.Math.mat()
	
	nPTS_at = xobj.getAttribute('nPTS')
	if(nPTS_at is None):
		print('Error: cannot find "nPTS" attribute\n')
		return PyMpc.Math.mat()
	
	nPts_at = xobj.getAttribute('nPts')
	if(nPts_at is None):
		print('Error: cannot find "nPts" attribute\n')
		return PyMpc.Math.mat()
	
	use_dT_at = xobj.getAttribute('use_dT')
	if(use_dT_at is None):
		print('Error: cannot find "use_dT" attribute\n')
		return PyMpc.Math.mat()
	
	dt_at = xobj.getAttribute('dt')
	if(dt_at is None):
		print('Error: cannot find "dt" attribute\n')
		return PyMpc.Math.mat()

def writeTcl(pinfo):
	
	#timeSeries PeerNGAMotion $tag $eqMotion $factor <-dT $dT> <-NPTS $nPts>
	xobj = pinfo.definition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	tag = xobj.parent.componentId
	
	# mandatory parameters
	eqMotion_at = xobj.getAttribute('eqMotion')
	if(eqMotion_at is None):
		raise Exception('Error: cannot find "eqMotion" attribute')
	eqMotion = eqMotion_at.string
	
	factor_at = xobj.getAttribute('factor')
	if(factor_at is None):
		raise Exception('Error: cannot find "factor" attribute')
	factor = factor_at.real
	
	
	# optional paramters
	sopt = ''
	
	use_dt_at = xobj.getAttribute('-dT')
	if(use_dt_at is None):
		raise Exception('Error: cannot find "-dT" attribute')
	use_dt = use_dt_at.boolean
	if use_dt:
		dT_at = xobj.getAttribute('dT')
		if(dT_at is None):
			raise Exception('Error: cannot find "dT" attribute')
		dT = dT_at.string
		sopt += ' -dT {}'.format(dT)
	
	NPTS_at = xobj.getAttribute('-NPTS')
	if(NPTS_at is None):
		raise Exception('Error: cannot find "-NPTS" attribute\n')
	NPTS = NPTS_at.boolean
	if NPTS:
		nPts_at = xobj.getAttribute('nPts')
		if(nPts_at is None):
			raise Exception('Error: cannot find "nPts" attribute')
		nPts = nPts_at.string
		sopt += ' -NPTS {}'.format(nPts)
	
	str_tcl = '{}timeSeries PeerNGAMotion {} {} {}{}\n'.format(pinfo.indent, tag, eqMotion, factor, sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
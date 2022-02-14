# enable default uniaxial tester for this module
from opensees.physical_properties.utils.tester.EnableTester1D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# strainPoints
	at_strainPoints = MpcAttributeMetaData()
	at_strainPoints.type = MpcAttributeType.QuantityVector
	at_strainPoints.name = 'strainPoints'
	at_strainPoints.group = '-strain'
	at_strainPoints.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('strainPoints')+'<br/>') + 
		html_par('array of strain points along stress-strain curve') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticMultiLinear_Material','ElasticMultiLinear Material')+'<br/>') +
		html_end()
		)
	
	# stressPoints
	at_stressPoints = MpcAttributeMetaData()
	at_stressPoints.type = MpcAttributeType.QuantityVector
	at_stressPoints.name = 'stressPoints'
	at_stressPoints.group = '-stress'
	at_stressPoints.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('stressPoints')+'<br/>') + 
		html_par('array of stress points along stress-strain curve') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticMultiLinear_Material','ElasticMultiLinear Material')+'<br/>') +
		html_end()
		)
	at_stressPoints.dimension = u.F/u.L**2
	
	# use_eta
	at_use_eta = MpcAttributeMetaData()
	at_use_eta.type = MpcAttributeType.Boolean
	at_use_eta.name = 'use_eta'
	at_use_eta.group = 'Non-linear'
	at_use_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('use_eta')+'<br/>') + 
		html_par('enable the use of damping tangent (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticMultiLinear_Material','ElasticMultiLinear Material')+'<br/>') +
		html_end()
		)
	
	# eta
	at_eta = MpcAttributeMetaData()
	at_eta.type = MpcAttributeType.Real
	at_eta.name = 'eta'
	at_eta.group = 'Non-linear'
	at_eta.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('eta')+'<br/>') + 
		html_par('damping tangent (optional, default=0.0)') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ElasticMultiLinear_Material','ElasticMultiLinear Material')+'<br/>') +
		html_end()
		)
	at_eta.setDefault(0.0)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'ElasticMultiLinear'
	xom.Xgroup = 'Other Uniaxial Materials'
	xom.addAttribute(at_use_eta)
	xom.addAttribute(at_eta)
	xom.addAttribute(at_strainPoints)
	xom.addAttribute(at_stressPoints)
	
	# eta-dep
	xom.setVisibilityDependency(at_use_eta, at_eta)
	
	return xom

def writeTcl(pinfo):
	
	#uniaxialMaterial ElasticMultiLinear $matTag -strain $strainPoints -stress $stressPoints <$eta>
	
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	strainPoints_at = xobj.getAttribute('strainPoints')
	if(strainPoints_at is None):
		raise Exception('Error: cannot find "strainPoints" attribute')
	strainPoints = strainPoints_at.quantityVector
	
	stressPoints_at = xobj.getAttribute('stressPoints')
	if(stressPoints_at is None):
		raise Exception('Error: cannot find "stressPoints" attribute')
	stressPoints = stressPoints_at.quantityVector
	
	if(len(strainPoints)!=len(stressPoints)):
		raise Exception('Error: the number of strain and stress points must be the same')
	
	# optional paramters
	sopt = ''
	
	use_eta_at = xobj.getAttribute('use_eta')
	if(use_eta_at is None):
		raise Exception('Error: cannot find "use_eta" attribute')
	use_eta = use_eta_at.boolean
	if use_eta:
		eta_at = xobj.getAttribute('eta')
		if(eta_at is None):
			raise Exception('Error: cannot find "eta" attribute')
		eta = eta_at.real
		
		sopt += '{}'.format(eta)
	
	# build command string
	indent2 = pinfo.indent+'\t'
	
	def to_multiline(source):
		n0 = 3
		n1 = len(source)//n0
		s1 = n1*n0
		n2 = len(source)-s1
		a = [0]*(n1+1)
		for i in range(1, n1+1):
			a[i] = a[i-1]+n0
		if n2 > 0:
			a.append(len(source))
		return '{}{}'.format(
			indent2,
			' \\\n{}'.format(indent2).join(
				' '.join(str(source.valueAt(j)) for j in range(a[i], a[i+1]))
				for i in range(len(a)-1) )
			)
	
	str_tcl = '{0}uniaxialMaterial ElasticMultiLinear {1} {5} \\\n{2}-strain \\\n{3} \\\n{2}-stress \\\n{4}\n'.format(
		pinfo.indent, tag, indent2, to_multiline(strainPoints), to_multiline(stressPoints), sopt)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
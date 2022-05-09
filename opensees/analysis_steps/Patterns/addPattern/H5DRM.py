import PyMpc.Units as u
import PyMpc.App
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import importlib

def makeXObjectMetaData():
	
	# TODO: change the URL of doc
	
	def mka(name, type, group, description):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(description) +
			html_par(html_href('https://github.com/OpenSees/OpenSees/pull/751','DRM')+'<br/>') +
			html_end()
			)
		return a
	
	condition = mka('H5DRM Condition', MpcAttributeType.Index, 'Mandatory', 'A previously defined H5DRM condition')
	condition.indexSource.type = MpcAttributeIndexSourceType.Condition
	condition.indexSource.addAllowedNamespace('Loads.Generic')
	condition.indexSource.addAllowedClass('H5DRM')
	
	xom = MpcXObjectMetaData()
	xom.name = 'H5DRM'
	xom.addAttribute(condition)
	
	return xom

def writeTcl(pinfo):
	
	'''
	pattern H5DRM $tag $filename $factor $crd_scale $distance_tolerance
	'''
	
	doc = PyMpc.App.caeDocument()
	if(doc is None):
		raise Exception('null cae document')
	
	xobj = pinfo.analysis_step.XObject
	tag = pinfo.analysis_step.id
	
	
	# write a description
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	# get attribute from an xobject
	def geta(xobject, name):
		a = xobject.getAttribute(name)
		if a is None:
			raise Exception('Cannot find "{}" attribute'.format(name))
		return a
	
	# we need the H5DRM condition
	condition_id = geta(xobj, 'H5DRM Condition').index
	condition = doc.getCondition(condition_id)
	if condition is None:
		raise Exception('Cannot find condition {} in the Document'.format(condition_id))
	cxobj = condition.XObject
	
	# condition attributes
	filename = geta(cxobj, 'File Name').string
	factor = geta(cxobj, 'factor').real
	crd_scale = geta(cxobj, 'crd_scale').real
	distance_tolerance = geta(cxobj, 'distance_tolerance').real
	
	# sanity checks
	if not filename:
		raise Exception('You should provide a valid file name')
	if crd_scale <= 0.0:
		raise Exception('crd_scale should be strictly positive')
	if distance_tolerance <= 0.0:
		raise Exception('distance_tolerance should be strictly positive') 
	
	# write
	pinfo.out_file.write('{}pattern H5DRM {} "{}" {} {} {}\n'.format(pinfo.indent, tag, filename, factor, crd_scale, distance_tolerance))

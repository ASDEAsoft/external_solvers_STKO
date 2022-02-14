# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester3D import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.utils.RandomMaterialTable as RMT

from scipy.spatial import KDTree
import numpy as np
import importlib
import os
from datetime import datetime

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

def makeXObjectMetaData():
	
	def mka(name, group, descr, atype, adim = None, dval = None):
		a = MpcAttributeMetaData()
		a.type = atype
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('https://asdeasoft.net/?stko-support','RandomizedMaterialWrapper')+'<br/>') +
			html_end()
			)
		if adim is not None:
			a.dimension = adim
		if dval is not None:
			a.setDefault(dval)
		return a
	
	source = mka('Source Material', 'Source', 'The source material whose parameters should be randomized', MpcAttributeType.Index)
	source.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	source.indexSource.addAllowedNamespace('materials.nD')
	
	type = mka('Randomizer Type', 'Randomizer', 'The randomizer type', MpcAttributeType.String)
	type.sourceType = MpcAttributeSourceType.List
	type.setSourceList(['From Table'])
	type.setDefault('From Table')
	
	table = mka('Table File', 'Randomizer', 'The random material table file', MpcAttributeType.String)
	table.stringType = 'OpenFilePath All supported files (*.rmt *.txt);;Random Material Table (*.rmt);;Text files (*.txt);;All files (*.* *)'
	
	xom = MpcXObjectMetaData()
	xom.name = 'RandomizedMaterialWrapper'
	xom.Xgroup = 'ASDEASoftware'
	
	xom.addAttribute(source)
	xom.addAttribute(type)
	xom.addAttribute(table)
	
	return xom

def onEditBegin(editor, xobj):
	onAttributeChanged(editor, xobj, 'Randomizer Type')

def onAttributeChanged(editor, xobj, attribute_name):
	attribute = _get_xobj_attribute(xobj, attribute_name)
	if attribute.name == 'Randomizer Type':
		type = attribute.string
		if type == 'From Table':
			_get_xobj_attribute(xobj, 'Table File').visible = True

def writeTcl(pinfo):
	
	# document
	doc = App.caeDocument()
	if doc is None:
		raise Exception(err('Cannot find a document'))
	
	# xobject
	phys_prop = pinfo.phys_prop
	xobj = phys_prop.XObject
	
	# standardized error
	def err(msg):
		return 'Error in "{}" at "PhysicalProperty {}":\n{}'.format(xobj.name, phys_prop.id, msg) 
	
	# get source material
	source_mat_id = _get_xobj_attribute(xobj, 'Source Material').index
	source_mat = doc.getPhysicalProperty(source_mat_id)
	source_mat_module_name = 'opensees.physical_properties.{}.{}'.format(source_mat.XObject.Xnamespace, source_mat.XObject.name)
	source_mat_module = importlib.import_module(source_mat_module_name)
	
	# create the RMT
	fname = _get_xobj_attribute(xobj, 'Table File').string
	if not os.path.isabs(fname):
		fname = os.path.join(pinfo.out_dir, fname)
	rmt = RMT.RMT(fname)
	
	# check arguments
	nargs = len(rmt.args)
	for iarg in rmt.args:
		at = source_mat.XObject.getAttribute(iarg)
		if at is None:
			raise Exception(err('Cannot find Argument "{}" of {} in the Physical Property'.format(iarg, args)))
		if at.type != MpcAttributeType.Real and at.type != MpcAttributeType.QuantityScalar and at.type != MpcAttributeType.QuantityVector:
			raise Exception(err('Argument "{}" of {} in the Physical Property should be MpcAttributeType.Real, MpcAttributeType.QuantityScalar or MpcAttributeType.QuantityVector, not {}'.format(iarg, args, at.type)))
	
	# write randomized materials to the materials.tcl file
	pinfo.out_file.write('\n{}# BEGIN RandomizedMaterialWrapper ({}) generated materials\n'.format(pinfo.indent, phys_prop.id))
	# this dictionary maps the new material ID from the Table File, to the ID generated in the materials.tcl file
	# because in STKO we may have some IDs already taken...
	new_mat_id_map = {}
	# utils to get/set data with appropriate supported types
	def get_val(at):
		if at.type == MpcAttributeType.Real:
			return at.real
		elif at.type == MpcAttributeType.QuantityScalar:
			return at.quantityScalar.value
		elif at.type == MpcAttributeType.QuantityVector:
			return [i for i in at.quantityVector.value]
		else:
			return 0.0
	def set_val(at, val):
		if at.type == MpcAttributeType.Real:
			at.real = val
		elif at.type == MpcAttributeType.QuantityScalar:
			at.quantityScalar.value = val
		elif at.type == MpcAttributeType.QuantityVector:
			at.quantityVector.resize(len(val), 1)
			for i in range(len(val)):
				at.quantityVector.setValueAt(i, val[i])
	# save original data
	saved_id = source_mat.id
	saved_values = [0.0]*nargs
	for i in range(nargs):
		saved_values[i] = get_val(_get_xobj_attribute(source_mat.XObject, rmt.args[i]))
	# HACK 1: put the source physicalProperty in pinfo
	pinfo.phys_prop = source_mat
	# parse
	try:
		for i in range(len(rmt.mat_id)):
			# get material local id and its values
			mat_local_id = rmt.mat_id[i]
			mat_values = rmt.mat_data[i]
			# HACK 2: update physicalProperty arguments and ID
			for j in range(nargs):
				set_val(_get_xobj_attribute(source_mat.XObject, rmt.args[j]), mat_values[j])
			mat_new_id = pinfo.next_physicalProperties_id
			pinfo.next_physicalProperties_id += 1
			source_mat.id = mat_new_id
			# write modified source physicalProperty
			source_mat_module.writeTcl(pinfo)
			# map file ID to TCL id
			new_mat_id_map[mat_local_id] = mat_new_id
	finally:
		# this must be done anyway... to revert the hacks above
		source_mat.id = saved_id
		for i in range(nargs):
			set_val(_get_xobj_attribute(source_mat.XObject, rmt.args[i]), saved_values[i])
		pinfo.phys_prop = phys_prop
	pinfo.out_file.write('{}# END RandomizedMaterialWrapper ({}) generated materials\n\n'.format(pinfo.indent, phys_prop.id))
	
	# find all elements with this material
	# prepare a list element ids and element center points (samples for the KDTree)
	mesh = doc.mesh
	ele_list = []
	ele_centers = []
	def process_domain(elements):
		for ele in elements:
			# element id
			ele_list.append(ele.id)
			# element center
			C = ele.computeCenter()
			ele_centers.append((C.x, C.y, C.z))
	for geom_id, geom in doc.geometries.items():
		mog = mesh.getMeshedGeometry(geom_id)
		pas = geom.physicalPropertyAssignment
		for i in range(len(pas.onEdges)):
			trial = pas.onEdges[i]
			if trial and trial.id == phys_prop.id:
				domain = mog.edges[i]
				process_domain(domain.elements)
		for i in range(len(pas.onFaces)):
			trial = pas.onFaces[i]
			if trial and trial.id == phys_prop.id:
				domain = mog.faces[i]
				process_domain(domain.elements)
		for i in range(len(pas.onSolids)):
			trial = pas.onSolids[i]
			if trial and trial.id == phys_prop.id:
				domain = mog.solids[i]
				process_domain(domain.elements)
	for inter_id, inter in doc.interactions.items():
		if inter.physicalProperty is xobj.parent:
			moi = mesh.getMeshedInteraction(inter_id)
			process_domain(moi.elements)
	
	# convert ele centers to numpy array
	ele_centers = np.asarray(ele_centers)
	if len(ele_centers) < 1:
		return
	
	# find, for each center, the 0-based position of the nearest material point
	print('RandomizedMaterialWrapper ({})'.format(phys_prop.id))
	print('    Finding nearest material points. This may take a while...')
	T1 = datetime.now()
	_, nearest_pos = rmt.tree.query(ele_centers)
	T2 = datetime.now()
	print('    Elapsed time: {} seconds'.format((T2-T1).total_seconds()))
	
	# save in pinfo
	if len(ele_list):
		for i in range(len(ele_list)):
			ele_id = ele_list[i]
			new_prop_id = new_mat_id_map[rmt.mat_point_ids[nearest_pos[i]]]
			pinfo.mpco_cdata_utils.mapPhysicalProperties(phys_prop.id, ele_id, new_prop_id)
'''
MonStrNode Description.

'''

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from PyMpc.Math import *
import os

import importlib
import opensees.conditions.DigitalTwin.MonStrNodeGui
importlib.reload(opensees.conditions.DigitalTwin.MonStrNodeGui)

from opensees.conditions.DigitalTwin.MonStrNodeGui import MonStrNodeWidget
from PySide2.QtWidgets import QSplitter
import shiboken2

'''
A global class with some utility
'''
class _global:
	'''
	stores a reference to the gui generated for this object
	'''
	gui = None
	_gui_hide_xobj_editor = False
	def clearGui(editor, xobj):
		if _global.gui is not None:
			if _global._gui_hide_xobj_editor:
				splitter = shiboken2.wrapInstance(editor.getChildPtr(MpcXObjectEditorChildCode.MainSplitter), QSplitter)
				splitter.widget(0).show()
			_global.gui.setParent(None)
			_global.gui.deleteLater()
			_global.gui = None
	def buildGui(editor, xobj):
		_global.clearGui(editor, xobj)
		_global.gui = MonStrNodeWidget()
		splitter = shiboken2.wrapInstance(editor.getChildPtr(MpcXObjectEditorChildCode.MainSplitter), QSplitter)
		splitter.addWidget(_global.gui)
		if _global._gui_hide_xobj_editor:
			splitter.widget(0).hide()
	'''
	the glyph prototype to be allocated only once for peformance reasons.
	'''
	_glyph_proto = None
	'''
	returns the glyph prototype of the MonStrNode, a FxShapeFace instance
	Tranform: return T*Math.vec3(x*lx, y*ly, z*lz) + pos
	'''
	def getGlyphProto():
		this_dir = os.path.dirname(__file__)
		glyph_file = os.path.join(this_dir, 'sensor_glyph.txt')
		# build once
		if _global._glyph_proto is None:
			with open(glyph_file, 'r+') as f:
				data = [i for i in f.read().splitlines() if i]
				line = data[0]
				words = line.split(' ')
				n1 = int(words[0])
				n2 = int(words[1])
				face = FxShapeFace()
				for i in range(n1):
					line = data[i+1]
					words = line.split(' ')
					face.vertices.append(Math.vertex(Math.vec3(float(words[0]), float(words[1]), float(words[2]))))
				for i in range(n2):
					line = data[i+1+n1]
					words = line.split(' ')
					face.triangles.append(Math.triangle(int(words[0]), int(words[1]), int(words[2])))
				_global._glyph_proto = face
		# return the instance
		return _global._glyph_proto

def onEditBegin(editor, xobj):
	print('onEditBegin')
	_global.buildGui(editor, xobj)

def onEditorClosing(editor, xobj):
	print('onEditorClosing')
	_global.clearGui(editor, xobj)

def onEditFinished(editor, xobj):
	print('onEditFinished')
	...

def makeXObjectMetaData():
	
	# make attributes
	def mka(type, name, group='Default', descr='', default=None):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.descr = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') +
			html_par(descr + '<br/>') +
			html_par(html_href('https://asdea.eu/hardware/monstr-nodes/','MonStrNode')+'<br/>') +
			html_end()
			)
		if default:
			a.setDefault(default)
		return a
	
	# MonStr nodes
	# SERIAL_NUMBER PART_NUMBER COORD_X COORD_Y COORD_Z X1 X2 X3 Y1 Y2 Y3 R G B
	node_serial = mka(MpcAttributeType.StringVector, 'SerialNumber')
	node_part = mka(MpcAttributeType.StringVector, 'PartNumber')
	node_pos = mka(MpcAttributeType.QuantityMatrix, 'Position')
	node_dx = mka(MpcAttributeType.QuantityMatrix, 'XDirection')
	node_dy = mka(MpcAttributeType.QuantityMatrix, 'YDirection')
	node_color = mka(MpcAttributeType.QuantityMatrix, 'Color')
	
	
	# XObject meta data
	xom = MpcXObjectMetaData()
	xom.name = 'MonStrNode'
	# MonStr nodes
	xom.addAttribute(node_serial)
	xom.addAttribute(node_part)
	xom.addAttribute(node_pos)
	xom.addAttribute(node_dx)
	xom.addAttribute(node_dy)
	xom.addAttribute(node_color)
	
	# add other inner items
	
	return xom

def buildCustomVRep(xobj, data):
	# get document
	doc = App.caeDocument()
	if doc is None: return
	# get condition
	cond = xobj.parent
	print("buildCustomVRep")
	print(cond.name)
	for geom, sset in cond.assignment.geometries.items():
		if geom is None or sset is None: continue
		# allocate the vrep map value for this geometry
		# use a fixed size so that the glyph does not scale
		output = MpcConditionVRepMapValue()
		output.shape = FxShape()
		output.max_glyph_size = 100.0
		output.min_glyph_size = 100.0
		# ...
		face = _global.getGlyphProto()
	
def makeConditionRepresentationData(xobj):
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.CustomVRep
	d.orientation = MpcConditionVRepOrientation.Global
	d.on_vertices = False
	d.on_edges = True
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = False
	return d
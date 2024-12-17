'''
MonStrNode Description.

'''

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from PyMpc.Math import *
import os

'''
A global class with some utility
'''
class _global:
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
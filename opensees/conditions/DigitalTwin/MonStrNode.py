'''
MonStrNode Description.

'''

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from PyMpc.Math import *

def makeXObjectMetaData():
	
	
	# XObject meta data
	xom = MpcXObjectMetaData()
	xom.name = 'MonStrNode'
	
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
		print(geom)
		print(sset.edges)
	
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
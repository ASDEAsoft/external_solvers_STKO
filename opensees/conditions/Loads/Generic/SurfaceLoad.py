'''
@package SurfacePressure
This module contains relevant code for a surface pressure
boundary condition.

Surface pressure is a pressure load applied on surfaces
along their local directions.
'''

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from PyMpc.Math import *
from opensees.conditions.utils import SpatialFunctionEval
from math import sin, cos, radians

####################################################################################
# Utilities
####################################################################################

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

def _description(title, body):
	return (
		html_par(html_begin()) +
		html_par(html_boldtext(title)+'<br/>') +
		html_par(body) +
		html_par(html_href('https://asdeasoft.net/?product-stko','stko')) +
		html_end()
		)

repartitionRuleDictionary = {0: 'Load as eleLoad on beam element.',
	1: 'Load as distributed on nodes along edge.',
	2: 'Load as concentrated load on vertices.'}

class Edge:
	def __init__(self, id, P0, P1, takeLoad = True, repartitionRule = 0, length = None):
		self.id = id
		# maybe for performance it is better a map...?
		self.P0 = P0
		self.P1 = P1
		self.takeLoad = takeLoad
		self.repartitionRule = repartitionRule
		self.discretizedEdge = Math.double_array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
		#for i in range(6):
		#	self.discretizedEdge[i] = float(i)
		self.nDiscretization = 2
		self.tributaryWidth = Math.double_array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
		self.loaded = False
		self.length = length

	def __str__(self):
		str = 'Edge id {}, from vertex {} to vertex {}'.format(self.id,self.P0,self.P1)
		str += '\n'
		str += 'Length = {}\n'.format(self.length)
		if self.takeLoad:
			str += 'Can take load. '
		else:
			str += 'Cannot take load. '
		str += repartitionRuleDictionary.get(self.repartitionRule)
		str += '\ndiscretizedEdge: ['
		for i in range(self.nDiscretization):
			str += '{}, '.format(self.discretizedEdge[i])
		str += ']\nlen of discretizedEdge = {}'.format(self.nDiscretization)
		str += '\nTributary width on discretizedEdge: ['
		for i in range(self.nDiscretization):
			str += '{}, '.format(self.tributaryWidth[i])
		str += ']\n'
		str += 'Is Loaded? {}'.format(self.loaded)
		return str

	def addPoint(self,alpha):
		self.discretizedEdge[self.nDiscretization] = alpha
		self.discretizedEdge = Math.double_array(list(sorted(set(self.discretizedEdge))))
		self.nDiscretization += 1

	def setLoad(self, idx, tw):
		if idx < self.nDiscretization:
			self.tributaryWidth[idx] = tw
		if not self.loaded:
			self.loaded = True

	def addLoad(self, idx, tw):
		if idx < self.nDiscretization:
			self.tributaryWidth[idx] += tw
		if not self.loaded:
			self.loaded = True
			
	def getLoadAt(self, x):
		# get Load at x coordinate (from 0 to 1)
		if x == 0.0:
			return self.tributaryWidth[0]
		if x == 1.0:
			return self.tributaryWidth[self.nDiscretization-1]
		for i in range(self.nDiscretization):
			if self.discretizedEdge[i+1] >= x:
				return (self.tributaryWidth[i+1]-self.tributaryWidth[i])/(self.discretizedEdge[i+1]-self.discretizedEdge[i])*(x-self.discretizedEdge[i])+self.tributaryWidth[i]
		
	def getSlopeAt(self,x):
		# get Load changeRate at x coordinate (from 0 to 1)
		if x == 0.0:
			return (self.tributaryWidth[1]-self.tributaryWidth[0])/(self.discretizedEdge[1]-self.discretizedEdge[0])
		if x == 1.0:
			return (self.tributaryWidth[self.nDiscretization-1]-self.tributaryWidth[self.nDiscretization-2])/(self.discretizedEdge[self.nDiscretization-1]-self.discretizedEdge[self.nDiscretization-2])
		for i in range(self.nDiscretization):
			if self.discretizedEdge[i+1] >= x:
				return (self.tributaryWidth[i+1]-self.tributaryWidth[i])/(self.discretizedEdge[i+1]-self.discretizedEdge[i])
	
	def isSubdivided(self):
		if self.nDiscretization > 2:
			return True
		else:
			return False
			
	def getDiscretizedTributaryWidth(self,x1,x2,n_max = 10):
		# Returns two vectors with coordinates and tributary widths with a maximum number of discretizations for linear parts equal to n_max
		discr = []
		trib = []
		# Find first sub-edge
		for d1 in range(self.nDiscretization-1):
			if x1 <= self.discretizedEdge[d1+1]:
				break
		# Find last sub-edge
		for d2 in range(self.nDiscretization):
			if x2 <= self.discretizedEdge[d2]:
				break
		discr.append(x1)
		trib.append(self.getLoadAt(x1))
		for d in range(d1+1,d2):
			if abs(self.discretizedEdge[d] - self.discretizedEdge[d-1]) < 1e-6:
				discr.append(self.discretizedEdge[d])
				trib.append(self.getLoadAt(self.discretizedEdge[d]))
				continue
			# guarda se variazione constante
			if abs(trib[len(discr)-1]-self.getLoadAt(self.discretizedEdge[d])) < 1e-8:
				# # costante
				discr.append(self.discretizedEdge[d])
				trib.append(self.getLoadAt(self.discretizedEdge[d]))
			else:
				# variabile, divido in n_max
				delta = (self.discretizedEdge[d] - discr[len(discr)-1]) / n_max
				for i in range(n_max):
					discr.append(delta + discr[len(discr)-1])
					trib.append(self.getLoadAt(discr[len(discr)-1]))
		# Variazione costante o lineare tra ultimo e x2
		if abs(trib[len(discr)-1]-self.getLoadAt(x2)) < 1e-8:
			# Costante
			discr.append(x2)
			trib.append(self.getLoadAt(x2))
		else:
			delta = (x2 - discr[len(discr)-1])/n_max
			for i in range(n_max):
				d = delta + discr[len(discr)-1]
				discr.append(d)
				trib.append(self.getLoadAt(d))
		discretizedEdge = Math.double_array(discr)
		tributaryWidth = Math.double_array(trib)
		return discretizedEdge, tributaryWidth
			

class Face:
	def __init__(self, id, vertices, dir, type):
		self.id = id
		# maybe for perfomance it is better a map...?
		self.vertices = vertices
		self.dir = dir
		self.type = type # 1: 1-way - 2: 2-way

	def __str__(self):
		str = 'Face id {}. Vertices: {}\n'.format(self.id,self.vertices)
		str += '\tDirection (angle respect to local x): {}\n'.format(self.dir)
		str += '\tType: {} floor slab\n'.format(self.type)
		return str

def _globalChecksFace(i,geom,pinfo):
	'''
	This function perform global checks to see if we can apply the SurfaceLoad
	on the i-th face.
	If face is not planar -> skip
	If face has physical property defined (is modelled) -> skip
	If face has localAxes other than rectangular -> skip
	If face has more than 4 vertices -> skip
	If not all edges are linear and with 2 nodes -> skip
	'''
	shape = geom.shape
	phy_prop_asn = geom.physicalPropertyAssignment

	p = shape.getFaceProperties(i)
	# check if planar
	if not p.isPlanar:
		IO.write_cerr('WARNING: face {} is not planar. Impossible to apply the equivalent surface load. Skipping the face.\n'.format(i))
		pinfo.out_file.write('# WARNING: face {} is not planar. Impossible to apply the equivalent surface load. Skipping the face.\n'.format(i))
		return False
	# check if face has defined a physical property
	if phy_prop_asn.onFaces[i] is not None:
		IO.write_cerr('WARNING: face {} has a physical property defined. It is suggested to use a FaceLoad to apply load to nodes of the face. Skipping the face.\n'.format(i))
		pinfo.out_file.write('# WARNING: face {} has a physical property defined. It is suggested to use a FaceLoad to apply load to nodes of the face. Skipping the face.\n'.format(i))
		return False
	# check if localAxes are other than rectangular (MASSIMO: Da fare, per esportare funzione)
	if False:
		IO.write_cerr('WARNING: face {} has non-rectangular local axes. Impossible to apply the equivalent surface load. Skipping the face.\n'.format(i))
		pinfo.out_file.write('# WARNING: face {} has non-rectangular local axes. Impossible to apply the equivalent surface load. Skipping the face.\n'.format(i))
		return False
	# Check if the face has more than 4 vertices
	nv = len(shape.getSubshapeChildren(i, MpcSubshapeType.Face, MpcSubshapeType.Vertex))
	if nv > 4:
		IO.write_cerr('WARNING: face {} has more than 4 vertices. Impossible to apply the equivalent surface load. Skipping the face.\n'.format(i))
		pinfo.out_file.write('# WARNING: face {} has more than 4 vertices. Impossible to apply the equivalent surface load. Skipping the face.\n'.format(i))
		return False
	# Now check edges if all linear and all have 2 nodes
	edges = shape.getSubshapeChildren(i, MpcSubshapeType.Face, MpcSubshapeType.Edge)
	ne = len(edges)
	are_linear = True
	are_twoNodes = True
	for e in edges:
		is_linear = shape.isStraightEdge(e)
		if not is_linear:
			are_linear = False
		nv = len(shape.getSubshapeChildren(e,MpcSubshapeType.Edge,MpcSubshapeType.Vertex))
		if nv != 2:
			are_twoNodes = False
	if not are_linear:
		IO.write_cerr('WARNING: face {} has one or more non-straight edges. Impossible to apply the equivalent surface load. Skipping the face.\n'.format(i))
		pinfo.out_file.write('# WARNING: face {} has one or more non-straight edges. Impossible to apply the equivalent surface load. Skipping the face.\n'.format(i))
		return False
	if not are_twoNodes:
		IO.write_cerr('WARNING: face {} has one or more edges with less or more than 2 vertices. Impossible to apply the equivalent surface load. Skipping the face.\n'.format(i))
		pinfo.out_file.write('# WARNING: face {} has one or more edges with less or more than 2 vertices. Impossible to apply the equivalent surface load. Skipping the face.\n'.format(i))
		return False
	return True

def _process_edges(i, geom, unsupporting_elements):
	'''
	This function process the edges of the i-th face in order to understand
	if and how to distribute load.
	The function returns the data_structure needed for subsequent elaborations
	INPUT: i, geom, unsupporting_elements
	OUTPUT: edges, edges_map
	'''
	edges_vec = []
	edges_map = {}

	shape = geom.shape
	phy_prop_asn = geom.physicalPropertyAssignment

	# All edges that are part of the i-th face
	edges = shape.getSubshapeChildren(i, MpcSubshapeType.Face, MpcSubshapeType.Edge)
	idx = 0
	for e in edges:
		takeLoad = True # By default the element is able to take load
		repartitionRule = 0 # By default load is transferred to edge with eleLoad
		# check if it is an element selected by user as "cannot take load"
		if e in unsupporting_elements:
			takeLoad = False
		# check if there is physical property assignment for the considered edge
		phys_prop = phy_prop_asn.onEdges[e]
		if phys_prop is None:
			# It has not any phycal property, let's check if it appartains to
			# a parent face element modelled
			parent_Faces = shape.getSubshapeParents(e, MpcSubshapeType.Edge, MpcSubshapeType.Face)
			if len(parent_Faces) == 1:
				print('WARNING: Edge {} has {} phycal property so its load will be assigned to extreme vertices.\n'.format(e,phys_prop))
				repartitionRule = 2 # Assign load only on two extreme nodes of the element
			else:
				face_modelled = False
				for f in parent_Faces:
					if f == i:
						continue
					else:
						if phy_prop_asn.onFaces[f] is not None:
							face_modelled = True
				if face_modelled:
					print('WARNING: Edge {} has {} phycal property but appartains to a modelled face, so its load will be applied to the nodes.\n'.format(e,phys_prop))
					repartitionRule = 1
				else:
					print('WARNING: Edge {} has {} phycal property so its load will be assigned to extreme vertices.\n'.format(e,phys_prop))
					repartitionRule = 2
		vertices = shape.getSubshapeChildren(e,MpcSubshapeType.Edge,MpcSubshapeType.Vertex)
		if not e in edges_map:
			edges_map.update({e: idx})
		# Understand order of vertices
		dx = Math.vec3()
		dy = Math.vec3()
		dz = Math.vec3()
		if not geom.getLocalAxesOnEdge(e, dx, dy, dz):
			raise Exception('Error: cannot get local axes from edge {}'.format(e))
		P0 = shape.vertexPosition(vertices[0])
		P1 = shape.vertexPosition(vertices[1])
		length = _distanceTwoPoints(P0,P1)
		if dx.dot(P1-P0) < 0:
			edges_vec.append(Edge(e,vertices[1],vertices[0], takeLoad = takeLoad, repartitionRule = repartitionRule, length = length))
		else:
			edges_vec.append(Edge(e,vertices[0],vertices[1], takeLoad = takeLoad, repartitionRule = repartitionRule, length = length))
		idx += 1
		
	return edges_vec, edges_map

def _computeTributaryOnEdges(i, geom, face, edges, edges_map):
	'''
	This function process the edges of the i-th face and calculates the tributary
	width for each of them.
	If needed, the edges are subdived assuming for each subdivision a linear
	variation of tributary width
	The function returns the updated edges
	INPUT: i, geom, unsupporting_elements
	OUTPUT: edges, edges_map
	'''
	# Compute direction vector
	# Obtain local axes of the faice
	dx = Math.vec3()
	dy = Math.vec3()
	dz = Math.vec3()
	if not geom.getLocalAxesOnFace(i, dx, dy, dz):
		raise Exception('Error: cannot get local axes from face {}'.format(i))
	# Create a vector representing the direction of the floor. It is a rotation of x-local by face.dir
	c = cos(radians(face.dir/2))
	s = sin(radians(face.dir/2))
	# create the quaternion
	q = Math.quaternion(c,dz[0]*s,dz[1]*s,dz[2]*s)
	#Create the floor direction vector
	dir_vec = q.rotate(dx)
	
	if _faceIsRectangular(i,geom):
		if face.type == 'one-way':
			# one-way floor system
			aligned, H = _rectangularFaceAlignedWithFloorDirection(geom,edges,dir_vec)
			if aligned:
				# Perform simplified calculation
				for e in edges:
					# if edge cannot take load continue
					if not e.takeLoad:
						continue
					else:
						P0 = geom.shape.vertexPosition(e.P0)
						P1 = geom.shape.vertexPosition(e.P1)
						dirEdge = P1-P0
						# compare direction of vec to direction vector to see if perpendicular
						if abs(dir_vec.dot(dirEdge)) < 1e-8:
							# The two vectors are perpendicular
							# Look for the opposite edge
							for e2 in edges:
								if e.P0 == e2.P0 or e.P1 == e2.P1 or e.P0 == e2.P1 or e.P1 == e2.P0:
									continue
								else:
									if e2.takeLoad:
										# The opposite edge can take load, you take the half of the tributary width.
										e.setLoad(0, H/2)
										e.setLoad(1, H/2)
									else:
										# The opposite edge can take load, you take all the tributary width.
										e.setLoad(0, H)
										e.setLoad(1, H)
			else:
				# Complex one-way
				_quadFaceTributaryAreaComputation(i, geom, face, edges, edges_map, dir_vec)
		else:
			# two-way floor system
			# NOTE: We assume all edges as supporting.
			# For now we don't support the case of free edges
			B, H = aligned, H = _rectangularDimensions(geom,face,edges,dir_vec)
			# For each edge I compute the tributary width
			if abs(B-H) < 1e-8:
				# It is a square. Each edge has a triangular load
				for e in edges:
					if not e.takeLoad:
						raise Exception("Two-way floor can be defined with only supporting elements. Edge {} was declared non-supporting".format(e.id))
					e.addPoint(0.5)
					e.setLoad(0,0.0)
					e.setLoad(1,H/2)
					e.setLoad(2,0.0)
			else:
				# It is a rectangle. The two long edges have trapezoidal load, the
				# two short edges have tringular load
				for e in edges:
					if not e.takeLoad:
						raise Exception("Two-way floor can be defined with only supporting elements. Edge {} was declared non-supporting".format(e.id))
					if abs(e.length - B) < 1e-8:
						# It is a long side
						e.addPoint(H/(2*B))
						e.addPoint(1.0-H/(2*B))
						e.setLoad(0,0.0)
						e.setLoad(1,H/2)
						e.setLoad(2,H/2)
						e.setLoad(3,0.0)
					else:
						# It is a short side
						e.addPoint(0.5)
						e.setLoad(0,0.0)
						e.setLoad(1,H/2)
						e.setLoad(2,0.0)
	else:
		if face.type == 'one-way':
			_quadFaceTributaryAreaComputation(i, geom, face, edges, edges_map, dir_vec, pinfo)
		else:
			raise Exception('Error: Face {} is defined as two-way floor but is not-rectangular. Method not yet implemented'.format(i))
	return edges

def _distanceTwoPoints(P1, P2):
	'''
	This function returns the distance between points P1 and P2
	(P1 and P2 are of type Vec3)
	'''
	dist = (P2.x - P1.x)**2
	dist += (P2.y - P1.y)**2
	dist += (P2.z - P1.z)**2
	dist = dist**0.5
	return dist

def _faceIsRectangular(i, geom):
	'''
	This function returns True if the i-th face is a rectangle
	'''
	dist = set()
	vertices = geom.shape.getSubshapeChildren(i,MpcSubshapeType.Face,MpcSubshapeType.Vertex)
	vertices_map = {}
	for v in vertices:
		vertices_map.update({v: geom.shape.vertexPosition(v)})
	if len(vertices) == 4:
		for v1 in vertices:
			for v2 in vertices:
				if v1 != v2:
					dist.add(round(_distanceTwoPoints(vertices_map.get(v1),vertices_map.get(v2)),6))
		if len(dist) > 3:
			return False
		else:
			return True
	else:
		return False

def _rectangularDimensions(geom, face, edges, dir_vec):
	# B, H represent width and height of rectangle. Note that B >= H
	B = 0.0
	H = 0.0
	sides = set()
	for e in edges:
		P0 = geom.shape.vertexPosition(e.P0)
		P1 = geom.shape.vertexPosition(e.P1)
		length = _distanceTwoPoints(P0,P1)
		sides.add(round(length,6))
	if len(sides) > 2:
		raise Exception('Error: Rectangle with more than 2 dimensions! sides = {}'.format(sides))
	B = max(sides)
	H = min(sides)
	print("Rectangle: B = {} H = {}".format(B,H))
	return B, H

def _rectangularFaceAlignedWithFloorDirection(geom, edges, dir_vec):
	'''
	This function checks if the rectangula floor has the direction aligned to one
	of the sides. In this case return the width of the floor to compute the 
	tributary width
	'''
	# H is the height of the rectangle (the side in direction parallel to dir)
	H = 0.0
	
	# Check if dir_vec is parallel to one of the sides of the rectangle
	aligned = False
	for e in edges:
		P0 = geom.shape.vertexPosition(e.P0)
		P1 = geom.shape.vertexPosition(e.P1)
		dirEdge = P1-P0
		# compare direction of vec to direction vector to see if parallel
		if abs(dir_vec.cross(dirEdge).norm()) < 1e-8:
			# The two vectors are parallel
			aligned = True
			H = dirEdge.norm()
			break
	return aligned, H
	
def _quadFaceTributaryAreaComputation(i, geom, face, edges, edges_map, dir_vec):
	shape = geom.shape
	dx = Math.vec3()
	dy = Math.vec3()
	dz = Math.vec3()
	# Get local system of face
	if not geom.getLocalAxesOnFace(i, dx, dy, dz):
		raise Exception('Error: cannot get local axes from face {}'.format(i))
	# Get vertices of face
	iv = shape.getSubshapeChildren(i, MpcSubshapeType.Face, MpcSubshapeType.Vertex)
	# map local vertices to global vertices
	map_face_vertices = {}
	ii = 0
	vertices = Math.mat(3,len(iv))
	dy = dir_vec
	dx = dy.cross(dz)
	R = Math.mat3(dx,dy,dz)
	RT = R.transpose()
	q = RT.toQuaternion()
	for j in iv:
		map_face_vertices[j] = ii
		p = shape.vertexPosition(j)
		p = q.rotate(p)
		vertices[0,ii] = p.x
		vertices[1,ii] = p.y
		vertices[2,ii] = p.z
		ii += 1
	
	# Phase 1: cycle on all vertices for finding intersections
	for v in range(len(iv)):
		vertex = iv[v]
		vertexCoorX = vertices[0,v]
		# For each vertex
		for e in edges:
			# for each edge
			if (e.P0 == vertex) or (e.P1 == vertex):
				continue
			else:
				# Check if exist intersection between floor line and edge e
				mapP0 = map_face_vertices[e.P0]
				mapP1 = map_face_vertices[e.P1]
				P0coorX = vertices[0,mapP0]
				P1coorX = vertices[0,mapP1]
				if ((P0coorX - vertexCoorX < -1e-8) and (P1coorX - vertexCoorX > 1e-8)) or ((P0coorX - vertexCoorX> 1e-8) and (P1coorX - vertexCoorX< -1e-8)):
					# An intersection exists
					alphaI = (vertexCoorX - P0coorX)/(P1coorX - P0coorX)
					e.addPoint(alphaI-1e-7)
					e.addPoint(alphaI+1e-7)
					
	# Phase 2: for each edge proceed and understand which is opposite edge
	for e in edges:
		if e.takeLoad:
			mapP0 = map_face_vertices[e.P0]
			mapP1 = map_face_vertices[e.P1]
			P0coor = Math.vec3(vertices[0,mapP0],vertices[1,mapP0],vertices[2,mapP0])
			P1coor = Math.vec3(vertices[0,mapP1],vertices[1,mapP1],vertices[2,mapP1])
			P1P0 = P1coor-P0coor
			P1P0 = P1P0*(1.0/P1P0.norm())
			cos_theta = P1P0.dot(Math.vec3(0,1,0))
			sin_theta = (1.0 - cos_theta**2)**0.5
			# For each edge of the face that is not parallel to direction of floor (DX = 0)
			if abs(P1coor[0]-P0coor[0]) > 1e-8:
				for ic in range(e.nDiscretization):
					csi = e.discretizedEdge[ic]
					pt = P0coor + (P1coor-P0coor) * csi
					for other_edge in edges:
						# For each other edge
						if not (e is other_edge):
							# Jump its self
							mapP0 = map_face_vertices[other_edge.P0]
							mapP1 = map_face_vertices[other_edge.P1]
							P0otherCoor = Math.vec3(vertices[0,mapP0],vertices[1,mapP0],vertices[2,mapP0])
							P1otherCoor = Math.vec3(vertices[0,mapP1],vertices[1,mapP1],vertices[2,mapP1])
							if ((abs(P0otherCoor[0] - pt[0]) < 1e-8) and (abs(P0otherCoor[1] - pt[1]) < 1e-8)) or ((abs(P1otherCoor[0] - pt[0]) < 1e-8) and (abs(P1otherCoor[1] - pt[1]) < 1e-8)):
								continue
							else:
								if ((P0otherCoor[0] - pt[0] < 1e-8) and (P1otherCoor[0] - pt[0] > -1e-8)) or ((P0otherCoor[0] - pt[0]> -1e-8) and (P1otherCoor[0] - pt[0] < 1e-8)):
									dist = abs((P0otherCoor[1]+(P1otherCoor[1]-P0otherCoor[1])/(P1otherCoor[0]-P0otherCoor[0])*(pt[0]-P0otherCoor[0]))-pt[1])
									if other_edge.takeLoad:
										# If the opposite edge can take load you should take only half (then later the other will take the other half)
										# Otherwise I will take 100% (and later the other will take 0%)
										dist = dist/ 2.0
									e.setLoad(ic,dist*sin_theta)
	
	
def _evaluateTclLoad(pinfo, doc, geom, mesh_of_geom, edge, i, FT, is_partitioned, process_id, process_block_count, first_done):
	pinfo.out_file.write('# Applying load in edge {}\n'.format(edge.id,i,geom.id))

	domain = mesh_of_geom.edges[edge.id]
	
	minUedge = 1e10
	maxUedge = -1e10
	segno = +1;
	for e in range(len(domain.elements)):
		elem = domain.elements[e]
		info = domain.elementGeomInfos[e]
		uv_el = []
		for j in range(len(elem.nodes)):
			node = elem.nodes[j]
			uv = info.uv[j]
			if uv[0] < minUedge:
				minUedge = uv[0]
			if uv[0] > maxUedge:
				maxUedge = uv[0]
			uv_el.append(uv[0])
		if uv_el[len(uv_el)-1] < uv_el[0]:
			segno = -1;
	
	for e in range(len(domain.elements)):
		elem = domain.elements[e]
		info = domain.elementGeomInfos[e]
		
		if is_partitioned :
			if doc.mesh.partitionData.elementPartition(elem.id) != process_id:
				continue
				
		minU = 1e10
		maxU = -1e10
		u = []
		u_edge = []
		
		n = len(elem.nodes)
		ngp = len(elem.integrationRule.integrationPoints)
		
		# obtain nodal values of the distributed condition
		nodal_values = [[0.0, 0.0, 0.0] for i in range(n)]
		
		for j in range(n):
			node = elem.nodes[j]
			uv = info.uv[j]
			if uv[0] < minU:
				minU = uv[0]
			if uv[0] > maxU:
				maxU = uv[0]
		for j in range(n):
			node = elem.nodes[j]
			uv = info.uv[j]
			
			if segno == -1:
				u_edge.append(segno*(uv[0]-minUedge)/(maxUedge-minUedge)+1)
				u.append(segno*(uv[0]-minU)/(maxU-minU)+1)
			else:
				u_edge.append((uv[0]-minUedge)/(maxUedge-minUedge))
				u.append((uv[0]-minU)/(maxU-minU))
			
			trib_width_node = edge.getLoadAt(u_edge[len(u_edge)-1])
			nodal_values[j][0] = trib_width_node*FT.x
			nodal_values[j][1] = trib_width_node*FT.y
			nodal_values[j][2] = trib_width_node*FT.z
			
		discr, trib = edge.getDiscretizedTributaryWidth(u_edge[0],u_edge[1],n_max=10)
		pinfo.out_file.write("# Elem {} \n".format(elem.id))
		
		if edge.repartitionRule == 0:
			pinfo.out_file.write("# Repartition as eleLoad\n")
			# Rotation to local system:
			Floc = elem.orientation.quaternion.conjugate().rotate(FT)
			# Creation of Tcl eleLoad
			eleTag = ''
			if is_partitioned :
				if not first_done:
					if process_block_count == 0:
						pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
					else:
						pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
					first_done = True
			eleTag += ' {}'.format(elem.id)
			for j in range(len(discr)-1):
				if abs(discr[j+1] - discr[j]) < 1e-6:
					continue
				tw = (trib[j] + trib[j+1]) / 2.0
				Wy = Floc[1]*tw
				Wz = Floc[2]*tw
				Wx = Floc[0]*tw
				a = u[1]/(u_edge[1]-u_edge[0])*(discr[j]-u_edge[0])
				b = u[1]/(u_edge[1]-u_edge[0])*(discr[j+1]-u_edge[0])
				if eleTag:
					str_tcl = '{}{}eleLoad -ele{} -type -beamUniform {} {} {} {} {}\n'.format(pinfo.indent, pinfo.tabIndent, eleTag, Wy, Wz, Wx, a, b)
				pinfo.out_file.write(str_tcl)
		elif edge.repartitionRule == 1:
			pinfo.out_file.write("# Repartition as edgeLoad\n")
			# do nodal lumping
			nodal_lumped_values = [[0.0, 0.0, 0.0, 0.0] for ii in range(n)]
			for gp in range(ngp):
				gauss_point = elem.integrationRule.integrationPoints[gp]
				N = elem.shapeFunctionsAt(gauss_point)
				det_J = elem.jacobianAt(gauss_point).det()
				W = gauss_point.w
				
				# interpolate nodal value at this gp
				fx = 0.0
				fy = 0.0
				fz = 0.0
				for ii in range(n):
					Ni = N[ii]
					fx += Ni * nodal_values[ii][0]
					fy += Ni * nodal_values[ii][1]
					fz += Ni * nodal_values[ii][2]
				
				for ii in range(n):
					fact = N[ii] * det_J * W
					lump = nodal_lumped_values[ii]
					lump[0] = elem.nodes[ii].id
					lump[1] += fx * fact
					lump[2] += fy * fact
					lump[3] += fz * fact
			for ii in range(n):
				lump = nodal_lumped_values[ii]
				lump[0] = elem.nodes[ii].id
				str_tcl = []
				sopt = ('\n'.join(['{} {}'.format(lump[1], lump[2])]))
				if (lump[0] in pinfo.node_to_model_map):
					if is_partitioned :
						if not first_done:
							if process_block_count == 0:
								pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', process_id, '} {'))
							else:
								pinfo.out_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$STKO_VAR_process_id == ', process_id, '} {'))
								
							first_done = True
							
					spatial_info = pinfo.node_to_model_map[lump[0]]
					node_ndm = spatial_info[0]
					node_ndf = spatial_info[1]
					
					if (node_ndm == 2):
						if (node_ndf == 3) or (node_ndf == 33):
							sopt += ('\n'.join([' 0.0']))
					else:
						sopt += ('\n'.join([' {}'.format( lump[3])]))
						if (node_ndf == 4):
							sopt += ('\n'.join([' 0.0']))
						elif (node_ndf == 6):
							sopt += ('\n'.join([' 0.0 0.0 0.0']))
				else :
					raise Exception('Error: node without assigned element')
				str_tcl.append('{}{}load {} {}'.format(pinfo.indent, pinfo.tabIndent, lump[0] , sopt))
				
				# now write the string into the file
				pinfo.out_file.write('\n'.join(str_tcl))
				pinfo.out_file.write('\n')
						
		else:
			pinfo.out_file.write('# Unknwon repartition Rule. Impossible to compute load on edge {} (face {} - geom {})\n'.format(edge.id,i,geom.id))
			IO.write_cerr('WARNING: Unknwon repartition Rule. Impossible to compute load on edge {} (face {} - geom {})\n'.format(edge.id,i,geom.id))
			raise Exception('Error: Unknwon repartition Rule. Impossible to compute load on edge edge {} (face {} - geom {})\n'.format(edge.id,i,geom.id))
		
	return first_done, process_block_count

####################################################################################
# Main methods
####################################################################################

def makeXObjectMetaData():
	'''
	fill the 3d vector data. set the pressure value
	at the z component, since the orientation is set to local
	'''

	# Type
	at_Type = MpcAttributeMetaData()
	at_Type.type = MpcAttributeType.String
	at_Type.name = 'Type'
	at_Type.group = 'Group'
	at_Type.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') +
		html_par('choose between "one-way" and "two-way"') +
		html_end()
		)
	at_Type.sourceType = MpcAttributeSourceType.List
	at_Type.setSourceList(['one-way', 'two-way'])
	at_Type.setDefault('one-way')

	# one-way
	at_oneway = MpcAttributeMetaData()
	at_oneway.type = MpcAttributeType.Boolean
	at_oneway.name = 'one-way'
	at_oneway.group = 'Data'
	at_oneway.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('one-way')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_oneway.editable = False

	# two-way
	at_twoway = MpcAttributeMetaData()
	at_twoway.type = MpcAttributeType.Boolean
	at_twoway.name = 'two-way'
	at_twoway.group = 'Data'
	at_twoway.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('two-way')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_twoway.editable = False

	# Direction
	at_Direction = MpcAttributeMetaData()
	at_Direction.type = MpcAttributeType.Real
	at_Direction.name = 'Direction'
	at_Direction.group = 'Data'
	at_Direction.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Dimension')+'<br/>') +
		html_par('Direction respect to local x axis in degrees') +
		html_end()
		)
	at_Direction.setDefault(90.0)

	# unsupporting elements
	at_unsupporting = MpcAttributeMetaData()
	at_unsupporting.type = MpcAttributeType.Index
	at_unsupporting.name = 'unsupportingSelectionSet'
	at_unsupporting.group = 'Group'
	at_unsupporting.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Unsupporting elements')+'<br/>') +
		html_par((
			'Elements that are considered not able to support the load.<br/>'
			'Choose a selection set that contains at least 1 edge. '
			'Only the edges will be considered.'
			)) +
		#html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Displacement_Control','Displacement Control')+'<br/>') +
		html_end()
		)
	at_unsupporting.indexSource.type = MpcAttributeIndexSourceType.SelectionSet

	# F
	at_F = MpcAttributeMetaData()
	at_F.type = MpcAttributeType.QuantityVector3
	at_F.name = 'F'
	at_F.group = 'Data'
	at_F.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('F')+'<br/>') +
		html_par('The 3d force vector') +
		html_end()
		)
	at_F.dimension = u.F/u.L**2

	# Orientation
	at_Orientation = MpcAttributeMetaData()
	at_Orientation.type = MpcAttributeType.String
	at_Orientation.name = 'Orientation'
	at_Orientation.group = 'Group'
	at_Orientation.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Orientation')+'<br/>') +
		html_par('Choose between "Global" and "Local". To define components in global coordinate system choose "Global". Otherwise choose "Local" to define components in local coordinate system.') +
		html_end()
		)
	at_Orientation.sourceType = MpcAttributeSourceType.List
	at_Orientation.setSourceList(['Global', 'Local'])
	at_Orientation.setDefault('Global')

	# global
	at_global = MpcAttributeMetaData()
	at_global.type = MpcAttributeType.Boolean
	at_global.name = 'Global'
	at_global.group = 'Data'
	at_global.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('global')+'<br/>') +
		html_par('') +
		html_end()
		)
	at_global.editable = False

	# projection
	at_projection = MpcAttributeMetaData()
	at_projection.type = MpcAttributeType.Boolean
	at_projection.name = 'Projection'
	at_projection.group = 'Data'
	at_projection.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('projection')+'<br/>') +
		html_par('') +
		html_end()
	)
	at_projection.default = False
	at_projection.editable = True


	xom = MpcXObjectMetaData()
	xom.name = 'SurfaceLoad'
	xom.addAttribute(at_Type)
	xom.addAttribute(at_oneway)
	xom.addAttribute(at_twoway)
	xom.addAttribute(at_Direction)
	xom.addAttribute(at_unsupporting)
	xom.addAttribute(at_F)
	xom.addAttribute(at_Orientation)
	xom.addAttribute(at_global)
	xom.addAttribute(at_projection)

	# visibility dependencies

	# oneway dependency
	xom.setVisibilityDependency(at_oneway, at_Direction)

	# projection dependency
	xom.setVisibilityDependency(at_global, at_projection)

	# auto-exclusive dependencies
	xom.setBooleanAutoExclusiveDependency(at_Type, at_oneway)
	xom.setBooleanAutoExclusiveDependency(at_Type, at_twoway)
	xom.setBooleanAutoExclusiveDependency(at_Orientation, at_global)

	return xom


def fillConditionRepresentationData(xobj, pos, data):
	'''
	Fills the 3D vector data.

	Set the pressure value
	at the z component, since the orientation is set to local
	'''
	print('Filling Condition Representation Data')
	F = xobj.getAttribute('F').quantityVector3.value

	data[0] = F.x
	data[1] = F.y
	data[2] = F.z

def makeConditionRepresentationData(xobj):
	'''
	Create the condition representation data for STKO.
	Here we want an arrow (vector) representation in global
	coordinate system, that can be applied only on faces.
	We need to allocate a 3d vector for the data attribute.
	The components of this vector will be set using
	@ref fillConditionRepresentationData
	'''
	print('Making Condition Representation Data')
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Arrows
	d.orientation = MpcConditionVRepOrientation.Global

	at_global = xobj.getAttribute('Global')
	if at_global is not None:
		if not at_global.boolean:
			d.orientation = MpcConditionVRepOrientation.Local

	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = False
	d.on_edges = False
	d.on_faces = True
	d.on_solids = False
	d.on_interactions = False
	return d

def _process_load (doc, pinfo, all_geom, F, is_partitioned, process_id, process_block_count, is_Global, is_Projected, Type, direction, unsupporting_selection_set):
	print('writing surface load...')

	# for each geometry to which a condition is applied
	first_done = False
	for geom, subset in all_geom.items():
		# geometry
		print('Processing geometry {}...'.format(geom.id))
		pinfo.out_file.write('# Processing geometry {}\n'.format(geom.id))

		mesh_of_geom = doc.mesh.getMeshedGeometry(geom.id)
		for i in subset.faces:
			pinfo.out_file.write('# Processing face {}\n'.format(i))
			print('Processing face {}...'.format(i))
			# Step 1: perform global checks (if not met, skip to next face)
			if not _globalChecksFace(i,geom,pinfo):
				continue

			vertices = geom.shape.getSubshapeChildren(i, MpcSubshapeType.Face, MpcSubshapeType.Vertex)
			face = Face(i, vertices, direction, Type)
			# Step 2: Create a set of unsupporting elements for this geometry
			unsupporting_elems = set()
			if unsupporting_selection_set is not None:
				for geom_id, geom_subset in unsupporting_selection_set.geometries.items():
					if geom_id == geom.id:
						for e in geom_subset.edges:
							unsupporting_elems.add(e)

			# Step 3: Process the face and create the data structure for edges
			edges, edges_map = _process_edges(i, geom, unsupporting_elems)

			# Step 4: Compute tributary width for each edge of the face
			edges = _computeTributaryOnEdges(i, geom, face, edges, edges_map)
			# print('\n***** DEBUG ********\n')
			# print('Computed tributary widths on edges...')
			# print('\n\n')
			# for e in edges:
				# if e.loaded:
					# print(e)
			# print(face)
			# print('***** END DEBUG ********')
			
			# Step 5: Compute the projection coefficient in case it is global and projected
			# Obtain local axes of the faice
			coeff_projection = 1.0
			if is_Global:
				if is_Projected:
					dx = Math.vec3()
					dy = Math.vec3()
					dz = Math.vec3()
					if not geom.getLocalAxesOnFace(i, dx, dy, dz):
						raise Exception('Error: cannot get local axes from face {}'.format(i))
					# The term related to the 2 rotation about X and Y is dz(3) = cos(alfa_x)*cos(alfa_y)
					coeff_projection = dz[2]
					# Se la superficie è nel piano questo coefficiente dovrebbe sempre essere 1
			
			# Step 6: compute forces in global system and projected
			# It is a plane, so I can refer to the same element?
			domain = mesh_of_geom.faces[i]
			elem = domain.elements[0]
			if not is_Global:
				FT = elem.orientation.quaternion.rotate(F)
			else:
				FT = F*coeff_projection
			
			# Step 6: apply load as eleLoad (rule 0) distributed (rule 1) vertices (rule 2)
			for e in edges:
				if e.loaded:
					first_done, process_block_count = _evaluateTclLoad(pinfo, doc, geom, mesh_of_geom,e,i,FT,is_partitioned, process_id, process_block_count, first_done)
					

	if is_partitioned :
		if first_done:
			process_block_count += 1
		if process_block_count > 0 and first_done:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
		return process_block_count

def onEditFinished(editor, xobj):
	# DEBUG - TO BE ERASED
	print('*****************************************')
	print('Edit Fineshed - summary of results:\n')
	print('Type: {}'.format(_get_xobj_attribute(xobj, 'Type').string))
	print('One-Way: {}'.format(_get_xobj_attribute(xobj, 'one-way').boolean))
	print('Two-way: {}'.format(_get_xobj_attribute(xobj, 'two-way').boolean))
	print('Direction: {}'.format(_get_xobj_attribute(xobj, 'Direction').real))
	print('unsupporting SelSet: {}'.format(_get_xobj_attribute(xobj, 'unsupportingSelectionSet').index))
	print('F: {}'.format(_get_xobj_attribute(xobj, 'F').quantityVector3.value))
	print('Orientation: {}'.format(_get_xobj_attribute(xobj, 'Orientation').string))
	print('Global: {}'.format(_get_xobj_attribute(xobj, 'Global').boolean))
	print('Projection: {}'.format(_get_xobj_attribute(xobj, 'Projection').boolean))
	# END DEBUG TO ERASE

def writeTcl_Load(pinfo, xobj):

	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName

	# Get all geometries to which the condition is applied
	all_geom = pinfo.condition.assignment.geometries
	if len(all_geom) == 0:
		return

	doc = App.caeDocument()
	# Get properties of the surface load
	direction = _get_xobj_attribute(xobj, 'Direction').real
	Type = _get_xobj_attribute(xobj, 'Type').string
	is_Global = _get_xobj_attribute(xobj, 'Global').boolean
	is_Projected = _get_xobj_attribute(xobj, 'Projection').boolean

	unsupporting_selection_set_ID = _get_xobj_attribute(xobj, 'unsupportingSelectionSet').index
	if unsupporting_selection_set_ID in doc.selectionSets:
		unsupporting_selection_set = doc.selectionSets[unsupporting_selection_set_ID]
	else:
		unsupporting_selection_set = None

	F = _get_xobj_attribute(xobj, 'F').quantityVector3.value

	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	if is_partitioned:
		process_block_count = 0
		for process_id in range(pinfo.process_count):
			process_block_count = _process_load (doc, pinfo, all_geom, F, is_partitioned, process_id, process_block_count, is_Global, is_Projected, Type, direction, unsupporting_selection_set)
	else :
		_process_load (doc, pinfo, all_geom, F, is_partitioned, 0, 0, is_Global, is_Projected, Type, direction, unsupporting_selection_set)

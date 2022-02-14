import numpy as np
class ASDEmbeddedNodeElementUtils:
	
	QSubs = ([
		[0,1,2],
		[0,2,3]
		])
	
	HSubs = ([
		[0,1,2,5],
		[3,0,2,7],
		[4,7,5,0],
		[6,5,7,2],
		[7,5,0,2]
		])
	
	# position matrix
	def posmat(nodes):
		n = len(nodes)
		X = np.zeros((3,n))
		for i in range(n):
			inode = nodes[i]
			X[0, i] = inode.x
			X[1, i] = inode.y
			X[2, i] = inode.z
		return X
	
	# local coordinates from global coordinates of a triangle
	def lct3(nodes, G):
		X = ASDEmbeddedNodeElementUtils.posmat(nodes)
		dN = np.asarray([
			[-1.0, -1.0, 0.0],
			[1.0, 0.0, 0.0],
			[0.0, 1.0, 0.0]])
		J = np.matmul(X,dN)
		vx = J[:,0]
		vy = J[:,1]
		vz = np.cross(vx, vy)
		vz /= max(np.linalg.norm(vz), 1.0e-16)
		J[:,2] = vz
		iJ = np.linalg.inv(J)
		J[:,2] = 0.0
		x,y = 0.0, 0.0
		N = np.asarray([[1.0-x-y],[x],[y]])
		P = np.matmul(X,N)
		D = G-P
		L = np.matmul(iJ,D)
		# result
		x,y = L[0,0], L[1,0]
		# check for negative values as an error measure
		N = np.asarray([[1.0-x-y],[x],[y]])
		distance = 0.0
		for i in range(3):
			iN = N[i][0]
			if iN < 0.0:
				distance = max(distance, -iN)
		return ((x,y), distance)
	
	# local coordinates from global coordinates of a tetrahedron
	def lct4(nodes, G):
		X = ASDEmbeddedNodeElementUtils.posmat(nodes)
		dN = np.asarray([
			[-1.0, -1.0, -1.0],
			[1.0, 0.0, 0.0],
			[0.0, 1.0, 0.0],
			[0.0, 0.0, 1.0]])
		J = np.matmul(X,dN)
		iJ = np.linalg.inv(J)
		x,y,z = 0.0, 0.0, 0.0
		N = np.asarray([[1.0-x-y-z],[x],[y],[z]])
		P = np.matmul(X,N)
		D = G-P
		L = np.matmul(iJ,D)
		x,y,z = L[0,0], L[1,0], L[2,0]
		N = np.asarray([[1.0-x-y-z],[x],[y],[z]])
		distance = 0.0
		for i in range(4):
			iN = N[i][0]
			if iN < 0.0:
				distance = max(distance, -iN)
		return ((x,y,z), distance)
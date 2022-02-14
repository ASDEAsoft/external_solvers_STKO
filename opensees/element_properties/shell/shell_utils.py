'''
Here we have some common utils for shell elements in OpenSees.
'''

class __permutations:
	t0 = [0, 1, 2]
	t1 = [1, 2, 0]
	t2 = [2, 0, 1]
	q40 = [0, 1, 2, 3]
	q41 = [1, 2, 3, 0]
	q90 = [0, 1, 2, 3,   4, 5, 6, 7,  8]
	q91 = [1, 2, 3, 0,   5, 6, 7, 4,  8]

def getNodeString(elem):
	
	'''
	In OpenSees shell elements do not allow end-user to set up a local coordinate system.
	They instead choose a predefined local X vector, usually equal to the 1st jacobian (at center) column
	in quadrilateral elements, and allined with the first 2 vertices in triangular elements.
	
	STKO already takes care of rotating results to the user defined coordinate system 
	in post processing. And this is enough for isotropic models.
	
	However if we use an anisotropic law, the user local orientation is important.
	The final aim is to make a modification in OpenSees so that all shell elements
	accept a user-defined local system.
	
	For the moment, to solve most of the problems, assuming the user makes a 
	non distorted mesh, we can allign the nodes (as much as possible) with the local coordinate system
	'''
	
	# user defined x axis
	uvx = elem.orientation.quaternion.toRotationMatrix().col(0)
	
	# find best permutation
	p = elem.nodes
	n = len(p)
	if n == 3:
		vx0 = (p[1].position - p[0].position).normalized()
		d0 = abs(uvx.dot(vx0))
		if d0 >= 0.99:
			perm = __permutations.t0
		else:
			vx1 = (p[2].position - p[1].position).normalized()
			d1 = abs(uvx.dot(vx1))
			if d1 >= 0.99:
				perm = __permutations.t1
			else:
				vx2 = (p[0].position - p[2].position).normalized()
				d2 = abs(uvx.dot(vx2))
				if d2 >= 0.99:
					perm = __permutations.t2
				else:
					# find maximum
					vmax = d0
					perm = __permutations.t0
					if d1 > vmax:
						vmax = d1
						perm = __permutations.t1
					if d2 > vmax:
						vmax = d2
						perm = __permutations.t2
		
	elif n == 4:
		vx = (p[2].position + p[1].position - p[3].position - p[0].position).normalized()
		if abs(uvx.dot(vx)) > 0.5:
			perm = __permutations.q40
		else:
			perm = __permutations.q41
	elif n == 9:
		vx = (p[2].position + p[1].position - p[3].position - p[0].position).normalized()
		if abs(uvx.dot(vx)) > 0.5:
			perm = __permutations.q90
		else:
			perm = __permutations.q91
	
	#if perm is not __permutations.t0 and perm is not __permutations.q40 and perm is not __permutations.q90:
	#	print('changing shell elem orientation')
	
	# done
	return ' '.join(str(elem.nodes[i].id) for i in perm)
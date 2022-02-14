from scipy.spatial import KDTree
import numpy as np

def _err(msg):
	return 'Error in RandomMaterialTable:\n{}'.format(msg)

class RMT:
	'''
	a class for dealing with Random Material Table file format.
	'''
	def __init__(self, fname):
		
		# open file and read all lines
		with open(fname, 'r') as tfile:
			lines = [line.strip() for line in tfile.read().split('\n') if line.strip()]
		
		# check file consistency
		nlines = len(lines)
		if nlines < 3:
			raise Exception(_err('At least 3 lines describing the contents are requested'))
		
		# number of materials
		try:
			nmat = int(lines[0])
		except:
			raise Exception(_err('Cannot read the number of random materials from the first line'))
		if nmat < 1:
			raise Exception(_err('At least 1 material should be provided in the Random Material Table File (Provided material count = {})').format(nmat))
		
		# arguments (self.args)
		self.args = [line.strip() for line in lines[1].split(',') if line.strip()]
		nargs = len(self.args)
		if nargs < 1:
			raise Exception(_err('At least 1 argument should be provided in the Random Material Table File (Provided argument count = {})').format(nargs))
		
		# number of sampling points
		try:
			npts = int(lines[2])
		except:
			raise Exception(_err('Cannot read the number of random material points from the third line'))
		if npts < 1:
			raise Exception(_err('At least 1 material point should be provided in the Random Material Table File (Provided material point count = {})').format(npts))
		if nlines != nmat+npts+3:
			raise Exception(_err('The total number of valid lines in the Random Material Table File ({}) is not equal to the number provided by the 3 header lines').format(npts))
		
		# read materials
		# save a IDs and DATA
		# self.mat_id = list(int) size = nmat
		# self.mat_data = list of arguments (tuple)
		self.mat_id = [0.0]*nmat
		self.mat_data = [None]*nmat
		for i in range(nmat):
			line = lines[i+3]
			words = line.split(',')
			if len(words) != 1+nargs:
				raise Exception(_err('Number of arguments at row {} should be equal to the number of arguments ({}) + 1'.format(i+3, nargs)))
			try:
				self.mat_id[i] = int(words[0])
				mat_values = [None]*nargs
				for j in range(nargs):
					jarg = words[j+1]
					if ';' in jarg:
						# a list
						mat_values[j] = [float(item) for item in jarg.split(';')]
					else:
						# a float
						mat_values[j] = float(jarg)
				mat_values = tuple(mat_values)
				self.mat_data[i] = mat_values
			except:
				raise Exception(_err('Parsing material data failed at row {}. It should contain 1 integer + {} reals/lists'.format(i+3, nargs)))
		
		# read all material points
		# store their coordinate into a numpy Nx3 matrix (self.mat_point_pos)
		# store also a list for each row of the matrix with the material id (self.mat_point_ids)
		self.mat_point_pos = np.zeros((npts, 3))
		self.mat_point_ids = [0]*npts
		for i in range(npts):
			line = lines[i+nmat+3]
			words = line.split(',')
			if len(words) != 4:
				raise Exception(_err('Number of arguments at row {} should be equal to 4 (X,Y,Z,ID)'.format(i+nmat+3)))
			try:
				self.mat_point_pos[i, 0] = float(words[0])
				self.mat_point_pos[i, 1] = float(words[1])
				self.mat_point_pos[i, 2] = float(words[2])
				self.mat_point_ids[i] = int(words[3])
			except:
				raise Exception(_err('Parsing material data failed at row {}. It should contain 1 integer + {} reals'.format(i+3, nargs)))
		
		# generate the KDTree
		perc = 0.0005
		LFS = max(1, int(float(npts)*perc))
		self.tree = KDTree(self.mat_point_pos, leafsize=LFS)
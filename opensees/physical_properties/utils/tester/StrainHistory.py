## @package srainHistory
# The StrainHistory packages contains all classes that define a strain history for
# material testing
#
# The strain history as required by the Tester(1D/2D/3D/3DUP) class, is a very simple class
# that must fullfil these requirements:
# 1) "strain" member of type list
# 2) an empty constructor
# 3) "build" method that takes 3 parameters, the target_strain, the number of cycles and
#    the number of subdivisions
# 4) "getDefaultParams" method that gives default parameters for editing the strain history
# Since it is so simple we don't need to make a base abstract class and use polymorphism at all

import math

## class documentation here
class StrainHistoryParameters:
	def __init__(self, num_cyc, n, target_strain, scale_pos, scale_neg, num_cyc_editable, custom_history_vector = []):
		self.num_cycles = num_cyc
		self.num_divisions = n
		self.target_strain = target_strain
		self.scale_pos = scale_pos
		self.scale_neg = scale_neg
		self.num_cycles_editable = num_cyc_editable
		self.custom_history_vector = custom_history_vector

# discretize strain hist
def _discretize(n, x):
	xmin = 1.0e20
	xmax = -xmin
	for i in x:
		xmin = min(xmin, i)
		xmax = max(xmax, i)
	Dx = xmax-xmin
	dx = Dx/max(n,1)
	y = [x[0]]
	if abs(dx) > 1.0e-16:
		for i in range(1, len(x)):
			Dxi = x[i] - x[i-1]
			ni = max(1, int(math.ceil(abs(Dxi/dx))))
			dxi = Dxi/ni
			iy = x[i-1]
			for j in range(ni):
				iy += dxi
				y.append(iy)
	return y

## This class creates a strain history using the reference curve 
## (i.e. same strains)
class StrainHistoryReference():
	#from PyMpc.Units import MpcQuantityVector
	
	def __init__(self):
		self.strain = []
	
	def getDefaultParams(self):
		return StrainHistoryParameters(1, 10, 0.0, 1.0, 1.0, False)
	
	def build(self, params):
		hist_vector = params.custom_history_vector
		
		self.strain = []
		for i in range(len(hist_vector)):
			self.strain.append(hist_vector.referenceValueAt(i))
		

## This class creates a custom strain history
class StrainHistoryCustom():
	#from PyMpc.Units import MpcQuantityVector
	
	def __init__(self):
		self.strain = []
	
	def getDefaultParams(self):
		return StrainHistoryParameters(1, 10, 0.0, 1.0, 1.0, True)
	
	def build(self, params):
		
		num_cyc = max(1, params.num_cycles)
		n = max(1, params.num_divisions)
		custom_hist_vector = params.custom_history_vector
		spos = params.scale_pos
		sneg = params.scale_neg
		
		# Create the history of strain
		self.strain = [0.0]
		for i in range(len(custom_hist_vector)):
			if i == 0:
				if custom_hist_vector.referenceValueAt(i) == 0:
					continue
			next_strain = custom_hist_vector.referenceValueAt(i)
			if next_strain > 0:
				next_strain *= spos
			elif next_strain < 0:
				next_strain *= sneg
			self.strain.append(next_strain)
		
		# discretize
		self.strain = _discretize(n, self.strain)

## This class creates
class StrainHistoryCyclicAsymmetric():
	def __init__(self):
		self.strain = []
	
	def getDefaultParams(self):
		return StrainHistoryParameters(1, 10, 0.0, 1.0, 1.0, True)
	
	def build(self, params):
		
		target_strain = params.target_strain
		num_cyc = params.num_cycles
		n = params.num_divisions
		spos = params.scale_pos
		sneg = params.scale_neg
		
		if target_strain < 0.0:
			spos,sneg = sneg,spos
		
		# Create the history of strain
		self.strain = [0.0]
		
		for c in range(num_cyc):
			self.strain.append(target_strain * spos)
			self.strain.append(0.0)
		
		# discretize
		self.strain = _discretize(n, self.strain)

## This class creates an asymmetric linearly increasing to target_strain strain history
class StrainHistoryCyclicAsymmLinearIncreasing():
	def __init__(self):
		self.strain = []
	
	def getDefaultParams(self):
		return StrainHistoryParameters(3, 10, 0.0, 1.0, 1.0, True)
	
	def build(self, params):
		
		target_strain = params.target_strain
		num_cyc = params.num_cycles
		n = params.num_divisions
		spos = params.scale_pos
		sneg = params.scale_neg
		
		if target_strain < 0.0:
			spos,sneg = sneg,spos
		
		# Create the history of strain
		self.strain = [0.0]
		
		for c in range(num_cyc):
			strain_c = target_strain / num_cyc * (c+1)
			self.strain.append(strain_c * spos)
			self.strain.append(0.0)
		
		# discretize
		self.strain = _discretize(n, self.strain)

## this class implements a strain history according to EN12512 where
## target_strain is defined as the strain corresponding to the third cycle 
## and is called Vy in EN125122. The cycle sequence is:
## 1x0.25Vy - 1x0.5Vy - 3x1.0Vy - 3x2.0Vy - 3x4.0Vy
class StrainHistoryCyclicEN12512():
	def __init__(self):
		self.strain = []
	
	def getDefaultParams(self):
		return StrainHistoryParameters(11, 10, 0.0, 1.0, 1.0, False)
	
	def build(self, params):
		
		target_strain = params.target_strain
		n = params.num_divisions
		spos = params.scale_pos
		sneg = params.scale_neg
		
		if target_strain < 0.0:
			spos,sneg = sneg,spos
		
		# Create the history of strain
		self.strain = [0.0]
		
		def __createCycle(strain, N):
			eps = []
			for c in range(N):
				eps.append(strain*spos)
				eps.append(- strain*sneg)
			
			return eps
		
		# First cycle at 0.25Y
		strain_c = target_strain/4
		self.strain = self.strain + __createCycle(strain_c,1)
		
		# First cycle at 0.50Y
		strain_c = target_strain/2;
		self.strain = self.strain + __createCycle(strain_c,1)
		
		# Three cycles at 1.00Y
		strain_c = target_strain;
		self.strain = self.strain + __createCycle(strain_c,3)
		
		# Three cycles at 2.00Y
		strain_c = 2 * target_strain;
		self.strain = self.strain + __createCycle(strain_c,3)
		
		# Three cycles at 4.00Y
		strain_c = 4 * target_strain;
		self.strain = self.strain + __createCycle(strain_c,3)
		
		# discretize
		self.strain = _discretize(n, self.strain)

## This class creates a cyclic symmetric linearly increasing strain history
class StrainHistoryCyclicSymmetric():
	def __init__(self):
		self.strain = []
	
	def getDefaultParams(self):
		return StrainHistoryParameters(1, 10, 0.0, 1.0, 1.0, True)
	
	def build(self, params):
		
		target_strain = params.target_strain
		num_cyc = params.num_cycles
		n = params.num_divisions
		spos = params.scale_pos
		sneg = params.scale_neg
		
		if target_strain < 0.0:
			spos,sneg = sneg,spos
		
		# Create the history of strain
		self.strain = [0.0]
		
		for c in range(num_cyc):
			self.strain.append(target_strain * spos)
			self.strain.append(-target_strain * sneg)
		self.strain.append(0.0)
		
		# discretize
		self.strain = _discretize(n, self.strain)

## This class creates a cyclic symmetric linearly increasing strain history
class StrainHistoryCyclicSymmLinearIncreasing():
	def __init__(self):
		self.strain = []
	
	def getDefaultParams(self):
		return StrainHistoryParameters(3, 10, 0.0, 1.0, 1.0, True)
	
	def build(self, params):
		
		target_strain = params.target_strain
		num_cyc = params.num_cycles
		n = params.num_divisions
		spos = params.scale_pos
		sneg = params.scale_neg
		
		if target_strain < 0.0:
			spos,sneg = sneg,spos
		
		# Create the history of strain
		self.strain = [0.0]
		
		for c in range(num_cyc):
			strain_c = target_strain / num_cyc * (c+1)
			self.strain.append(strain_c * spos)
			self.strain.append(-strain_c * sneg)
		self.strain.append(0.0)
		
		# discretize
		self.strain = _discretize(n, self.strain)

## This class creates a strain history for monotonic load.
## The number of cycles is not editable
## Only one scale factor is active in relation to the target strain
class StrainHistoryMonotonic():
	def __init__(self):
		self.strain = []
	
	def getDefaultParams(self):
		return StrainHistoryParameters(1, 100, 0.0, 1.0, 1.0, False)
	
	def build(self, params):
		
		target_strain = params.target_strain
		n = params.num_divisions
		spos = params.scale_pos
		sneg = params.scale_neg
		
		if target_strain < 0.0:
			spos,sneg = sneg,spos
		
		# Create the history of strain
		self.strain = [0.0, target_strain*spos]
		
		# discretize
		self.strain = _discretize(n, self.strain)

## A Factory class used to generate strain histories given their names
class StrainHistoryFactory:
	
	## A static dictionary that maps class names to class types
	supportedTypes = {
		"CyclicAsymmetric" : StrainHistoryCyclicAsymmetric,
		"CyclicAsymmLinearIncreasing" : StrainHistoryCyclicAsymmLinearIncreasing,
		"CyclicEN12512" : StrainHistoryCyclicEN12512,
		"CyclicSymmetric" : StrainHistoryCyclicSymmetric,
		"CyclicSymmLinearIncreasing" : StrainHistoryCyclicSymmLinearIncreasing,
		"Monotonic" : StrainHistoryMonotonic,
		"Custom" : StrainHistoryCustom,
		"ReferenceCurveHistory": StrainHistoryReference
		}
	
	## Gives a list of names of all supported strain history types
	@staticmethod
	def getTypes():
		return StrainHistoryFactory.supportedTypes.keys()
	
	## Constructs the required type given its name.
	# @note If the given name is not among the ones given by @ref getTypes
	# and Exception will be thrown
	@staticmethod
	def make(className):
		if not className in StrainHistoryFactory.supportedTypes.keys():
			raise Exception('The given class "{}" is not supported by the StrainHistoryFactory'.format(className))
		classType = StrainHistoryFactory.supportedTypes[className]
		return classType()
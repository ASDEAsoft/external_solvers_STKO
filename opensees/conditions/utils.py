
class SpatialFunctionEval:
	def __init__(self, pos):
		from asteval import Interpreter
		self.make = Interpreter()
		self.make.symtable['x'] = pos.x
		self.make.symtable['y'] = pos.y
		self.make.symtable['z'] = pos.z
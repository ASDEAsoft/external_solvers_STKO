"""
@package beam_section_utils
This module contains common utilities for beam special purpose properties.

More details.
"""

class beam_int_lobatto:
	W = ({
		2 : [0.5, 0.5] ,
		3 : [0.1666666666666665, 0.6666666666666665, 0.1666666666666665] ,
		4 : [0.0833333333333335, 0.4166666666666665, 0.4166666666666665, 0.0833333333333335] ,
		5 : [0.05, 0.2722222222, 0.35555555555, 0.2722222222, 0.05] ,
		6 : [0.033333333335, 0.1892374781, 0.2774291885, 0.2774291885, 0.1892374781, 0.033333333335] ,
		7 : [0.02380952381, 0.13841302365, 0.2158726906, 0.2438095238, 0.2158726906, 0.13841302365, 0.02380952381] ,
		8 : [0.017857142855, 0.10535211355, 0.1705613462, 0.2062293973, 0.2062293973, 0.1705613462, 0.10535211355, 0.017857142855] ,
		9 : [0.01388888889, 0.08274768075, 0.13726935625, 0.17321425545, 0.18575963715, 0.17321425545, 0.13726935625, 0.08274768075, 0.01388888889] ,
		10 : [0.01111111111, 0.0666529954, 0.11244467105, 0.1460213418, 0.16376988055, 0.16376988055, 0.1460213418, 0.11244467105, 0.0666529954, 0.01111111111] ,
	})
	
	L = ({
		2 : [0.0, 1.0] ,
		3 : [0.0, 0.5, 1.0] ,
		4 : [0.0, 0.2763932, 0.7236068, 1.0] ,
		5 : [0.0, 0.172673165, 0.5, 0.827326835, 1.0] ,
		6 : [0.0, 0.1174723381, 0.3573842418, 0.6426157582, 0.8825276620, 1.0] ,
		7 : [0.0, 0.0848880519, 0.2655756033, 0.5, 0.7344243967, 0.9151119481, 1.0] ,
		8 : [0.0000000000, 0.0641299258, 0.2041499093, 0.3953503911, 0.6046496090, 0.7958500907, 0.9358700743, 1.0000000000] ,
		9 : [0.0, 0.0501210023, 0.1614068603, 0.3184412681, 0.5, 0.6815587319, 0.8385931398, 0.9498789977, 1.0] ,
		10 : [0.0000000000, 0.0402330459, 0.1306130675, 0.2610375251, 0.4173605212, 0.5826394789, 0.7389624749, 0.8693869326, 0.9597669541, 1.0000000000] ,
	})
	
	@staticmethod
	def get_weights(np):
		if not np in beam_int_lobatto.W:
			raise Exception('invalid number of sections for Lobatto integration rule. min number = 2, max number = 10, given = {}'.format(np))
		return beam_int_lobatto.W[np]
		
	@staticmethod
	def get_locations(np):
		if not np in beam_int_lobatto.L:
			raise Exception('invalid number of sections for Lobatto integration rule. min number = 2, max number = 10, given = {}'.format(np))
		return beam_int_lobatto.L[np]
		
	@staticmethod
	def get_minIntPoints():
		return 2
	
	@staticmethod
	def get_maxIntPoints():
		return 10
		
	

class beam_int_legendre:
	W = ({
		1 : [1.0] ,
		2 : [0.5, 0.5] ,
		3 : [0.277777777777778, 0.4444444444444445, 0.277777777777778] ,
		4 : [0.173927422568727, 0.326072577431273, 0.326072577431273, 0.173927422568727] ,
		5 : [0.1184634425280945, 0.239314335249683, 0.2844444444444445, 0.239314335249683, 0.1184634425280945] ,
		6 : [0.085662246189585, 0.1803807865240695, 0.2339569672863455, 0.2339569672863455, 0.1803807865240695, 0.085662246189585] ,
		7 : [0.064742483084435, 0.1398526957446385, 0.1909150252525595, 0.2089795918367345, 0.1909150252525595, 0.1398526957446385, 0.064742483084435] ,
		8 : [0.050614268145188, 0.111190517226687, 0.1568533229389435, 0.181341891689181, 0.181341891689181, 0.1568533229389435, 0.111190517226687, 0.050614268145188] ,
		9 : [0.040637194180787, 0.0903240803474285, 0.1303053482014675, 0.1561735385200015, 0.16511967750063, 0.1561735385200015, 0.1303053482014675, 0.0903240803474285, 0.040637194180787] ,
		10 : [0.033335672154344, 0.0747256745752905, 0.109543181257991, 0.134633359654998, 0.1477621123573765, 0.1477621123573765, 0.134633359654998, 0.109543181257991, 0.0747256745752905, 0.033335672154344] ,
	})
	@staticmethod
	def get_weights(np):
		if not np in beam_int_legendre.W:
			raise Exception('invalid number of sections for Legendre integration rule. min number = 1, max number = 10, given = {}'.format(np))
		return beam_int_legendre.W[np]

class beam_int_radau:
	W = ({
		1 : [1.0] ,
		2 : [0.25, 0.75] ,
		3 : [0.1111111111, 0.512485826, 0.3764030627] ,
		4 : [0.0625, 0.32884431995, 0.3881934688, 0.22046221115] ,
		5 : [0.04, 0.22310390105, 0.31182652295, 0.2813560151, 0.14371356075] ,
		6 : [0.027777777775, 0.1598203766, 0.2426935942, 0.26046339155, 0.20845066715, 0.1007941926] ,
		7 : [0.020408163265, 0.1196137446, 0.1904749368, 0.2235549145, 0.2123518895, 0.1591021157, 0.07449423555] ,
		8 : [0.015625, 0.0926790774, 0.1520653103, 0.18825877265, 0.1957860837, 0.1735073978, 0.12482395065, 0.05725440735] ,
		9 : [0.01234567901, 0.0738270095, 0.1235946891, 0.1584218878, 0.17413650135, 0.16884698345, 0.14319334815, 0.100276649, 0.04535725246] ,
		10 : [0.01, 0.06014833525, 0.1021350659, 0.1340974189, 0.15292964385, 0.1567912286, 0.1453050824, 0.11959671585, 0.08218800635, 0.03680850274] ,
	})
	@staticmethod
	def get_weights(np):
		if not np in beam_int_radau.W:
			raise Exception('invalid number of sections for Radau integration rule. min number = 1, max number = 10, given = {}'.format(np))
		return beam_int_radau.W[np]

class beam_int_newton_cotes:
	W = ({
		2 : [0.5, 0.5] ,
		3 : [0.1666666666666665, 0.6666666666666665, 0.1666666666666665] ,
		4 : [0.125, 0.375, 0.375, 0.125] ,
		5 : [0.0777777778, 0.35555555555, 0.13333333335, 0.35555555555, 0.0777777778] ,
		6 : [0.0659722222, 0.26041666665, 0.1736111111, 0.1736111111, 0.26041666665, 0.0659722222] ,
		7 : [0.04880952381, 0.25714285715, 0.032142857145, 0.3238095238, 0.032142857145, 0.25714285715, 0.04880952381] ,
		8 : [0.04346064815, 0.2070023148, 0.0765625, 0.17297453705, 0.17297453705, 0.0765625, 0.2070023148, 0.04346064815] ,
		9 : [0.03488536155, 0.20768959435, -0.032733686065, 0.3702292769, -0.16014109345, 0.3702292769, -0.032733686065, 0.20768959435, 0.03488536155] ,
		10 : [0.031886160715, 0.17568080355, 0.01205357143, 0.21589285715, 0.06448660715, 0.06448660715, 0.21589285715, 0.01205357143, 0.17568080355, 0.031886160715] ,
	})
	@staticmethod
	def get_weights(np):
		if not np in beam_int_newton_cotes.W:
			raise Exception('invalid number of sections for Newton-Cotes integration rule. min number = 2, max number = 10, given = {}'.format(np))
		return beam_int_newton_cotes.W[np]

def _generate_trapezoidal(np):
	wti = 1.0/(np-1)
	wt = [wti]*np
	wt[0] = wt[np-1] = wti/2.0
	return wt
class beam_int_trapezoidal:
	W = ({
		2 :  _generate_trapezoidal(2 ),
		3 :  _generate_trapezoidal(3 ),
		4 :  _generate_trapezoidal(4 ),
		5 :  _generate_trapezoidal(5 ),
		6 :  _generate_trapezoidal(6 ),
		7 :  _generate_trapezoidal(7 ),
		8 :  _generate_trapezoidal(8 ),
		9 :  _generate_trapezoidal(9 ),
		10 : _generate_trapezoidal(10),
	})
	@staticmethod
	def get_weights(np):
		if np < 2:
			raise Exception('invalid number of sections for Trapezoidal integration rule. min number = 2, given = {}'.format(np))
		if not np in beam_int_trapezoidal.W:
			return _generate_trapezoidal(np)
		return beam_int_trapezoidal.W[np]

def _generate_composite_simpson(np):
	if (np < 1) or (np % 2 != 1):
		raise Exception('invalid number of sections for Composite Simpson integration rule. expected a positive odd number, given = {}'.format(np))
	'''
	note that this is different from the simpson rule in opensees... check
	it and comment it to the developers
	'''
	wt = [0.0]*np
	ni = np-1
	if ni == 0:
		wt[0] = 1.0
	else:
		h = 1.0/ni
		wt[0] = wt[np-1] = h/3.0
		for i in range(1,np,2):
			wt[i] = 4.0*h/3.0
		for i in range(2,np-1,2):
			wt[i] = 2.0*h/3.0
	return wt
class beam_int_composite_simpson:
	W = ({
		1 :  _generate_composite_simpson(1 ),
		3 :  _generate_composite_simpson(3 ),
		5 :  _generate_composite_simpson(5 ),
		7 :  _generate_composite_simpson(7 ),
		9 :  _generate_composite_simpson(9 ),
		11:  _generate_composite_simpson(11),
		13:  _generate_composite_simpson(13),
		15:  _generate_composite_simpson(15),
	})
	@staticmethod
	def get_weights(np):
		if not np in beam_int_composite_simpson.W:
			return _generate_composite_simpson(np)
		return beam_int_composite_simpson.W[np]

class integration_rule_registry:
	STANDARD_RULES = ({
		'Lobatto' : beam_int_lobatto, 
		'Legendre' : beam_int_legendre, 
		'Radau' : beam_int_radau, 
		'NewtonCotes' : beam_int_newton_cotes, 
		'Trapezoidal' : beam_int_trapezoidal, 
		'CompositeSimpson' : beam_int_composite_simpson,
	})

# if __name__ == '__main__':
	
	# for rule_name, rule in integration_rule_registry.RULES.items():
		# print('RULE:',rule_name)
		# for k,v in rule.W.items():
			# sv = 0.0
			# for x in v:
				# sv += x
			# print('   [', k, ']', v, '(', sv, ')')
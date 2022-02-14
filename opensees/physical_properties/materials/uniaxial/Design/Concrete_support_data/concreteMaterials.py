from math import log

# EN1992 - Eurocode 2
standardConcreteEC1992 = {
	'12': {'name': 'C12', 'fck': 12, 'Rck':  15}, # 'fcm': 20, 'fctm': 1.6, 'fctk005': 1.1, 'ftk095': 2.0, 'Ecm': 27e3, 'eps_c1': 1.8e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'16': {'name': 'C16', 'fck': 16, 'Rck':  20}, # 'fcm': 24, 'fctm': 1.9, 'fctk005': 1.3, 'ftk095': 2.5, 'Ecm': 29e3, 'eps_c1': 1.9e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'20': {'name': 'C20', 'fck': 20, 'Rck':  25}, # 'fcm': 28, 'fctm': 2.2, 'fctk005': 1.5, 'ftk095': 2.9, 'Ecm': 30e3, 'eps_c1': 2.0e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'25': {'name': 'C25', 'fck': 25, 'Rck':  30}, # 'fcm': 33, 'fctm': 2.6, 'fctk005': 1.8, 'ftk095': 3.3, 'Ecm': 31e3, 'eps_c1': 2.1e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'30': {'name': 'C30', 'fck': 30, 'Rck':  37}, # 'fcm': 38, 'fctm': 2.9, 'fctk005': 2.0, 'ftk095': 3.8, 'Ecm': 33e3, 'eps_c1': 2.2e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'35': {'name': 'C35', 'fck': 35, 'Rck':  45}, # 'fcm': 43, 'fctm': 3.2, 'fctk005': 2.2, 'ftk095': 4.2, 'Ecm': 34e3, 'eps_c1': 2.25e-3, 'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'40': {'name': 'C40', 'fck': 40, 'Rck':  50}, # 'fcm': 48, 'fctm': 3.5, 'fctk005': 2.5, 'ftk095': 4.6, 'Ecm': 35e3, 'eps_c1': 2.3e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'45': {'name': 'C45', 'fck': 45, 'Rck':  55}, # 'fcm': 53, 'fctm': 3.8, 'fctk005': 2.7, 'ftk095': 4.9, 'Ecm': 36e3, 'eps_c1': 2.4e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'50': {'name': 'C50', 'fck': 50, 'Rck':  60}, # 'fcm': 58, 'fctm': 4.1, 'fctk005': 2.9, 'ftk095': 5.3, 'Ecm': 37e3, 'eps_c1': 2.45e-3, 'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'55': {'name': 'C55', 'fck': 55, 'Rck':  67}, # 'fcm': 63, 'fctm': 4.2, 'fctk005': 3.0, 'ftk095': 5.5, 'Ecm': 38e3, 'eps_c1': 2.5e-3,  'eps_cu1': 3.2e-3, 'eps_c2': 2.2e-3, 'eps_cu2': 3.1e-3, 'n': 1.75, 'eps_c3': 1.8e-3,  'eps_cu3': 3.1e-3},
	'60': {'name': 'C60', 'fck': 60, 'Rck':  75}, # 'fcm': 68, 'fctm': 4.4, 'fctk005': 3.1, 'ftk095': 5.7, 'Ecm': 39e3, 'eps_c1': 2.6e-3,  'eps_cu1': 3.0e-3, 'eps_c2': 2.3e-3, 'eps_cu2': 2.9e-3, 'n': 1.6,  'eps_c3': 1.9e-3,  'eps_cu3': 2.9e-3},
	'70': {'name': 'C70', 'fck': 70, 'Rck':  85}, # 'fcm': 78, 'fctm': 4.6, 'fctk005': 3.2, 'ftk095': 6.0, 'Ecm': 41e3, 'eps_c1': 2.7e-3,  'eps_cu1': 2.8e-3, 'eps_c2': 2.4e-3, 'eps_cu2': 2.7e-3, 'n': 1.45, 'eps_c3': 2.0e-3,  'eps_cu3': 2.7e-3},
	'80': {'name': 'C80', 'fck': 80, 'Rck':  95}, # 'fcm': 88, 'fctm': 4.8, 'fctk005': 3.4, 'ftk095': 6.3, 'Ecm': 42e3, 'eps_c1': 2.8e-3,  'eps_cu1': 2.8e-3, 'eps_c2': 2.5e-3, 'eps_cu2': 2.6e-3, 'n': 1.4,  'eps_c3': 2.2e-3,  'eps_cu3': 2.6e-3},
	'90': {'name': 'C90', 'fck': 90, 'Rck': 105}, # 'fcm': 98, 'fctm': 5.0, 'fctk005': 3.5, 'ftk095': 6.6, 'Ecm': 44e3, 'eps_c1': 2.8e-3,  'eps_cu1': 2.8e-3, 'eps_c2': 2.6e-3, 'eps_cu2': 2.6e-3, 'n': 1.4,  'eps_c3': 2.3e-3,  'eps_cu3': 2.6e-3},
	}

class concreteEC1992:
	def __init__(self,strength):
		# Strength is the string representing the stength class of concrete. e.g.: "<c20" means fck = 20 MPa
		self.strengthClass = strength
		self.update()
		
	def set_strength_class(self, strength ):
		# strength is a value in Mpa
		self.strengthClass = '{}'.format(strength)
		self.update()
		
	def _interpolate(self, quantity, strength1, strength2):
		# Interpolate the selected quantity (e.g. "Rck") between strength classes 1 and 2
		return (float(self.strengthClass) - float(strength1))*(standardConcreteEC1992[strength2][quantity]-standardConcreteEC1992[strength1][quantity])/(float(strength2)-float(strength1))+standardConcreteEC1992[strength1][quantity]
		
	def update(self ):
		if (standardConcreteEC1992.get(self.strengthClass) is not None):
			values = standardConcreteEC1992.get(self.strengthClass)
			self.fck = values['fck']
			self.Rck = values['Rck']
		else:
			self.fck = float(self.strengthClass)
			# check strength within boundaries
			if self.fck < 16 or self.fck > 90:
				print("Error. The strength class for structural concrete should be higher than 16 MPa and lower than 90 MPa. Check your data")
				return
			# Compute Rck as linear regression
			class1 = 12
			class2 = 90
			for s in standardConcreteEC1992:
				if (float(s) <= float(self.strengthClass)) and (float(s) > float(class1)):
					class1 = s
				if (float(s) > float(self.strengthClass)) and (float(s) < float(class2)):
					class2 = s
					break
			self.Rck = self._interpolate('Rck',class1, class2)
		self.fcm = self.fck + 8
		self.fctm = 0.3*(self.fck)**(2.0/3) if self.fck <= 50 else 2.12 * log(1+(self.fcm/10.0))
		self.fctk005 = 0.7 * self.fctm
		self.fctk095 = 1.3 * self.fctm
		self.Ecm = 22e3 * (self.fcm/10.0)**0.3
		self.eps_c1 = 1e-3 * min(0.7*self.fcm**0.31,2.8)
		self.eps_cu1 = 3.5e-3 if self.fck < 50 else (2.8+27*((98-self.fcm)/100)**4.0)*1e-3
		self.eps_c2 = 2.0e-3 if self.fck < 50 else (2.0 + 0.085*(self.fck-50)**0.53)*1e-3
		self.eps_cu2 = 3.5e-3 if self.fck < 50 else (2.6+35*((90-self.fck)/100)**4.0)*1e-3
		self.n = 2 if self.fck < 50 else 1.4+23.4*((90-self.fck)/100)**4.0
		self.eps_c3 = 1.75e-3 if self.fck < 50 else (1.75 + 0.55*(self.fck-50)/40)*1e-3
		self.eps_cu3 = 3.5e-3 if self.fck < 50 else (2.6+35*((90-self.fck)/100)**4.0)*1e-3
		
	def __str__(self):
		return 'concreteNTC2018 Material. Strength class {}.\nfck = {}\nRck = {}\nfcm = {}\nfctm = {}\nfctk005 = {}\nfctk095 = {}\nEcm = {}\neps_c1 = {}\neps_cu1 = {}\neps_c2 = {}\neps_cu2 = {}\nn = {}\neps_c3 = {}\neps_cu3 = {}'.format(self.strengthClass,self.fck, self.Rck, self.fcm, self.fctm, self.fctk005, self.fctk095, self.Ecm, self.eps_c1, self.eps_cu1, self.eps_c2, self.eps_cu2, self.n, self.eps_c3, self.eps_cu3)
		
	def __repr__(self):
		return 'concreteMaterials.concreteEC1992({})'.format(self.strengthClass)
		
# NTC2018 - Norme tecniche per le costruzioni 2018
standardConcreteNTC2018 = {
	'12' : {'name':  'C12/15', 'fck': 12, 'Rck':  15},# 'fcm': 20, 'fctm': 1.6, 'fctk005': 1.1, 'ftk095': 2.0, 'Ecm': 27e3, 'eps_c1': 1.8e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'16' : {'name':  'C16/20', 'fck': 16, 'Rck':  20},# 'fcm': 24, 'fctm': 1.9, 'fctk005': 1.3, 'ftk095': 2.5, 'Ecm': 29e3, 'eps_c1': 1.9e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'20' : {'name':  'C20/25', 'fck': 20, 'Rck':  25},# 'fcm': 28, 'fctm': 2.2, 'fctk005': 1.5, 'ftk095': 2.9, 'Ecm': 30e3, 'eps_c1': 2.0e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'25' : {'name':  'C25/30', 'fck': 25, 'Rck':  30},# 'fcm': 33, 'fctm': 2.6, 'fctk005': 1.8, 'ftk095': 3.3, 'Ecm': 31e3, 'eps_c1': 2.1e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'28' : {'name':  'C28/35', 'fck': 28, 'Rck':  35},# 'fcm': 33, 'fctm': 2.6, 'fctk005': 1.8, 'ftk095': 3.3, 'Ecm': 31e3, 'eps_c1': 2.1e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'30' : {'name':  'C30/37', 'fck': 30, 'Rck':  37},# 'fcm': 38, 'fctm': 2.9, 'fctk005': 2.0, 'ftk095': 3.8, 'Ecm': 33e3, 'eps_c1': 2.2e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'32' : {'name':  'C32/40', 'fck': 32, 'Rck':  40},# 'fcm': 38, 'fctm': 2.9, 'fctk005': 2.0, 'ftk095': 3.8, 'Ecm': 33e3, 'eps_c1': 2.2e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'35' : {'name':  'C35/45', 'fck': 35, 'Rck':  45},# 'fcm': 43, 'fctm': 3.2, 'fctk005': 2.2, 'ftk095': 4.2, 'Ecm': 34e3, 'eps_c1': 2.25e-3, 'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'40' : {'name':  'C40/50', 'fck': 40, 'Rck':  50},# 'fcm': 48, 'fctm': 3.5, 'fctk005': 2.5, 'ftk095': 4.6, 'Ecm': 35e3, 'eps_c1': 2.3e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'45' : {'name':  'C45/55', 'fck': 45, 'Rck':  55},# 'fcm': 53, 'fctm': 3.8, 'fctk005': 2.7, 'ftk095': 4.9, 'Ecm': 36e3, 'eps_c1': 2.4e-3,  'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'50' : {'name':  'C50/60', 'fck': 50, 'Rck':  60},# 'fcm': 58, 'fctm': 4.1, 'fctk005': 2.9, 'ftk095': 5.3, 'Ecm': 37e3, 'eps_c1': 2.45e-3, 'eps_cu1': 3.5e-3, 'eps_c2': 2.0e-3, 'eps_cu2': 3.5e-3, 'n': 2.0,  'eps_c3': 1.75e-3, 'eps_cu3': 3.5e-3},
	'55' : {'name':  'C55/67', 'fck': 55, 'Rck':  67},# 'fcm': 63, 'fctm': 4.2, 'fctk005': 3.0, 'ftk095': 5.5, 'Ecm': 38e3, 'eps_c1': 2.5e-3,  'eps_cu1': 3.2e-3, 'eps_c2': 2.2e-3, 'eps_cu2': 3.1e-3, 'n': 1.75, 'eps_c3': 1.8e-3,  'eps_cu3': 3.1e-3},
	'60' : {'name':  'C60/75', 'fck': 60, 'Rck':  75},# 'fcm': 68, 'fctm': 4.4, 'fctk005': 3.1, 'ftk095': 5.7, 'Ecm': 39e3, 'eps_c1': 2.6e-3,  'eps_cu1': 3.0e-3, 'eps_c2': 2.3e-3, 'eps_cu2': 2.9e-3, 'n': 1.6,  'eps_c3': 1.9e-3,  'eps_cu3': 2.9e-3},
	'70' : {'name':  'C70/85', 'fck': 70, 'Rck':  85},# 'fcm': 78, 'fctm': 4.6, 'fctk005': 3.2, 'ftk095': 6.0, 'Ecm': 41e3, 'eps_c1': 2.7e-3,  'eps_cu1': 2.8e-3, 'eps_c2': 2.4e-3, 'eps_cu2': 2.7e-3, 'n': 1.45, 'eps_c3': 2.0e-3,  'eps_cu3': 2.7e-3},
	'80' : {'name':  'C80/95', 'fck': 80, 'Rck':  95},# 'fcm': 88, 'fctm': 4.8, 'fctk005': 3.4, 'ftk095': 6.3, 'Ecm': 42e3, 'eps_c1': 2.8e-3,  'eps_cu1': 2.8e-3, 'eps_c2': 2.5e-3, 'eps_cu2': 2.6e-3, 'n': 1.4,  'eps_c3': 2.2e-3,  'eps_cu3': 2.6e-3},
	'90' : {'name': 'C90/105', 'fck': 90, 'Rck': 105},# 'fcm': 98, 'fctm': 5.0, 'fctk005': 3.5, 'ftk095': 6.6, 'Ecm': 44e3, 'eps_c1': 2.8e-3,  'eps_cu1': 2.8e-3, 'eps_c2': 2.6e-3, 'eps_cu2': 2.6e-3, 'n': 1.4,  'eps_c3': 2.3e-3,  'eps_cu3': 2.6e-3},
	}

class concreteNTC2018:
	def __init__(self,strength):
		# Strength is the string representing the stength class of concrete. e.g.: "<c20" means fck = 20 MPa
		self.strengthClass = strength
		self.update()
		
	def set_strength_class(self, strength ):
		self.strengthClass = strength
		self.update()
		
	def _interpolate(self, quantity, strength1, strength2):
		# Interpolate the selected quantity (e.g. "Rck") between strength classes 1 and 2
		return (float(self.strengthClass) - float(strength1))*(standardConcreteNTC2018[strength2][quantity]-standardConcreteNTC2018[strength1][quantity])/(float(strength2)-float(strength1))+standardConcreteNTC2018[strength1][quantity]
		
	def update(self ):
		if (standardConcreteNTC2018.get(self.strengthClass) is not None):
			values = standardConcreteNTC2018.get(self.strengthClass)
			self.fck = values['fck']
			self.Rck = values['Rck']
		else:
			self.fck = float(self.strengthClass)
			# check strength within boundaries
			if self.fck < 16 or self.fck > 90:
				print("Error. The strength class for structural concrete should be higher than 16 MPa and lower than 90 MPa. Check your data")
				print('Given {}'.format(self.strengthClass))
				return
			# Compute Rck as linear regression
			class1 = 12
			class2 = 90
			for s in standardConcreteNTC2018:
				if (float(s) <= float(self.strengthClass)) and (float(s) > float(class1)):
					class1 = s
				if (float(s) > float(self.strengthClass)) and (float(s) < float(class2)):
					class2 = s
					break
			self.Rck = self._interpolate('Rck',class1, class2)
		self.fcm = self.fck + 8
		self.fctm = 0.3*(self.fck)**(2.0/3) if self.fck <= 50 else 2.12 * log(1+(self.fcm/10.0))
		self.fctk005 = 0.7 * self.fctm
		self.fctk095 = 1.3 * self.fctm
		self.Ecm = 22e3 * (self.fcm/10.0)**0.3
		# self.ec1 = 1e-3 * min(0.7*self.fcm**0.31,2.8)
		# self.ecu1 = 3.5e-3 if self.fck < 50 else (2.8+27*((98-self.fcm)/100)**4.0)*1e-3
		self.eps_c2 = 2.0e-3 if self.fck < 50 else (2.0 + 0.085*(self.fck-50)**0.53)*1e-3
		self.eps_cu2 = 3.5e-3 if self.fck < 50 else (2.6+35*((90-self.fck)/100)**4.0)*1e-3
		self.eps_c3 = 1.75e-3 if self.fck < 50 else (1.75 + 0.55*(self.fck-50)/40)*1e-3
		self.eps_cu3 = 3.5e-3 if self.fck < 50 else (2.6+35*((90-self.fck)/100)**4.0)*1e-3
		
	def __str__(self):
		return 'concreteNTC2018 Material. Strength class {}.\nfck = {}\nRck = {}\nfcm = {}\nfctm = {}\nfctk005 = {}\nfctk095 = {}\nEcm = {}\neps_c2 = {}\neps_cu2 = {}\neps_c3 = {}\neps_cu3 = {}'.format(self.strengthClass,self.fck, self.Rck, self.fcm, self.fctm, self.fctk005, self.fctk095, self.Ecm, self.eps_c2, self.eps_cu2, self.eps_c3, self.eps_cu3)
		
	def __repr__(self):
		return 'concreteMaterials.concreteNTC2018({})'.format(self.strengthClass)


class concreteStandardFactory:
	## A static dictionary that maps class names to class types
	supportedTypes = {
		"EN1992" : [standardConcreteEC1992, concreteEC1992],
		"NTC2018": [standardConcreteNTC2018, concreteNTC2018],
		}
	
	## Gives a list of names of all supported strain history types
	@staticmethod
	def getTypes():
		return concreteStandardFactory.supportedTypes.keys()
	
	## Constructs the required type given its name.
	# @note If the given name is not among the ones given by @ref getTypes
	# and Exception will be thrown
	@staticmethod
	def make(standardName):
		if not standardName in concreteStandardFactory.supportedTypes.keys():
			raise Exception('The given standard "{}" is not supported by the concreteStandardFactory'.format(standardName))
		className = concreteStandardFactory.supportedTypes[standardName][1]
		standardValues = concreteStandardFactory.supportedTypes[standardName][0]
		return [standardValues, className]
		



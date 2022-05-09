
class utils:
	indent ='\t'
	def nIndent(n):
		return(n*'\t')

class element_nodal_dims:
	def __init__(self, nodes, dims):
		self.nodes = nodes
		self.dims = dims

class node_with_age:
	def __init__(self, _id, _age):
		self.id = _id
		self.age = _age

class mpco_cdata_utils_t:
	'''
	This class is used to store information about automatic changes in the model
	during the writing of input file, thus not in STKO.
	- For example, in the BeamWithShearHinge, where the element from STKO is split
	  into sub-elements.
	'''
	def __init__(self):
		# a flag that tells if something has been remapped
		self.done = False
		# remapped elements
		# KEY = source element in STKO, VALUE = list of auto-generated elements
		self.mapped_elements = {}
		# remapped physical properties
		# should be a dictionary of dictionaries
		# DATA = dict( KEY = WrapperID (source material) : VALUE =  SUB_DATA (all elements with source materials remapped to new materials )
		# SUB_DATA = dict( KEY = EleID : VALUE = new_phys_prop_id )
		self.mapped_physical_properties = {}
		
	def mapElement(self, source, other):
		if source in self.mapped_elements:
			values = self.mapped_elements[source]
		else:
			values = []
			self.mapped_elements[source] = values
		if not other in values:
			values.append(other)
			self.done = True
	
	def mapPhysicalProperties(self, source_id, ele_id, new_id):
		if source_id in self.mapped_physical_properties:
			value = self.mapped_physical_properties[source_id]
		else:
			value = {}
			self.mapped_physical_properties[source_id] = value
		value[ele_id] = new_id
		self.done = True

class mpco_cdata_ele_info_reader:
	def __init__(self, s):
		self.s = s
		self.i = 0
		self.j = 0
	def read(self):
		self.j = self.s.find(' ', self.i)
		res = self.s[self.i : self.j]
		self.i = self.j + 1
		return res
	def read_int(self):
		return int(self.read())
	def read_str(self):
		n = self.read_int()
		self.j = self.i + n
		res = self.s[self.i : self.j]
		self.i = self.j + 1
		return res
	def read_all(self):
		ele_id = self.read_int()
		geom_id = self.read_int()
		geom_name = self.read_str()
		subgeom_id = self.read_int()
		type = self.read()
		ppid = self.read_int()
		ppname = self.read_str()
		epid = self.read_int()
		epname = self.read_str()
		# the first item is kept as string... so it does not mess up the parser... startswith!
		return [str(ele_id), geom_id, geom_name, subgeom_id, type, ppid, ppname, epid, epname]

class process_info:
	def __init__(self):
		'''
		the current output directory where the opensees input files are to be written
		'''
		self.out_dir = None
		'''
		reference to the current output file
		'''
		self.out_file = None
		'''
		utils for monitor
		'''
		self.monitor = False
		'''
		utils for indentation
		'''
		self.indent = ''
		self.tabIndent = '\t'
		'''
		the following data are required for the writeTcl method 
		in each component
		'''
		self.elem = None
		self.definition = None
		self.phys_prop = None
		self.elem_prop = None
		self.condition = None
		self.analysis_step = None
		'''
		a global variable to see if it is the first random Variable
		'''
		self.firstRandomVariable = False
		'''
		the following data are required for mapping and tracking the
		current NDM/NDF pair
		'''
		self.ndm = 0
		self.ndf = 0
		self.ndm_ndf_per_process = [[0,0]]
		'''
		the following data are required for writing partioned TCL files
		for OpenSees MP
		'''
		self.process_id = 0
		self.process_count = 1
		'''
		mapping for models based on nodes/elements spatial dimension {node_id: (ndm, ndf)}
		'''
		self.node_to_model_map = {}
		self.element_nodal_dims_list = []
		'''
		inverse of node_to_model_map
		'''
		self.inv_map = {}
		'''
		mapping for mass and node {node_id: mass}
		'''
		self.mass_to_node_map = {}
		""" 
		utility ...
		"""
		self.currentDescription = ''
		"""
		the index used for extra nodes and elements (not in STKO model) and definitions and conditions
		"""
		self.next_node_id = 1
		self.next_elem_id = 1
		self.next_physicalProperties_id = 1
		self.next_definitions_id = 1
		self.next_conditions_id = 1
		self.next_analysis_step_id = 1
		"""
		all lagrangian nodes are written outside the model bounding box
		use these coordinates
		"""
		self.lagrangian_node_xyz = [0.0, 0.0, 0.0]
		'''
		a dictionary that maps a element id (key) to an instance of auto_generated_element_data.
		some elements may need to produce auto-generated data like new elements that are not in STKO.
		we need to keep track of them for different purposes.
		If one wants to know if element 5 generated some extra data, one can do:
		if 5 in tcl_input.auto_generated_element_data_map:
			auto_gen_data_for_elem_5 = tcl_input.auto_generated_element_data_map[5]
		'''
		self.auto_generated_element_data_map = {}
		'''
		mapping for tag 'add to parameter' and tag_parameter {id_addToParameter: (tag_parameter)}
		tag parameter for command parameter-addToParameter and updateParameter
		'''
		self.map_tag_add_to_parameter_id_partition = {}
		self.tag_parameter = 1
		'''
		data to support staged models.
		a set of nodes and elements as a subset of the entire mesh.
		if None, then we need to write the entire model.
		otherwise it should be a set or nodes/elements of the current subset
		'''
		self.loaded_node_subset = set()
		self.loaded_element_subset = set()
		self.node_subset = None
		self.element_subset = None
		'''
		custom map of cusotm data
		'''
		self.custom_data = {}
		'''
		cdata utilities
		'''
		self.mpco_cdata_utils = mpco_cdata_utils_t()
		
	def setProcessCount(self, pc):
		'''
		a function that sets the number of processes.
		it should be called only once at the beginning of the write method
		'''
		_pc = max(1, pc)
		if _pc != self.process_count:
			self.process_count = _pc
			self.ndm_ndf_per_process = []
			for i in range(_pc):
				self.ndm_ndf_per_process.append([0,0])
		
	def setProcessId(self, pid):
		'''
		sets the current process id.
		'''
		if pid < 0 or pid >= self.process_count:
			raise Exception('PID out of range')
		if pid != self.process_id:
			'''
			if the current process id is different fromt the previous one,
			then we store the ndm-ndf pair assciated with the current process id
			'''
			self.process_id = pid
			current_ndm_ndf_pair = self.ndm_ndf_per_process[self.process_id]
			self.ndm = current_ndm_ndf_pair[0]
			self.ndf = current_ndm_ndf_pair[1]
		
	def updateModelBuilder(self, _ndm, _ndf):
		'''
		update model builder, needed for some elements/materials
		'''
		if _ndf == 32:
			_ndf = 2
		if _ndf == 33:
			_ndf = 3
		if (self.ndm != _ndm) or (self.ndf != _ndf):
			self.ndm = _ndm
			self.ndf = _ndf
			self.out_file.write('\nmodel basic -ndm {} -ndf {}\n'.format(self.ndm, self.ndf))
			self.out_file.write('# source definitions\n')
			self.out_file.write('source definitions.tcl\n')
			self.currentDescription = ''
			
	def get_double_formatter(self):
		return lambda arg: format(arg, '.10g')
	
	def updateMpcoCdataFiles(self):
		import os
		'''
		some elements might have been generated automatically
		or some phys_prop remapped...
		'''
		if not self.mpco_cdata_utils.done:
			return
		print('Updating MPCO CDATA files in "{}"'.format(self.out_dir))
		#
		# some common data
		UNKNOWN = -1
		LOCAL_AXES = 0
		SECTION_OFFSET = 1
		BEAM_PROFILE_ASSIGNMENT = 2
		ELEMENT_INFO = 3
		command_names = {
			LOCAL_AXES :'*LOCAL_AXES',
			SECTION_OFFSET : '*SECTION_OFFSET',
			BEAM_PROFILE_ASSIGNMENT : '*BEAM_PROFILE_ASSIGNMENT',
			ELEMENT_INFO : '*ELEMENT_INFO'
		}
		command_names_inv = {}
		for k,v in command_names.items():
			command_names_inv[v] = k
		#
		# find all files
		for file in os.listdir(self.out_dir):
			if file.endswith('mpco.cdata'):
				print('... Updating file: "{}"'.format(file))
				with open('{}/{}'.format(self.out_dir, file), 'r+') as f:
					#
					# read lines, remove comments and empty lines
					contents = [i for i in f.read().split('\n') if len(i) > 0 and not i[0].startswith('#')]
					# split each line in words (watch out for ELEMENT_INFO!)
					is_ele_info = False
					lines = []
					for line in contents:
						if line.startswith('*'):
							is_ele_info = False
							if line.startswith('*ELEMENT_INFO'):
								is_ele_info = True
							lines.append([line])
						else:
							if is_ele_info:
								# parse element info where names can contain white spaces...
								lines.append(mpco_cdata_ele_info_reader(line).read_all())
							else:
								# split with white char
								lines.append([i.strip() for i in line.split(' ') if i])
					#lines = [ [i.strip() for i in line.split(' ') if i] for line in lines if line ]
					#
					# 1. parse and find all commands that need to be added for remapped elements.
					#    Note: old lines are not removed, since in STKO the new lines overrides the old one
					#          when using maps...
					command_words = {
						LOCAL_AXES : [],
						SECTION_OFFSET : [],
						BEAM_PROFILE_ASSIGNMENT : []
					}
					pars = UNKNOWN
					for words in lines:
						if len(words) == 0:
							continue
						w0 = words[0]
						if w0.startswith('*'):
							pars = command_names_inv.get(w0, UNKNOWN)
						else:
							if pars == ELEMENT_INFO or pars == BEAM_PROFILE_ASSIGNMENT or pars == LOCAL_AXES:
								source_id = int(w0)
								if source_id in self.mpco_cdata_utils.mapped_elements:
									mapped = self.mpco_cdata_utils.mapped_elements[source_id]
									if pars in command_words:
										where = command_words[pars]
										for i_mapped in mapped:
											new_words = words[:]
											new_words[0] = i_mapped
											where.append(new_words)
					first_done = False
					for k, v in command_words.items():
						if len(v) > 0:
							if not first_done:
								f.write('\n#NEW DATA FOR AUTO-GENERATED ELEMENTS\n')
								first_done = True
							f.write('{}\n'.format(command_names[k]))
							for iv in v:
								f.write(' '.join([str(iw) for iw in iv]))
								f.write('\n')
					#
					# 2. add lines of ELEMENT_INFO for remapped physical properties
					pars = UNKNOWN
					mapped_lines = []
					for words in lines:
						if len(words) == 0:
							continue
						w0 = words[0]
						if w0.startswith('*'):
							pars = command_names_inv.get(w0, UNKNOWN)
						else:
							if pars == ELEMENT_INFO:
								# (ele_id, geom_id, geom_name, subgeom_id, type, ppid, ppname, epid, epname)
								ppid = words[5] # original physical property id
								values = self.mpco_cdata_utils.mapped_physical_properties.get(ppid, None)
								if values:
									ele_id = int(words[0]) # it is a string from the read_all !
									if ele_id in values:
										new_ppid = values[ele_id]
										words[5] = new_ppid
										mapped_lines.append(words)
					if len(mapped_lines) > 0:
						f.write(
							'\n#Begin ELEMENT INFO data (FOR AUTO-REMAPPED PROPERTIES).\n'
							'#For each element in the mesh (or a subset of them) the following data is provided:\n'
							'#ELEM_ID GEOM (LENGTH+)GEOMNAME SUBGEOM TYPE PPID (LENGTH+)PPNAME EPID (LENGTH+)EPNAME\n'
							'#Where: #ELEM_ID = the id of the element\n'
							'#GEOM = the parent geometry id (0 if none)\n'
							'#GEOMNAME = the parent geometry name\n'
							'#SUBGEOM = the 0-based index of the sub-geometry\n'
							'#TYPE = the type of the subgeometry\n'
							'*ELEMENT_INFO\n'
							)
						for v in mapped_lines:
							f.write('{} {} {} {} {} {} {} {} {} {} {} {}\n'.format(
								v[0], v[1], len(v[2]), v[2], v[3], v[4], v[5], len(v[6]), v[6], v[7], len(v[8]), v[8]
								))

class auto_generated_element_data:
	def __init__(self):
		self.elements = []
		# an autogenerated element is not in STKO. so we may need to store its connectivity
		self.elements_connectivity = []
	def __repr__(self):
		return ','.join(['<', 'E:', str(self.elements), '>'])
	def __str__(self):
		return '\n'.join(['auto generated data info:', 'elements:', str(self.elements)])
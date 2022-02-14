import importlib
import opensees.utils.tcl_input as tclin
import PyMpc
import PyMpc.App

class _remapper_t:
	def __init__(self, pinfo):
		self.doc = PyMpc.App.caeDocument()
		self.pp_data = pinfo.mpco_cdata_utils.mapped_physical_properties
		if len(self.pp_data) == 0:
			self.pp_data = None
		self.pp_sub_data = None
		self.pp_original_id = -1
	def set_source_phys_prop(self, p):
		self.pp_sub_data = None
		self.pp_original_id = -1
		if self.pp_data:
			if p:
				self.pp_sub_data = self.pp_data.get(p.id, None)
				self.pp_original_id = p.id
	def remap_phys_prop(self, p, ele_id):
		if self.pp_sub_data:
			if p:
				new_id = self.pp_sub_data.get(ele_id, -1)
				if new_id != -1:
					p.id = new_id
				else:
					p.id = self.pp_original_id
	def reset_phys_prop(self, p):
		if self.pp_sub_data:
			if p:
				p.id = self.pp_original_id

def __write_geom_domain_partition(partition_data, pinfo, domain_collection, phys_prop_asn_on, elem_prop_asn_on):
	# create remapper
	remapper = _remapper_t(pinfo)
	# for each domain (i.e. for each subshape of geom)
	for domain_id in range(len(domain_collection)):
		domain = domain_collection[domain_id]
		# get physical and element property assigned to this domain
		phys_prop = phys_prop_asn_on[domain_id]
		elem_prop = elem_prop_asn_on[domain_id]
		# begin remapper with new source
		remapper.set_source_phys_prop(phys_prop)
		# a null element property is not and error, it means: don't write this element
		# (for example boundary elements)
		# we don't do any check on the phys_prop prop, it's up to the element formulation to check
		# whether it should be non-null
		if(elem_prop is None):
			continue
		# get elem formulation module
		elem_xobj = elem_prop.XObject
		if(elem_xobj is None):
			raise Exception('null XObject in element property object')
		elem_module_name = 'opensees.element_properties.{}.{}'.format(elem_xobj.Xnamespace, elem_xobj.name)
		elem_module = importlib.import_module(elem_module_name)
		if not hasattr(elem_module, 'writeTcl'):
			continue
		pinfo.phys_prop = phys_prop
		pinfo.elem_prop = elem_prop
		# split domain elements by partition
		per_part_elements = [[] for i in range(len(partition_data.partitions))]
		for elem in domain.elements:
			if (pinfo.element_subset is not None) and (elem.id not in pinfo.element_subset):
				continue # skip it in case of staged models if not in current stage
			per_part_elements[partition_data.elementPartition(elem.id)].append(elem)
		# write elements grouped by partitions
		for processor_id in range(len(partition_data.partitions)):
			part_elements = per_part_elements[processor_id]
			if(len(part_elements) == 0):
				continue
			# set process id
			pinfo.setProcessId(processor_id)
			# open process scope
			pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', processor_id, '} {'))
			# write in process scope
			for elem in part_elements:
				try:
					# remap
					remapper.remap_phys_prop(phys_prop, elem.id)
					pinfo.elem = elem
					elem_module.writeTcl(pinfo)
				finally:
					remapper.reset_phys_prop(phys_prop)
				pinfo.loaded_element_subset.add(elem.id) # mark as written
				PyMpc.App.monitor().sendAutoIncrement()
			# close process scope
			pinfo.out_file.write('{}{}\n'.format(pinfo.indent, '}'))
		pinfo.setProcessId(0) # back to default

def write_geom_partition(doc, pinfo, element_file):
	PyMpc.App.monitor().sendMessage('write geometry...')
	# for each geometry ...
	for geom_id, geom in doc.geometries.items():
		# get the mesh of this geometry
		mesh_of_geom = doc.mesh.meshedGeometries[geom_id]
		# get physical and element property assignments
		phys_prop_asn = geom.physicalPropertyAssignment
		elem_prop_asn = geom.elementPropertyAssignment
		# process all subdomains
		__write_geom_domain_partition(doc.mesh.partitionData, pinfo, mesh_of_geom.edges,  phys_prop_asn.onEdges, elem_prop_asn.onEdges)
		__write_geom_domain_partition(doc.mesh.partitionData, pinfo, mesh_of_geom.faces,  phys_prop_asn.onFaces, elem_prop_asn.onFaces)
		__write_geom_domain_partition(doc.mesh.partitionData, pinfo, mesh_of_geom.solids, phys_prop_asn.onSolids, elem_prop_asn.onSolids)

def __write_geom_domain(pinfo, domain_collection, phys_prop_asn_on, elem_prop_asn_on):
	# create remapper
	remapper = _remapper_t(pinfo)
	# for each domain (i.e. for each subshape of geom)
	for domain_id in range(len(domain_collection)):
		domain = domain_collection[domain_id]
		# get physical and element property assigned to this domain
		phys_prop = phys_prop_asn_on[domain_id]
		elem_prop = elem_prop_asn_on[domain_id]
		# begin remapper with new source
		remapper.set_source_phys_prop(phys_prop)
		# a null element property is not and error, it means: don't write this element
		# (for example boundary elements)
		# we don't do any check on the phys_prop prop, it's up to the element formulation to check
		# whether it should be non-null
		if(elem_prop is None):
			continue
		# get elem formulation module
		elem_xobj = elem_prop.XObject
		if(elem_xobj is None):
			raise Exception('null XObject in element property object')
		elem_module_name = 'opensees.element_properties.{}.{}'.format(elem_xobj.Xnamespace, elem_xobj.name)
		elem_module = importlib.import_module(elem_module_name)
		if not hasattr(elem_module, 'writeTcl'):
			continue
		pinfo.phys_prop = phys_prop
		pinfo.elem_prop = elem_prop
		for elem in domain.elements:
			if (pinfo.element_subset is not None) and (elem.id not in pinfo.element_subset):
				continue # skip it in case of staged models if not in current stage
			try:
				# remap
				remapper.remap_phys_prop(phys_prop, elem.id)
				pinfo.elem = elem
				elem_module.writeTcl(pinfo)
			finally:
				remapper.reset_phys_prop(phys_prop)
			pinfo.loaded_element_subset.add(elem.id) # mark as written
			PyMpc.App.monitor().sendAutoIncrement()

def write_geom(doc, pinfo):
	PyMpc.App.monitor().sendMessage('write geometry...')
	# for each geometry ...
	for geom_id, geom in doc.geometries.items():
		# get the mesh of this geometry
		mesh_of_geom = doc.mesh.meshedGeometries[geom_id]
		# get physical and element property assignments
		phys_prop_asn = geom.physicalPropertyAssignment
		elem_prop_asn = geom.elementPropertyAssignment
		# process all subdomains
		__write_geom_domain(pinfo, mesh_of_geom.edges,  phys_prop_asn.onEdges, elem_prop_asn.onEdges)
		__write_geom_domain(pinfo, mesh_of_geom.faces,  phys_prop_asn.onFaces, elem_prop_asn.onFaces)
		__write_geom_domain(pinfo, mesh_of_geom.solids, phys_prop_asn.onSolids, elem_prop_asn.onSolids)

def write_inter_partition(doc, pinfo, element_file):
	PyMpc.App.monitor().sendMessage('write interactions...')
	processor_id = 0
	# create remapper
	remapper = _remapper_t(pinfo)
	for partition in doc.mesh.partitionData.partitions:
		pinfo.setProcessId(processor_id)
		if processor_id == 0:
			element_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$process_id == ', processor_id, '} {'))
		else:
			element_file.write('{}{}{}{}\n'.format(pinfo.indent, ' elseif {$process_id == ', processor_id, '} {'))
		for inter_id, inter in doc.interactions.items():
			mesh_of_inter = doc.mesh.meshedInteractions[inter_id]
			phys_prop = inter.physicalProperty
			elem_prop = inter.elementProperty
			# begin remapper with new source
			remapper.set_source_phys_prop(phys_prop)
			# a null element property is not and error, it means: don't write this element
			# (for example boundary elements)
			# we don't do any check on the phys_prop prop, it's up to the element formulation to check
			# whether it should be non-null
			if(elem_prop is None):
				continue
			# get elem formulation module
			elem_xobj = elem_prop.XObject
			if(elem_xobj is None):
				raise Exception('null XObject in element property object')
			elem_module_name = 'opensees.element_properties.{}.{}'.format(elem_xobj.Xnamespace, elem_xobj.name)
			elem_module = importlib.import_module(elem_module_name)
			if not hasattr(elem_module, 'writeTcl'):
				continue
			pinfo.phys_prop = phys_prop
			pinfo.elem_prop = elem_prop
			for elem in mesh_of_inter.elements:
				if doc.mesh.partitionData.elementPartition(elem.id) == processor_id:
					if (pinfo.element_subset is not None) and (elem.id not in pinfo.element_subset):
						continue # skip it in case of staged models if not in current stage
					try:
						# remap
						remapper.remap_phys_prop(phys_prop, elem.id)
						pinfo.elem = elem
						elem_module.writeTcl(pinfo)
					finally:
						remapper.reset_phys_prop(phys_prop)
					pinfo.loaded_element_subset.add(elem.id) # mark as written
					PyMpc.App.monitor().sendAutoIncrement()
		element_file.write('{}{}'.format(pinfo.indent, '}'))
		processor_id +=1
	pinfo.setProcessId(0) # back to default
	
def write_inter(doc, pinfo):
	PyMpc.App.monitor().sendMessage('write interactions...')
	# create remapper
	remapper = _remapper_t(pinfo)
	# for each interaction
	for inter_id, inter in doc.interactions.items():
		mesh_of_inter = doc.mesh.meshedInteractions[inter_id]
		phys_prop = inter.physicalProperty
		elem_prop = inter.elementProperty
		# begin remapper with new source
		remapper.set_source_phys_prop(phys_prop)
		# a null element property is not and error, it means: don't write this element
		# (for example boundary elements)
		# we don't do any check on the phys_prop prop, it's up to the element formulation to check
		# whether it should be non-null
		if(elem_prop is None):
			continue
		# get elem formulation module
		elem_xobj = elem_prop.XObject
		if(elem_xobj is None):
			raise Exception('null XObject in element property object')
		elem_module_name = 'opensees.element_properties.{}.{}'.format(elem_xobj.Xnamespace, elem_xobj.name)
		elem_module = importlib.import_module(elem_module_name)
		if not hasattr(elem_module, 'writeTcl'):
			continue
		pinfo.phys_prop = phys_prop
		pinfo.elem_prop = elem_prop
		for elem in mesh_of_inter.elements:
			if (pinfo.element_subset is not None) and (elem.id not in pinfo.element_subset):
				continue # skip it in case of staged models if not in current stage
			try:
				# remap
				remapper.remap_phys_prop(phys_prop, elem.id)
				pinfo.elem = elem
				elem_module.writeTcl(pinfo)
			finally:
				remapper.reset_phys_prop(phys_prop)
			pinfo.loaded_element_subset.add(elem.id) # mark as written
			PyMpc.App.monitor().sendAutoIncrement()
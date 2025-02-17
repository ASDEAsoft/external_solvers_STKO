import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
from PyMpc.Math import *

def makeXObjectMetaData():
	at_b = MpcAttributeMetaData()
	at_b.type = MpcAttributeType.QuantityVector3
	at_b.name = 'b'
	at_b.group = 'Data'
	at_b.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('b')+'<br/>') + 
		html_par('Gravity acceleration vector. It will be multiplied by the mass density (rho) of the associated material to obtain the body force vector') +
		html_end()
		)
	at_b.dimension = u.L/u.t**2
	xom = MpcXObjectMetaData()
	xom.name = 'ASDAbsorbingBoundary3DSelfWeight'
	xom.addAttribute(at_b)
	return xom

def fillConditionRepresentationData(xobj, pos, data):
	b = xobj.getAttribute('b').quantityVector3.value
	data[0] = b.x
	data[1] = b.y
	data[2] = b.z

def makeConditionRepresentationData(xobj):
	d = MpcConditionRepresentationData()
	d.type = MpcConditionVRepType.Arrows
	d.orientation = MpcConditionVRepOrientation.Global
	d.data = Math.double_array([0.0, 0.0, 0.0])
	d.on_vertices = False
	d.on_edges = False
	d.on_faces = False
	d.on_solids = False
	d.on_interactions = False
	return d

def writeTcl_Force(pinfo, xobj):
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	b_at = xobj.getAttribute('b')
	if(b_at is None):
		raise Exception('Error: cannot find "b" attribute')
	# acceleration vector
	gvec = b_at.quantityVector3.value
	
	manager = pinfo.custom_data.get('ASDAbsorbingBoundary3D', None)
	if manager is None:
		raise Exception("Cannot find ASDAbsorbingBoundary3D, probably you didn't use ASDAbsorbingBoundary3DAuto elements")
	
	doc = App.caeDocument()
	is_partitioned = False
	if pinfo.process_count > 1:
		is_partitioned = True
	
	# pre-process all nodes where each auto-generated bnd element should put self-weight.
	# here manager.element_volumes already contains either L-R-F-K or corners.
	# for the single bcode we can lump load at the nodes not in STKO mesh (i.e outer 4 nodes).
	# for corners, only at the outer-most 2 nodes, not shared by the pure sides!
	map_nodes_by_sides = {}
	for pid, ele_data in manager.element_volumes.items():
		for etag, ex_volume, conn, bcode, rho in ele_data:
			if isinstance(bcode, int): # pure side
				nodes_on_sides = map_nodes_by_sides.get(bcode, None)
				if nodes_on_sides is None:
					nodes_on_sides = set()
					map_nodes_by_sides[bcode] = nodes_on_sides
				for inode in conn:
					if inode not in doc.mesh.nodes:
						nodes_on_sides.add(inode)
	
	for pid, ele_data in manager.element_volumes.items():
		# open partition-if-block
		if is_partitioned:
			pinfo.out_file.write('\n{}{}{}{}\n'.format(pinfo.indent, 'if {$STKO_VAR_process_id == ', pid, '} {'))
		
		# process each absorbing element auto-generated on this partition
		for etag, ex_volume, conn, bcode, rho in ele_data:
			# extract only nodes that should be loaded
			# we assume 
			if isinstance(bcode, int):
				allowed = map_nodes_by_sides[bcode]
				ex_nodes = [i for i in conn if i in allowed]
			else:
				allowed_1 = map_nodes_by_sides[bcode[0]]
				allowed_2 = map_nodes_by_sides[bcode[1]]
				ex_nodes = [i for i in conn if (i not in allowed_1 and i not in allowed_2 and i not in doc.mesh.nodes)]
			dV = ex_volume / float(len(ex_nodes))
			b = gvec * rho
			for inode in ex_nodes:
				pinfo.out_file.write('{}load {} {:.12g} {:.12g} {:.12g}\n'.format(pinfo.indent, inode, b[0]*dV, b[1]*dV, b[2]*dV))
		# close partition-if-block
		if is_partitioned:
			pinfo.out_file.write('{}{}'.format(pinfo.indent, '}'))
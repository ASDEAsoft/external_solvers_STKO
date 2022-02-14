import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

def makeXObjectMetaData():
	
	def descr(title, text):
		return (
			html_par(html_begin()) +
			html_par(html_boldtext(title)+'<br/>') +
			html_par(text) +
			#html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/ZeroLength_Element','ZeroLength Element')+'<br/>') +
			html_end()
			)
	
	# mat_x
	at_mat_x = MpcAttributeMetaData()
	at_mat_x.type = MpcAttributeType.Index
	at_mat_x.name = 'X Material'
	at_mat_x.group = 'Materials'
	at_mat_x.description = descr('X Material', 'Uniaxial material for the local X direction')
	at_mat_x.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_mat_x.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# mat_x
	at_mat_y = MpcAttributeMetaData()
	at_mat_y.type = MpcAttributeType.Index
	at_mat_y.name = 'Y Material'
	at_mat_y.group = 'Materials'
	at_mat_y.description = descr('Y Material', 'Uniaxial material for the local Y direction')
	at_mat_y.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_mat_y.indexSource.addAllowedNamespace("materials.uniaxial")
	
	# K
	at_K = MpcAttributeMetaData()
	at_K.type = MpcAttributeType.Real
	at_K.name = 'K (penalty)'
	at_K.group = 'Misc'
	at_K.description = descr(
		'K (Penalty)', 
		'A penalty value to enforce continuity in the other DOFs (Ux, Uy, Uz, Rz) in the local coordinate system')
	at_K.setDefault(1.0e18)
	
	xom = MpcXObjectMetaData()
	xom.name = 'RCJointModel3D'
	xom.Xgroup = 'RC Beam-Column Joint Models'
	xom.addAttribute(at_mat_x)
	xom.addAttribute(at_mat_y)
	xom.addAttribute(at_K)
	
	return xom
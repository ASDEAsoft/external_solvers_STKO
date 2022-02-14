# enable default 3D tester for this module
from opensees.physical_properties.utils.tester.EnableTester2DPlaneStress import *

import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# materials
	at_materials = MpcAttributeMetaData()
	at_materials.type = MpcAttributeType.IndexVector
	at_materials.name = 'materials'
	at_materials.group = 'Default'
	at_materials.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('materials')+'<br/>') + 
		html_par('vector of tag of previously defined uniaxial materials') +
		#html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Material','Plane Stress Material')+'<br/>') +
		html_end()
		)
	at_materials.indexSource.type = MpcAttributeIndexSourceType.PhysicalProperty
	at_materials.indexSource.addAllowedNamespace('materials.nD')
	
	# thicknesses
	at_thicknesses = MpcAttributeMetaData()
	at_thicknesses.type = MpcAttributeType.QuantityVector
	at_thicknesses.name = 'thicknesses'
	at_thicknesses.group = 'Default'
	at_thicknesses.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('thicknesses')+'<br/>') + 
		html_par('vector of thicknesses') +
		#html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Plane_Stress_Material','Plane Stress Material')+'<br/>') +
		html_end()
		)
	at_thicknesses.dimension = u.L
	
	xom = MpcXObjectMetaData()
	xom.name = 'PlaneStressLayeredMaterial'
	xom.Xgroup = 'Other nD Materials'
	xom.addAttribute(at_materials)
	xom.addAttribute(at_thicknesses)
	
	return xom

def writeTcl(pinfo):
	
	#nDMaterial PlaneStressLayeredMaterial $tag $nLayers $matTag1 $t1 ... $matTagN $tn
	xobj = pinfo.phys_prop.XObject
	tag = xobj.parent.componentId
	
	# mandatory parameters
	materials_at = xobj.getAttribute('materials')
	if(materials_at is None):
		raise Exception('Error: cannot find "materials" attribute')
	materials = materials_at.indexVector
	
	thicknesses_at = xobj.getAttribute('thicknesses')
	if(thicknesses_at is None):
		raise Exception('Error: cannot find "thicknesses" attribute')
	thicknesses = thicknesses_at.quantityVector
	
	if len(materials) != len(thicknesses):
		raise Exception('Error: "materials" and "thicknesses" vector must have the same size')
	if len(materials) == 0:
		raise Exception('Error: "materials" and "thicknesses" vector must have at least 1 component')
	
	# now write the string into the file
	pinfo.out_file.write(
		'{}nDMaterial PlaneStressLayeredMaterial {} {} {}\n'.format(
			pinfo.indent, tag, len(materials), 
			' '.join(
				[ '{} {}'.format(materials[i], thicknesses.valueAt(i)) for i in range(len(materials)) ]
				)
			)
		)
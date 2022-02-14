import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	# velocityPoints
	at_velocityPoints = MpcAttributeMetaData()
	at_velocityPoints.type = MpcAttributeType.QuantityVector
	at_velocityPoints.name = 'velocityPoints'
	at_velocityPoints.group = 'Group'
	at_velocityPoints.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('velocityPoints')+'<br/>') + 
		html_par('array of velocity points along friction-velocity curve') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Multi-Linear_Velocity_Dependent_Friction','Multi-Linear Velocity Dependent Friction')+'<br/>') +
		html_end()
		)
	
	# frictionPoints
	at_frictionPoints = MpcAttributeMetaData()
	at_frictionPoints.type = MpcAttributeType.QuantityVector
	at_frictionPoints.name = 'frictionPoints'
	at_frictionPoints.group = 'Group'
	at_frictionPoints.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('frictionPoints')+'<br/>') + 
		html_par('array of friction points along friction-velocity curve') +
		html_par(html_href('http://opensees.berkeley.edu/wiki/index.php/Multi-Linear_Velocity_Dependent_Friction','Multi-Linear Velocity Dependent Friction')+'<br/>') +
		html_end()
		)
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'VelDepMultiLinear'
	xom.addAttribute(at_velocityPoints)
	xom.addAttribute(at_frictionPoints)
	
	
	return xom

def writeTcl(pinfo):
	
	#frictionModel VelDepMultiLinear $frnTag -vel $velocityPoints -frn $frictionPoints
	xobj = pinfo.definition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	frnTag = xobj.parent.componentId
	
	velocityPoints_at = xobj.getAttribute('velocityPoints')
	if(velocityPoints_at is None):
		raise Exception('Error: cannot find "velocityPoints" attribute')
	velocityPoints = velocityPoints_at.quantityVector
	
	frictionPoints_at = xobj.getAttribute('frictionPoints')
	if(frictionPoints_at is None):
		raise Exception('Error: cannot find "frictionPoints" attribute')
	frictionPoints = frictionPoints_at.quantityVector
	
	if len(velocityPoints) != len(frictionPoints):
		raise Exception('Error in VelDepMultiLinear: velocity and friction vectors must have the same length')
	if len(velocityPoints) < 2:
		raise Exception('Error in VelDepMultiLinear: velocity and friction vectors must have at least 2 values')
	
	velocityPoints_str = ''
	frictionPoints_str = ''
	for i in range(len(velocityPoints)):
		if i > 0:
			velocityPoints_str += ' '
			frictionPoints_str += ' '
		velocityPoints_str += str(velocityPoints.valueAt(i))
		frictionPoints_str += str(frictionPoints.valueAt(i))
	
	str_tcl = '{0}frictionModel VelDepMultiLinear {1} -vel {2} -frn {3}\n'.format(pinfo.indent, frnTag, velocityPoints_str, frictionPoints_str)
	
	# now write the string into the file
	pinfo.out_file.write(str_tcl)
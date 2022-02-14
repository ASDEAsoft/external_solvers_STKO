import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin
import opensees.element_properties.beam_column_elements.internalBeamColumnElement as internalBeamColumnElement

def makeXObjectMetaData():
	
	# 2D
	at_2D = MpcAttributeMetaData()
	at_2D.type = MpcAttributeType.Boolean
	at_2D.name = '2D'
	at_2D.group = 'Group'
	at_2D.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('2D')+'<br/>') +
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_2D.setDefault(True)
	at_2D.editable = False
	
	xom = MpcXObjectMetaData()
	xom.name = 'forceBeamColumnCBDI'
	xom.addAttribute(at_2D)
	
	internalBeamColumnElement.internalBeamFunction(xom)
	
	return xom

def getNodalSpatialDim(xobj, xobj_phys_prop):
	return [(2,3),(2,3)]	# (ndm,ndf)

def writeTcl(pinfo):
	
	pinfo.updateModelBuilder(2,3)
	
	# writeTcl_internalBeamFunction
	internalBeamColumnElement.writeTcl_internalBeamFunction(pinfo)
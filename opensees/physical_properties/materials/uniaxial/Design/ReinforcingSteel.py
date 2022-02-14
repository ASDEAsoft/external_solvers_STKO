import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *

import os
import PyMpc
import traceback
from io import StringIO

class _constants:
	#gui
	gui = None
	#version
	version = 1

def makeXObjectMetaData():

	def make_attr(name, group, descr):
		at = MpcAttributeMetaData()
		at.name = name
		at.group = group
		at.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('http://www.google.it','Ref Link')+'<br/>') +
			html_end()
			)
		return at

	xom = MpcXObjectMetaData()
	xom.name = 'ReinforcingSteel'
	# xom.Xgroup = 'Design'
	
	# Material parameters
	# Yield strength
	at_fy = make_attr('fy', 'Material Properties', 'Yield strength of steel. Characteristic value if new construction, mean value if existing construction')
	at_fy.type = MpcAttributeType.QuantityScalar
	at_fy.setDefault(0.0)
	at_fy.dimension = u.F/u.L**2
	at_fy.visible = True
	at_fy.editable = True
	# Yield strength
	at_eps_su = make_attr('eps_su', 'Material Properties', 'Ultimate strain of steel ')
	at_eps_su.type = MpcAttributeType.Real
	at_eps_su.setDefault(0.0)
	at_eps_su.visible = True
	at_eps_su.editable = True
	# Elastic modulus of concrete
	at_Es = make_attr('Es', 'Material Properties', 'Elastic modulus of steel')
	at_Es.type = MpcAttributeType.QuantityScalar
	at_Es.dimension = u.F/u.L**2
	at_Es.setDefault(0.0)
	at_Es.visible = True
	at_Es.editable = True
	
	# add a last attribute for versioning
	av = MpcAttributeMetaData()
	av.type = MpcAttributeType.Integer
	av.description = (
		html_par('Version {}'.format(_constants.version))
		)
	av.name = 'version'
	av.setDefault(_constants.version)
	av.editable = False
	av.visible = True
	
	xom.addAttribute(at_fy)
	xom.addAttribute(at_eps_su)
	xom.addAttribute(at_Es)
	xom.addAttribute(av)

	return xom

def _get_xobj_attribute(xobj, at_name):
	attribute = xobj.getAttribute(at_name)
	if attribute is None:
		raise Exception('Error: cannot find "{}" attribute'.format(at_name))
	return attribute

	
# def onConvertOldVersion(xobj, old_xobj):
	# '''
	# try to convert objects from old versions to the current one.
	# current version: 1
	# '''
	
	# version = 0 # default one
	# av = old_xobj.getAttribute('version')
	# if av:
		# version = av.integer
	
	# # just a safety check
	# cav = xobj.getAttribute('version')
	# if cav is None:
		# IO.write_cerr('Cannot find "version" attribute in AnalysesCommand\n')
		# return
		
	# cav.integer = _constants.version
		
	# # Check version
	# if version == 0:
		# # It should never happen because the xboj was included with version 1, so nobody should have an old version of the xobj
		# pass
	# if version < cav.integer:
		# # The current version is newer than the file version, will do whatever will be needed
		# # Here the logic for version change (update) should be included. For instance what to do when moving from version 1 to 2, to 3 etc.
		# pass
		
	


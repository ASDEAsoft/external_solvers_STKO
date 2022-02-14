import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import opensees.utils.tcl_input as tclin

def makeXObjectMetaData():
	
	xom = MpcXObjectMetaData()
	xom.name = 'domainChange'
	
	return xom

def writeTcl(pinfo):
	
	# domainChange
	
	xobj = pinfo.analysis_step.XObject
	tag_add_to_parameter =  xobj.parent.id
	
	FileName = xobj.name
	if pinfo.currentDescription != FileName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, FileName))
		pinfo.currentDescription = FileName
	
	pinfo.out_file.write('{}domainChange\n'.format(pinfo.indent))

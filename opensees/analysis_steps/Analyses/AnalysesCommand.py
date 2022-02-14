from PyMpc import *
from mpc_utils_html import *
import opensees.analysis_steps.Analyses.constraints as constraints
import opensees.analysis_steps.Analyses.numberer as numberer
import opensees.analysis_steps.Analyses.system as system
import opensees.analysis_steps.Analyses.test as test
import opensees.analysis_steps.Analyses.algorithm as algorithm
import opensees.analysis_steps.Analyses.integrator as integrator
import opensees.analysis_steps.Analyses.analysis as analysis
import opensees.analysis_steps.Analyses.analyze as analyze
import opensees.analysis_steps.Analyses.loadConst as loadConst
import opensees.analysis_steps.Analyses.wipeAnalysis as wipeAnalysis
import PyMpc.App
import os

class _internals:
	version = 1 # the current version

def makeXObjectMetaData():
	
	xom = MpcXObjectMetaData()
	xom.name = 'AnalysesCommand'
	
	# analysis
	analysis.analysisCommand(xom)
	
	# constraints
	constraints.constraintsCommand(xom)
	
	# numberer
	numberer.numbererCommand(xom)
	
	# system
	system.systemCommand(xom)
	
	# algorithm
	algorithm.algorithmCommand(xom)
	
	# test
	test.testCommand(xom)
	
	# integrator
	integrator.integratorCommand(xom)
	
	# analyze
	analyze.analyzeCommand(xom)
	
	# loadConst
	loadConst.loadConstCommand(xom)
	
	# wipeAnalysis
	wipeAnalysis.wipeAnalysisCommand(xom)
	
	# visibility dependencies
	# dt Transient-dep
	xom.setVisibilityDependency(xom.getAttribute('Transient'), xom.getAttribute('duration/transient'))
	
	# auto-exclusive dependencies
	xom.setBooleanAutoExclusiveDependency(xom.getAttribute('analysisType'), xom.getAttribute('Static'))
	xom.setBooleanAutoExclusiveDependency(xom.getAttribute('analysisType'), xom.getAttribute('Transient'))
	xom.setBooleanAutoExclusiveDependency(xom.getAttribute('Time Step Type'), xom.getAttribute('Adaptive Time Step'))
	xom.setBooleanAutoExclusiveDependency(xom.getAttribute('Time Step Type'), xom.getAttribute('Fixed Time Step'))
	
	# add a last attribute for versioning
	av = MpcAttributeMetaData()
	av.type = MpcAttributeType.Integer
	av.name = 'version'
	av.setDefault(_internals.version)
	av.editable = False
	xom.addAttribute(av)
	
	return xom

class _myglobals:
	integrators_with_adaptive = ['Load Control', 'Displacement Control', 'Parallel Displacement Control', 'Arc-Length Control', 'EQPath', 'HSConstraint'
	,'Newmark Method', 'Hilber-Hughes-Taylor Method', 'Generalized Alpha Method', 'AlphaOS_TP', 'AlphaOSGeneralized_TP', 'TRBDF2']
	integrators_no_test = ['Explicit Difference', 'KRAlphaExplicit_TP', 'HHTGeneralizedExplicit_TP', 'HHT_TP', 'HHTExplicit_TP', 'Central Difference', 'Newmark Explicit']

def onAttributeChanged(editor, xobj, attribute_name):
	'''
	This method is called everytime the value of an attribute is changed.
	The xobject containing the modified attribute and the attribute name
	are passed as input arguments to this function.
	'''
	
	# common
	is_static = (xobj.getAttribute('analysisType').string == 'Static')
	
	# adaptive time step
	def hide_adapt(integrator):
		# hide them all if not supported, otherwise leave them as they are
		if not integrator in _myglobals.integrators_with_adaptive:
			xobj.getAttribute('Time Step Type').visible = False
			xobj.getAttribute('Time Step Type').string = 'Fixed Time Step'
			xobj.getAttribute('Adaptive Time Step').boolean = False
			xobj.getAttribute('Fixed Time Step').boolean = True
			xobj.getAttribute('max factor').visible = False
			xobj.getAttribute('min factor').visible = False
			xobj.getAttribute('max factor incr').visible = False
			xobj.getAttribute('min factor incr').visible = False
		else:
			xobj.getAttribute('Time Step Type').visible = True
	if is_static:
		hide_adapt(xobj.getAttribute('staticIntegrators').string)
	else:
		hide_adapt(xobj.getAttribute('transientIntegrators').string)
	
	# cyclic disp control
	if is_static:
		integrator = xobj.getAttribute('staticIntegrators').string
		if integrator == 'Displacement Control':
			cyclic = xobj.getAttribute('Cyclic').boolean
			xobj.getAttribute('Target Displacement').visible = not cyclic
			xobj.getAttribute('Target Displacement History').visible = cyclic
		elif integrator == 'Parallel Displacement Control':
			cyclic = xobj.getAttribute('Cyclic/parallelDisplacementControl').boolean
			xobj.getAttribute('Target Displacement/parallelDisplacementControl').visible = not cyclic
			xobj.getAttribute('Target Displacement History/parallelDisplacementControl').visible = cyclic
	
	# explicit methods do not need test command
	# it should be done everytime
	# TODO...
	pass

def onEditBegin(editor, xobj):
	onAttributeChanged(editor, xobj, 'staticIntegrators')

def onConvertOldVersion(xobj, old_xobj):
	'''
	try to convert objects from old versions to the current one.
	current version: 1
	'''
	
	version = 0 # default one
	av = old_xobj.getAttribute('version')
	if av:
		version = av.integer
	
	# just a safety check
	cav = xobj.getAttribute('version')
	if cav is None:
		IO.write_cerr('Cannot find "version" attribute in AnalysesCommand\n')
		return
	cav.integer = _internals.version
	
	# check version
	if version == 0:
		
		# convert delta increment to full duration
		def check_dt():
			try:
				n = xobj.getAttribute('numIncr').integer
				if xobj.getAttribute('Static').boolean:
					integrator = xobj.getAttribute('staticIntegrators').string
					if integrator == 'Load Control':
						dt = xobj.getAttribute('lambda').real
						duration = dt*float(n)
						xobj.getAttribute('duration').real = duration
						print('AnalysesCommand - (static load control) conversion dt->duration = {} (version {} -> {})'.format(duration, version, _internals.version))
					elif integrator == 'Displacement Control':
						dt = xobj.getAttribute('incr').real
						duration = dt*float(n)
						xobj.getAttribute('Target Displacement').real = duration
						print('AnalysesCommand - (static displacement control) conversion dt->duration = {} (version {} -> {})'.format(duration, version, _internals.version))
					elif integrator == 'Parallel Displacement Control':
						dt = xobj.getAttribute('incr/parallelDisplacementControl').real
						duration = dt*float(n)
						xobj.getAttribute('Target Displacement/parallelDisplacementControl').real = duration
						print('AnalysesCommand - (static parallel displacement control) conversion dt->duration = {} (version {} -> {})'.format(duration, version, _internals.version))
					elif integrator == 'Arc-Length Control':
						dt = xobj.getAttribute('s').real
						duration = dt*float(n)
						xobj.getAttribute('Target Arc-Length').real = duration
						print('AnalysesCommand - (static arc-length control) conversion dt->duration = {} (version {} -> {})'.format(duration, version, _internals.version))
				else:
					dt = xobj.getAttribute('dt Transient').real
					duration = dt*float(n)
					xobj.getAttribute('duration/transient').real = duration
					print('AnalysesCommand - (transient) conversion dt->duration = {} (version {} -> {})'.format(duration, version, _internals.version))
			except Exception as e:
				pass
		
		# do all checks
		check_dt()

def writeTcl(pinfo):
	
	xobj = pinfo.analysis_step.XObject
	
	def geta(name):
		at = xobj.getAttribute(name)
		if at is None:
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return at
	
	def WriteLoadControl():
		duration = geta('duration').real
		numIncr_at = geta('numIncr').integer
		
		if (duration * float(numIncr_at)) == 0.0:
			pinfo.out_file.write('# Analysis skipped: duration({}) * increments({}) = 0\n'.format(duration, numIncr_at))
			return
			
		if(geta('Adaptive Time Step').boolean):
			template_filename = '{}/template_lc_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__initial_num_incr__', str(numIncr_at)).replace(
			'__max_iter__', str(iter)).replace(
			'__des_iter__', str(int(des_iter))).replace(
			'__total_time__', str(duration)).replace(
			'__max_factor__', str(max_factor)).replace(
			'__min_factor__', str(min_factor)).replace(
			'__max_factor_incr__', str(max_factor_incr)).replace(
			'__min_factor_incr__', str(min_factor_incr)).replace(
			'__integrator_type__', 'LoadControl').replace(
			'__more_int_data__', ''))
		else:
			template_filename = '{}/template_lc_no_adapt_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__initial_num_incr__', str(numIncr_at)).replace(
			'__total_time__', str(duration)).replace(
			'__integrator_type__', 'LoadControl').replace(
			'__more_int_data__', ''))
	
	def WriteDisplacementControl(staticIntegrators):
		numIncr_at = geta('numIncr').integer
		doc = PyMpc.App.caeDocument()
		if(doc is None):
			raise Exception('null cae document')
		time= '{'
		U= '{'
		tstag = -1
		U_temp =[]
		if (staticIntegrators == 'Parallel Displacement Control'):
			SelectionSet_at = geta('SelectionSet/parallelDisplacementControl')
			dof=geta('dof/parallelDisplacementControl').integer
			if(geta('Cyclic/parallelDisplacementControl').boolean):
				tstag = geta('Target Displacement History/parallelDisplacementControl').index
			targ_disp = geta('Target Displacement/parallelDisplacementControl')
		if (staticIntegrators == 'Displacement Control'):
			SelectionSet_at = geta('SelectionSet')
			dof=geta('dof').integer
			if(geta('Cyclic').boolean):
				tstag = geta('Target Displacement History').index
			targ_disp = geta('Target Displacement')
		if(tstag>-1):
			timeseries= doc.getDefinition(tstag).XObject
			if (timeseries is None):
				raise Exception('Error: timeseries path is not selected')
			list_value = timeseries.getAttribute('list_of_values').quantityVector
			if len(list_value) < 2:
				raise Exception('Error: the time series for the Cyclic displacement control should have at least 2 values')
			if(timeseries.getAttribute('constant').boolean):
				dt= timeseries.getAttribute('dt').real
				ix = 0.0
				for i in range(len(list_value)):
					U += '{} '.format(list_value.valueAt(i))
					time+= '{} '.format(ix)
					ix += dt
					U_temp.append(list_value.valueAt(i))
			else:
				list_Time= timeseries.getAttribute('list_of_times').quantityVector
				if(len(list_value)!=len(list_Time)):
					raise Exception('Different length of vectors')
				else:
					for i in range(len(list_value)):
						U += '{} '.format(list_value.valueAt(i))
						time+= '{} '.format(list_Time.valueAt(i))
						U_temp.append(list_value.valueAt(i))
			U += '}'
			time+='}'
		else:
			time += '0 1.0}'
			U +='0 {} {}'.format(targ_disp.real,'}')
			U_temp.append(0)
			U_temp.append(targ_disp.real)
		d = 0.0
		for i in range(1,len(U_temp)):
			d = max(abs(U_temp[i]-U_temp[i-1]), d)
		
		if numIncr_at == 0:
			trial_disp_incr = 0.0
		else:
			trial_disp_incr = d/numIncr_at
		
		if (trial_disp_incr * float(numIncr_at)) == 0.0:
			pinfo.out_file.write('# Analysis skipped: dU({}) * increments({}) = 0\n'.format(trial_disp_incr, numIncr_at))
			return
		
		selection_set = doc.selectionSets[SelectionSet_at.index]
		for geometry_id, geometry_subset in selection_set.geometries.items():
			mesh_of_geom = doc.mesh.meshedGeometries[geometry_id]
			if len(geometry_subset.vertices) != 1: 
				raise Exception('Error: the selection set for DisplacementControl must contain 1 vertex (found {} vertices)'.format(len(geometry_subset.vertices)));
			for domain_id in geometry_subset.vertices:
				node = mesh_of_geom.vertices[domain_id].id
		
		if(geta('Adaptive Time Step').boolean):
			template_filename = '{}/template_dc_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__trial_disp_incr__', str(trial_disp_incr)).replace(
			'__max_iter__', str(iter)).replace(
			'__des_iter__', str(int(des_iter))).replace(
			'__max_factor__', str(max_factor)).replace(
			'__min_factor__', str(min_factor)).replace(
			'__max_factor_incr__', str(max_factor_incr)).replace(
			'__min_factor_incr__', str(min_factor_incr)).replace(
			'__controlNode__', str(node)).replace(
			'__controlDOF__',str(dof)).replace(
			'__time__', time).replace(
			'__U__',U))
			
		if(geta('Fixed Time Step').boolean):
			template_filename = '{}/template_dc_no_adapt_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__trial_disp_incr__', str(trial_disp_incr)).replace(
			'__max_iter__', str(iter)).replace(
			'__des_iter__', str(int(des_iter))).replace(
			'__controlNode__', str(node)).replace(
			'__controlDOF__',str(dof)).replace(
			'__time__', time).replace(
			'__U__',U))
	
	def WriteArcLengthControl():
		duration = geta('Target Arc-Length').real
		numIncr_at = geta('numIncr').integer
		
		if (duration * float(numIncr_at)) == 0.0:
			pinfo.out_file.write('# Analysis skipped: arc-length({}) * increments({}) = 0\n'.format(duration, numIncr_at))
			return
		
		alpha = geta('alpha').real
		integrator_type = 'ArcLength'
		if not geta('Adaptive Time Step').boolean:
			template_filename = '{}/template_lc_no_adapt_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__initial_num_incr__', str(numIncr_at)).replace(
			'__total_time__', str(duration)).replace(
			'__integrator_type__', str(integrator_type)).replace(
			'__more_int_data__', str(alpha)))
		else:
			template_filename = '{}/template_lc_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__initial_num_incr__', str(numIncr_at)).replace(
			'__max_iter__', str(iter)).replace(
			'__des_iter__', str(int(des_iter))).replace(
			'__total_time__', str(duration)).replace(
			'__max_factor__', str(max_factor)).replace(
			'__min_factor__', str(min_factor)).replace(
			'__max_factor_incr__', str(max_factor_incr)).replace(
			'__min_factor_incr__', str(min_factor_incr)).replace(
			'__integrator_type__', str(integrator_type)).replace(
			'__more_int_data__', str(alpha)))
	
	def WriteEQPath():
		duration = geta('Target Arc-Length/EQPath').real
		numIncr_at = geta('numIncr').integer
		
		if (duration * float(numIncr_at)) == 0.0:
			pinfo.out_file.write('# Analysis skipped: arc-length({}) * increments({}) = 0\n'.format(duration, numIncr_at))
			return
		
		eq_type = geta('type/EQPath').string
		int_type = 0
		if eq_type == 'Minimum Residual Disp':
			int_type = 1
		if eq_type == 'Normal Plain':
			int_type = 2
		if eq_type == 'Update Normal Plain':
			int_type = 3
		if eq_type == 'Cylindrical Arc-Length':
			int_type = 4
		integrator_type = 'EQPath'
		if not geta('Adaptive Time Step').boolean:
			template_filename = '{}/template_lc_no_adapt_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__initial_num_incr__', str(numIncr_at)).replace(
			'__total_time__', str(duration)).replace(
			'__integrator_type__', str(integrator_type)).replace(
			'__more_int_data__', str(int_type)))
		else:
			template_filename = '{}/template_lc_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__initial_num_incr__', str(numIncr_at)).replace(
			'__max_iter__', str(iter)).replace(
			'__des_iter__', str(int(des_iter))).replace(
			'__total_time__', str(duration)).replace(
			'__max_factor__', str(max_factor)).replace(
			'__min_factor__', str(min_factor)).replace(
			'__max_factor_incr__', str(max_factor_incr)).replace(
			'__min_factor_incr__', str(min_factor_incr)).replace(
			'__integrator_type__', str(integrator_type)).replace(
			'__more_int_data__', str(int_type)))
	
	def WriteHSConstraint():
		duration = geta('Target Arc-Length/HSConstraint').real
		numIncr_at = geta('numIncr').integer
		
		if (duration * float(numIncr_at)) == 0.0:
			pinfo.out_file.write('# Analysis skipped: arc-length({}) * increments({}) = 0\n'.format(duration, numIncr_at))
			return
		
		integrator_type = 'HSConstraint'
		if not geta('Adaptive Time Step').boolean:
			template_filename = '{}/template_lc_no_adapt_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__initial_num_incr__', str(numIncr_at)).replace(
			'__total_time__', str(duration)).replace(
			'__integrator_type__', str(integrator_type)).replace(
			'__more_int_data__', ''))
		else:
			template_filename = '{}/template_lc_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__initial_num_incr__', str(numIncr_at)).replace(
			'__max_iter__', str(iter)).replace(
			'__des_iter__', str(int(des_iter))).replace(
			'__total_time__', str(duration)).replace(
			'__max_factor__', str(max_factor)).replace(
			'__min_factor__', str(min_factor)).replace(
			'__max_factor_incr__', str(max_factor_incr)).replace(
			'__min_factor_incr__', str(min_factor_incr)).replace(
			'__integrator_type__', str(integrator_type)).replace(
			'__more_int_data__', ''))
	
	def WriteTransientTemplate(more_int_data):
		
		if (duration * float(numIncr_at)) == 0.0:
			pinfo.out_file.write('# Analysis skipped: duration({}) * increments({}) = 0\n'.format(duration, numIncr_at))
			return
		
		if not geta('Adaptive Time Step').boolean:
			template_filename = '{}/template_trans_no_adapt_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__initial_num_incr__', str(numIncr_at)).replace(
			'__total_time__', str(duration)).replace(
			'__integrator_type__', str(integrator_type)).replace(
			'__more_int_data__', more_int_data))
		else:
			template_filename = '{}/template_trans_rev.tcl'.format(os.path.dirname(__file__))
			template_file = open(template_filename, 'r')
			template = template_file.read()
			template_file.close()
			pinfo.out_file.write(template.replace(
			'__initial_num_incr__', str(numIncr_at)).replace(
			'__max_iter__', str(iter)).replace(
			'__des_iter__', str(int(des_iter))).replace(
			'__total_time__', str(duration)).replace(
			'__max_factor__', str(max_factor)).replace(
			'__min_factor__', str(min_factor)).replace(
			'__max_factor_incr__', str(max_factor_incr)).replace(
			'__min_factor_incr__', str(min_factor_incr)).replace(
			'__integrator_type__', str(integrator_type)).replace(
			'__more_int_data__', more_int_data))
	
	sopt = ''
	
	# now write the string into the file
	pinfo.out_file.write('\n{}# analyses command\n'.format(pinfo.indent))
	pinfo.out_file.write('{}domainChange\n'.format(pinfo.indent))
	
	# constraints
	constraints.writeTcl_constraints(pinfo, xobj)
	
	# numberer
	numberer.writeTcl_numberer(pinfo, xobj)
	
	# system
	system.writeTcl_system(pinfo, xobj)
	
	# Compute common data for adaptive time step
	iter = xobj.getAttribute('iter/{}'.format( 
		test.getOpenSeesCommandName(geta('testCommand').string) 
		)).integer
	des_iter = iter
	iter_ov = None
	if(geta('Adaptive Time Step').boolean):
		iter = iter * 2
		iter_ov = iter
	
	# test
	test.writeTcl_test(pinfo, xobj, iter_override = iter_ov)
	
	# algorithm
	algorithm.writeTcl_algorithm(pinfo, xobj)
	
	# integrator
	integrator.writeTcl_integrator(pinfo, xobj)
	
	# The analysis and analyze command are now written in a custom way
	# using a custom loop to include the adaptive time stepping in TCL
	
	if(geta('Adaptive Time Step').boolean):
		max_factor = geta('max factor').real
		min_factor = geta('min factor').real
		max_factor_incr = geta('max factor incr').real
		min_factor_incr = geta('min factor incr').real
		if(max_factor<1):
			raise Exception('Error: max factor shoulb be >=1')
		if(min_factor<0 or min_factor>1):
			raise Exception('Error: min factor shoulb be <=1 and >=0')
		if(max_factor_incr<1):
			raise Exception('Error: max factor incr shoulb be >1')
		if(min_factor_incr<0 or min_factor_incr>1):
			raise Exception('Error: min factor incr shoulb be >=0 and <1')
	
	# Process Static or Transient types
	if geta('Static').boolean:
		# Static analyses
		pinfo.out_file.write('{}analysis {}\n'.format(pinfo.indent, 'Static'))
		# Common data
		staticIntegrators = geta('staticIntegrators').string
		# Process integrator type
		if staticIntegrators == 'Load Control':
			WriteLoadControl()
		elif (staticIntegrators == 'Displacement Control') or (staticIntegrators == 'Parallel Displacement Control'):
			WriteDisplacementControl(staticIntegrators)
		elif staticIntegrators == 'Arc-Length Control':
			WriteArcLengthControl()
		elif staticIntegrators == 'EQPath':
			WriteEQPath()
		elif staticIntegrators == 'HSConstraint':
			WriteHSConstraint()
		else:
			# standard proc for non-adaptive types
			# analyze
			analyze.writeTcl_analyze(pinfo, xobj)
	else:
		# Transient analyses
		pinfo.out_file.write('{}analysis {}\n'.format(pinfo.indent, 'Transient'))
		# Common data
		transientIntegrators = geta('transientIntegrators').string
		duration = geta('duration/transient').real
		numIncr_at = geta('numIncr').integer
		# Process integrator type
		if transientIntegrators == 'Central Difference':
			integrator_type = 'CentralDifference'
			more_int_data=''
		elif transientIntegrators == 'Newmark Method':
			integrator_type = 'Newmark'
			gamma = geta('gamma').real
			beta = geta('beta').real
			more_int_data= '{} {}'.format(gamma, beta)
		elif transientIntegrators == 'Newmark Explicit':
			integrator_type = 'NewmarkExplicit'
			gamma = geta('gamma').real
			more_int_data= '{}'.format(gamma)
		elif transientIntegrators == 'Hilber-Hughes-Taylor Method':
			integrator_type = 'HHT'
			alpha = geta('alpha/HHT').real
			more_int_data= '{}'.format(alpha)
		elif transientIntegrators == 'Generalized Alpha Method':
			integrator_type = 'GeneralizedAlpha'
			alphaM = geta('alphaM').real
			alphaF = geta('alphaF').real
			more_int_data= '{} {}'.format(alphaM, alphaF)
		elif transientIntegrators == 'TRBDF2':
			integrator_type = 'TRBDF2'
			more_int_data=''
		elif transientIntegrators == 'Explicit Difference':
			integrator_type = 'Explicitdifference'
			more_int_data=''
		elif transientIntegrators == 'AlphaOS_TP':
			integrator_type = 'AlphaOS_TP'
			alphaAlphaOS_TP = geta('alpha/AlphaOS_TP').real
			more_int_data= '{}'.format(alphaAlphaOS_TP)
		elif transientIntegrators == 'AlphaOSGeneralized_TP':
			integrator_type = 'AlphaOSGeneralized_TP'
			rhoInfAOSF_TP = geta('rhoInf/AlphaOSGeneralized_TP').real
			more_int_data= '{}'.format(rhoInfAOSF_TP)
		elif transientIntegrators == 'HHTExplicit_TP':
			integrator_type = 'HHTExplicit_TP'
			alpha_HHTExplicit_TP = geta('alpha/HHTExplicit_TP').real
			more_int_data= '{}'.format(alpha_HHTExplicit_TP)
		elif transientIntegrators == 'HHT_TP':
			integrator_type = 'HHT_TP'
			alpha_HHT_TP = geta('alpha/HHT_TP').real
			more_int_data= '{}'.format(alpha_HHT_TP)
		elif transientIntegrators == 'HHTGeneralizedExplicit_TP':
			integrator_type = 'HHTGeneralizedExplicit_TP'
			sopt_HHTGE = ''
			if geta('rhoB alphaF').boolean:
				sopt_HHTGE += ' {}'.format(geta('rhoB/HHTGeneralizedExplicit_TP').real)
				sopt_HHTGE += ' {}'.format(geta('alphaF/HHTGeneralizedExplicit_TP').real)
			if geta('alphaI alphaF beta gamma').boolean:
				sopt_HHTGE += ' {}'.format(geta('alphaI/HHTGeneralizedExplicit_TP').real)
				sopt_HHTGE += ' {}'.format(geta('alphaF/HHTGeneralizedExplicit_TP').real)
				sopt_HHTGE += ' {}'.format(geta('beta/HHTGeneralizedExplicit_TP').real)
				sopt_HHTGE += ' {}'.format(geta('gamma/HHTGeneralizedExplicit_TP').real)
			more_int_data= '{}'.format(sopt_HHTGE)
		elif transientIntegrators == 'KRAlphaExplicit_TP':
			integrator_type = 'KRAlphaExplicit_TP'
			rhoInf_KRAlphaExplicit_TP = geta('rhoInf/KRAlphaExplicit_TP').real
			more_int_data= '{}'.format(rhoInf_KRAlphaExplicit_TP)
		WriteTransientTemplate(more_int_data)
	
	pinfo.out_file.write('\n')
	# loadConst
	loadConst.writeTcl_loadConst(pinfo, xobj)
	
	# wipeAnalysis
	wipeAnalysis.writeTcl_wipeAnalysis(pinfo, xobj)

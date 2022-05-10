from PyMpc import *
from mpc_utils_html import *
import os

def makeXObjectMetaData():
	
	# utilities ==================================================================================
	
	def mka(type, name, group, descr):
		a = MpcAttributeMetaData()
		a.type = type
		a.name = name
		a.group = group
		a.description = (
			html_par(html_begin()) +
			html_par(html_boldtext(name)+'<br/>') + 
			html_par(descr) +
			html_par(html_href('','')+'<br/>') +
			html_end()
		)
		return a
	def mka_nr(name):
		return mka(MpcAttributeType.Boolean, name, 'Nodal results', '')
	def mka_er(name):
		return mka(MpcAttributeType.Boolean, name, 'element results', '')
	
	# Generic ==================================================================================
	
	at_recorders_name = mka(MpcAttributeType.String, 'name', 'Generic', '')
	at_recorders_name.stringType = 'SaveFilePath MPC Output database (*.mpco)'
	
	# Nodal results ==================================================================================
	
	at_displacement = mka_nr('displacement')
	at_rotation = mka_nr('rotation')
	at_velocity = mka_nr('velocity')
	at_angularVelocity = mka_nr('angularVelocity')
	at_acceleration = mka_nr('acceleration')
	at_angularAcceleration = mka_nr('angularAcceleration')
	at_reactionForce = mka_nr('reactionForce')
	at_reactionMoment = mka_nr('reactionMoment')
	at_reactionForceIncludingInertia = mka_nr('reactionForceIncludingInertia')
	at_reactionMomentIncludingInertia = mka_nr('reactionMomentIncludingInertia')
	at_rayleighForce = mka_nr('rayleighForce')
	at_rayleighMoment = mka_nr('rayleighMoment')
	at_pressure = mka_nr('pressure')
	at_modesOfVibration = mka_nr('modesOfVibration')
	at_modesOfVibrationRotational = mka_nr('modesOfVibrationRotational')
	
	# Element results ==================================================================================
	
	at_force = mka_er('force')
	at_localForce = mka_er('localForce')
	at_deformation = mka_er('deformation')
	at_damage = mka_er('damage')
	at_equivalentPlasticStrain = mka_er('equivalentPlasticStrain')
	at_cw = mka_er('cw')
	
	at_material_stress = mka_er('material.stress')
	at_material_strain = mka_er('material.strain')
	at_material_damage = mka_er('material.damage')
	at_material_equivalentPlasticStrain = mka_er('material.equivalentPlasticStrain')
	at_material_cw = mka_er('material.cw')
	
	at_section_force = mka_er('section.force')
	at_section_deformation = mka_er('section.deformation')
	at_section_fiber_stress = mka_er('section.fiber.stress')
	at_section_fiber_strain = mka_er('section.fiber.strain')
	at_section_fiber_damage = mka_er('section.fiber.damage')
	at_section_fiber_equivalentPlasticStrain = mka_er('section.fiber.equivalentPlasticStrain')
	at_section_fiber_cw = mka_er('section.fiber.cw')
	
	at_custom = mka(MpcAttributeType.StringVector, 'custom', 'custom element results', 
		'You can define 1 string for each result not mentioned in the built-in ones')
	
	# Time ==================================================================================
	
	at_opt_time_type = mka(MpcAttributeType.String, 'Record frequency', 'Time options', 
				html_par('Defines the frequency of the recorder. Possible options are:<br/>' + 
				html_boldtext('always') + ': records every time step.<br/>' +
				html_boldtext('dt') + ': records (approximately) every "dt" increment of time.<br/>' +
				html_boldtext('nsteps') + ': records every "nsteps" time steps.<br/>'))
	at_opt_time_type.sourceType = MpcAttributeSourceType.List
	at_opt_time_type.setSourceList(['always', 'dt', 'nsteps'])
	at_opt_time_type.setDefault('always')
	
	at_use_always = mka(MpcAttributeType.Boolean, 'always', 'Time options', '')
	at_use_always.editable = False
	
	at_use_dt = mka(MpcAttributeType.Boolean, 'dt', 'Time options', '')
	at_use_dt.editable = False
	
	at_use_nsteps = mka(MpcAttributeType.Boolean, 'nsteps', 'Time options', '')
	at_use_nsteps.editable = False
	
	at_dt = mka(MpcAttributeType.Real, 'dt/time', 'Time options', 'time increment')
	at_dt.setDefault(0.0)
	
	at_nsteps = mka(MpcAttributeType.Integer, 'nsteps/time', 'Time options', 'number of steps')
	at_nsteps.setDefault(0)
	
	# Regions ==================================================================================
	
	at_regions = mka(MpcAttributeType.IndexVector, 'Regions', 'Regions', 
			('Select one or multiple regions if you want to save results only on those parts of the model.'
			'Leave this vector empty (default) if you want to save results using the whole model.'))
	at_regions.indexSource.type = MpcAttributeIndexSourceType.AnalysisStep
	at_regions.indexSource.addAllowedNamespace("Misc_commands")
	at_regions.indexSource.addAllowedClass("region")
	
	# Make XOM ==================================================================================
	
	xom = MpcXObjectMetaData()
	xom.name = 'MPCORecorder'
	
	xom.addAttribute(at_recorders_name)
	
	xom.addAttribute(at_displacement)
	xom.addAttribute(at_rotation)
	xom.addAttribute(at_velocity)
	xom.addAttribute(at_angularVelocity)
	xom.addAttribute(at_acceleration)
	xom.addAttribute(at_angularAcceleration)
	xom.addAttribute(at_reactionForce)
	xom.addAttribute(at_reactionMoment)
	xom.addAttribute(at_reactionForceIncludingInertia)
	xom.addAttribute(at_reactionMomentIncludingInertia)
	xom.addAttribute(at_rayleighForce)
	xom.addAttribute(at_rayleighMoment)
	xom.addAttribute(at_pressure)
	xom.addAttribute(at_modesOfVibration)
	xom.addAttribute(at_modesOfVibrationRotational)
	
	xom.addAttribute(at_force)
	xom.addAttribute(at_deformation)
	xom.addAttribute(at_localForce)
	xom.addAttribute(at_damage)
	xom.addAttribute(at_equivalentPlasticStrain)
	xom.addAttribute(at_cw)
	xom.addAttribute(at_section_force)
	xom.addAttribute(at_section_deformation)
	xom.addAttribute(at_material_stress)
	xom.addAttribute(at_material_strain)
	xom.addAttribute(at_material_damage)
	xom.addAttribute(at_material_equivalentPlasticStrain)
	xom.addAttribute(at_material_cw)
	xom.addAttribute(at_section_fiber_stress)
	xom.addAttribute(at_section_fiber_strain)
	xom.addAttribute(at_section_fiber_damage)
	xom.addAttribute(at_section_fiber_equivalentPlasticStrain)
	xom.addAttribute(at_section_fiber_cw)
	
	xom.addAttribute(at_custom)
	
	xom.addAttribute(at_opt_time_type)
	xom.addAttribute(at_dt)
	xom.addAttribute(at_nsteps)
	xom.addAttribute(at_use_always)
	xom.addAttribute(at_use_dt)
	xom.addAttribute(at_use_nsteps)
	
	xom.addAttribute(at_regions)
	
	# visibility dependencies

	xom.setBooleanAutoExclusiveDependency(at_opt_time_type, at_use_always)
	xom.setBooleanAutoExclusiveDependency(at_opt_time_type, at_use_dt)
	xom.setBooleanAutoExclusiveDependency(at_opt_time_type, at_use_nsteps)

	xom.setVisibilityDependency(at_use_dt, at_dt)
	xom.setVisibilityDependency(at_use_nsteps, at_nsteps)
	
	return xom

def writeTcl(pinfo):
	
	xobj = pinfo.analysis_step.XObject
	
	def geta(name):
		a = xobj.getAttribute(name)
		if(a is None):
			raise Exception('Error: cannot find "{}" attribute'.format(name))
		return a
		
	################################################################
	# write command for database name
	################################################################
	
	mpco_file_name = geta('name').string
	# make sure file path is not empty
	mpco_file_name = mpco_file_name.strip()
	if not mpco_file_name:
		raise Exception(
			'MPCORecorder Error: The file name cannot be empty!.\n'
			'please choose a correct file name.')
	# make sure the directory already exists
	# but we allow a null dir, meaning it will be considered as a relative path
	mpco_file_dir = os.path.dirname(mpco_file_name)
	if mpco_file_dir and not os.path.exists(mpco_file_dir):
		raise Exception(
			'MPCORecorder Error: The specified directory ("{}") does not exists!.\n'
			'please choose a correct file name.'.format(mpco_file_dir))
	# make sure the file name is not empty
	if not os.path.basename(mpco_file_name):
		raise Exception(
			'MPCORecorder Error: The file name cannot be empty!.\n'
			'please choose a correct file name.')
	# make sure the file name does not contain unicode chars, hdf5 cannot handle them!
	invalid_chars = []
	for ichar in mpco_file_name:
		if ord(ichar) >= 128:
			invalid_chars.append(ichar)
	if len(invalid_chars) > 0:
		invalid_chars = set(invalid_chars)
		raise Exception(
			'MPCORecorder Error: The file name cannot contain Unicode characters.\n'
			'The following invalid characters ({}) were found in "{}".'
			.format(
				', '.join('"{}"'.format(ic) for ic in invalid_chars),
				mpco_file_name
				)
			)
	
	# remove extension, it will be added automatically later on
	if mpco_file_name.endswith('.mpco'):
		mpco_file_name = mpco_file_name[0:len(mpco_file_name)-5]
	
	if pinfo.process_count > 1:
		pinfo.out_file.write('\n{}recorder mpco "{}.part-$process_id.mpco"'.format(pinfo.indent, mpco_file_name))
	else:
		pinfo.out_file.write('\n{}recorder mpco "{}.mpco"'.format(pinfo.indent, mpco_file_name))
	
	################################################################
	# write command for nodal results
	################################################################
	
	sopt = ''
	
	if geta('displacement').boolean:
		sopt += ' "displacement"'
	if geta('rotation').boolean:
		sopt += ' "rotation"'
	if geta('velocity').boolean:
		sopt += ' "velocity"'
	if geta('angularVelocity').boolean:
		sopt += ' "angularVelocity"'
	if geta('acceleration').boolean:
		sopt += ' "acceleration"'
	if geta('angularAcceleration').boolean:
		sopt += ' "angularAcceleration"'
	if geta('reactionForce').boolean:
		sopt += ' "reactionForce"'
	if geta('reactionMoment').boolean:
		sopt += ' "reactionMoment"'
	if geta('reactionForceIncludingInertia').boolean:
		sopt += ' "reactionForceIncludingInertia"'
	if geta('reactionMomentIncludingInertia').boolean:
		sopt += ' "reactionMomentIncludingInertia"'
	if geta('rayleighForce').boolean:
		sopt += ' "rayleighForce"'
	if geta('rayleighMoment').boolean:
		sopt += ' "rayleighMoment"'
	if geta('pressure').boolean:
		sopt += ' "pressure"'
	if geta('modesOfVibration').boolean:
		sopt += ' "modesOfVibration"'
	if geta('modesOfVibrationRotational').boolean:
		sopt += ' "modesOfVibrationRotational"'
	
	if sopt:
		pinfo.out_file.write(' \\\n{}-N{}'.format(pinfo.indent, sopt))
		sopt = ''
	
	################################################################
	# write command for output frequency
	################################################################
	
	if geta('dt').boolean:
		sopt += ' dt {}'.format(geta('dt/time').real)
	
	if geta('nsteps').boolean:
		sopt += ' nsteps {}'.format(geta('nsteps/time').integer)
	
	if sopt:
		pinfo.out_file.write(' \\\n{}-T{}'.format(pinfo.indent, sopt))
		sopt = ''
	
	################################################################
	# write command for built-int element results
	################################################################
	
	if geta('force').boolean:
		sopt += ' "force"'
	if geta('deformation').boolean:
		sopt += ' "deformation"'
	if geta('localForce').boolean:
		sopt += ' "localForce"'
	if geta('damage').boolean:
		sopt += ' "damage"'
	if geta('equivalentPlasticStrain').boolean:
		sopt += ' "equivalentPlasticStrain"'
	if geta('cw').boolean:
		sopt += ' "cw"'
	if geta('section.force').boolean:
		sopt += ' "section.force"'
	if geta('section.deformation').boolean:
		sopt += ' "section.deformation"'
	if geta('material.stress').boolean:
		sopt += ' "material.stress"'
	if geta('material.strain').boolean:
		sopt += ' "material.strain"'
	if geta('material.damage').boolean:
		sopt += ' "material.damage"'
	if geta('material.equivalentPlasticStrain').boolean:
		sopt += ' "material.equivalentPlasticStrain"'
	if geta('material.cw').boolean:
		sopt += ' "material.cw"'
	if geta('section.fiber.stress').boolean:
		sopt += ' "section.fiber.stress"'
	if geta('section.fiber.strain').boolean:
		sopt += ' "section.fiber.strain"'
	if geta('section.fiber.damage').boolean:
		sopt += ' "section.fiber.damage"'
	if geta('section.fiber.equivalentPlasticStrain').boolean:
		sopt += ' "section.fiber.equivalentPlasticStrain"'
	if geta('section.fiber.cw').boolean:
		sopt += ' "section.fiber.cw"'
	
	if sopt:
		pinfo.out_file.write(' \\\n{}-E{}'.format(pinfo.indent, sopt))
		sopt = ''
	
	################################################################
	# write command for custom element results
	################################################################
	
	custom = geta('custom').stringVector
	if len(custom) > 0:
		pinfo.out_file.write(' \\\n')
		pinfo.out_file.write('-E {}'.format(' '.join(['"{}"'.format(item) for item in custom])))
	
	################################################################
	# write command for regions
	################################################################
	
	regions = geta('Regions').indexVector
	if len(regions) > 0:
		pinfo.out_file.write(' \\\n')
		pinfo.out_file.write(' \\\n'.join(['-R {}'.format(item) for item in regions]))
	
	################################################################
	# write the cdata file in the same location and 
	# with the same name as the mpco file
	################################################################
	
	doc = App.caeDocument()
	if doc is not None:
		if pinfo.process_count > 1:
			for i in range(pinfo.process_count):
				cdata_filename = '{}.part-{}.mpco.cdata'.format(mpco_file_name, i)
				if not os.path.isabs(cdata_filename):
					cdata_filename = os.path.normpath(os.path.join(pinfo.out_dir, cdata_filename))
				cdata_io = MpcMeshIOMpcoCdata(cdata_filename)
				cdata_io.setPartition(i)
				cdata_io.write(doc.mesh)
		else:
			cdata_filename = '{}.mpco.cdata'.format(mpco_file_name)
			if not os.path.isabs(cdata_filename):
				cdata_filename = os.path.normpath(os.path.join(pinfo.out_dir, cdata_filename))
			cdata_io = MpcMeshIOMpcoCdata(cdata_filename)
			cdata_io.write(doc.mesh)
	
	################################################################
	# write the last newline
	################################################################
	
	pinfo.out_file.write("\n")
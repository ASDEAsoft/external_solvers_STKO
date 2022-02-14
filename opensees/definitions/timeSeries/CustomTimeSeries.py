import PyMpc.Units as u
from PyMpc import *
from mpc_utils_html import *
import PyMpc
import PyMpc.Math
import math
import opensees.utils.tcl_input as tclin

from scipy.signal import chirp, spectrogram
from scipy.fft import fft, ifft
import numpy as np
#import eqsig

def makeXObjectMetaData():
	
	# Function
	at_Function = MpcAttributeMetaData()
	at_Function.type = MpcAttributeType.String
	at_Function.name = '__mpc_function__'
	at_Function.group = 'Group'
	at_Function.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Function')+'<br/>') + 
		html_par('') +
		html_par(html_href('','')+'<br/>') +
		html_end()
		)
	at_Function.editable = False
	
	# Select type of custom time series
	at_selectType = MpcAttributeMetaData()
	at_selectType.type = MpcAttributeType.String
	at_selectType.name = 'Select_Type'
	at_selectType.group = 'Group'
	at_selectType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Select Type of Custom time series')+'<br/>') +
		html_par('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_selectType.sourceType = MpcAttributeSourceType.List
	at_selectType.setSourceList(['SineSweep',
								'WhiteNoise'])
	at_selectType.setDefault('SineSweep')
	
	# SineSweep
	at_sineSweep = MpcAttributeMetaData()
	at_sineSweep.type = MpcAttributeType.Boolean
	at_sineSweep.name = 'SineSweep'
	at_sineSweep.group = 'Group'
	at_sineSweep.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Sine Sweep')+'<br/>') + 
		html_par('') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXX','Sine Sweep')+'<br/>') +
		html_end()
		)
	at_sineSweep.editable = False
	
	# f0
	at_f0 = MpcAttributeMetaData()
	at_f0.type = MpcAttributeType.Real
	at_f0.name = 'f0'
	at_f0.group = '-frequency'
	at_f0.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('f0')+'<br/>') + 
		html_par('Initial frequency.') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_f0.setDefault(2.0)
		
	# f1
	at_f1 = MpcAttributeMetaData()
	at_f1.type = MpcAttributeType.Real
	at_f1.name = 'f1'
	at_f1.group = '-frequency'
	at_f1.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('f1')+'<br/>') + 
		html_par('Final frequency.') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_f1.setDefault(1.0)
	
	# amplitude
	at_amplitude = MpcAttributeMetaData()
	at_amplitude.type = MpcAttributeType.Real
	at_amplitude.name = 'Amplitude'
	at_amplitude.group = '-Amplitude'
	at_amplitude.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Amplitude signal')+'<br/>') + 
		html_par('Amplitude signal.') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_amplitude.setDefault(0.1)
	
	
	# time of octaves
	at_timeForOctaves = MpcAttributeMetaData()
	at_timeForOctaves.type = MpcAttributeType.Real
	at_timeForOctaves.name = 'timeForOctaves'
	at_timeForOctaves.group = '-timeForOctaves'
	at_timeForOctaves.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Time of octaves')+'<br/>') + 
		html_par('Time of octaves.') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_timeForOctaves.setDefault(30.0)
		
	# Division
	at_Division = MpcAttributeMetaData()
	at_Division.type = MpcAttributeType.Real
	at_Division.name = 'Division'
	at_Division.group = '-Division'
	at_Division.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Division')+'<br/>') + 
		html_par('Division.') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_Division.setDefault(1000.0)
	
	# WhiteNoise
	at_WhiteNoise = MpcAttributeMetaData()
	at_WhiteNoise.type = MpcAttributeType.Boolean
	at_WhiteNoise.name = 'WhiteNoise'
	at_WhiteNoise.group = 'Group'
	at_WhiteNoise.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('White Noise')+'<br/>') + 
		html_par('WhiteNoise') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_WhiteNoise.editable = False
	
	# ScaleF
	at_ScaleF = MpcAttributeMetaData()
	at_ScaleF.type = MpcAttributeType.Real
	at_ScaleF.name = 'ScaleF'
	at_ScaleF.group = '-Scale'
	at_ScaleF.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('ScaleF')+'<br/>') + 
		html_par('Scale Facor.') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_ScaleF.setDefault(1.0)
	
	# fmin
	at_fmin = MpcAttributeMetaData()
	at_fmin.type = MpcAttributeType.Real
	at_fmin.name = 'fmin'
	at_fmin.group = '-frequency'
	at_fmin.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fmin')+'<br/>') + 
		html_par('Minimum frequency.') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_fmin.setDefault(100.0)
	
	# fmax
	at_fmax = MpcAttributeMetaData()
	at_fmax.type = MpcAttributeType.Real
	at_fmax.name = 'fmax'
	at_fmax.group = '-frequency'
	at_fmax.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('fmax')+'<br/>') + 
		html_par('Maximum frequency.') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_fmax.setDefault(500.0)
	
	
	# Sample Rate
	at_SampleRate = MpcAttributeMetaData()
	at_SampleRate.type = MpcAttributeType.Real
	at_SampleRate.name = 'SampleRate'
	at_SampleRate.group = '-Sample'
	at_SampleRate.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Sample Rate')+'<br/>') + 
		html_par('Sample Rate.') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_SampleRate.setDefault(2000.0)
		
	# Number of Samples
	at_NSamples = MpcAttributeMetaData()
	at_NSamples.type = MpcAttributeType.Integer
	at_NSamples.name = 'NSamples'
	at_NSamples.group = '-Sample'
	at_NSamples.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Number of Samples')+'<br/>') + 
		html_par('Number of Samples.') +
		html_par(html_href('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX','Custom TimeSeries')+'<br/>') +
		html_end()
		)
	at_NSamples.setDefault(3500)
	
	
	# PLOT OPTION
	# Data type
	
	at_DataType = MpcAttributeMetaData()
	at_DataType.type = MpcAttributeType.String
	at_DataType.name = 'Data_Type_Plot'
	at_DataType.group = 'Plot Options'
	at_DataType.description = (
		html_par(html_begin()) +
		html_par(html_boldtext('Data type')+'<br/>') + 
		html_par('Data type') +
		html_end()
		)
	at_DataType.sourceType = MpcAttributeSourceType.List
	at_DataType.setSourceList(['TimeSeries',
								'FourierSpectra',
								'ResponceSpectra'])
	at_DataType.setDefault('TimeSeries')
	
	
	xom = MpcXObjectMetaData()
	xom.name = 'CustomTimeSeries'
	xom.addAttribute(at_Function)
	xom.addAttribute(at_selectType)
	xom.addAttribute(at_sineSweep)
	xom.addAttribute(at_f0)
	xom.addAttribute(at_f1)
	xom.addAttribute(at_amplitude)
	xom.addAttribute(at_timeForOctaves)
	xom.addAttribute(at_Division)
	xom.addAttribute(at_WhiteNoise)
	xom.addAttribute(at_ScaleF)
	xom.addAttribute(at_fmin)
	xom.addAttribute(at_fmax)
	xom.addAttribute(at_SampleRate)
	xom.addAttribute(at_NSamples)
	xom.addAttribute(at_DataType)
	
	# Sine Sweep-dep
	xom.setVisibilityDependency(at_sineSweep, at_f0)
	xom.setVisibilityDependency(at_sineSweep, at_f1)
	xom.setVisibilityDependency(at_sineSweep, at_amplitude)
	xom.setVisibilityDependency(at_sineSweep, at_timeForOctaves)
	xom.setVisibilityDependency(at_sineSweep, at_Division)
	
	# Sine Sweep-dep
	xom.setVisibilityDependency(at_WhiteNoise, at_fmin)
	xom.setVisibilityDependency(at_WhiteNoise, at_fmax)
	xom.setVisibilityDependency(at_WhiteNoise, at_SampleRate)
	xom.setVisibilityDependency(at_WhiteNoise, at_NSamples)
	xom.setVisibilityDependency(at_WhiteNoise, at_ScaleF)

	
	# auto-exclusive dependencies
	# constant or non_constant
	xom.setBooleanAutoExclusiveDependency(at_selectType, at_sineSweep)
	xom.setBooleanAutoExclusiveDependency(at_selectType, at_WhiteNoise)
	
	return xom

def evaluateFunctionAttribute(xobj):
	if(xobj is None):
		print('Error: xobj is null\n')
		return PyMpc.Math.mat()
	
	if(xobj.name != 'CustomTimeSeries'):
		print('Error: invalid xobj type, expected "CustomTimeSeries", given "{}"'.format(xobj.name))
		return PyMpc.Math.mat()
	
	func_at = xobj.getAttribute('__mpc_function__')
	if(func_at is None):
		print('Error: cannot find "__mpc_function__" attribute\n')
		return PyMpc.Math.mat()
		
	selectType_at = xobj.getAttribute('Select_Type')
	if(selectType_at is None):
		print('Error: cannot find "Select_Type" attribute\n')
		return PyMpc.Math.mat()
		
	SineSweep_at = xobj.getAttribute('SineSweep')
	if(SineSweep_at is None):
		print('Error: cannot find "SineSweep" attribute\n')
		return PyMpc.Math.mat()
		
	WhiteNoise_at = xobj.getAttribute('WhiteNoise')
	if(WhiteNoise_at is None):
		print('Error: cannot find "WhiteNoise" attribute\n')
		return PyMpc.Math.mat()
		
		
	DataTypePlot_at = xobj.getAttribute('Data_Type_Plot')
	if(WhiteNoise_at is None):
		print('Error: cannot find "Data_Type_Plot" attribute\n')
		return PyMpc.Math.mat()
		
	DataTypePlot_at = DataTypePlot_at.string
		
	SineSweep = SineSweep_at.boolean
	WhiteNoise = WhiteNoise_at.boolean
	
	
	ScaleF = 1.0
			
	if(SineSweep == True):
	
		f0_at = xobj.getAttribute('f0')
		if(f0_at is None):
			print('Error: cannot find "f0" attribute\n')
			return PyMpc.Math.mat()
			
		f1_at = xobj.getAttribute('f1')
		if(f1_at is None):
			print('Error: cannot find "f1" attribute\n')
			return PyMpc.Math.mat()
			
		Amplitude_at = xobj.getAttribute('Amplitude')
		if(Amplitude_at is None):
			print('Error: cannot find "Amplitude" attribute\n')
			return PyMpc.Math.mat()
			
		timeForOctaves_at = xobj.getAttribute('timeForOctaves')
		if(timeForOctaves_at is None):
			print('Error: cannot find "timeForOctaves" attribute\n')
			return PyMpc.Math.mat()
		
		Division_at = xobj.getAttribute('Division')
		if(Division_at is None):
			print('Error: cannot find "Division" attribute\n')
			return PyMpc.Math.mat()
			
		f0=f0_at.real
		f1=f1_at.real
		
		Amplitude=Amplitude_at.real
		timeForOctaves=timeForOctaves_at.real
		Division=Division_at.real
		
		NOctave=int(np.log(f0/f1)/np.log(2))
		t1=timeForOctaves*NOctave
		f0_last=f1
		
		for i in range(0,NOctave):
			f0_last=f0_last*2
			f0=f0_last
		
		t = np.linspace(0, timeForOctaves*NOctave, timeForOctaves*NOctave*Division)
		x = chirp(t, f0=f0, f1=f1, t1=t1, method='linear')*Amplitude
		
		xy = PyMpc.Math.mat(len(x), 2)
		
		for i in range(len(t)):
			xy[i, 0] = t[i]
			xy[i, 1] = x[i]
		
		
	
	if(WhiteNoise == True):
	
		fmin_at = xobj.getAttribute('fmin')
		if(fmin_at is None):
			print('Error: cannot find "fmin" attribute\n')
			return PyMpc.Math.mat()
			
		fmax_at = xobj.getAttribute('fmax')
		if(fmax_at is None):
			print('Error: cannot find "fmax" attribute\n')
			return PyMpc.Math.mat()
			
		SampleRate_at = xobj.getAttribute('SampleRate')
		if(SampleRate_at is None):
			print('Error: cannot find "SampleRate" attribute\n')
			return PyMpc.Math.mat()
			
		NSamples_at = xobj.getAttribute('NSamples')
		if(NSamples_at is None):
			print('Error: cannot find "NSamples" attribute\n')
			return PyMpc.Math.mat()
			
		ScaleF_at = xobj.getAttribute('ScaleF')
		if(ScaleF_at is None):
			print('Error: cannot find "ScaleF" attribute\n')
			return PyMpc.Math.mat()
	
		def fftnoise(f):
			f = np.array(f, dtype='complex')
			Np = (len(f) - 1) // 2
			phases = np.random.rand(Np) * 2 * np.pi
			phases = np.cos(phases) + 1j * np.sin(phases)
			f[1:Np+1] *= phases
			f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
		
			return np.fft.ifft(f).real
		
		def band_limited_noise(min_freq, max_freq, samples, samplerate):
			freqs = np.abs(np.fft.fftfreq(samples, 1/samplerate))
			f = np.zeros(samples)
			idx = np.where(np.logical_and(freqs>=min_freq, freqs<=max_freq))[0]
			f[idx] = 1
			
			return fftnoise(f)
		
		ScaleF=ScaleF_at.real
		Fmin=fmin_at.real
		Fmax=fmax_at.real
		SampleRate=SampleRate_at.real
		Sample=NSamples_at.integer
		
		
		Durate=Sample*(1/SampleRate)
		t=np.linspace(0.0,Durate,int(SampleRate*(Sample/SampleRate)))
		
		
		x = band_limited_noise(Fmin, Fmax, Sample, SampleRate)
		x = x * (2**15 - 1)
		
		xy = PyMpc.Math.mat(len(x), 2)
		x=list(x)
		
		for i in range(len(x)):
			xy[i, 0] = t[i]
			xy[i, 1] = x[i]*ScaleF
			
			
	# if DataTypePlot_at=='FourierSpectra':
	
		# org_signal = eqsig.Signal(x, t[1]-t[0])
		
		# Tmax=5.0
		# d_step = Tmax / 100
		# T = np.arange(d_step * 1, Tmax, d_step)
		
		# org_signal.gen_fa_spectrum()
		
		# FuSpec=abs(org_signal.fa_spectrum)
		# FuFreq=org_signal.fa_frequencies
		
		# xy = PyMpc.Math.mat(len(FuFreq), 2)
		
		
		# for i in range(len(FuFreq)):
			# xy[i, 0] = FuFreq[i]
			# xy[i, 1] = FuSpec[i]
	
	# if DataTypePlot_at=='ResponceSpectra':
	
		# org_signal = eqsig.AccSignal(x, t[1]-t[0])
		
		# Tmax=5.0
		# d_step = Tmax / 100
		# T = np.arange(d_step * 1, Tmax, d_step)
		# xy = PyMpc.Math.mat(len(T), 2)
		# org_signal.generate_response_spectrum(response_times=T,xi=0.05)
		
		# SpSc=org_signal.s_a
		
		
		# for i in range(len(SpSc)):
			# xy[i, 0] = T[i]
			# xy[i, 1] = SpSc[i]

	
	return xy

def writeTcl(pinfo):
	
	xobj = pinfo.definition.XObject
	
	ClassName = xobj.name
	if pinfo.currentDescription != ClassName:
		pinfo.out_file.write('\n{}# {} {}\n'.format(pinfo.indent, xobj.Xnamespace, ClassName))
		pinfo.currentDescription = ClassName
	
	tag = xobj.parent.componentId
	
	sopt = ''	#optional string
	
	#with both 'SineSweep' and 'WhiteNoise'

	Amplitude_at = xobj.getAttribute('Amplitude')
	if(Amplitude_at is None):
		raise Exception('Error: cannot find "Amplitude" attribute')
	Amplitude = Amplitude_at.real
	#sopt += ' -factor {}'.format(Amplitude)
	
	
	SineSweep_at = xobj.getAttribute('SineSweep')
	if(SineSweep_at is None):
		raise Exception('Error: cannot find "SineSweep" attribute')
	SineSweep = SineSweep_at.boolean
	
	WhiteNoise_at = xobj.getAttribute('WhiteNoise')
	if(WhiteNoise_at is None):
		raise Exception('Error: cannot find "WhiteNoise" attribute')
	WhiteNoise = WhiteNoise_at.boolean

	
	if SineSweep:
		# with 'SineSweep'
		#timeSeries Path $tag -time {list_of_times} -values {list_of_values} <-factor $Amplitude> <-useLast>
		
		f0_at = xobj.getAttribute('f0')
		if(f0_at is None):
			raise Exception('Error: cannot find "f0" attribute')
		f0 = f0_at.real
		
		f1_at = xobj.getAttribute('f1')
		if(f1_at is None):
			raise Exception('Error: cannot find "f1" attribute')
		f1 = f1_at.real
	
		timeForOctaves_at = xobj.getAttribute('timeForOctaves')
		if(timeForOctaves_at is None):
			raise Exception('Error: cannot find "timeForOctaves" attribute')
		timeForOctaves = timeForOctaves_at.real
		
		Division_at = xobj.getAttribute('Division')
		if(Division_at is None):
			raise Exception('Error: cannot find "Division" attribute')
		Division = Division_at.real
		
		
		NOctave=int(np.log(f0/f1)/np.log(2))
		t1=timeForOctaves*NOctave
		f0_last=f1
		
		for i in range(0,NOctave):
			f0_last=f0_last*2
			f0=f0_last
		
		t = np.linspace(0, timeForOctaves*NOctave, timeForOctaves*NOctave*Division)
		w = chirp(t, f0=f0, f1=f1, t1=t1, method='linear')*Amplitude
		
		listTimes = t
		listValues = w
		
		#set list TCL
		times_str = 'set timeSeries_list_of_times_{}'.format(tag)+' {'
		values_str = 'set timeSeries_list_of_values_{}'.format(tag)+' {'
		
		nLettersT = len(times_str)
		nLettersV = len(values_str)
		nTabT = nLettersT // 4
		nTabV = nLettersV // 4
		
		n = 1
		for i in range(len(listTimes)):
			if (i == (10*n)):
				times_str += '\\\n{}{}'.format(pinfo.indent, tclin.utils.nIndent(nTabT))
				values_str += '\\\n{}{}'.format(pinfo.indent, tclin.utils.nIndent(nTabV))
				n += 1
			if (i!=len(listTimes)-1):
				times_str += '{} '.format(listTimes[i])
				values_str += '{} '.format(listValues[i])
			else:
				times_str += '{}'.format(listTimes[i])
				values_str += '{}'.format(listValues[i])
		
		times_str += '}\n'
		values_str += '}\n'
		pinfo.out_file.write(times_str)
		pinfo.out_file.write(values_str)
		
		#end list TCL
		#now write the 'non_constant' string into the file
		str_tcl = '{0}timeSeries Path {1} -time $timeSeries_list_of_times_{1} -values $timeSeries_list_of_values_{1}{2}\n'.format(pinfo.indent, tag, sopt)
		
	if(WhiteNoise == True):
	
		ScaleF_at = xobj.getAttribute('ScaleF')
		if(ScaleF_at is None):
			raise Exception('Error: cannot find "ScaleF" attribute')
		ScaleF = ScaleF_at.real
		
		fmin_at = xobj.getAttribute('fmin')
		if(fmin_at is None):
			raise Exception('Error: cannot find "fmin" attribute')
		Fmin = fmin_at.real
			
		fmax_at = xobj.getAttribute('fmax')
		if(fmax_at is None):
			raise Exception('Error: cannot find "fmax" attribute')
		Fmax = fmax_at.real
		
		SampleRate_at = xobj.getAttribute('SampleRate')
		if(SampleRate_at is None):
			raise Exception('Error: cannot find "SampleRate" attribute')
		SampleRate = SampleRate_at.real
			
		NSamples_at = xobj.getAttribute('NSamples')
		if(NSamples_at is None):
			raise Exception('Error: cannot find "NSamples" attribute')
		Sample = NSamples_at.integer
		
	
		def fftnoise(f):
			f = np.array(f, dtype='complex')
			Np = (len(f) - 1) // 2
			phases = np.random.rand(Np) * 2 * np.pi
			phases = np.cos(phases) + 1j * np.sin(phases)
			f[1:Np+1] *= phases
			f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
		
			return np.fft.ifft(f).real
		
		def band_limited_noise(min_freq, max_freq, samples, samplerate):
			freqs = np.abs(np.fft.fftfreq(samples, 1/samplerate))
			f = np.zeros(samples)
			idx = np.where(np.logical_and(freqs>=min_freq, freqs<=max_freq))[0]
			f[idx] = 1
			
			return fftnoise(f)
		
		
		Durate=Sample*(1/SampleRate)
		t=np.linspace(0.0,Durate,int(SampleRate*(Sample/SampleRate)))
		
		
		x = band_limited_noise(Fmin, Fmax, Sample, SampleRate)
		x = x * (2**15 - 1)
		
		x=[xi*ScaleF for xi in x]
		
		listTimes = t
		listValues = x
		
		#set list TCL
		times_str = 'set timeSeries_list_of_times_{}'.format(tag)+' {'
		values_str = 'set timeSeries_list_of_values_{}'.format(tag)+' {'
		
		nLettersT = len(times_str)
		nLettersV = len(values_str)
		nTabT = nLettersT // 4
		nTabV = nLettersV // 4
		
		n = 1
		for i in range(len(listTimes)):
			if (i == (10*n)):
				times_str += '\\\n{}{}'.format(pinfo.indent, tclin.utils.nIndent(nTabT))
				values_str += '\\\n{}{}'.format(pinfo.indent, tclin.utils.nIndent(nTabV))
				n += 1
			if (i!=len(listTimes)-1):
				times_str += '{} '.format(listTimes[i])
				values_str += '{} '.format(listValues[i])
			else:
				times_str += '{}'.format(listTimes[i])
				values_str += '{}'.format(listValues[i])
		
		times_str += '}\n'
		values_str += '}\n'
		pinfo.out_file.write(times_str)
		pinfo.out_file.write(values_str)
		
		#end list TCL
		#now write the 'non_constant' string into the file
		str_tcl = '{0}timeSeries Path {1} -time $timeSeries_list_of_times_{1} -values $timeSeries_list_of_values_{1}{2}\n'.format(pinfo.indent, tag, sopt)
	
	pinfo.out_file.write(str_tcl)
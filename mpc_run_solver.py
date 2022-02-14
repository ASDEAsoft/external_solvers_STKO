def run(wdir, command, script, np, do_pause):
	import os
	import subprocess
	import platform

	def error():
		raise Exception(
			'Run Solver function not yet implemented for platform: {} - {}'.format(
				platform.system(), 
				platform.dist()))
	
	def getfiles(directory):
		return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

	runner_base_name = 'RunSolver'
	monitor_base_name = 'LaunchSTKOMonitor'
	
	if platform.system() == 'Linux':
		
		if platform.dist()[0] == 'Ubuntu':
			# create and launch solver runner script
			runner_name = '{}.sh'.format(runner_base_name)
			fname = os.path.join(wdir, runner_name)
			with open(fname, 'w+') as f:
				f.write('#!/bin/sh\n')
				f.write('"{}" "{}" {}\n'.format(command, script, np))
				if do_pause:
					f.write('read -p "Press [Enter] key to continue..." dummy')
			os.chmod(fname, 0o777)
			subprocess.Popen(['gnome-terminal', '--', './{}'.format(runner_name)], cwd=wdir)
			# launch monitor
			monitor_name = '{}.sh'.format(monitor_base_name)
			if monitor_name in getfiles(wdir):
				subprocess.Popen(['sh', './{}'.format(monitor_name)], cwd=wdir)
			
		else:
			# todo: implement for other platforms
			error()
		
		
	elif platform.system() == 'Windows':
		# create and launch solver runner script
		runner_name = '{}.bat'.format(runner_base_name)
		fname = os.path.join(wdir, runner_name)
		with open(fname, 'w+') as f:
			f.write('"{}" "{}" {}'.format(command.replace('/', '\\'), script.replace('/', '\\'), np))
			if do_pause:
				f.write(' & pause')
			else:
				f.write('\n')
		current_wdir = os.getcwd()
		try:
			os.chdir(wdir)
			subprocess.Popen(runner_name)
			# launch monitor
			monitor_name = '{}.bat'.format(monitor_base_name)
			if monitor_name in getfiles(wdir):
				subprocess.Popen(monitor_name, creationflags=0x08000000)
		finally:
			os.chdir(current_wdir)
	
	else:
		# todo: implement for other platforms
		error()

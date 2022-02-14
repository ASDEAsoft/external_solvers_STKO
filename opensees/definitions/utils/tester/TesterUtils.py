## @package TesterUtils
# The TesterUtils packages contains utility functions commonly used by all testers
# to promote code re-use

from io import StringIO
import subprocess

# converts a list of floats to a string buffer
# ready to be written in a tcl file. long lists are
# arranged in multiple lines with 10 items each
def listToStringBuffer(_data):
	buffer = StringIO()
	i = 0
	for idata in _data:
		i = i+1
		buffer.write('{} '.format(idata))
		if i == 10 :
			buffer.write('\\\n')
			i = 0
	return buffer

# define a function to run a process async and to
# communicate with it in real time
def executeAsync(command, working_dir):
	# Make process
	if platform.system() == 'Windows':
		process = subprocess.Popen(
			command, shell=False, 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
			creationflags=0x08000000, cwd=working_dir)
	else:
		process = subprocess.Popen(
			command, shell=False, 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
			cwd=working_dir)
	# Poll process for new output until finished
	while process.poll() is None:
		nextline = process.stdout.readline().decode().rstrip()
		yield nextline
	# do the same with the remaining output if any...
	output = process.communicate()[0]
	for nextline in output.decode().splitlines():
		yield nextline
	exitCode = process.returncode
	if (exitCode != 0):
		raise Exception(command, exitCode, output)

## a simple class that tells how to treat a tensor component
# in nD material tester, i.e. if the component is strain or stress controlled
# and, if strain controlled, if the component used the input strain history or
# a fixed value
class TensorComponentData:
	# contants
	STRESS = 1
	STRAIN = 2 
	TESTED = 1
	FIXED = 2
	# constructor
	def __init__(self, control=STRAIN, type=FIXED, value=0.0):
		# component can be either strain or stress controlled
		self.control = control
		# component can be either fixed or controlled by the testing strain cycle
		# in case self.control = STRAIN
		self.type = type
		# the reference value in case self.type is fixed
		self.value = value
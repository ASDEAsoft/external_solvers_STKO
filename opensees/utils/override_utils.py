def get_function_from_module(mod, fun):
	import sys
	import inspect
	module = sys.modules[mod]
	if fun in dir(module) and inspect.isfunction(getattr(module, fun)):
		_old = getattr(module, fun)
	else:
		_old = None
	return _old
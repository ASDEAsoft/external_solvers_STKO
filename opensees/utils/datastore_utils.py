from PyMpc import MpcIndexWrapper, MpcIndexVectorWrapper, MpcIndexWrapperUtils
import json

# Encoder
class MpcDataStoreEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, MpcIndexWrapper):
			# call the c++ code utility to encode in a string
			return MpcIndexWrapperUtils.encodeIndex(o)
		elif isinstance(o, MpcIndexVectorWrapper):
			# call the c++ code utility to encode in a string
			return MpcIndexWrapperUtils.encodeIndexVector(o)
		# fallback to default implementation
		return json.JSONEncoder.default(self, o)

# Decoder
class MpcDataStoreDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
	def _process_dict(self, dct):
		for k,v in dct.items():
			if isinstance(v, dict):
				# recursive call to support nested dicts
				dct[k] = self._process_dict(v)
			elif isinstance(v, str):
				# if it is a string, it may be convertible
				if MpcIndexWrapperUtils.canDecodeIndex(v):
					dct[k] = MpcIndexWrapperUtils.decodeIndex(v)
				elif MpcIndexWrapperUtils.canDecodeIndexVector(v):
					dct[k] = MpcIndexWrapperUtils.decodeIndexVector(v)
		return dct
	def object_hook(self, dct):
		return self._process_dict(dct)
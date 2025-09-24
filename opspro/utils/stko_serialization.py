'''
This module provides a class decorator to make classes serializable to and from a base64 string using pickle.
'''

import pickle
import base64

def serializable(cls):
    """
    A class decorator to make a class serializable to a base64 string using pickle.
    """
    def serialize(self) -> str:
        pickled_data = pickle.dumps(self)
        base64_data = base64.b64encode(pickled_data).decode('utf-8')
        return base64_data

    @classmethod
    def deserialize(cls, base64_string):
        pickled_data = base64.b64decode(base64_string.encode('utf-8'))
        obj = pickle.loads(pickled_data)
        if not isinstance(obj, cls):
            raise TypeError(f"Deserialized object is not of type {cls.__name__}")
        return obj

    cls.serialize = serialize
    cls.deserialize = deserialize
    return cls
# flexparser, flexcache, pint
import opspro.parameters.UnitSystemTools as UnitSystemTools
from asteval import Interpreter
import pint
import math
import numpy as np
import itertools
from typing import List

class _silent_writer:
    @staticmethod
    def write(msg):
        ...

def _make_protected_dict() -> dict:
    """
    Creates and returns a dictionary of safe functions and constants for use in user expressions.

    The returned dictionary includes:
        - All public functions and constants from the `math` module.
        - Mathematical constants `pi` and `e`.
        - The `numpy` module as `np`.
        - A helper function `_OPUNIT` for handling units via `ParameterManager.ureg`.

    Returns:
        dict: A dictionary containing safe math functions, constants, numpy as `np`, and a unit helper function.
    """
    # add safe math functions for user expressions
    safe_dict = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    safe_dict.update({"pi": math.pi, "e": math.e})
    # add numpy as np
    safe_dict['np'] = np
    # add helper function to handle units
    safe_dict[UnitSystemTools._OPUNIT_FUN_NAME] = lambda u: ParameterManager.ureg(u)
    # done
    return safe_dict

# a global singleton to manage parameters
class ParameterManager:

    # the unit registry
    ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)

    unit_common_symbols = UnitSystemTools.build_common_unit_symbols(ureg)
    unit_common_quantity_map = UnitSystemTools.build_common_quantity_map(ureg)

    # a default dictionary of safe math functions for user expressions
    safe_dict = _make_protected_dict()

    # a global asteval interpreter, built with the default safe_dict
    evaluator = Interpreter(symtable=safe_dict, writer=_silent_writer, err_writer=_silent_writer) 

    # prevent instantiation
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Cannot instantiate ParameterManager, use class methods only")

    @staticmethod
    def getAllSymbols() -> List[str]:
        # return a sorted list of parameter names (TODO), symbols in the safe_dict, and units
        return sorted(itertools.chain(
            ParameterManager.safe_dict.keys(), 
            ParameterManager.unit_common_symbols
            ))

    @staticmethod
    def reset():
        # remove from safe_dict any custom parameters added, i.e. those not in the original safe_dict
        current_keys = set(ParameterManager.evaluator.symtable.keys())
        pass

    @staticmethod
    def evaluate(expr: str) -> pint.Quantity:
        expr_processed = UnitSystemTools.preprocess_units(expr)
        retval = ParameterManager.evaluator(expr_processed)
        if isinstance(retval, (int, float, np.ndarray)):
            return retval * ParameterManager.ureg.dimensionless
        elif isinstance(retval, pint.Quantity):
            return retval
        else:
            extra = ''
            if len(ParameterManager.evaluator.error) > 0:
                extra = '<br>' + '<br>'.join(['{}:{}'.format(*err.get_error()) for err in ParameterManager.evaluator.error])
                ParameterManager.evaluator.error = []
            raise ValueError(f"Expression \"{expr}\" did not evaluate to a number or quantity.{extra}")
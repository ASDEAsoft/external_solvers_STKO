# flexparser, flexcache, pint
from asteval import Interpreter
import pint
import math
import numpy as np
import itertools
from typing import List


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
    safe_dict['_OPUNIT'] = lambda u: ParameterManager.ureg(u)
    # done
    return safe_dict

def _preprocess_units(expr: str) -> str:
    """
    Preprocesses a unit expression string by replacing square brackets with a function call,
    stripping whitespace, and removing a leading asterisk if present.

    Args:
        expr (str): The unit expression string to preprocess.

    Returns:
        str: The preprocessed unit expression string.
    """
    # Step 1 + 2: blunt replacement
    expr = expr.replace('[', '* _OPUNIT("').replace(']', '")')
    # Step 3: strip leading/trailing spaces
    expr = expr.strip()
    # Step 4: if it starts with '*', drop it
    if expr.startswith('*'):
        expr = expr[1:].lstrip()
    return expr

# a global singleton to manage parameters
class ParameterManager:

    # the unit registry
    ureg = pint.UnitRegistry()

    # a default dictionary of safe math functions for user expressions
    safe_dict = _make_protected_dict()

    # a global asteval interpreter, built with the default safe_dict
    aeval = Interpreter(symtable=safe_dict) 

    # prevent instantiation
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Cannot instantiate ParameterManager, use class methods only")

    @staticmethod
    def getAllSymbols() -> List[str]:
        # return a sorted list of parameter names (TODO), symbols in the safe_dict, and units
        return sorted(itertools.chain(ParameterManager.safe_dict.keys(), ParameterManager.ureg))

    @staticmethod
    def reset():
        # remove from safe_dict any custom parameters added, i.e. those not in the original safe_dict
        current_keys = set(ParameterManager.aeval.symtable.keys())
        pass

    @staticmethod
    def evaluate(expr: str) -> pint.Quantity:
        expr_processed = _preprocess_units(expr)
        retval = ParameterManager.aeval(expr_processed)
        if isinstance(retval, (int, float, np.ndarray)):
            return retval * ParameterManager.ureg.dimensionless
        elif isinstance(retval, pint.Quantity):
            return retval
        else:
            # TODO: improve error handling
            raise ValueError(f"Expression did not evaluate to a number or quantity: {expr}")
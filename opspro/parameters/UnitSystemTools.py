import pint
import itertools
from typing import List, Dict

_OPUNIT_FUN_NAME = '_OPUNIT'
_OPUNIT_FUN_MATCH_1 = '* _OPUNIT("'
_OPUNIT_FUN_MATCH_2 = '")'

def preprocess_units(expr: str) -> str:
    """
    Preprocesses a unit expression string by replacing square brackets with a function call,
    stripping whitespace, and removing a leading asterisk if present.

    Args:
        expr (str): The unit expression string to preprocess.

    Returns:
        str: The preprocessed unit expression string.
    """
    # Step 1 + 2: blunt replacement
    expr = expr.replace('[', _OPUNIT_FUN_MATCH_1).replace(']', _OPUNIT_FUN_MATCH_2)
    # Step 3: strip leading/trailing spaces
    expr = expr.strip()
    # Step 4: if it starts with '*', drop it
    if expr.startswith('*'):
        expr = expr[1:].lstrip()
    return expr

def build_common_unit_symbols(ureg : pint.UnitRegistry) -> List[str]:
    """
    Build a list of common unit symbols for various physical quantities.
    This function defines and aggregates commonly used unit symbols,
    including both SI and non-SI units (such as Imperial, US customary, and other widely used units).
    It is intended to provide a comprehensive set of unit abbreviations for use with a Pint UnitRegistry.
    Parameters:
        ureg (pint.UnitRegistry): The Pint UnitRegistry instance used to validate or process unit symbols.
    Returns:
        List[str]: A list of unit symbol strings representing common units for length, mass, time, force, pressure etc... .
    """

    LENGTH = [
        # SI (restricted to 1e-9 .. 1e+9 m)
        'nm',   # nanometer (1e-9 m)
        'um',   # micrometer (1e-6 m)
        'mm',   # millimeter (1e-3 m)
        'cm',   # centimeter (1e-2 m)
        'dm',   # decimeter (1e-1 m)
        'm',    # meter (base)
        'dam',  # decameter (1e1 m)
        'hm',   # hectometer (1e2 m)
        'km',   # kilometer (1e3 m)
        'Mm',   # megameter (1e6 m)
        'Gm',   # gigameter (1e9 m)

        # Imperial / US customary
        'in',   # inch
        'ft',   # foot
        'yd',   # yard
        'mi',   # mile

        # Nautical
        'nmi',  # nautical mile

        # Astronomical
        'au',   # astronomical unit
        'ly',   # light-year
        'pc',   # parsec
    ]

    MASS = [
        # SI (restricted to 1e-9 g .. 1e+9 g)
        'ng',   # nanogram (1e-9 g)
        'ug',   # microgram (1e-6 g)
        'mg',   # milligram (1e-3 g)
        'cg',   # centigram (1e-2 g)
        'dg',   # decigram (1e-1 g)
        'g',    # gram (base for prefixes, even though SI base is kg)
        'dag',  # decagram (1e1 g)
        'hg',   # hectogram (1e2 g)
        'kg',   # kilogram (1e3 g, official SI base)
        'Mg',   # megagram (1e6 g) = metric ton (t)
        'Gg',   # gigagram (1e9 g)

        # SI alias
        't',    # tonne (metric ton, 1e3 kg = 1 Mg)

        # Imperial / US customary
        'oz',    # ounce
        'lb',    # pound
        'stone', # stone
        'cwt',   # hundredweight (UK/US differ, but commonly known)
        'ton',   # short ton (US customary)
    ]
    
    TIME = [
        # SI (restricted to 1e-9 .. 1e+9 s)
        'ns',   # nanosecond (1e-9 s)
        'us',   # microsecond (1e-6 s)
        'ms',   # millisecond (1e-3 s)
        'cs',   # centisecond (1e-2 s)
        'ds',   # decisecond (1e-1 s)
        's',    # second (base)
        'das',  # decasecond (1e1 s)
        'hs',   # hectosecond (1e2 s)
        'ks',   # kilosecond (1e3 s)
        'Ms',   # megasecond (1e6 s)
        'Gs',   # gigasecond (1e9 s)

        # Common multiples (non-SI but widely used)
        'min',  # minute
        'h',    # hour
        'd',    # day
        'week', # week
        'yr',   # year
    ]

    FORCE = [
        # SI (restricted to 1e-9 .. 1e+9 N)
        'nN',   # nanonewton (1e-9 N)
        'uN',   # micronewton (1e-6 N)
        'mN',   # millinewton (1e-3 N)
        'cN',   # centinewton (1e-2 N)
        'dN',   # decinewton (1e-1 N)
        'N',    # newton (base)
        'daN',  # decanewton (1e1 N)
        'hN',   # hectonewton (1e2 N)
        'kN',   # kilonewton (1e3 N)
        'MN',   # meganewton (1e6 N)
        'GN',   # giganewton (1e9 N)

        # Non-SI but used
        'kpond',   # kilopond (aka kilogram-force, obsolete but still seen)

        # Imperial / US customary
        'lbf',  # pound-force
        'ozf',  # ounce-force
        'tf', # ton-force (short ton-force, sometimes kip for 1000 lbf)
        'ton_force', # metric ton-force (t)
        'kip',  # kip (1000 lbf, common in structural engineering)
    ]
    
    PRESSURE = [
        # SI (restricted to 1e-9 .. 1e+9 Pa)
        'nPa',  # nanopascal (1e-9 Pa)
        'uPa',  # micropascal (1e-6 Pa)
        'mPa',  # millipascal (1e-3 Pa)
        'cPa',  # centipascal (1e-2 Pa)
        'dPa',  # decipascal (1e-1 Pa)
        'Pa',   # pascal (base)
        'daPa', # decapascal (1e1 Pa)
        'hPa',  # hectopascal (1e2 Pa) = millibar, common in meteorology
        'kPa',  # kilopascal (1e3 Pa)
        'MPa',  # megapascal (1e6 Pa)
        'GPa',  # gigapascal (1e9 Pa)

        # Common non-SI
        'bar',   # bar (1e5 Pa)
        'mbar',  # millibar (100 Pa), meteorology
        'atm',   # standard atmosphere (101325 Pa)
        'torr',  # 1/760 atm ≈ 133.3 Pa
        'mmHg',  # millimeter of mercury
        'inHg',  # inch of mercury
        'psi',   # pounds per square inch
    ]

    TEMPERATURE = [
        'K',    # kelvin (base)
        'degC', # degree Celsius
        'degF', # degree Fahrenheit
        'degR', # degree Rankine
    ]

    ANGLE = [
        'rad',  # radian (base)
        'deg', '°',  # degree
        'grad', # gradian
        'arcmin', # arcminute
        'arcsec', # arcsecond
    ]

    return list(itertools.chain(
        LENGTH,
        MASS,
        TIME,
        FORCE,
        PRESSURE,
        TEMPERATURE,
        ANGLE
    ))

def build_common_quantity_map(ureg : pint.UnitRegistry) -> Dict[str, str]:
    """
    Builds a mapping from dimensionality strings (as produced by Pint's UnitRegistry)
    to common physical quantity names.
    Args:
        ureg (pint.UnitRegistry): The unit registry instance from Pint, used to generate dimensionalities.
    Returns:
        Dict[str, str]: A dictionary mapping the string representation of dimensionalities
                        to human-readable names of physical quantities (e.g., 'Length', 'Force', 'Energy').
    Notes:
        - The mapping covers basic, derived, force-related, energy, density, and cross-sectional quantities.
        - Multiple physical quantities may share the same dimensionality and are separated by semicolons in the values.
    """
    return {
        # Basics
        str((ureg.m).dimensionality): 'Length',
        str((ureg.kg).dimensionality): 'Mass',
        str((ureg.s).dimensionality): 'Time',
        str((ureg.K).dimensionality): 'Temperature',

        # Derived
        str((ureg.m / ureg.s).dimensionality): 'Velocity',
        str((ureg.m / ureg.s**2).dimensionality): 'Acceleration',

        # Force-related
        str((ureg.N).dimensionality): 'Force; Moment-Per-Unit-Length',
        str((ureg.N*ureg.m).dimensionality): 'Moment; Work; Energy',
        str((ureg.N/ureg.m).dimensionality): 'Stiffness; Force-Per-Unit-Length',
        str((ureg.N/ureg.m**2).dimensionality): 'Pressure; Stress; Material-Modulus(E, G, K); Energy-Density',

        # energy
        str((ureg.J).dimensionality): 'Energy; Work; Moment',
        str((ureg.W).dimensionality): 'Power',

        # Densities
        str((ureg.kg/ureg.m**3).dimensionality): 'Mass-Density',
        str((ureg.N/ureg.m**3).dimensionality): 'Weight-Density',

        # Cross-Sectional-related
        str((ureg.m**2).dimensionality): 'Area',
        str((ureg.m**3).dimensionality): 'Volume; First-Moment-Area; Static-Moment',
        str((ureg.m**4).dimensionality): 'Second-Moment-Area; Area-Moment-of-Inertia',

    }

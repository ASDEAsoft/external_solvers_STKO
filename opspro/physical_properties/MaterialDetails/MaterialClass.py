from dataclasses import dataclass, field
from opspro.utils.stko_serialization import serializable

@dataclass
@serializable
class MaterialClass:
    E: float = 0.0
    v: float = 0.0
    rho: float = 0.0
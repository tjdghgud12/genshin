from .claymore import info as claymoreGetFightProp
from .polearm import info as polearmGetFightProp
from .sword import info as swordGetFightProp
from .catalyst import info as catalystGetFightProp
from .bow import info as bowGetFightProp

getTotalWeaponFightProp = {
    **claymoreGetFightProp,
    **polearmGetFightProp,
    **swordGetFightProp,
    **catalystGetFightProp,
    **bowGetFightProp,
}

__all__ = ["getTotalWeaponFightProp"]

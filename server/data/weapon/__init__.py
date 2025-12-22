from .claymore import weaponInfo as claymoreWeaponInfo
from .polearm import weaponInfo as polearmWeaponInfo
from .sword import weaponInfo as swordWeaponInfo
from .catalyst import weaponInfo as catalystWeaponInfo
from .bow import weaponInfo as bowWeaponInfo

weaponInfo = {
    **claymoreWeaponInfo,
    **polearmWeaponInfo,
    **swordWeaponInfo,
    **catalystWeaponInfo,
    **bowWeaponInfo,
}

__all__ = ["weaponInfo"]

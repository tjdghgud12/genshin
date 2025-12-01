from data.character import fightPropTemplate
import data.weapon as weaponData
from services.ambrApi import getAmbrApi
from schemas.fightProp import fightPropSchema
from ambr import AmbrAPI, WeaponDetail, WeaponPromote
from copy import deepcopy


async def getWeaponBaseFightProp(id: int, level: int) -> fightPropSchema:
    ambrApi: AmbrAPI = await getAmbrApi()
    ambrWeaponCurveInfo = weaponData.ambrWeaponCurve[str(level)]["curveInfos"]
    ambrWeaponDetail: WeaponDetail = await ambrApi.fetch_weapon_detail(id)

    fightProp = deepcopy(fightPropTemplate)

    promoteStat = max(
        (promote for promote in ambrWeaponDetail.upgrade.promotes if promote.unlock_max_level <= level),
        key=lambda x: x.unlock_max_level,
        default=WeaponPromote,
    )

    for baseStat in ambrWeaponDetail.upgrade.base_stats:
        if baseStat.prop_type is not None:
            fightProp.add(baseStat.prop_type, baseStat.init_value * ambrWeaponCurveInfo[baseStat.growth_type])
    for addStat in getattr(promoteStat, "add_stats", []):
        fightProp.add(addStat.id, addStat.value)

    return fightProp

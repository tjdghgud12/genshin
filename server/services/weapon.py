from fastapi import HTTPException, Depends
from typing import cast
from ambr import AmbrAPI, WeaponDetail, WeaponPromote
from services.ambrApi import getAmbrApi
from data.character import CharacterFightPropType
import data.weapon as weaponData


def genWeaponList():
    # 여기는 ambr을 통해서 통합 무기 list를 제작 예정
    # front에게 넘겨주기 위한 데이터
    weaponList = []

    return weaponList


def weaponFightPropInit() -> CharacterFightPropType:
    fightProp: CharacterFightPropType = cast(CharacterFightPropType, {key: 0.0 for key in CharacterFightPropType.__annotations__.keys()})
    return fightProp


async def getAmosBow(id: int, level: int, refinement: int, options: dict) -> CharacterFightPropType:
    ambrApi: AmbrAPI = await getAmbrApi()
    optionRefinementMap = [[0.12, 0.08], [0.15, 0.10], [0.18, 0.12], [0.21, 0.14], [0.24, 0.16]]

    fightProp: CharacterFightPropType = weaponFightPropInit()
    ambrWeaponCurve = weaponData.ambrWeaponCurve[str(level)]["curveInfos"]
    ambrWeaponDetail: WeaponDetail = await ambrApi.fetch_weapon_detail(id)

    refinementValue = optionRefinementMap[refinement - 1]

    promoteStat = max(
        (promote for promote in ambrWeaponDetail.upgrade.promotes if promote.unlock_max_level <= level),
        key=lambda x: x.unlock_max_level,
        default=WeaponPromote,
    )

    for baseStat in ambrWeaponDetail.upgrade.base_stats:
        if baseStat.prop_type is not None:
            fightProp[baseStat.prop_type] = baseStat.init_value * ambrWeaponCurve[baseStat.growth_type]
    for addStat in promoteStat.add_stats or []:
        fightProp[addStat.id] += addStat.value

    for i, option in enumerate(options):
        value = refinementValue[i]
        fightProp["FIGHT_PROP_NOMAL_ATTACK_ATTACK_ADD_HURT"] += value if i == 0 else value * option["stack"]
        fightProp["FIGHT_PROP_CHARGED_ATTACK_ATTACK_ADD_HURT"] += value if i == 0 else value * option["stack"]

    return fightProp


getTotalWeaponFightProp = {"아모스의 활": getAmosBow}

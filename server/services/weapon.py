from fastapi import HTTPException, Depends
from typing import cast
from ambr import AmbrAPI, WeaponDetail, WeaponPromote
from services.ambrApi import getAmbrApi
from data.character import CharacterFightPropType, fightPropTemplate
import data.weapon as weaponData


def genWeaponList():
    # 여기는 ambr을 통해서 통합 무기 list를 제작 예정
    # front에게 넘겨주기 위한 데이터
    weaponList = []

    return weaponList


async def getWeaponBaseFightProp(id: int, level: int) -> CharacterFightPropType:
    ambrApi: AmbrAPI = await getAmbrApi()
    ambrWeaponCurve = weaponData.ambrWeaponCurve[str(level)]["curveInfos"]
    ambrWeaponDetail: WeaponDetail = await ambrApi.fetch_weapon_detail(id)

    fightProp: CharacterFightPropType = {**fightPropTemplate}

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

    return fightProp


async def getAmosBowFightProp(id: int, level: int, refinement: int, options: dict) -> CharacterFightPropType:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.12, 0.08], [0.15, 0.10], [0.18, 0.12], [0.21, 0.14], [0.24, 0.16]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            fightProp["FIGHT_PROP_NOMAL_ATTACK_ATTACK_ADD_HURT"] += value if i == 0 else value * option["stack"]
            fightProp["FIGHT_PROP_CHARGED_ATTACK_ATTACK_ADD_HURT"] += value if i == 0 else value * option["stack"]

    return fightProp


async def getMistsplitterReforgedFightProp(id: int, level: int, refinement: int, options: dict) -> CharacterFightPropType:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.12, [0.08, 0.16, 0.28]], [0.15, [0.10, 0.20, 0.35]], [0.18, [0.12, 0.24, 0.42]], [0.21, [0.14, 0.28, 0.49]], [0.24, [0.16, 0.32, 0.56]]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            fightProp["FIGHT_PROP_ATTACK_ADD_HURT"] += value if i == 0 else value[int(option["stack"]) - 1]

    return fightProp


async def getLionsRoarFightProp(id: int, level: int, refinement: int, options: dict) -> CharacterFightPropType:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.2], [0.24], [0.28], [0.32], [0.36]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            fightProp["FIGHT_PROP_ATTACK_ADD_HURT"] += value

    return fightProp


getTotalWeaponFightProp = {"아모스의 활": getAmosBowFightProp, "안개를 가르는 회광": getMistsplitterReforgedFightProp, "용의 포효": getLionsRoarFightProp}

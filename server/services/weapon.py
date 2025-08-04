from fastapi import HTTPException, Depends
from typing import cast, TypedDict, Literal
from ambr import AmbrAPI, WeaponDetail, WeaponPromote
from services.ambrApi import getAmbrApi
from data.character import CharacterFightPropSchema, fightPropTemplate
from data.globalVariable import fightPropKeys
import data.weapon as weaponData


class WeaponDataReturnSchema(TypedDict, total=True):
    fightProp: CharacterFightPropSchema
    afterAddProps: list[str]
    afterAddFlag: bool


def genWeaponList():
    # 여기는 ambr을 통해서 통합 무기 list를 제작 예정
    # front에게 넘겨주기 위한 데이터
    weaponList = []

    return weaponList


async def getWeaponBaseFightProp(id: int, level: int) -> CharacterFightPropSchema:
    ambrApi: AmbrAPI = await getAmbrApi()
    ambrWeaponCurve = weaponData.ambrWeaponCurve[str(level)]["curveInfos"]
    ambrWeaponDetail: WeaponDetail = await ambrApi.fetch_weapon_detail(id)

    fightProp: CharacterFightPropSchema = {**fightPropTemplate}

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


async def getAmosBowFightProp(id: int, level: int, refinement: int, options: dict) -> CharacterFightPropSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.12, 0.08], [0.15, 0.10], [0.18, 0.12], [0.21, 0.14], [0.24, 0.16]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            fightProp[fightPropKeys.NOMAL_ATTACK_ATTACK_ADD_HURT.value] += value if i == 0 else value * option["stack"]
            fightProp[fightPropKeys.CHARGED_ATTACK_ATTACK_ADD_HURT.value] += value if i == 0 else value * option["stack"]

    return fightProp


async def getMistsplitterReforgedFightProp(id: int, level: int, refinement: int, options: dict) -> CharacterFightPropSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.12, [0.08, 0.16, 0.28]], [0.15, [0.10, 0.20, 0.35]], [0.18, [0.12, 0.24, 0.42]], [0.21, [0.14, 0.28, 0.49]], [0.24, [0.16, 0.32, 0.56]]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            fightProp[fightPropKeys.ATTACK_ADD_HURT.value] += value if i == 0 else value[int(option["stack"]) - 1]

    return fightProp


async def getLionsRoarFightProp(id: int, level: int, refinement: int, options: dict) -> CharacterFightPropSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.2], [0.24], [0.28], [0.32], [0.36]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            fightProp[fightPropKeys.ATTACK_ADD_HURT.value] += value

    return fightProp


async def getAThousandFloatingDreamsFightProp(id: int, level: int, refinement: int, options: dict) -> CharacterFightPropSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[32, 0.10], [40, 0.14], [48, 0.18], [56, 0.22], [64, 0.26]]
    refinementValue = optionRefinementMap[refinement - 1]
    if options[0]["stack"] == 3 and options[1]["stack"] == 3:
        options[0]["stack"] = 2

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            key = fightPropKeys.ELEMENT_MASTERY.value if i == 0 else fightPropKeys.ATTACK_ADD_HURT.value
            fightProp[key] += value * option["stack"]

    return fightProp


async def getEngulfingLightningFightProp(id: int, level: int, refinement: int, options: dict) -> CharacterFightPropSchema:
    # 여기서 fightProp뿐만 아니라 추후 연산에 대한 정보도 넘겨줘야해.
    # 그래야 추후 연산할 때 또 다시 호출해서 연산 진행할 테니까.
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.30, [0.28, 0.80]],
        [0.35, [0.35, 0.90]],
        [0.40, [0.42, 0.100]],
        [0.45, [0.49, 0.110]],
        [0.50, [0.56, 0.120]],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            key = fightPropKeys.CHARGE_EFFICIENCY if i == 0 else fightPropKeys.ATTACK_ADD_HURT
            # 진행 중

            fightProp[key.value] += value

    # fightProp["afterAddProps"] = [fightPropKeys.ATTACK_ADD_HURT]

    return fightProp


getTotalWeaponFightProp = {
    "아모스의 활": getAmosBowFightProp,
    "안개를 가르는 회광": getMistsplitterReforgedFightProp,
    "용의 포효": getLionsRoarFightProp,
    "떠오르는 천일 밤의 꿈": getAThousandFloatingDreamsFightProp,
    "예초의 번개": getEngulfingLightningFightProp,
}

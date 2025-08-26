from typing import TypedDict
from ambr import AmbrAPI, WeaponDetail, WeaponPromote
from services.ambrApi import getAmbrApi
from data.character import fightPropTemplate
from models.character import CharacterFightPropModel
from data.globalVariable import fightPropKeys
import data.weapon as weaponData
from copy import deepcopy


class WeaponDataReturnSchema(TypedDict, total=True):
    fightProp: CharacterFightPropModel
    afterAddProps: list[str] | None


async def getWeaponBaseFightProp(id: int, level: int) -> CharacterFightPropModel:
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


async def getAmosBowFightProp(id: int, level: int, refinement: int, options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.12, 0.08], [0.15, 0.10], [0.18, 0.12], [0.21, 0.14], [0.24, 0.16]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i] if i == 0 else refinementValue[i] * option["stack"]
            fightProp.add(fightPropKeys.NOMAL_ATTACK_ATTACK_ADD_HURT.value, value)
            fightProp.add(fightPropKeys.CHARGED_ATTACK_ATTACK_ADD_HURT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getMistsplitterReforgedFightProp(id: int, level: int, refinement: int, options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.12, [0.08, 0.16, 0.28]], [0.15, [0.10, 0.20, 0.35]], [0.18, [0.12, 0.24, 0.42]], [0.21, [0.14, 0.28, 0.49]], [0.24, [0.16, 0.32, 0.56]]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i] if i == 0 else refinementValue[i][int(option["stack"]) - 1]
            fightProp.add(fightPropKeys.ATTACK_ADD_HURT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getLionsRoarFightProp(id: int, level: int, refinement: int, options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.2], [0.24], [0.28], [0.32], [0.36]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            fightProp.add(fightPropKeys.ATTACK_ADD_HURT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getAThousandFloatingDreamsFightProp(id: int, level: int, refinement: int, options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[32, 0.10], [40, 0.14], [48, 0.18], [56, 0.22], [64, 0.26]]
    refinementValue = optionRefinementMap[refinement - 1]
    if options[0]["stack"] == 3 and options[1]["stack"] == 3:
        options[0]["stack"] = 2
        options[1]["stack"] = 2

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            key = fightPropKeys.ELEMENT_MASTERY.value if i == 0 else fightPropKeys.ATTACK_ADD_HURT.value
            fightProp.add(key, value * option["stack"])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getEngulfingLightningFightProp(id: int, level: int, refinement: int, options: dict, characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.30, [0.28, 0.80]],
        [0.35, [0.35, 0.90]],
        [0.40, [0.42, 1]],
        [0.45, [0.49, 1.10]],
        [0.50, [0.56, 1.20]],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            key = fightPropKeys.CHARGE_EFFICIENCY.value if i == 0 else fightPropKeys.ATTACK_PERCENT.value
            if i == 1:
                chargeEfficiency = getattr(characterFightProp, fightPropKeys.CHARGE_EFFICIENCY.value)
                addAttackPercent = value[0] * (chargeEfficiency - 1)
                if value[1] < addAttackPercent:
                    addAttackPercent = value[1]
                fightProp.add(key, addAttackPercent)
            else:
                fightProp.add(key, value)

    return {"fightProp": fightProp, "afterAddProps": [fightPropKeys.ATTACK_PERCENT.value]}


async def getStaffOfHomaFightProp(id: int, level: int, refinement: int, options: dict, characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.20, 0.008, 0.01],
        [0.25, 0.010, 0.012],
        [0.30, 0.012, 0.014],
        [0.35, 0.014, 0.016],
        [0.40, 0.016, 0.018],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            key = fightPropKeys.HP_PERCENT.value if i == 0 else fightPropKeys.ATTACK.value
            if i != 0:
                baseHp = getattr(characterFightProp, fightPropKeys.BASE_HP.value)
                hpPercent = getattr(characterFightProp, fightPropKeys.HP_PERCENT.value)
                hp = getattr(characterFightProp, fightPropKeys.HP.value)
                totalHp = baseHp * (hpPercent + 1) + hp
                addAttack = totalHp * value
                fightProp.add(key, addAttack)
            else:
                fightProp.add(key, value)

    return {"fightProp": fightProp, "afterAddProps": [fightPropKeys.ATTACK.value]}


async def getSplendorOfTranquilWatersFightProp(id: int, level: int, refinement: int, options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.08, 0.14],
        [0.10, 0.175],
        [0.12, 0.21],
        [0.14, 0.245],
        [0.16, 0.28],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            key = fightPropKeys.ELEMENT_SKILL_ATTACK_ADD_HURT.value if i == 0 else fightPropKeys.HP_PERCENT.value
            fightProp.add(key, value * option["stack"])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getAzurelightFightProp(id: int, level: int, refinement: int, options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.24, [0.24, 0.40]],
        [0.30, [0.30, 0.50]],
        [0.36, [0.36, 0.60]],
        [0.42, [0.42, 0.70]],
        [0.48, [0.48, 0.80]],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            value = refinementValue[i]
            match i:
                case 0:
                    fightProp.add(fightPropKeys.ATTACK_PERCENT.value, value)
                case 1:
                    fightProp.add(fightPropKeys.ATTACK_PERCENT.value, value[0])
                    fightProp.add(fightPropKeys.CRITICAL_HURT.value, value[1])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getSymphonistOfScentsFightProp(id: int, level: int, refinement: int, options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.12, 0.12, 0.32],
        [0.15, 0.15, 0.40],
        [0.18, 0.18, 0.48],
        [0.21, 0.21, 0.56],
        [0.24, 0.24, 0.64],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        value = refinementValue[i]
        match i:
            case 0:
                fightProp.add(fightPropKeys.ATTACK_PERCENT.value, value)
            case 1:
                if option["active"]:
                    fightProp.add(fightPropKeys.ATTACK_PERCENT.value, value)
            case 2:
                if option["active"]:
                    fightProp.add(fightPropKeys.ATTACK_PERCENT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getStarcallersWatchFightProp(id: int, level: int, refinement: int, options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [100, 0.28],
        [125, 0.35],
        [150, 0.42],
        [175, 0.49],
        [200, 0.56],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        value = refinementValue[i]
        match i:
            case 0:
                fightProp.add(fightPropKeys.ELEMENT_MASTERY.value, value)
            case 1:
                if option["active"]:
                    fightProp.add(fightPropKeys.ATTACK_ADD_HURT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getTomeOfTheEternalFlowFightProp(id: int, level: int, refinement: int, options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.16, 0.14],
        [0.20, 0.18],
        [0.24, 0.22],
        [0.28, 0.26],
        [0.32, 0.30],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        value = refinementValue[i]
        match i:
            case 0:
                fightProp.add(fightPropKeys.ELEMENT_MASTERY.value, value)
            case 1:
                fightProp.add(fightPropKeys.ATTACK_ADD_HURT.value, value * option["stack"])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getAThousandBlazingSunsFightProp(id: int, level: int, refinement: int, options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.20, 0.28],
        [0.25, 0.35],
        [0.30, 0.42],
        [0.35, 0.49],
        [0.40, 0.56],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option["active"]:
            match i:
                case 0:
                    fightProp.add(fightPropKeys.CRITICAL_HURT.value, refinementValue[0])
                    fightProp.add(fightPropKeys.ATTACK_PERCENT.value, refinementValue[1])
                case 1:
                    fightProp.add(fightPropKeys.CRITICAL_HURT.value, refinementValue[0] * 0.75)
                    fightProp.add(fightPropKeys.ATTACK_PERCENT.value, refinementValue[1] * 0.75)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getApprenticesNotesFightProp(id: int, level: int, _refinement: int, _options: dict, _characterFightProp: CharacterFightPropModel) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)

    return {"fightProp": fightProp, "afterAddProps": None}


getTotalWeaponFightProp = {
    "아모스의 활": getAmosBowFightProp,
    "안개를 가르는 회광": getMistsplitterReforgedFightProp,
    "용의 포효": getLionsRoarFightProp,
    "떠오르는 천일 밤의 꿈": getAThousandFloatingDreamsFightProp,
    "예초의 번개": getEngulfingLightningFightProp,
    "호마의 지팡이": getStaffOfHomaFightProp,
    "고요히 샘솟는 빛": getSplendorOfTranquilWatersFightProp,
    "창백한 섬광": getAzurelightFightProp,
    "맛의 지휘자": getSymphonistOfScentsFightProp,
    "별지기의 시선": getStarcallersWatchFightProp,
    "영원히 샘솟는 법전": getTomeOfTheEternalFlowFightProp,
    "학도의 노트": getApprenticesNotesFightProp,
    "타오르는 천 개의 태양": getAThousandBlazingSunsFightProp,
}

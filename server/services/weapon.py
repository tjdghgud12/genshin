from data.character import fightPropTemplate
from data.globalVariable import fightPropMpa
import data.weapon as weaponData
from services.ambrApi import getAmbrApi
from schemas.fightProp import fightPropSchema
from schemas.weapon import weaponDataSchema
from ambr import AmbrAPI, WeaponDetail, WeaponPromote
from copy import deepcopy
from typing import TypedDict


class WeaponDataReturnSchema(TypedDict, total=True):
    fightProp: fightPropSchema
    afterAddProps: list[str] | None


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


async def getAmosBowFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.12, 0.08], [0.15, 0.10], [0.18, 0.12], [0.21, 0.14], [0.24, 0.16]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            value = refinementValue[i] if i == 0 else refinementValue[i] * option.stack
            fightProp.add(fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_HURT.value, value)
            fightProp.add(fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_HURT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getMistsplitterReforgedFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.12, [0.08, 0.16, 0.28]], [0.15, [0.10, 0.20, 0.35]], [0.18, [0.12, 0.24, 0.42]], [0.21, [0.14, 0.28, 0.49]], [0.24, [0.16, 0.32, 0.56]]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            value = refinementValue[i] if i == 0 else refinementValue[i][int(option.stack) - 1]
            fightProp.add(fightPropMpa.FIRE_ADD_HURT.value, value)
            fightProp.add(fightPropMpa.WATER_ADD_HURT.value, value)
            fightProp.add(fightPropMpa.ELEC_ADD_HURT.value, value)
            fightProp.add(fightPropMpa.WIND_ADD_HURT.value, value)
            fightProp.add(fightPropMpa.GRASS_ADD_HURT.value, value)
            fightProp.add(fightPropMpa.ICE_ADD_HURT.value, value)
            fightProp.add(fightPropMpa.ROCK_ADD_HURT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getLionsRoarFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.2], [0.24], [0.28], [0.32], [0.36]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            value = refinementValue[i]
            fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getAThousandFloatingDreamsFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[32, 0.10], [40, 0.14], [48, 0.18], [56, 0.22], [64, 0.26]]
    refinementValue = optionRefinementMap[refinement - 1]
    if options[0].stack == 3 and options[1].stack == 3:
        options[0].stack = 2
        options[1].stack = 2

    for i, option in enumerate(options):
        if option.active:
            value = refinementValue[i]
            key = fightPropMpa.ELEMENT_MASTERY.value if i == 0 else fightPropMpa.ATTACK_ADD_HURT.value
            fightProp.add(key, value * option.stack)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getEngulfingLightningFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
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
        if option.active:
            value = refinementValue[i]
            key = fightPropMpa.CHARGE_EFFICIENCY.value if i == 0 else fightPropMpa.ATTACK_PERCENT.value
            if i == 1:
                chargeEfficiency = getattr(characterFightProp, fightPropMpa.CHARGE_EFFICIENCY.value)
                addAttackPercent = value[0] * (chargeEfficiency - 1)
                if value[1] < addAttackPercent:
                    addAttackPercent = value[1]
                fightProp.add(key, addAttackPercent)
            else:
                fightProp.add(key, value)

    return {"fightProp": fightProp, "afterAddProps": [fightPropMpa.ATTACK_PERCENT.value]}


async def getStaffOfHomaFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
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
        if option.active:
            value = refinementValue[i]
            key = fightPropMpa.HP_PERCENT.value if i == 0 else fightPropMpa.ATTACK.value
            if i != 0:
                baseHp = getattr(characterFightProp, fightPropMpa.BASE_HP.value)
                hpPercent = getattr(characterFightProp, fightPropMpa.HP_PERCENT.value)
                hp = getattr(characterFightProp, fightPropMpa.HP.value)
                totalHp = baseHp * (hpPercent + 1) + hp
                addAttack = totalHp * value
                fightProp.add(key, addAttack)
            else:
                fightProp.add(key, value)

    return {"fightProp": fightProp, "afterAddProps": [fightPropMpa.ATTACK.value]}


async def getSplendorOfTranquilWatersFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
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
        if option.active:
            value = refinementValue[i]
            key = fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value if i == 0 else fightPropMpa.HP_PERCENT.value
            fightProp.add(key, value * option.stack)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getAzurelightFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
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
        if option.active:
            value = refinementValue[i]
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, value)
                case 1:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, value[0])
                    fightProp.add(fightPropMpa.CRITICAL_HURT.value, value[1])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getSymphonistOfScentsFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
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
                fightProp.add(fightPropMpa.ATTACK_PERCENT.value, value)
            case 1:
                if option.active:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, value)
            case 2:
                if option.active:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getStarcallersWatchFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
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
                fightProp.add(fightPropMpa.ELEMENT_MASTERY.value, value)
            case 1:
                if option.active:
                    fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getTomeOfTheEternalFlowFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
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
                fightProp.add(fightPropMpa.ELEMENT_MASTERY.value, value)
            case 1:
                fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, value * option.stack)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getAThousandBlazingSunsFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
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
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.CRITICAL_HURT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[1])
                case 1:
                    fightProp.add(fightPropMpa.CRITICAL_HURT.value, refinementValue[0] * 0.75)
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[1] * 0.75)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getApprenticesNotesFightProp(
    id: int, level: int, _refinement: int, _options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getAbsolutionFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.20, 0.16],
        [0.25, 0.20],
        [0.30, 0.24],
        [0.35, 0.28],
        [0.40, 0.32],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.CRITICAL_HURT.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, refinementValue[1] * option.maxStack)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getCrimsonMoonsSemblanceFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.12, 0.24],
        [0.16, 0.32],
        [0.20, 0.40],
        [0.24, 0.48],
        [0.28, 0.56],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, refinementValue[1])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getTheUnforgedFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [0.04, 0.05, 0.06, 0.07, 0.08]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue * option.stack)
                case 1:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue * options[0].stack)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getVerdictFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.20, 0.18],
        [0.25, 0.225],
        [0.30, 0.27],
        [0.35, 0.315],
        [0.40, 0.36],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value, refinementValue[1] * option.stack)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getRustFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [0.4, 0.5, 0.6, 0.7, 0.8]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_HURT.value, refinementValue)
                case 1:
                    fightProp.add(fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_HURT.value, -0.1)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getThunderingPulseFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.20, [0, 0.12, 0.24, 0.40]],
        [0.25, [0, 0.15, 0.30, 0.50]],
        [0.30, [0, 0.18, 0.36, 0.60]],
        [0.35, [0, 0.21, 0.42, 0.70]],
        [0.40, [0, 0.24, 0.48, 0.80]],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_HURT.value, refinementValue[1][option.stack])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getSongOfBrokenPinesFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.16, 0.20],
        [0.20, 0.25],
        [0.24, 0.30],
        [0.28, 0.35],
        [0.32, 0.40],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[1])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getKagurasVerityFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.12, 0.12],
        [0.15, 0.15],
        [0.18, 0.18],
        [0.21, 0.21],
        [0.24, 0.24],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value, refinementValue[0] * option.stack)
                    if option.stack >= option.maxStack:
                        fightProp.add(fightPropMpa.FIRE_ADD_HURT.value, refinementValue[1])
                        fightProp.add(fightPropMpa.WATER_ADD_HURT.value, refinementValue[1])
                        fightProp.add(fightPropMpa.ELEC_ADD_HURT.value, refinementValue[1])
                        fightProp.add(fightPropMpa.WIND_ADD_HURT.value, refinementValue[1])
                        fightProp.add(fightPropMpa.GRASS_ADD_HURT.value, refinementValue[1])
                        fightProp.add(fightPropMpa.ICE_ADD_HURT.value, refinementValue[1])
                        fightProp.add(fightPropMpa.ROCK_ADD_HURT.value, refinementValue[1])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getTheWidsithFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        {"서장(공격력)": 0.60, "영탄곡(모든 원소 피해)": 0.48, "간주곡(원소 마스터리)": 240},
        {"서장(공격력)": 0.75, "영탄곡(모든 원소 피해)": 0.60, "간주곡(원소 마스터리)": 300},
        {"서장(공격력)": 0.90, "영탄곡(모든 원소 피해)": 0.72, "간주곡(원소 마스터리)": 360},
        {"서장(공격력)": 1.05, "영탄곡(모든 원소 피해)": 0.84, "간주곡(원소 마스터리)": 420},
        {"서장(공격력)": 1.20, "영탄곡(모든 원소 피해)": 0.96, "간주곡(원소 마스터리)": 480},
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    if option.select:
                        addList = []
                        if option.select == "서장(공격력)":
                            addList.append(fightPropMpa.ATTACK_PERCENT.value)
                        if option.select == "영탄곡(모든 원소 피해)":
                            addList.append(fightPropMpa.FIRE_ADD_HURT.value)
                            addList.append(fightPropMpa.WATER_ADD_HURT.value)
                            addList.append(fightPropMpa.ELEC_ADD_HURT.value)
                            addList.append(fightPropMpa.WIND_ADD_HURT.value)
                            addList.append(fightPropMpa.GRASS_ADD_HURT.value)
                            addList.append(fightPropMpa.ICE_ADD_HURT.value)
                            addList.append(fightPropMpa.ROCK_ADD_HURT.value)
                        if option.select == "간주곡(원소 마스터리)":
                            addList.append(fightPropMpa.ELEMENT_MASTERY.value)
                        for key in addList:
                            fightProp.add(key, refinementValue[option.select])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getFavoniusWarbowFightProp(
    id: int, level: int, _refinement: int, _options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getAmenomaKageuchiFightProp(
    id: int, level: int, _refinement: int, _options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getWolfFangFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.16, 0.02],
        [0.20, 0.025],
        [0.24, 0.03],
        [0.28, 0.035],
        [0.32, 0.04],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.ELEMENT_BURST_ATTACK_ADD_HURT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.ELEMENT_SKILL_CRITICAL.value, refinementValue[1] * option.stack)
                    fightProp.add(fightPropMpa.ELEMENT_BURST_CRITICAL.value, refinementValue[1] * option.stack)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getCalamityQuellerFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.12, 0.032],
        [0.15, 0.04],
        [0.18, 0.048],
        [0.21, 0.056],
        [0.24, 0.064],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.FIRE_ADD_HURT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.WATER_ADD_HURT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.ELEC_ADD_HURT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.WIND_ADD_HURT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.GRASS_ADD_HURT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.ICE_ADD_HURT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.ROCK_ADD_HURT.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[1] * option.stack)
                case 2:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[1] * options[1].stack)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getPrimordialJadeWingedSpearFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.032, 0.12],
        [0.039, 0.15],
        [0.046, 0.18],
        [0.053, 0.21],
        [0.060, 0.24],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[0] * option.stack)
                    if option.stack == option.maxStack:
                        fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, refinementValue[1])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getLostPrayerToTheSacredWindsFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [0.08, 0.10, 0.12, 0.14, 0.16]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.FIRE_ADD_HURT.value, refinementValue)
                    fightProp.add(fightPropMpa.WATER_ADD_HURT.value, refinementValue)
                    fightProp.add(fightPropMpa.ELEC_ADD_HURT.value, refinementValue)
                    fightProp.add(fightPropMpa.WIND_ADD_HURT.value, refinementValue)
                    fightProp.add(fightPropMpa.GRASS_ADD_HURT.value, refinementValue)
                    fightProp.add(fightPropMpa.ICE_ADD_HURT.value, refinementValue)
                    fightProp.add(fightPropMpa.ROCK_ADD_HURT.value, refinementValue)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getSacrificialJadeFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.32, 40],
        [0.4, 50],
        [0.48, 60],
        [0.56, 70],
        [0.64, 80],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.HP_PERCENT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.ELEMENT_MASTERY.value, refinementValue[1])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getLightofFoliarIncisionFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.04, 1.2],
        [0.05, 1.5],
        [0.06, 1.8],
        [0.07, 2.1],
        [0.08, 2.4],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.CRITICAL.value, refinementValue[0])
                case 1:
                    value = characterFightProp.FIGHT_PROP_ELEMENT_MASTERY * refinementValue[0]
                    fightProp.add(fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_POINT.value, value)
                    fightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_POINT.value, value)

    return {"fightProp": fightProp, "afterAddProps": [fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_POINT.value, fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_POINT.value]}


async def getWolfsGravestoneFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.2, 0.4],
        [0.25, 0.5],
        [0.3, 0.6],
        [0.35, 0.7],
        [0.4, 0.8],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[1])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getThrillingTalesofDragonSlayersFightProp(
    id: int, level: int, _refinement: int, _options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getSacrificialFragmentsFightProp(
    id: int, level: int, _refinement: int, _options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getDeathmatchFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.16, 0.24],
        [0.20, 0.30],
        [0.24, 0.36],
        [0.28, 0.42],
        [0.32, 0.48],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        match i:
            case 0:
                if option.active:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.DEFENSE_PERCENT.value, refinementValue[0])
                else:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, refinementValue[1])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getAquaSimulacraFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.16, 0.20],
        [0.20, 0.25],
        [0.24, 0.30],
        [0.28, 0.35],
        [0.32, 0.40],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.HP_PERCENT.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, refinementValue[1])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getFavoniusLanceFightProp(
    id: int, level: int, _refinement: int, _options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
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
    "사면": getAbsolutionFightProp,
    "붉은 달의 형상": getCrimsonMoonsSemblanceFightProp,
    "무공의 검": getTheUnforgedFightProp,
    "녹슨 활": getRustFightProp,
    "비뢰의 고동": getThunderingPulseFightProp,
    "송뢰가 울릴 무렵": getSongOfBrokenPinesFightProp,
    "카구라의 진의": getKagurasVerityFightProp,
    "음유시인의 악장": getTheWidsithFightProp,
    "페보니우스 활": getFavoniusWarbowFightProp,
    "아메노마 카게우치가타나": getAmenomaKageuchiFightProp,
    "늑대 송곳니": getWolfFangFightProp,
    "식재": getCalamityQuellerFightProp,
    "화박연": getPrimordialJadeWingedSpearFightProp,
    "사풍 원서": getLostPrayerToTheSacredWindsFightProp,
    "제사의 옥": getSacrificialJadeFightProp,
    "잎을 가르는 빛": getLightofFoliarIncisionFightProp,
    "늑대의 말로": getWolfsGravestoneFightProp,
    "드래곤 슬레이어 영웅담": getThrillingTalesofDragonSlayersFightProp,
    "제례의 악장": getSacrificialFragmentsFightProp,
    "결투의 창": getDeathmatchFightProp,
    "약수": getAquaSimulacraFightProp,
    "페보니우스 장창": getFavoniusLanceFightProp,
}

from data.globalVariable import fightPropMpa
from schemas.fightProp import fightPropSchema
from schemas.weapon import weaponDataSchema, WeaponDataReturnSchema
from services.weapon.commonData import getWeaponBaseFightProp


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


async def getFavoniusSwordFightProp(
    id: int, level: int, _refinement: int, _options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getPeakPatrolSongFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.08, 0.10, 0.08, 0.256],
        [0.10, 0.125, 0.10, 0.32],
        [0.12, 0.15, 0.12, 0.384],
        [0.14, 0.175, 0.14, 0.448],
        [0.16, 0.20, 0.16, 0.512],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    # 1. 방어력 8/10/12/14/16% 증가
                    fightProp.add(fightPropMpa.DEFENSE_PERCENT.value, refinementValue[0] * option.stack)
                    # 2. 모든 원소 피해 보너스 10/12.5/15/17.5/20% 증가
                    value = refinementValue[1] * option.stack
                    fightProp.add(fightPropMpa.FIRE_ADD_HURT.value, value)
                    fightProp.add(fightPropMpa.WATER_ADD_HURT.value, value)
                    fightProp.add(fightPropMpa.ELEC_ADD_HURT.value, value)
                    fightProp.add(fightPropMpa.WIND_ADD_HURT.value, value)
                    fightProp.add(fightPropMpa.GRASS_ADD_HURT.value, value)
                    fightProp.add(fightPropMpa.ICE_ADD_HURT.value, value)
                    fightProp.add(fightPropMpa.ROCK_ADD_HURT.value, value)
                    # 3. 해당 효과 2스택 중첩 또는 2스택의 지속 시간 갱신 시, 장착 캐릭터의 방어력에 기반해 1000pt마다 파티 내 주변에 있는 모든 캐릭터의 모든 원소 피해 보너스가 8/10/12/14/16% 증가하고,
                    # 최대 25.6/32/38.4/44.8/51.2%까지 증가한다.
                    if option.stack == option.maxStack:
                        baseDefense = characterFightProp.FIGHT_PROP_BASE_DEFENSE
                        characterDefense = characterFightProp.FIGHT_PROP_DEFENSE
                        characterDefensePercent = characterFightProp.FIGHT_PROP_DEFENSE_PERCENT
                        characterDefenseTotal = baseDefense * (characterDefensePercent + 1)
                        characterDefenseTotal = characterDefenseTotal + characterDefense
                        additionalElementHurt = round(characterDefenseTotal / 1000 * refinementValue[2], 1)

                        if additionalElementHurt > refinementValue[3]:
                            additionalElementHurt = refinementValue[3]
                        fightProp.add(fightPropMpa.FIRE_ADD_HURT.value, additionalElementHurt)
                        fightProp.add(fightPropMpa.WATER_ADD_HURT.value, additionalElementHurt)
                        fightProp.add(fightPropMpa.ELEC_ADD_HURT.value, additionalElementHurt)
                        fightProp.add(fightPropMpa.WIND_ADD_HURT.value, additionalElementHurt)
                        fightProp.add(fightPropMpa.GRASS_ADD_HURT.value, additionalElementHurt)
                        fightProp.add(fightPropMpa.ICE_ADD_HURT.value, additionalElementHurt)
                        fightProp.add(fightPropMpa.ROCK_ADD_HURT.value, additionalElementHurt)

    return {
        "fightProp": fightProp,
        "afterAddProps": [
            fightPropMpa.FIRE_ADD_HURT.value,
            fightPropMpa.WATER_ADD_HURT.value,
            fightPropMpa.ELEC_ADD_HURT.value,
            fightPropMpa.WIND_ADD_HURT.value,
            fightPropMpa.GRASS_ADD_HURT.value,
            fightPropMpa.ICE_ADD_HURT.value,
            fightPropMpa.ROCK_ADD_HURT.value,
        ],
    }


async def getTheBlackSwordFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [0.20, 0.25, 0.30, 0.35, 0.40]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.NOMAL_ATTACK_CRITICAL.value, refinementValue)
                    fightProp.add(fightPropMpa.CHARGED_ATTACK_CRITICAL.value, refinementValue)

    return {"fightProp": fightProp, "afterAddProps": None}


info = {
    "안개를 가르는 회광": getMistsplitterReforgedFightProp,
    "용의 포효": getLionsRoarFightProp,
    "고요히 샘솟는 빛": getSplendorOfTranquilWatersFightProp,
    "창백한 섬광": getAzurelightFightProp,
    "사면": getAbsolutionFightProp,
    "아메노마 카게우치가타나": getAmenomaKageuchiFightProp,
    "늑대 송곳니": getWolfFangFightProp,
    "잎을 가르는 빛": getLightofFoliarIncisionFightProp,
    "페보니우스 검": getFavoniusSwordFightProp,
    "바위산을 맴도는 노래": getPeakPatrolSongFightProp,
    "칠흑검": getTheBlackSwordFightProp,
}

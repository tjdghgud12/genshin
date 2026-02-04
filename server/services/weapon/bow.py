from data.globalVariable import fightPropMap
from schemas.fightProp import fightPropSchema
from schemas.weapon import weaponDataSchema, WeaponDataReturnSchema
from services.weapon.commonData import getWeaponBaseFightProp


async def getAmosBowFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [[0.12, 0.08], [0.15, 0.10], [0.18, 0.12], [0.21, 0.14], [0.24, 0.16]]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            value = refinementValue[i] if i == 0 else refinementValue[i] * option.stack
            fightProp.add(fightPropMap.NOMAL_ATTACK_ATTACK_ADD_HURT.value, value)
            fightProp.add(fightPropMap.CHARGED_ATTACK_ATTACK_ADD_HURT.value, value)

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
                    fightProp.add(fightPropMap.NOMAL_ATTACK_ATTACK_ADD_HURT.value, refinementValue)
                case 1:
                    fightProp.add(fightPropMap.CHARGED_ATTACK_ATTACK_ADD_HURT.value, -0.1)

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
                    fightProp.add(fightPropMap.ATTACK_PERCENT.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMap.CHARGED_ATTACK_ATTACK_ADD_HURT.value, refinementValue[1][option.stack])

    return {"fightProp": fightProp, "afterAddProps": None}


async def getFavoniusWarbowFightProp(
    id: int, level: int, _refinement: int, _options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)

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
                    fightProp.add(fightPropMap.HP_PERCENT.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMap.ATTACK_ADD_HURT.value, refinementValue[1])

    return {"fightProp": fightProp, "afterAddProps": None}


info = {
    "아모스의 활": getAmosBowFightProp,
    "녹슨 활": getRustFightProp,
    "비뢰의 고동": getThunderingPulseFightProp,
    "페보니우스 활": getFavoniusWarbowFightProp,
    "약수": getAquaSimulacraFightProp,
}

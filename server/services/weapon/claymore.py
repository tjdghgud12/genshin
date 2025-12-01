from data.globalVariable import fightPropMpa
from schemas.fightProp import fightPropSchema
from schemas.weapon import weaponDataSchema, WeaponDataReturnSchema
from services.weapon.commonData import getWeaponBaseFightProp


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


info = {
    "타오르는 천 개의 태양": getAThousandBlazingSunsFightProp,
    "무공의 검": getTheUnforgedFightProp,
    "송뢰가 울릴 무렵": getSongOfBrokenPinesFightProp,
    "늑대의 말로": getWolfsGravestoneFightProp,
}

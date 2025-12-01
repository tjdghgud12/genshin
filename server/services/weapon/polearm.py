from data.globalVariable import fightPropMpa
from schemas.fightProp import fightPropSchema
from schemas.weapon import weaponDataSchema, WeaponDataReturnSchema
from services.weapon.commonData import getWeaponBaseFightProp


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


async def getFavoniusLanceFightProp(
    id: int, level: int, _refinement: int, _options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getTheCatchFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.16, 0.06],
        [0.20, 0.075],
        [0.24, 0.09],
        [0.28, 0.105],
        [0.32, 0.12],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ELEMENT_BURST_ATTACK_ADD_HURT.value, refinementValue[0])
                    fightProp.add(fightPropMpa.ELEMENT_BURST_CRITICAL.value, refinementValue[1])

    return {"fightProp": fightProp, "afterAddProps": None}


info = {
    "예초의 번개": getEngulfingLightningFightProp,
    "호마의 지팡이": getStaffOfHomaFightProp,
    "맛의 지휘자": getSymphonistOfScentsFightProp,
    "붉은 달의 형상": getCrimsonMoonsSemblanceFightProp,
    "식재": getCalamityQuellerFightProp,
    "화박연": getPrimordialJadeWingedSpearFightProp,
    "결투의 창": getDeathmatchFightProp,
    "페보니우스 장창": getFavoniusLanceFightProp,
    "「어획」": getTheCatchFightProp,
}

from data.globalVariable import fightPropMpa
from schemas.fightProp import fightPropSchema
from schemas.weapon import weaponDataSchema, WeaponDataReturnSchema
from services.weapon.commonData import getWeaponBaseFightProp


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


async def getApprenticesNotesFightProp(
    id: int, level: int, _refinement: int, _options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)

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


async def getReliquaryOfTruthFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [0.08, 80, 0.24],
        [0.10, 100, 0.30],
        [0.12, 120, 0.36],
        [0.14, 140, 0.42],
        [0.16, 160, 0.48],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.CRITICAL.value, refinementValue[0])
                case 1:
                    value = refinementValue[1]
                    if options[2].active:
                        value = refinementValue[1] * 1.5
                    fightProp.add(fightPropMpa.ELEMENT_MASTERY.value, value)
                case 2:
                    value = refinementValue[2]
                    if options[1].active:
                        value = refinementValue[2] * 1.5
                    fightProp.add(fightPropMpa.CRITICAL_HURT.value, value)

    return {"fightProp": fightProp, "afterAddProps": None}


async def getNightweaversLookingGlassFightProp(
    id: int, level: int, refinement: int, options: list[weaponDataSchema.extendedWeaponOptionSchema], _characterFightProp: fightPropSchema
) -> WeaponDataReturnSchema:
    fightProp = await getWeaponBaseFightProp(id, level)
    optionRefinementMap = [
        [60, 60, 1.2, 0.8, 0.4],
        [75, 75, 1.5, 1.0, 0.5],
        [90, 90, 1.8, 1.2, 0.6],
        [105, 105, 2.1, 1.4, 0.7],
        [120, 120, 2.4, 1.6, 0.8],
    ]
    refinementValue = optionRefinementMap[refinement - 1]

    for i, option in enumerate(options):
        if option.active:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ELEMENT_MASTERY.value, refinementValue[0])
                case 1:
                    fightProp.add(fightPropMpa.ELEMENT_MASTERY.value, refinementValue[1])

    # 둘 다 켜져있는 경우. 개화, 만개, 발화 달개화 피해증가 추가
    if options[0].active and options[1].active:
        fightProp.add(fightPropMpa.BLOOM_ADD_HURT.value, refinementValue[2])
        fightProp.add(fightPropMpa.HYPERBLOOM_ADD_HURT.value, refinementValue[3])
        fightProp.add(fightPropMpa.BURGEON_ADD_HURT.value, refinementValue[3])
        fightProp.add(fightPropMpa.LUNARBLOOM_ADD_HURT.value, refinementValue[4])

    return {"fightProp": fightProp, "afterAddProps": None}


info = {
    "떠오르는 천일 밤의 꿈": getAThousandFloatingDreamsFightProp,
    "별지기의 시선": getStarcallersWatchFightProp,
    "영원히 샘솟는 법전": getTomeOfTheEternalFlowFightProp,
    "학도의 노트": getApprenticesNotesFightProp,
    "카구라의 진의": getKagurasVerityFightProp,
    "음유시인의 악장": getTheWidsithFightProp,
    "사풍 원서": getLostPrayerToTheSacredWindsFightProp,
    "제사의 옥": getSacrificialJadeFightProp,
    "드래곤 슬레이어 영웅담": getThrillingTalesofDragonSlayersFightProp,
    "제례의 악장": getSacrificialFragmentsFightProp,
    "진실의 함": getReliquaryOfTruthFightProp,
    "밤을 엮는 거울": getNightweaversLookingGlassFightProp,
}

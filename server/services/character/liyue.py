from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMap
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from ambr import CharacterDetail
from copy import deepcopy


async def getGanyuFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    # ----------------------- Base Fight Prop -----------------------
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 획린(獲麟), 구름 여행, 잡초 근절, 살생의 발걸음의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "이슬 먹는 신수":
                    if constellation.options[0].active:  # pyright: ignore[reportIndexIssue]
                        newFightProp.add(fightPropMap.ICE_RES_MINUS.value, 0.15)
                case "서수(西狩)":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.ATTACK_ADD_HURT.value, constellation.options[0].stack * 0.05)
                case "구름 여행":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "잡초 근절":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 감우의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "단 하나의 마음":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.CHARGED_ATTACK_CRITICAL.value, 0.2)
                case "천지교태":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.ICE_ADD_HURT.value, 0.2)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getKeqingFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- constellations -----------------------
    # # 가연, 등루, 이등의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "조율":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.ATTACK_PERCENT.value, 0.25)
                case "염정":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.ELEC_ADD_HURT.value, constellation.options[0].stack * 0.06)
                case "등루":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "이등":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 각청의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "옥형의 품격":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.CRITICAL.value, 0.15)
                        newFightProp.add(fightPropMap.CHARGE_EFFICIENCY.value, 0.15)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getHuTaoFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalAttackPoints: list[dict] = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- passive -----------------------
    # 모습을 감춘 나비는 호두의 fightProp에 영향X
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "핏빛 분장":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.FIRE_ADD_HURT.value, 0.33)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    # ----------------------- constellations -----------------------
    # 비처럼 내리는 불안이 가장 마지막 최대HP기준으로 적용되어야 하기 때문에 해당 위치로 이동
    # 진홍의 꽃다발, 적색 피의 의식, 영원한 안식의 정원, 꽃잎 향초의 기도는 호두의 fightProp에 영향 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "비처럼 내리는 불안":
                    additionalAttackPoints.append({"key": fightPropMap.NOMAL_ATTACK_ATTACK_ADD_POINT.value, "value": ("HP", 0.1), "additionalAttack": "혈매향"})
                case "나비 잔향":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.CRITICAL.value, 1.00)
                case "적색 피의 의식":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "꽃잎 향초의 기도":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
    # ----------------------- active -----------------------
    # 가장 마지막 최대HP기준으로 적용되어야 하기 때문에 해당 위치로 이동
    activeSkillLevelMap = {
        "나비의 서": [
            0.0384,  # Level 1
            0.0407,  # Level 2
            0.0430,  # Level 3
            0.0460,  # Level 4
            0.0483,  # Level 5
            0.0506,  # Level 6
            0.0536,  # Level 7
            0.0566,  # Level 8
            0.0596,  # Level 9
            0.0626,  # Level 10
            0.0656,  # Level 11
            0.0685,  # Level 12
            0.0715,  # Level 13
            0.0745,  # Level 14
            0.0775,  # Level 15
        ]
    }

    for active in characterInfo.activeSkill:
        match active.name:
            case "나비의 서":
                if active.options[0].active:
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "적색 피의 의식"))
                    addLevel = 3 if addElementalSkillLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    baseHp = getattr(newFightProp, fightPropMap.BASE_HP.value)
                    hpPercent = getattr(newFightProp, fightPropMap.HP_PERCENT.value)
                    hp = getattr(newFightProp, fightPropMap.HP.value)
                    totalHp = baseHp * (hpPercent + 1) + hp
                    newFightProp.add(fightPropMap.ATTACK.value, totalHp * skillValue)

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMap, f"BASE_{pointKey}").value) * (
            1 + getattr(newFightProp, getattr(fightPropMap, f"{pointKey}_PERCENT").value)
        ) + getattr(newFightProp, getattr(fightPropMap, pointKey).value)

        if "additionalAttack" in additionalAttackPoint:
            newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[additionalAttackPoint["additionalAttack"]].add(fightPropMap.ATTACK_ADD_POINT.value, 0.1)
        else:
            newFightProp.add(key, finalPoint * value)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getYelanFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalAttackPoints: list[dict] = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "선공의 묘수":
                    if passive.options[0].active:
                        values = [0.0, 0.06, 0.12, 0.18, 0.30]
                        newFightProp.add(fightPropMap.HP_PERCENT.value, values[passive.options[0].stack])
                case "마음 가는 대로":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.ATTACK_ADD_HURT.value, passive.options[0].stack * 0.035 + 0.01)

    # ----------------------- constellations -----------------------
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "이화접목의 현혹술":
                    newFightProp.add(fightPropMap.HP_PERCENT.value, constellation.options[0].stack * 0.1)
                case "노름꾼의 주사위":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "눈보다 빠른 손":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
    # ----------------------- active -----------------------
    # 야란의 active 스킬은 fightProp 영향 X

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMap, f"BASE_{pointKey}").value) * (
            1 + getattr(newFightProp, getattr(fightPropMap, f"{pointKey}_PERCENT").value)
        ) + getattr(newFightProp, getattr(fightPropMap, pointKey).value)

        if "additionalAttack" in additionalAttackPoint:
            newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[additionalAttackPoint["additionalAttack"]].add(fightPropMap.ATTACK_ADD_POINT.value, 0.1)
        else:
            newFightProp.add(key, finalPoint * value)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getShenheFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalAttackPoints: list[dict] = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]
    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "대동미라존법":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.ICE_ADD_HURT.value, 0.15)
                case "박령통진법인":
                    if passive.options[0].active:
                        if passive.options[0].select == "짧은 터치":
                            # 원폭 및 원소스킬
                            newFightProp.add(fightPropMap.ELEMENT_BURST_ATTACK_ADD_HURT.value, 0.15)
                            newFightProp.add(fightPropMap.ELEMENT_SKILL_ATTACK_ADD_HURT.value, 0.15)
                        elif passive.options[0].select == "홀드":
                            # 일반공격 및 강공격 및 낙하공격
                            newFightProp.add(fightPropMap.NOMAL_ATTACK_ATTACK_ADD_HURT.value, 0.15)
                            newFightProp.add(fightPropMap.CHARGED_ATTACK_ATTACK_ADD_HURT.value, 0.15)
                            newFightProp.add(fightPropMap.FALLING_ATTACK_ATTACK_ADD_HURT.value, 0.15)

    # ----------------------- constellations -----------------------
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "정몽":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.ICE_CRITICAL_HURT.value, 0.15)  # 얼음 원소 전용 치명타 피해 증가
                case "잠허":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "통관":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.ELEMENT_SKILL_ATTACK_ADD_HURT.value, constellation.options[0].stack * 0.05)
                case "화신":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    # ----------------------- active -----------------------
    elementSkillLevelMap = {
        "위령 소환 구사술": [
            0.457,
            0.491,
            0.525,
            0.571,
            0.605,
            0.639,
            0.685,
            0.731,
            0.776,
            0.822,
            0.868,
            0.913,
            0.970,
            1.03,
            1.08,
        ],
        "신녀 강령 비결": [0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
    }

    for active in characterInfo.activeSkill:
        match active.name:
            case "위령 소환 구사술":
                if active.options[0].active:
                    # 얼음의 깃
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "잠허"))
                    addLevel = 3 if addElementalSkillLevel.unlocked else 0
                    skillValue = elementSkillLevelMap[active.name][active.level + addLevel - 1]
                    baseAttack = getattr(newFightProp, fightPropMap.BASE_ATTACK.value)
                    attackPercent = getattr(newFightProp, fightPropMap.ATTACK_PERCENT.value)
                    attack = baseAttack * (attackPercent + 1) + getattr(newFightProp, fightPropMap.ATTACK.value)
                    newFightProp.add(fightPropMap.ICE_ADD_POINT.value, skillValue * attack)
            case "신녀 강령 비결":
                if active.options[0].active:
                    # 내성 감소
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "화신"))
                    addLevel = 3 if addElementalSkillLevel.unlocked else 0
                    skillValue = elementSkillLevelMap[active.name][active.level + addLevel - 1]
                    newFightProp.add(fightPropMap.ICE_RES_MINUS.value, skillValue)
                    newFightProp.add(fightPropMap.PHYSICAL_RES_MINUS.value, skillValue)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getXianglingFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # ----------------------- active -----------------------
    # 향릉의 active 스킬은 fightProp 영향 X

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]
    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "절운차오톈자오":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.ATTACK_ADD_HURT.value, 0.1)

    # ----------------------- constellations -----------------------
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "겉은 바삭, 속은 촉촉":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.FIRE_RES_MINUS.value, 0.15)
                case "센 불로 조리하기":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "흉포한 누룽지":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "토네이도 화륜":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.FIRE_ADD_HURT.value, 0.15)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "감우": getGanyuFightProp,
    "각청": getKeqingFightProp,
    "호두": getHuTaoFightProp,
    "야란": getYelanFightProp,
    "신학": getShenheFightProp,
    "향릉": getXianglingFightProp,
}

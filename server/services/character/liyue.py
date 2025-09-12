from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMpa
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
                        newFightProp.add(fightPropMpa.ICE_RES_MINUS.value, 0.15)
                case "서수(西狩)":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, constellation.options[0].stack * 0.05)
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
                        newFightProp.add(fightPropMpa.CHARGED_ATTACK_CRITICAL.value, 0.2)
                case "천지교태":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.ICE_ADD_HURT.value, 0.2)

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
                case "계뢰":  # 원소 전투 스킬 추가 피해
                    description = "뇌설이 존재하는 동안 다시 원소 전투 스킬 발동 시 공격력의 50%의 번개 원소 피해 추가"
                case "조율":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.25)
                case "염정":
                    newFightProp.add(fightPropMpa.ELEC_ADD_HURT.value, constellation.options[0].stack * 0.06)
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
                        newFightProp.add(fightPropMpa.CRITICAL.value, 0.15)
                        newFightProp.add(fightPropMpa.CHARGE_EFFICIENCY.value, 0.15)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getHuTaoFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

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
                        newFightProp.add(fightPropMpa.FIRE_ADD_HURT.value, 0.33)

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
                case "나비 잔향":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.CRITICAL.value, 1.00)
                case "비처럼 내리는 불안":
                    # 최종 hp의 10%만큼
                    target = newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK.get("혈매향")
                    if target:
                        baseHp = getattr(newFightProp, fightPropMpa.BASE_HP.value)
                        hpPercent = getattr(newFightProp, fightPropMpa.HP_PERCENT.value)
                        hp = getattr(newFightProp, fightPropMpa.HP.value)
                        totalHp = baseHp * (hpPercent + 1) + hp
                        target.add(fightPropMpa.ATTACK_ADD_POINT.value, totalHp * 0.1)
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
                    baseHp = getattr(newFightProp, fightPropMpa.BASE_HP.value)
                    hpPercent = getattr(newFightProp, fightPropMpa.HP_PERCENT.value)
                    hp = getattr(newFightProp, fightPropMpa.HP.value)
                    totalHp = baseHp * (hpPercent + 1) + hp
                    newFightProp.add(fightPropMpa.ATTACK.value, totalHp * skillValue)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "감우": getGanyuFightProp,
    "각청": getKeqingFightProp,
    "호두": getHuTaoFightProp,
}

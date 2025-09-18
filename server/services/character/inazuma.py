from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMpa
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from ambr import CharacterDetail
from copy import deepcopy


async def getKamisatoAyakaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # # 서리에 검게 물든 벚꽃, 삼중 서리 관문, 흩날리는 카미후부키, 화운종월경의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "삼중 서리 관문":  # 최종 데미지 기준 추가 피해
                    newFightProp.add(fightPropMpa.FINAL_ELEMENT_BURST_ATTACK_ADD_HURT.value, 1.4)
                case "영고성쇠":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.DEFENSE_MINUS.value, 0.3)
                case "물에 비친 달":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_HURT.value, 2.98)
                case "흩날리는 카미후부키":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "화운종월경":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 아야카의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "천죄국죄 진사":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_HURT.value, 0.3)
                        newFightProp.add(fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_HURT.value, 0.3)
                case "한천선명 축사":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.ICE_ADD_HURT.value, 0.18)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getRaidenShogunFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 악요 명문(銘文), 진영의 과거, 진리의 맹세, 쇼군의 현형, 염원의 대행인의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "강철 절단":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.DEFENSE_IGNORE.value, 0.6)
                case "진영의 과거":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "쇼군의 현형":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    activeSkillLevelMap = {
        "초월·악요개안": [
            0.0022,  # Level 1
            0.0023,  # Level 2
            0.0024,  # Level 3
            0.0025,  # Level 4
            0.0026,  # Level 5
            0.0027,  # Level 6
            0.0028,  # Level 7
            0.0029,  # Level 8
            0.0030,  # Level 9
            0.0030,  # Level 10
            0.0030,  # Level 11
            0.0030,  # Level 12
            0.0030,  # Level 13
            0.0030,  # Level 14
            0.0030,  # Level 15
        ]
    }

    for active in characterInfo.activeSkill:
        match active.name:
            case "초월·악요개안":
                if active.options[0].active:
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "쇼군의 현형"))
                    addLevel = 3 if addElementalSkillLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    newFightProp.add(fightPropMpa.ELEMENT_BURST_ATTACK_ADD_HURT.value, 90 * skillValue)  # 90은 라이덴의 원소 에너지

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "비범한 옥체":
                    if passive.options[0].active:
                        val = getattr(newFightProp, fightPropMpa.CHARGE_EFFICIENCY.value) - 1
                        if val > 0:
                            newFightProp.add(fightPropMpa.ELEC_ADD_HURT.value, val * 0.4)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getYoimiyaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 폭죽장인의 깨달음, 나가노하라 유성군의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "적옥의 유금":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.2)
                case "만등 점화":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.FIRE_ADD_HURT.value, 0.25)
                case "쥐불놀이":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "한여름의 전야제":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    activeSkillLevelMap = {
        "염초 정화(庭火)의 춤": [
            0.379,  # Level 1
            0.402,  # Level 2
            0.425,  # Level 3
            0.454,  # Level 4
            0.477,  # Level 5
            0.499,  # Level 6
            0.529,  # Level 7
            0.558,  # Level 8
            0.588,  # Level 9
            0.617,  # Level 10
            0.647,  # Level 11
            0.677,  # Level 12
            0.706,  # Level 13
            0.736,  # Level 14
            0.765,  # Level 15
        ]
    }
    # 염초 정화(庭火)의 춤
    for active in characterInfo.activeSkill:
        match active.name:
            case "염초 정화(庭火)의 춤":
                if active.options[0].active:
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "쥐불놀이"))
                    addLevel = 3 if addElementalSkillLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    if characterInfo.activeSkill[0].baseFightProp.nomal is not None and characterInfo.activeSkill[0].baseFightProp.nomal.element is not None:
                        characterInfo.activeSkill[0].baseFightProp.nomal.element.append("fire")
                    newFightProp.add(fightPropMpa.FINAL_NOMAL_ATTACK_ATTACK_ADD_HURT.value, skillValue)

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "소매불 백경도":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.FIRE_ADD_HURT.value, passive.options[0].stack * 0.02)

                case "한낮의 풍물시":
                    if passive.options[0].active:
                        firstPassive = next((passive for passive in characterInfo.passiveSkill if passive.name == "소매불 백경도"))
                        if firstPassive.options[0].active:
                            newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, firstPassive.options[0].stack * 0.01)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "카미사토 아야카": getKamisatoAyakaFightProp,
    "라이덴 쇼군": getRaidenShogunFightProp,
    "요이미야": getYoimiyaFightProp,
}

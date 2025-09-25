from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMpa
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from ambr import CharacterDetail
from copy import deepcopy


async def getSkirkFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- constellations -----------------------
    # 심연, 악연, 소망, 멸류는 fightProp에 영향 없거나 각 스킬 연산 시 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "심연":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.7)
                case "악연":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "소망":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    activeSkillLevelMap = {
        "극악기·멸": [
            [0.035, 0.066, 0.088, 0.110],
            [0.040, 0.072, 0.096, 0.120],
            [0.045, 0.078, 0.104, 0.130],
            [0.050, 0.084, 0.112, 0.140],
            [0.055, 0.090, 0.120, 0.150],
            [0.060, 0.096, 0.128, 0.160],
            [0.065, 0.102, 0.136, 0.170],
            [0.070, 0.108, 0.144, 0.180],
            [0.075, 0.114, 0.152, 0.190],
            [0.080, 0.120, 0.160, 0.200],
            [0.085, 0.126, 0.168, 0.210],
            [0.090, 0.132, 0.176, 0.220],
            [0.095, 0.138, 0.184, 0.230],
            [0.100, 0.144, 0.192, 0.240],
            [0.105, 0.150, 0.200, 0.250],
        ]
    }
    for active in characterInfo.activeSkill:
        match active.name:
            case "극악기·멸":
                option = active.options[0]
                if option.active:
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "악연"))
                    secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "심연"))
                    addLevel = 3 if addElementalSkillLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    if secondConstellation.unlocked:
                        description = "뱀의 계략 pt에 따라 원폭 계수 추가"
                    newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK["일곱빛 섬광(일반공격)"].add(fightPropMpa.ATTACK_ADD_HURT.value, skillValue[option.stack])

    # ----------------------- passive -----------------------
    # 이치 너머의 이치는 원소전투스킬과 원소폭발의 계수 추가. 계수 추가는 미개발 상태
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "흐름의 적멸":
                    if passive.options[0].active:
                        normal = [0, 1.1, 1.2, 1.7]
                        burst = [0, 1.05, 1.15, 1.6]
                        newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK["일곱빛 섬광(일반공격)"].add(
                            fightPropMpa.FINAL_NOMAL_ATTACK_ATTACK_ADD_HURT.value, normal[passive.options[0].stack]
                        )
                        newFightProp.add(fightPropMpa.FINAL_ELEMENT_BURST_ATTACK_ADD_HURT.value, burst[passive.options[0].stack])

                        fourthConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "멸류"))
                        if fourthConstellation.unlocked:
                            addAttackPercent = [0, 0.1, 0.2, 0.4]
                            newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, addAttackPercent[passive.options[0].stack])

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "스커크": getSkirkFightProp,
}

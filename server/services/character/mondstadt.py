from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMpa
from schemas.calculation import requestCharacterInfoSchema
from schemas.character import damageBaseFightPropSchema, additionalAttackSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from ambr import CharacterDetail
from copy import deepcopy


async def getEulaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- constellations -----------------------
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "빛의 환상":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.PHYSICAL_ADD_HURT.value, 0.3)
                case "로렌스의 혈통":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "열등감 속 고집":
                    if constellation.options[0].active:
                        newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK["빛의 검"].add(fightPropMpa.ATTACK_ADD_HURT.value, 0.25)
                case "기사의 소양":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    activeSkillLevelMap = {"얼음 파도의 와류": [0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]}
    for active in characterInfo.activeSkill:
        match active.name:
            case "얼음 파도의 와류":
                if active.options[0].active:
                    newFightProp.add(fightPropMpa.DEFENSE_PERCENT.value, active.options[0].stack * 0.3)
                option = active.options[1]
                if option.active:
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "기사의 소양"))
                    addLevel = 3 if addElementalSkillLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    newFightProp.add(fightPropMpa.ICE_RES_MINUS.value, skillValue)
                    newFightProp.add(fightPropMpa.PHYSICAL_RES_MINUS.value, skillValue)

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "소용돌이치는 서리":
                    if passive.options[0].active:
                        passive.additionalAttack = [
                            additionalAttackSchema(name="부서진 빛의 검", type="elementalBurst", baseFightProp=damageBaseFightPropSchema(ATTACK=1, element=["physical"]))
                        ]

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {"유라": getEulaFightProp}

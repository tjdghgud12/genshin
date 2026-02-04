from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMap
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from ambr import CharacterDetail
from copy import deepcopy
from schemas.character import damageBaseFightPropSchema, additionalAttackSchema


async def getArlecchinoFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalAttackPoints = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- constellations -----------------------
    # 「모든 원한과 빚은 내가 갚고…」, 「모든 상벌은 내가 내릴 것이다…」, 「앞으로 사이좋게 지내거라…」 는 fightProp에 영향 없거나 각 스킬 연산 시 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "「우리의 새 가족이 되었으니…」":
                    characterInfo.activeSkill[0].level -= 3 if enkaDataFlag else 0
                case "「고독한 우리는 망자와 다름없으나…」":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "「앞으로 우리는 새 생명을 누리리라」":
                    additionalAttackPoints.append({"key": fightPropMap.ELEMENT_BURST_ATTACK_ADD_POINT.value, "value": ("ATTACK", (constellation.options[0].stack * 7) / 100)})
                    if constellation.options[1].active:
                        newFightProp.add(fightPropMap.NOMAL_ATTACK_CRITICAL.value, 0.1)
                        newFightProp.add(fightPropMap.NOMAL_ATTACK_CRITICAL_HURT.value, 0.7)
                        newFightProp.add(fightPropMap.ELEMENT_BURST_CRITICAL.value, 0.1)
                        newFightProp.add(fightPropMap.ELEMENT_BURST_CRITICAL_HURT.value, 0.7)

    # ----------------------- active -----------------------
    activeSkillLevelMap = {"사형장으로의 초대": [1.204, 1.302, 1.4, 1.54, 1.638, 1.75, 1.904, 2.058, 2.212, 2.38, 2.548, 2.716, 2.884, 3.052, 3.22]}
    for active in characterInfo.activeSkill:
        match active.name:
            case "사형장으로의 초대":
                option = active.options[0]
                if option.active:
                    firstConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "「모든 원한과 빚은 내가 갚고…」"))
                    addElementalBurstLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "「우리의 새 가족이 되었으니…」"))
                    addLevel = 3 if addElementalBurstLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    if firstConstellation.unlocked:
                        skillValue += 1
                    addPointValue = (option.stack * skillValue) / 100
                    additionalAttackPoints.append({"key": fightPropMap.NOMAL_ATTACK_ATTACK_ADD_POINT.value, "value": ("ATTACK", addPointValue)})
                    additionalAttackPoints.append({"key": fightPropMap.CHARGED_ATTACK_ATTACK_ADD_POINT.value, "value": ("ATTACK", addPointValue)})
                    additionalAttackPoints.append({"key": fightPropMap.FALLING_ATTACK_ATTACK_ADD_POINT.value, "value": ("ATTACK", addPointValue)})

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "재액의 달만이 알 수 있다":
                    newFightProp.add(fightPropMap.FIRE_ADD_HURT.value, 0.4)

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
        newFightProp.add(key, finalPoint * value)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "아를레키노": getArlecchinoFightProp,
}

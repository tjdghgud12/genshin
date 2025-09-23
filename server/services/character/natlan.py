from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMpa
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from ambr import CharacterDetail
from copy import deepcopy


async def getCitlaliFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
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
    # 구름뱀의 깃털 왕관, 불길한 닷새의 저주, 죽음을 거부하는 자의 영혼 해골은 fightProp에 영향 없거나 스킬에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "사백 개의 별빛":  # 스킬 계수 추가
                    description = "파티 내 캐릭터가 공격 시 소모되는 별빛 검 스텍을 10개 획득. 별빛 검은 시틀라리의 원소 마스터리의 200%만큼 피해 증가"
                    additionalAttackPoints.append({"key": fightPropMpa.ATTACK_ADD_POINT.value, "value": ("ELEMENT_MASTERY", 2)})
                case "심장을 삼키는 자의 순행":
                    newFightProp.add(fightPropMpa.ELEMENT_MASTERY.value, 125)
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ELEMENT_MASTERY.value, 250)
                case "아홉 번째 하늘의 계약":
                    newFightProp.add(fightPropMpa.FIRE_ADD_HURT.value, 0.015 * constellation.options[0].stack)
                    newFightProp.add(fightPropMpa.WATER_ADD_HURT.value, 0.015 * constellation.options[0].stack)
                    newFightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, 0.025 * constellation.options[0].stack)
                case "구름뱀의 깃털 왕관":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "불길한 닷새의 저주":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
    # ----------------------- active -----------------------
    # active: 시틀라리의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "다섯 번째 하늘의 서리비":
                    if passive.options[0].active:
                        secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "심장을 삼키는 자의 순행"))
                        if secondConstellation.unlocked:
                            newFightProp.add(fightPropMpa.FIRE_RES_MINUS.value, 0.2)
                            newFightProp.add(fightPropMpa.WATER_RES_MINUS.value, 0.2)
                        newFightProp.add(fightPropMpa.FIRE_RES_MINUS.value, 0.2)
                        newFightProp.add(fightPropMpa.WATER_RES_MINUS.value, 0.2)
                case "하얀 불나비의 별옷":  # 스킬 계수 추가
                    # 원소전투 스킬 검은 서리별의 이즈파파가 일으킨 서리운석 폭풍이 주는 피해가 시틀라리 원소 마스터리의 90%만큼 증가
                    # 원소폭발 반짝이는 칙령의 얼음 폭풍이 주는 피해가 시틀라리 원소 마스터리의 1200%만큼 증가
                    additionalAttackPoints.append({"key": fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_POINT, "value": ("ELEMENT_MASTERY", 0.9)})
                    additionalAttackPoints.append({"key": fightPropMpa.ELEMENT_BURST_ATTACK_ADD_POINT, "value": ("ELEMENT_MASTERY", 12)})

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMpa, pointKey).value)
        newFightProp.add(key, finalPoint * value)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getMavuikaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
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
    # 타오르는 태양, 진정한 의미, 「지도자」의 각오는 fightProp에 영향 없거나 다른 곳에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "밤 주인의 계시":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.4)
                case "잿더미의 대가":  # 스킬 계수 추가(일반공격, 강공격, 원소폭발의 석양 베기로 주는 피해가 마비카 공격력의 60%/90%/120%만큼 증가)
                    newFightProp.add(fightPropMpa.BASE_ATTACK.value, 200)
                    additionalAttackPoints.append({"key": fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_POINT.value, "value": ("ATTACK", 0.6)})
                    additionalAttackPoints.append({"key": fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_POINT.value, "value": ("ATTACK", 0.9)})
                    additionalAttackPoints.append({"key": fightPropMpa.ELEMENT_BURST_ATTACK_ADD_POINT.value, "value": ("ATTACK", 1.2)})
                case "「인간의 이름」 해방":  # 스킬 계수 추가
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.DEFENSE_MINUS.value, 0.2)
                    description = "불볕 고리: 공격 적중 시 공격력의 200%에 해당하는 밤혼 성질의 불 원소 피해 추가. 바이크 : 주변 적 방어력 20% 감소 및 3초마다 공격력의 500%에 해당하는 밤혼 성질의 불 원소 피해 추가"
                case "타오르는 태양":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "진정한 의미":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 마비카의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "타오르는 꽃의 선물":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.3)
                case "「키온고지」":
                    option = passive.options[0]
                    if option.active:
                        fourthConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "「지도자」의 각오"))
                        if fourthConstellation.unlocked:
                            option.stack = option.maxStack
                            newFightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, 0.1)
                        newFightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, 0.002 * option.stack)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMpa, f"BASE_{pointKey}").value) * (
            1 + getattr(newFightProp, getattr(fightPropMpa, f"{pointKey}_PERCENT").value)
        ) + getattr(newFightProp, getattr(fightPropMpa, pointKey).value)
        newFightProp.add(key, finalPoint * value)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "시틀라리": getCitlaliFightProp,
    "마비카": getMavuikaFightProp,
}

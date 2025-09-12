from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMpa
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from ambr import CharacterDetail
from copy import deepcopy


async def getNahidaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- constellations -----------------------
    # # 지혜를 머금은 씨앗, 감화된 성취의 싹, 달변으로 맺은 열매, 깨달음을 주는 잎의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "올곧은 선견의 뿌리":
                    # 연소, 개화, 만개, 발화의 치명타 발생
                    # 활성, 촉진, 발산 반응 시 방어력 감소만 적용
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.DEFENSE_MINUS.value, 0.3)
                        newFightProp.add(fightPropMpa.BLOOM_CRITICAL.value, 0.2)
                        newFightProp.add(fightPropMpa.BLOOM_CRITICAL_HURT.value, 1.0)
                        newFightProp.add(fightPropMpa.HYPERBLOOM_CRITICAL.value, 0.2)
                        newFightProp.add(fightPropMpa.HYPERBLOOM_CRITICAL_HURT.value, 1.0)
                        newFightProp.add(fightPropMpa.BURGEON_CRITICAL.value, 0.2)
                        newFightProp.add(fightPropMpa.BURGEON_CRITICAL_HURT.value, 1.0)
                        newFightProp.add(fightPropMpa.BURNING_CRITICAL.value, 0.2)
                        newFightProp.add(fightPropMpa.BURNING_CRITICAL_HURT.value, 1.0)

                case "추론으로 드러난 줄기":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ELEMENT_MASTERY.value, constellation.options[0].stack * 20 + 80)
                case "감화된 성취의 싹":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "깨달음을 주는 잎":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    activeSkillLevelMap = {
        "마음이 그리는 환상": [
            (0.149, 0.223),
            (0.160, 0.240),
            (0.171, 0.257),
            (0.186, 0.279),
            (0.197, 0.296),
            (0.208, 0.312),
            (0.223, 0.335),
            (0.238, 0.357),
            (0.253, 0.379),
            (0.268, 0.402),
            (0.283, 0.424),
            (0.298, 0.446),
            (0.316, 0.474),
            (0.335, 0.502),
            (0.353, 0.530),
        ]
    }

    for active in characterInfo.activeSkill:
        match active.name:
            case "마음이 그리는 환상":  # 번개, 물의 경우 fightProp에 영향 X. 각 쿨감 및 지속시간 증가.
                option = active.options[0]  #  0번지가 불
                if option.active:
                    addElementalBurstLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "깨달음을 주는 잎"))
                    seedsOfWisdom = next((constellation for constellation in characterInfo.constellations if constellation.name == "지혜를 머금은 씨앗"))
                    addLevel = 3 if addElementalBurstLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    stack = min(option.stack + (1 if seedsOfWisdom.unlocked else 0), 2)

                    target = newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK.get("삼업의 정화")
                    secondTarget = newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK.get("삼업의 정화·업의 사면")
                    if target:
                        target.add(fightPropMpa.ATTACK_ADD_HURT.value, skillValue[stack - 1])
                    if secondTarget:
                        secondTarget.add(fightPropMpa.ATTACK_ADD_HURT.value, skillValue[stack - 1])

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "정선으로 포용한 명론":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.ELEMENT_MASTERY.value, min(getattr(newFightProp, fightPropMpa.ELEMENT_MASTERY.value) * 0.25, 250))
                case "지혜로 깨우친 지론":
                    if passive.options[0].active:
                        val = min(getattr(newFightProp, fightPropMpa.ELEMENT_MASTERY.value) - 200, 800)
                        if val > 0:
                            target = newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK.get("삼업의 정화")
                            secondTarget = newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK.get("삼업의 정화·업의 사면")
                            if target:
                                target.add(fightPropMpa.CRITICAL.value, val * 0.03 / 100)
                                target.add(fightPropMpa.ATTACK_ADD_HURT.value, val * 0.1 / 100)
                            if secondTarget:
                                secondTarget.add(fightPropMpa.CRITICAL.value, val * 0.03 / 100)
                                secondTarget.add(fightPropMpa.ATTACK_ADD_HURT.value, val * 0.1 / 100)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "나히다": getNahidaFightProp,
}

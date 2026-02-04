from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMap
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from ambr import CharacterDetail
from copy import deepcopy


async def getFurinaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalAttackPoints = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 6돌을 제외한 모든 돌파 옵션은 fightProp에 영향 없거나 active에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "「모두 사랑의 축배를 들렴!」":
                    if constellation.options[0].active:
                        description = "원소 전투 스킬 발동 시 일반공격, 강공격, 낙하공격이 hp최대치의 18%만큼 증가하는 물 원소 피해로 변경. 프뉴마 상태일 때 일반공격, 강공격, 낙하공격의 추락충격으로 주는 피해가 hp최대치의 25%만큼 증가"
                        additionalAttackPoints.append({"key": fightPropMap.NOMAL_ATTACK_ATTACK_ADD_POINT.value, "value": ("HP", 0.43)})
                        additionalAttackPoints.append({"key": fightPropMap.CHARGED_ATTACK_ATTACK_ADD_POINT.value, "value": ("HP", 0.43)})
                        additionalAttackPoints.append({"key": fightPropMap.FALLING_ATTACK_ATTACK_ADD_POINT.value, "value": ("HP", 0.43)})
                case "「내 이름은 그 누구도 모르리라」":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "「난 알았노라, 그대의 이름은…!」":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    activeSkillLevelMap = {
        "성대한 카니발": [
            [0.0007, 0.0001],  # Level 1
            [0.0009, 0.0002],  # Level 2
            [0.0011, 0.0003],  # Level 3
            [0.0013, 0.0004],  # Level 4
            [0.0015, 0.0005],  # Level 5
            [0.0017, 0.0006],  # Level 6
            [0.0019, 0.0007],  # Level 7
            [0.0021, 0.0008],  # Level 8
            [0.0023, 0.0009],  # Level 9
            [0.0025, 0.0010],  # Level 10
            [0.0027, 0.0011],  # Level 11
            [0.0029, 0.0012],  # Level 12
            [0.0031, 0.0013],  # Level 13
            [0.0033, 0.0014],  # Level 14
            [0.0035, 0.0015],  # Level 15
        ]
    }

    for active in characterInfo.activeSkill:
        match active.name:
            case "성대한 카니발":
                option = active.options[0]
                if option.active:
                    addElementalBurstLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "「내 이름은 그 누구도 모르리라」"))
                    firstConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "「사랑은 애걸해도 길들일 수 없는 새」"))
                    secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "「여자의 마음은 흔들리는 부평초」"))
                    addLevel = 3 if addElementalBurstLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]

                    if firstConstellation.unlocked:
                        option.stack = min(option.stack + 150, 400)
                    if secondConstellation.unlocked:
                        newFightProp.add(fightPropMap.HP_PERCENT.value, 0.0035 * option.stack)

                    newFightProp.add(fightPropMap.ATTACK_ADD_HURT.value, skillValue[0] * option.stack)
                    # newFightProp[fightPropMap.ATTACK_ADD_HURT.value] += skillValue[1] * active.stack # 치유 보너스

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    # ----------------------- passive -----------------------
    # 가장 마지막 최대HP기준으로 적용되어야 하기 때문에 해당 위치로 이동
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "고독한 독백":
                    baseHp = getattr(newFightProp, fightPropMap.BASE_HP.value)
                    hpPercent = getattr(newFightProp, fightPropMap.HP_PERCENT.value)
                    hp = getattr(newFightProp, fightPropMap.HP.value)
                    totalHp = baseHp * (hpPercent + 1) + hp
                    newFightProp.add(fightPropMap.ELEMENT_SKILL_ATTACK_ADD_HURT.value, min(totalHp / 1000 * 0.007, 0.28))

    # 추가 계수 입력부
    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMap, f"BASE_{pointKey}").value) * (
            1 + getattr(newFightProp, getattr(fightPropMap, f"{pointKey}_PERCENT").value)
        ) + getattr(newFightProp, getattr(fightPropMap, pointKey).value)
        newFightProp.add(key, finalPoint * value)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getNeuvilletteFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- constellations -----------------------
    # 위대한 제정, 법의 계율, 고대의 의제, 연민의 왕관, 정의의 판결 fightProp에 영향 없거나 스킬에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "분노의 보상":  # 스킬 계수 추가
                    description = "강공격 명중 시 hp최대치의 10% 물 원소 피해를 주는 격류 2개 소환"
                case "고대의 의제":
                    characterInfo.activeSkill[0].level -= 3 if enkaDataFlag else 0
                case "정의의 판결":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 느비예트의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "생존한 고대바다의 계승자":
                    option = passive.options[0]
                    if option.active:
                        finalCharged = [0, 0.10, 1.25, 1.60]  # 최종 데미지 곱연산(강공격)
                        newFightProp.add(fightPropMap.FINAL_CHARGED_ATTACK_ATTACK_ADD_HURT.value, finalCharged[option.stack])

                        firstConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "위대한 제정"))
                        secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "법의 계율"))
                        if firstConstellation.unlocked:
                            option.stack = min(option.stack + 1, 3)
                        if secondConstellation.unlocked:
                            newFightProp.add(fightPropMap.CHARGED_ATTACK_CRITICAL_HURT.value, 0.14 * option.stack)
                case "드높은 중재의 규율":
                    option = passive.options[0]
                    if option.active:
                        newFightProp.add(fightPropMap.WATER_ADD_HURT.value, (0.6 * option.stack) / 100)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getEscoffierFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
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
    # 로즈마리 비밀 레시피는 fightProp에 영향X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "미각을 깨우는 식전 공연":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.CRITICAL_HURT.value, 0.6)
                case "예술의 경지에 이른 스튜":  # 스킬 계수 추가
                    description = "원소 전투 스킬 발동 시 피해를 에스코피에의 공격력의 240%만큼 증가시키는 즉석 요리 스텍 획득(신학 깃털 효과)"
                    additionalAttackPoints.append({"key": fightPropMap.ATTACK_ADD_POINT.value, "value": ("ATTACK", 2.4)})
                case "무지갯빛 티타임":  # 스킬 계수 추가
                    description = "현재 필드 위에 있는 파티 내 자신의 캐릭터의 일반공격, 강공격, 낙하공격이 명중 시 에스코피에의 공격력의 500%에 해당하는 얼음 원소 추가 피해"
                case "캐러멜화의 마법":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "다채로운 소스의 교향곡":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 에스코피에의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    # 밥이 보약은 fightProp에 영향X
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "영감의 조미료":
                    option = passive.options[0]
                    if option.active:
                        addIceWarterResMinus = [0, 0.05, 0.1, 0.15, 0.55]
                        newFightProp.add(fightPropMap.ICE_RES_MINUS.value, addIceWarterResMinus[option.stack])
                        newFightProp.add(fightPropMap.WATER_RES_MINUS.value, addIceWarterResMinus[option.stack])

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


async def getClorindeFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
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
    #  「지금부터 촛불의 장막을 지나」, 「지금부터 긴 밤의 위험에 맞선다」  fightProp에 영향 없거나 다른 곳에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "「눈물, 생명, 사랑을 간직하며」":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.ELEMENT_BURST_ATTACK_ADD_HURT.value, constellation.options[0].stack * 0.02)
                case "「절대 희망을 버리지 않으리라」":  # 스킬 계수 추가(일반공격, 강공격, 원소폭발의 석양 베기로 주는 피해가 마비카 공격력의 60%/90%/120%만큼 증가)
                    newFightProp.add(fightPropMap.CRITICAL.value, 0.1)
                    newFightProp.add(fightPropMap.CRITICAL_HURT.value, 0.7)
                case "「난 낮의 맹세를 명심하고」":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "「언젠가 찾아올 여명을 믿겠다」":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 클로린드의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "밤을 가르는 불꽃":
                    option = passive.options[0]
                    if option.active:
                        value = 0.2
                        max = 1800
                        secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "「지금부터 긴 밤의 위험에 맞선다」"))
                        if secondConstellation.unlocked:
                            option.stack = option.maxStack
                            value = 0.3
                            max = 2700
                        additionalAttackPoints.append({"key": fightPropMap.NOMAL_ATTACK_ELEC_ADD_POINT.value, "value": ("ATTACK", value * option.stack), "max": max})
                        additionalAttackPoints.append({"key": fightPropMap.ELEMENT_BURST_ELEC_ADD_POINT.value, "value": ("ATTACK", value * option.stack), "max": max})
                case "계약의 보상":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.CRITICAL.value, 0.1 * passive.options[0].stack)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        max = additionalAttackPoint["max"]
        finalPoint = getattr(newFightProp, getattr(fightPropMap, f"BASE_{pointKey}").value) * (
            1 + getattr(newFightProp, getattr(fightPropMap, f"{pointKey}_PERCENT").value)
        ) + getattr(newFightProp, getattr(fightPropMap, pointKey).value)
        newFightProp.add(key, min(finalPoint * value, max))

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getNaviaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
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
    # 숙녀의 거리감 수칙 fightProp에 영향 없거나 다른 곳에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "통솔자의 승승장구":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.ELEMENT_SKILL_CRITICAL.value, constellation.options[0].stack * 0.12)
                case "경영자의 넓은 시야":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "맹세자의 엄격함":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.ROCK_RES_MINUS.value, 0.2)
                case "협상가의 단호함":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "보스의 기민한 수완":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.ELEMENT_SKILL_CRITICAL_HURT.value, constellation.options[0].stack * 0.45)

    # ----------------------- active -----------------------
    for active in characterInfo.activeSkill:
        match active.name:
            case "결정 축포":
                if active.options[0].active:
                    stack = active.options[0].stack - 3
                    if stack > 0:
                        newFightProp.add(fightPropMap.ELEMENT_BURST_ATTACK_ADD_HURT.value, active.options[0].stack * 0.15)

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "비밀 유통 경로":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.NOMAL_ATTACK_ROCK_ADD_HURT.value, 0.40)
                        newFightProp.add(fightPropMap.CHARGED_ATTACK_ROCK_ADD_HURT.value, 0.40)
                        newFightProp.add(fightPropMap.FALLING_ATTACK_ROCK_ADD_HURT.value, 0.40)

                case "상호 협력망":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.ATTACK_PERCENT.value, passive.options[0].stack * 0.20)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        max = additionalAttackPoint["max"]
        finalPoint = getattr(newFightProp, getattr(fightPropMap, f"BASE_{pointKey}").value) * (
            1 + getattr(newFightProp, getattr(fightPropMap, f"{pointKey}_PERCENT").value)
        ) + getattr(newFightProp, getattr(fightPropMap, pointKey).value)
        newFightProp.add(key, min(finalPoint * value, max))

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "푸리나": getFurinaFightProp,
    "느비예트": getNeuvilletteFightProp,
    "에스코피에": getEscoffierFightProp,
    "클로린드": getClorindeFightProp,
    "나비아": getNaviaFightProp,
}

from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMap
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from ambr import CharacterDetail
from copy import deepcopy


async def getLaumaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    newFightProp.add(fightPropMap.ELEMENT_MASTERY.value, 200)  # 라우마는 1레벨부터 기본 200의 원마를 보유
    additionalAttackPoints = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact, characterInfo)
    newFightProp = weaponArtifactData["fightProp"]

    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- constellations -----------------------
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                # 첫 번째: "생명으로 엮은 실" 부여(회복/스태미나/지속시간), 계산 내 피격 효과는 여기서 별도 구현 X
                # 네 번째: 원소 에너지 회복 효과(공격 명중시)
                case "「극북의 충고와 전설을 엮어라」":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMap.LUNARBLOOM_ADD_HURT.value, 0.4)

                case "「진실을 증명할 수만 있다면」":
                    # 원소전투 스킬 레벨 +3
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "「그대여, 교활한 여우의 길을 탐하지 말라」":
                    # 원소폭발 레벨 +3
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "「내 피와 눈물을 달빛에 바치리라」":
                    if characterInfo.moonsign == "초승":
                        newFightProp.add(fightPropMap.LUNAR_ADD_HURT.value, 0.25)

    # ----------------------- active -----------------------
    # 별도 버프 없음. 추가 공격/피해는 이미 위에서 처리됨.
    # 푸른찬송가 효과 적용
    # 푸른 찬송가 스택별 원소 마스터리 기반 달개화 추가 피해 관련 표(정리용)
    # 푸른찬송가 스택별 달개화 추가 피해 계수표 (레벨: [달개화/개화 만개 발화])
    blueChantLunarBloomMultipliersMap = [
        (2.778, 2.222),
        (2.986, 2.389),
        (3.194, 2.556),
        (3.472, 2.778),
        (3.680, 2.945),
        (3.889, 3.111),
        (4.166, 3.334),
        (4.444, 3.556),
        (4.722, 3.778),
        (5.000, 4.000),
        (5.277, 4.223),
        (5.555, 4.445),
        (5.902, 4.723),
        (6.250, 5.000),
        (6.597, 5.278),
    ]
    for skill in characterInfo.activeSkill:
        if skill.name == "성가·달빛 소원" and skill.options and skill.options[0].active:
            # 푸른찬송가가 활성화된 경우, 원소폭발(성가·달빛 소원) 스킬 레벨에 맞는 계수 적용
            # constellation에 따라 "성가·달빛 소원" 스킬의 레벨 증감 구현
            # 3번째 별자리: 원소폭발 레벨 +3
            # 2번째 별자리 효과로 인한 증가량 추가 계산 필요
            secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "「극북의 충고와 전설을 엮어라」"), None)
            addElementalBurstLevel = next(
                (constellation for constellation in characterInfo.constellations if constellation.name == "「그대여, 교활한 여우의 길을 탐하지 말라」"), None
            )
            addLevel = 3 if addElementalBurstLevel and addElementalBurstLevel.unlocked else 0
            skillLevel = max(0, min(skill.level + addLevel - 1, len(blueChantLunarBloomMultipliersMap) - 1))
            bloomMul, lunarBloomMul = blueChantLunarBloomMultipliersMap[skillLevel]

            if secondConstellation.unlocked:
                bloomMul += 5
                lunarBloomMul += 4

            bloomMul = bloomMul * newFightProp.FIGHT_PROP_ELEMENT_MASTERY
            lunarBloomMul = lunarBloomMul * newFightProp.FIGHT_PROP_ELEMENT_MASTERY
            newFightProp.add(fightPropMap.BLOOM_ADD_POINT.value, bloomMul)  # 스킬 계수 기반 적용
            newFightProp.add(fightPropMap.HYPERBLOOM_ADD_POINT.value, bloomMul)
            newFightProp.add(fightPropMap.BURGEON_ADD_POINT.value, bloomMul)
            newFightProp.add(fightPropMap.LUNARBLOOM_EXTRA_DAMAGE.value, lunarBloomMul)

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "서리밤에 바치는 빛":
                    # 달빛 징조 옵션별 효과
                    if characterInfo.moonsign == "초승":
                        # 달빛 징조·초승 효과 - 치확15, 치피100, 부여
                        newFightProp.add(fightPropMap.BLOOM_CRITICAL.value, 0.15)
                        newFightProp.add(fightPropMap.HYPERBLOOM_CRITICAL.value, 0.15)
                        newFightProp.add(fightPropMap.BURGEON_CRITICAL.value, 0.15)
                        newFightProp.FIGHT_PROP_BLOOM_CRITICAL_HURT = max(1.0, newFightProp.FIGHT_PROP_BLOOM_CRITICAL_HURT)
                        newFightProp.FIGHT_PROP_HYPERBLOOM_CRITICAL_HURT = max(1.0, newFightProp.FIGHT_PROP_HYPERBLOOM_CRITICAL_HURT)
                        newFightProp.FIGHT_PROP_BURGEON_CRITICAL_HURT = max(1.0, newFightProp.FIGHT_PROP_BURGEON_CRITICAL_HURT)
                    elif characterInfo.moonsign == "보름":
                        # 달빛 징조·보름 효과 - 달개화 치확10 치피20%
                        newFightProp.add(fightPropMap.LUNARBLOOM_CRITICAL.value, 0.1)
                        newFightProp.add(fightPropMap.LUNARBLOOM_CRITICAL_HURT.value, 0.2)
                case "샘물에 바치는 정화":
                    # 원소 마스터리 비례 스킬피해 및 쿨감
                    skillAdd = min(newFightProp.FIGHT_PROP_ELEMENT_MASTERY * 0.0004, 0.32)
                    newFightProp.add(fightPropMap.ELEMENT_SKILL_ATTACK_ADD_HURT.value, skillAdd)
                case "달빛 징조의 축복·자연의 은총":
                    # 달개화 기본 피해 증가
                    lunarBloomAdd = min(newFightProp.FIGHT_PROP_ELEMENT_MASTERY * 0.000175, 0.14)
                    newFightProp.add(fightPropMap.LUNARBLOOM_BASE_ADD_HURT.value, lunarBloomAdd)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getNeferFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalAttackPoints = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact, characterInfo)
    newFightProp = weaponArtifactData["fightProp"]

    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- constellations -----------------------
    # 관찰은 계획의 초석은 passive에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "계획은 성공의 시작":
                    # 환영극 총 5타에 전부 각각 60%씩 계수 추가되기 때문에 최종 300%의 계수 추가 발생
                    additionalAttackPoints.append({"key": fightPropMap.LUNARBLOOM_ADD_POINT.value, "value": ("ELEMENT_MASTERY", 3), "additionalAttack": "환영극"})
                case "진실을 가리는 거짓":
                    # 원소전투 스킬 레벨 +3
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "마음을 홀리는 함정":
                    newFightProp.add(fightPropMap.GRASS_RES_MINUS.value, 0.2)
                case "기회를 포착한 순간":
                    # 원소폭발 레벨 +3
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "거머쥔 역전의 승리":
                    additionalAttackPoints.append({"key": fightPropMap.LUNARBLOOM_ADD_POINT.value, "value": ("ELEMENT_MASTERY", 0.85), "additionalAttack": "환영극"})
                    if characterInfo.moonsign == "보름":
                        newFightProp.add(fightPropMap.LUNARBLOOM_PROMOTION.value, 0.15)

    # ----------------------- passive -----------------------
    # 모래의 딸은 fightProp에 영향 X
    elementBurstVeilOfDeceptionMap = [0.13, 0.16, 0.19, 0.22, 0.25, 0.28, 0.31, 0.34, 0.37, 0.40, 0.43, 0.46, 0.49, 0.52, 0.55]
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "달빛 승부사":
                    if characterInfo.moonsign == "보름":
                        option = passive.options[0]
                        if option:
                            secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "관찰은 계획의 초석"))
                            if secondConstellation.unlocked:
                                option.maxStack = 5
                                if enkaDataFlag:
                                    option.stack = 5
                            if option.stack >= option.maxStack:
                                newFightProp.add(fightPropMap.ELEMENT_MASTERY.value, 200 if option.stack >= option.maxStack else 100)
                            newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK["환영극"].add(fightPropMap.LUNARBLOOM_ADD_HURT.value, 0.08 * option.stack)
                            skillLevel = characterInfo.activeSkill[2].level
                            newFightProp.add(fightPropMap.ELEMENT_BURST_ATTACK_ADD_HURT.value, elementBurstVeilOfDeceptionMap[skillLevel] * option.stack)

                case "달빛 징조의 축복·황혼의 그림자":
                    lunarBloomAdd = min(newFightProp.FIGHT_PROP_ELEMENT_MASTERY * 0.000175, 0.14)
                    newFightProp.add(fightPropMap.LUNARBLOOM_BASE_ADD_HURT.value, lunarBloomAdd)

    # ----------------------- active -----------------------
    # active는 fightProp에 영향 X

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMap, pointKey).value)
        newFightProp.add(key, finalPoint * value)
        if additionalAttackPoint["additionalAttack"]:
            newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[additionalAttackPoint["additionalAttack"]] = additionalAttackFightPropSchema()

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getColumbinaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalFightProp = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact, characterInfo)
    newFightProp = weaponArtifactData["fightProp"]
    for info in [*characterInfo.constellations, *characterInfo.activeSkill, *characterInfo.passiveSkill]:
        if info.additionalAttack:
            for attack in info.additionalAttack:
                newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[attack.name] = additionalAttackFightPropSchema()

    # ----------------------- active -----------------------
    activeSkillLevelMap = {
        "향수에 잠긴 달": [
            0.13,  # Level 1
            0.16,  # Level 2
            0.19,  # Level 3
            0.22,  # Level 4
            0.25,  # Level 5
            0.28,  # Level 6
            0.31,  # Level 7
            0.34,  # Level 8
            0.37,  # Level 9
            0.40,  # Level 10
            0.43,  # Level 11
            0.46,  # Level 12
            0.49,  # Level 13
            0.52,  # Level 14
            0.55,  # Level 15
        ]
    }

    for active in characterInfo.activeSkill:
        match active.name:
            case "향수에 잠긴 달":
                if active.options[0].active:
                    newFightProp.add(fightPropMap.LUNAR_ADD_HURT.value, activeSkillLevelMap[active.name][active.level])

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "달의 유혹":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMap.CRITICAL.value, passive.options[0].stack * 0.05)
                case "달빛 징조의 축복·월광":
                    additionalFightProp.append({"key": fightPropMap.LUNAR_BASE_ADD_HURT.value, "value": ("HP", 0.002), "max": 0.07})

    # ----------------------- constellations -----------------------
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "꽃바다를 품은 산속의 달":
                    newFightProp.add(fightPropMap.LUNAR_PROMOTION.value, 0.015)

                case "밤의 달빛과 그대의 동행":
                    newFightProp.add(fightPropMap.LUNAR_PROMOTION.value, 0.07)
                    newFightProp.add(fightPropMap.HP_PERCENT.value, 0.4)

                    if characterInfo.moonsign == "보름":
                        match constellation.options[0].select:
                            case "달 감전":
                                additionalFightProp.append({"key": fightPropMap.ATTACK_ADD_POINT.value, "value": ("HP", 0.01)})  # 달감전 계수 추가
                            case "달 개화":
                                additionalFightProp.append({"key": fightPropMap.ELEMENT_MASTERY.value, "value": ("HP", 0.0035)})  # 달개화 계수 추가
                            case "달 결정":
                                additionalFightProp.append({"key": fightPropMap.DEFENSE_PERCENT.value, "value": ("HP", 0.01)})  # 달결정 계수 추가

                case "빛의 결정과 꿈의 물결":
                    # 원소전투 스킬 레벨 +3
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                    newFightProp.add(fightPropMap.LUNAR_PROMOTION.value, 0.015)
                case "꽃과 산에 드리운 그림자":
                    additionalFightProp.append({"key": fightPropMap.LUNARBLOOM_ADD_POINT.value, "value": ("HP", 0.0035), "additionalAttack": "보름달·달 개화"})  # 달개화 계수 추가
                    additionalFightProp.append({"key": fightPropMap.LUNARCHARGED_ADD_POINT.value, "value": ("HP", 0.01), "additionalAttack": "보름달·달 감전"})  # 달감전 계수 추가
                    additionalFightProp.append(
                        {"key": fightPropMap.LUNARCRYSTALLIZE_ADD_POINT.value, "value": ("HP", 0.002), "additionalAttack": "보름달·달 결정"}
                    )  # 달결정 계수 추가
                    newFightProp.add(fightPropMap.LUNAR_PROMOTION.value, 0.015)
                case "적막 속 그대의 노랫소리":
                    # 원소폭발 레벨 +3
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                    newFightProp.add(fightPropMap.LUNAR_PROMOTION.value, 0.015)
                case "어두운 밤 달빛의 인도":
                    newFightProp.add(fightPropMap.WATER_CRITICAL_HURT.value, 0.8)
                    newFightProp.add(fightPropMap.ELEC_CRITICAL_HURT.value, 0.8)
                    newFightProp.add(fightPropMap.GRASS_CRITICAL_HURT.value, 0.8)
                    newFightProp.add(fightPropMap.ROCK_CRITICAL_HURT.value, 0.8)
                    newFightProp.add(fightPropMap.LUNAR_PROMOTION.value, 0.07)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    for additionalFightPropPoint in additionalFightProp:
        key = additionalFightPropPoint["key"]
        pointKey, value = additionalFightPropPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMap, pointKey).value)
        finalValue = finalPoint * value if additionalFightPropPoint["max"] is None else min(finalPoint * value, additionalFightPropPoint["max"])

        if "additionalAttack" in additionalFightPropPoint:
            newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[additionalFightPropPoint["additionalAttack"]].add(key, finalValue)
        else:
            newFightProp.add(key, finalValue)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "라우마": getLaumaFightProp,
    "네페르": getNeferFightProp,
    "콜롬비나": getColumbinaFightProp,
}

from services.character.commonData import CharacterFightPropReturnData, CharacterFightPropGetter, genCharacterBaseStat, getWeaponArtifactFightProp, getAfterWeaponArtifactFightProp
from data.globalVariable import fightPropMpa
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from ambr import CharacterDetail
from copy import deepcopy


async def getLaumaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    newFightProp.add(fightPropMpa.ELEMENT_MASTERY.value, 200)  # 라우마는 1레벨부터 기본 200의 원마를 보유
    additionalAttackPoints = []

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
                # 첫 번째: "생명으로 엮은 실" 부여(회복/스태미나/지속시간), 계산 내 피격 효과는 여기서 별도 구현 X
                # 네 번째: 원소 에너지 회복 효과(공격 명중시)
                case "「극북의 충고와 전설을 엮어라」":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.LUNARBLOOM_ADD_HURT.value, 0.4)

                case "「진실을 증명할 수만 있다면」":
                    # 원소전투 스킬 레벨 +3
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "「그대여, 교활한 여우의 길을 탐하지 말라」":
                    # 원소폭발 레벨 +3
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "「내 피와 눈물을 달빛에 바치리라」":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.LUNARBLOOM_ADD_HURT.value, 0.25)

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
            newFightProp.add(fightPropMpa.BLOOM_ADD_POINT.value, bloomMul)  # 스킬 계수 기반 적용
            newFightProp.add(fightPropMpa.HYPERBLOOM_ADD_POINT.value, bloomMul)
            newFightProp.add(fightPropMpa.BURGEON_ADD_POINT.value, bloomMul)
            newFightProp.add(fightPropMpa.LUNARBLOOM_ADD_POINT.value, lunarBloomMul)

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "서리밤에 바치는 빛":
                    # 달빛 징조 옵션별 효과
                    if passive.options and passive.options[0].select == "초승":
                        # 달빛 징조·초승 효과 - 치확15, 치피100, 부여
                        newFightProp.add(fightPropMpa.BLOOM_CRITICAL.value, 0.15)
                        newFightProp.add(fightPropMpa.HYPERBLOOM_CRITICAL.value, 0.15)
                        newFightProp.add(fightPropMpa.BURGEON_CRITICAL.value, 0.15)
                        newFightProp.FIGHT_PROP_BLOOM_CRITICAL_HURT = max(1.0, newFightProp.FIGHT_PROP_BLOOM_CRITICAL_HURT)
                        newFightProp.FIGHT_PROP_HYPERBLOOM_CRITICAL_HURT = max(1.0, newFightProp.FIGHT_PROP_HYPERBLOOM_CRITICAL_HURT)
                        newFightProp.FIGHT_PROP_BURGEON_CRITICAL_HURT = max(1.0, newFightProp.FIGHT_PROP_BURGEON_CRITICAL_HURT)
                    elif passive.options and passive.options[0].select == "보름":
                        # 달빛 징조·보름 효과 - 달개화 치확10 치피20%
                        newFightProp.add(fightPropMpa.LUNARBLOOM_CRITICAL.value, 0.1)
                        newFightProp.add(fightPropMpa.LUNARBLOOM_CRITICAL_HURT.value, 0.2)
                case "샘물에 바치는 정화":
                    # 원소 마스터리 비례 스킬피해 및 쿨감
                    skillAdd = min(newFightProp.FIGHT_PROP_ELEMENT_MASTERY * 0.0004, 0.32)
                    newFightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value, skillAdd)
                case "달빛 징조의 축복·자연의 은총":
                    # 달개화 기본 피해 증가
                    lunarBloomAdd = min(newFightProp.FIGHT_PROP_ELEMENT_MASTERY * 0.000175, 0.14)
                    newFightProp.add(fightPropMpa.LUNARBLOOM_BASE_ADD_HURT.value, lunarBloomAdd)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getNeferFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
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
    # 관찰은 계획의 초석은 passive에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "계획은 성공의 시작":
                    if constellation.options[0].active:
                        # 환영극 총 5타에 전부 각각 60%씩 계수 추가되기 때문에 최종 300%의 계수 추가 발생
                        additionalAttackPoints.append({"key": fightPropMpa.LUNARBLOOM_ADD_POINT.value, "value": ("elementMastery", 3), "additionalAttack": "환영극"})
                case "진실을 가리는 거짓":
                    # 원소전투 스킬 레벨 +3
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "마음을 홀리는 함정":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.GRASS_RES_MINUS.value, 0.2)
                case "기회를 포착한 순간":
                    # 원소폭발 레벨 +3
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "거머쥔 역전의 승리":
                    if constellation.options[0].active:
                        additionalAttackPoints.append({"key": fightPropMpa.LUNARBLOOM_ADD_POINT.value, "value": ("elementMastery", 0.85), "additionalAttack": "환영극"})

    # ----------------------- passive -----------------------
    # 모래의 딸은 fightProp에 영향 X
    elementBurstVeilOfDeceptionMap = [0.13, 0.16, 0.19, 0.22, 0.25, 0.28, 0.31, 0.34, 0.37, 0.40, 0.43, 0.46, 0.49, 0.52, 0.55]
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "달빛 승부사":
                    option = passive.options[0]
                    if option:
                        secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "관찰은 계획의 초석"))
                        if secondConstellation.unlocked:
                            option.maxStack = 5
                            if enkaDataFlag:
                                option.stack = 5
                        if option.stack >= option.maxStack:
                            newFightProp.add(fightPropMpa.ELEMENT_MASTERY.value, 200 if option.stack >= option.maxStack else 100)
                        newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK["환영극"].add(fightPropMpa.LUNARBLOOM_ADD_HURT.value, 0.08 * option.stack)
                        skillLevel = characterInfo.activeSkill[2].level
                        newFightProp.add(fightPropMpa.ELEMENT_BURST_ATTACK_ADD_HURT.value, elementBurstVeilOfDeceptionMap[skillLevel] * option.stack)

                case "달빛 징조의 축복·황혼의 그림자":
                    lunarBloomAdd = min(newFightProp.FIGHT_PROP_ELEMENT_MASTERY * 0.000175, 0.14)
                    newFightProp.add(fightPropMpa.LUNARBLOOM_BASE_ADD_HURT.value, lunarBloomAdd)

    # ----------------------- active -----------------------
    # active는 fightProp에 영향 X

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMpa, pointKey).value)
        newFightProp.add(key, finalPoint * value)
        if additionalAttackPoint["additionalAttack"]:
            newFightProp.FIGHT_PROP_ADDITIONAL_ATTACK[additionalAttackPoint["additionalAttack"]] = additionalAttackFightPropSchema()

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "라우마": getLaumaFightProp,
    "네페르": getNeferFightProp,
}

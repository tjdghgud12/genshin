from services.ambrApi import getAmbrApi
from services.character import getFightProp
from schemas.calculation import requestCharacterInfoSchema, responseDamageResult, responseFightPropSchema
from schemas.character import damageBaseFightPropSchema
from schemas.fightProp import fightPropSchema
from ambr import AmbrAPI
from typing import Literal
from pydantic import BaseModel
import time


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 매우 중요 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# RM: 반응 계수
# LM: 레벨 계수
# EM: 원마 보너스 -> 각 반응 마다 전부 다르기 때문에 별도 연산 필요.
#       - 증폭:         2.78 * 원마/(원마+1400)
#       - 격변,확산:    16 * 원마/(원마+2000)
#       - 격화:         5 * 원마/(원마+1200)
#       - 결정화:       4.44 * 원마/(원마+1400)
# RB: 반응 피해 증가 보너스
# PB: 피해 증가
# DEF: 방어력 계수
# RES: 내성 계수
# 격화 반응
#   Flat(C)=RM×LM×(1+EM+RB)
#   DMG=((DMG(B)+Flat(C))×(1+∑PB−피해감소)×DEF×RES
# 격변 반응
#   DMG(T)=RM×LM×(1+EM+RB)
#   DMG(Tr)=DMG(T)*RES  -> 격변 반응은 내성이 존재. 각 원소 내성깍에 따라 연산 필요.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 매우 중요 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def amplificationReaction(attackPoint: float, elementalMastery: float, amplicationBonus: float):
    # 증폭: 2.78 * 원마/(원마+1400)
    # AM=RM×(1+EM+RB)

    class amplicationDamage(BaseModel):
        forward: float
        reverse: float

    masteryBonus = 2.78 * elementalMastery / (elementalMastery + 1400)
    amplication = 1.5 * (1 + masteryBonus + amplicationBonus) * attackPoint
    reversAmplication = 2 * (1 + masteryBonus + amplicationBonus) * attackPoint

    return amplicationDamage(forward=amplication, reverse=reversAmplication)


def getFinalProp(fightProp: responseFightPropSchema, target: Literal["HP", "ATTACK", "DEFENSE"]):
    base = getattr(fightProp, f"FIGHT_PROP_BASE_{target}")
    nomal = getattr(fightProp, f"FIGHT_PROP_{target}")
    persent = getattr(fightProp, f"FIGHT_PROP_{target}_PERCENT")

    return base * (persent + 1) + nomal


def getToleranceCoefficient(tolerance: float = 0.1, decrease: float = 0.0):
    value = tolerance - decrease
    if value < 0:
        return 1 - (value / 2)
    elif value > 0.75:
        return 1 / (4 * value + 1)
    else:
        return 1 - value


def getCriticalDamageInfo(damage: float, critical: float, criticalHurt: float):

    class criticalDamageSchema(BaseModel):
        criticalDamage: float
        nonCriticalDamage: float
        expectedDamage: float

    criticalDamage = damage * (1 + criticalHurt)
    expectedDamage = (damage * (1 + criticalHurt) * critical) + (damage * (1 - critical))

    return criticalDamageSchema(criticalDamage=criticalDamage, nonCriticalDamage=damage, expectedDamage=expectedDamage)


async def damageCalculation(characterInfo: requestCharacterInfoSchema, additionalFightProp: fightPropSchema):
    # 몬스터 레벨은 100, 모든 내성은 10%로 고정
    ambrApi: AmbrAPI = await getAmbrApi()
    ambrCharacterDetail = await ambrApi.fetch_character_detail(str(characterInfo.id))
    getTotalFightProp = getFightProp.get(characterInfo.name)
    damageResult = responseDamageResult()
    element = ambrCharacterDetail.element
    elementKey = {"Fire": "FIRE", "Elec": "ELEC", "Water": "WATER", "Grass": "GRASS", "Wind": "WIND", "Rock": "ROCK", "Ice": "ICE"}
    reactions = {
        "Fire": ["융해", "증발", "연소", "발화", "과부하"],
        "Elec": ["촉진", "만개", "과부하", "감전", "초전도", "달감전"],
        "Water": ["증발", "개화", "감전", "달감전"],
        "Grass": ["발산", "개화", "연소"],
        "Wind": ["확산"],
        "Rock": ["결정화"],
        "Ice": ["융해", "초전도"],
    }
    attackTypeKey = {
        "nomal": "NOMAL_ATTACK",
        "charge": "CHARGED_ATTACK",
        "falling": "FALLING_ATTACK",
        "elementalSkill": "ELEMENT_SKILL",
        "elementalBurst": "ELEMENT_BURST",
    }

    if getTotalFightProp is not None:
        result = await getTotalFightProp(ambrCharacterDetail, characterInfo)
        fightProp: responseFightPropSchema = responseFightPropSchema(**result.fightProp.model_dump())
        for key, value in additionalFightProp.model_dump().items():
            fightProp.add(key, value)

    # 최종 기반스텟 연산
    setattr(fightProp, "FIGHT_PROP_HP_FINAL", getFinalProp(fightProp, "HP"))
    setattr(fightProp, "FIGHT_PROP_ATTACK_FINAL", getFinalProp(fightProp, "ATTACK"))
    setattr(fightProp, "FIGHT_PROP_DEFENSE_FINAL", getFinalProp(fightProp, "DEFENSE"))

    # 중간 연산 값(내성 계수, 방어력 계수)
    monsterLevel = 100
    defensCoefficient = (characterInfo.level + 100) / (
        ((monsterLevel + 100) * (1 - fightProp.FIGHT_PROP_DEFENSE_MINUS) * (1 - fightProp.FIGHT_PROP_DEFENSE_IGNORE)) + (characterInfo.level + 100)
    )
    elementToleranceCoefficient = getToleranceCoefficient(decrease=getattr(fightProp, f"FIGHT_PROP_{elementKey[element]}_RES_MINUS"))
    physicalToleranceCoefficient = getToleranceCoefficient(decrease=fightProp.FIGHT_PROP_PHYSICAL_RES_MINUS)

    enableReaction = reactions[element]
    reactionResult = []
    for skill in characterInfo.activeSkill:
        for attackType, baseFightProp in {k: v for k, v in skill.baseFightProp.model_dump().items() if v is not None}.items():
            # 차스카의 경우 별도로 처리 필요!
            targetNonCritical = getattr(damageResult, f"{attackType}NonCritical")
            targetCritical = getattr(damageResult, f"{attackType}Critical")
            targetExpected = getattr(damageResult, attackType)
            key = attackTypeKey[attackType]
            critical = fightProp.FIGHT_PROP_CRITICAL + getattr(fightProp, f"FIGHT_PROP_{key}_CRITICAL")
            criticalHurt = fightProp.FIGHT_PROP_CRITICAL_HURT + getattr(fightProp, f"FIGHT_PROP_{key}_CRITICAL_HURT")
            addHurt = fightProp.FIGHT_PROP_ATTACK_ADD_HURT + getattr(fightProp, f"FIGHT_PROP_{key}_ATTACK_ADD_HURT")
            elementAddHurt = getattr(fightProp, f"FIGHT_PROP_{key}_{elementKey[element]}_ADD_HURT") + getattr(fightProp, f"FIGHT_PROP_{elementKey[element]}_ADD_HURT")
            physicalAddHurt = fightProp.FIGHT_PROP_PHYSICAL_ADD_HURT
            finalFightProp = sum(getattr(fightProp, f"FIGHT_PROP_{key}_FINAL") * value for key, value in baseFightProp.items() if value is not None)

            targetNonCritical.physicalDamage = finalFightProp * (1 + physicalAddHurt + addHurt) * physicalToleranceCoefficient * defensCoefficient
            targetNonCritical.elementalDamage = finalFightProp * (1 + elementAddHurt + addHurt) * elementToleranceCoefficient * defensCoefficient

            for reaction in enableReaction:
                # 원소 반응 연산
                match (reaction):
                    case "융해":
                        amplication = amplificationReaction(targetNonCritical.elementalDamage, fightProp.FIGHT_PROP_ELEMENT_MASTERY, fightProp.FIGHT_PROP_MELT_ADD_HURT)
                        forward = getCriticalDamageInfo(damage=amplication.forward, critical=critical, criticalHurt=criticalHurt)
                        reverse = getCriticalDamageInfo(damage=amplication.reverse, critical=critical, criticalHurt=criticalHurt)
                        targetNonCritical.meltDamage = forward.nonCriticalDamage
                        targetNonCritical.reverseMeltDamage = reverse.nonCriticalDamage
                        targetCritical.meltDamage = forward.criticalDamage
                        targetCritical.reverseMeltDamage = reverse.criticalDamage
                        targetExpected.meltDamage = forward.expectedDamage
                        targetExpected.reverseMeltDamage = reverse.expectedDamage
                    case "증발":
                        amplication = amplificationReaction(targetNonCritical.elementalDamage, fightProp.FIGHT_PROP_ELEMENT_MASTERY, fightProp.FIGHT_PROP_EVAPORATION_ADD_HURT)
                        targetNonCritical.evaporationDamage = amplication.forward
                        targetNonCritical.reverseEvaporationDamage = amplication.reverse
                        forward = getCriticalDamageInfo(damage=amplication.forward, critical=critical, criticalHurt=criticalHurt)
                        reverse = getCriticalDamageInfo(damage=amplication.reverse, critical=critical, criticalHurt=criticalHurt)
                        targetNonCritical.evaporationDamage = forward.nonCriticalDamage
                        targetNonCritical.reverseEvaporationDamage = reverse.nonCriticalDamage
                        targetCritical.evaporationDamage = forward.criticalDamage
                        targetCritical.reverseEvaporationDamage = reverse.criticalDamage
                        targetExpected.evaporationDamage = forward.expectedDamage
                        targetExpected.reverseEvaporationDamage = reverse.expectedDamage
                    case "촉진":
                        a = 0
                    case "발산":
                        a = 0
                    case "감전":
                        a = 0
                    case "달감전":
                        a = 0
                    case "과부하":
                        a = 0
                    case "초전도":
                        a = 0
                    case "확산":
                        a = 0
                    case "개화":
                        a = 0
                    case "만개":
                        a = 0
                    case "연소":
                        a = 0
                    case "발화":
                        a = 0

    # 저렇게 하기보단, 좀 다르게 정리하는게 나중에 쓰기 편할꺼같은데,
    # class로 정리하긴 애매하고, 걍 딕셔너리로???
    # 이제 리턴할 데미지 관련 class도 하나 정의해야할듯한디
    # fightProp은 그대로 있는 상태에서, 최종 스텟들 추가해서 넘기고, FINAL HP, DEF, ATTACK 라던가
    # 나머지는 그대로 들어가되, 역증발 역융해, 정증발, 정융해는 또 별도로 해야함.

    # 각각 치명 데미지 노치명데미지를 다 줘야해.
    # 치명타가 발생 가능한 항목은 전부

    # 연산 필요 항목
    # 1. base있는 항목의 최종 값.
    # 2. 치명타 시 데미지, 노 치명타 시 데미지
    # 3. 원소 반응에 따른 데미지
    #   3-1. 증폭 반응: 융해, 증발 => 최종 곱연산
    #   3-2. 격화 반응: 촉진 발산 => 스킬계수에 추가(신학 깃털)
    #   3-3. 격변 반응: 개화(풀) 발화(불) 만개(풀) 연소(불) 과부하(불) 감전(번개) 달감전(번개) 초전도(얼음) 쇄빙(물리) 확산(반응한 원소) => 추가타격
    #   3-4. 확산 반응: 확산 => 추가 타격
    # 해당 반응들 전부 필요.
    # 연산 순서
    #   1. 원소 반응에 따른 보너스 데미지 연산
    #   2. 피해증가 및 치명타 곱연산 적용
    #   3. 무반응 시 데미지 연산.
    # 데미지 출력은 하되, 가능한 반응에 대해서만 정리 해야겠네

    return {"damage": {}, "totalFightProps": {}}

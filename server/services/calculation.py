from services.ambrApi import getAmbrApi
from services.character import getFightProp
from schemas.calculation import requestCharacterInfoSchema, responseDamageResult, responseFightPropSchema
from schemas.character import damageBaseFightPropSchema
from schemas.fightProp import fightPropSchema
from data.globalVariable import levelCoefficient
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


def catalyzeReaction(level: int, elementalMastery: float, catalyzeBonus: float, totalAddHurt: float, coefficient: float):
    # EM = 5 * 원마/(원마+1200)
    masteryBonus = 5 * elementalMastery / (elementalMastery + 1200)
    return levelCoefficient[level] * coefficient * (1 + masteryBonus + catalyzeBonus) * totalAddHurt


def transformativeReaction(level: int, elementalMastery: float, transformativeBonus: float, toleranceCoefficient: float, coefficient: float):
    # EM = 16 * 원마/(원마+2000)
    masteryBonus = 16 * elementalMastery / (elementalMastery + 2000)
    return levelCoefficient[level] * coefficient * (1 + masteryBonus + transformativeBonus) * toleranceCoefficient


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
            # 커스텀 영역에 대해서 처리 필요!
            targetNonCritical = getattr(damageResult, f"{attackType}NonCritical")
            targetCritical = getattr(damageResult, f"{attackType}Critical")
            targetExpected = getattr(damageResult, attackType)

            key = attackTypeKey[attackType]

            critical = fightProp.FIGHT_PROP_CRITICAL + getattr(fightProp, f"FIGHT_PROP_{key}_CRITICAL")
            criticalHurt = fightProp.FIGHT_PROP_CRITICAL_HURT + getattr(fightProp, f"FIGHT_PROP_{key}_CRITICAL_HURT")

            addHurt = fightProp.FIGHT_PROP_ATTACK_ADD_HURT + getattr(fightProp, f"FIGHT_PROP_{key}_ATTACK_ADD_HURT")
            elementAddHurt = getattr(fightProp, f"FIGHT_PROP_{key}_{elementKey[element]}_ADD_HURT") + getattr(fightProp, f"FIGHT_PROP_{elementKey[element]}_ADD_HURT")
            physicalAddHurt = fightProp.FIGHT_PROP_PHYSICAL_ADD_HURT

            totalElementalAddHurt = (1 + elementAddHurt + addHurt) * elementToleranceCoefficient * defensCoefficient

            finalFightProp = sum(getattr(fightProp, f"FIGHT_PROP_{key}_FINAL") * value for key, value in baseFightProp.items() if value is not None)

            targetNonCritical.physicalDamage = finalFightProp * (1 + physicalAddHurt + addHurt) * physicalToleranceCoefficient * defensCoefficient
            targetNonCritical.elementalDamage = finalFightProp * totalElementalAddHurt

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
                        amplication = amplificationReaction(targetNonCritical.elementalDamage, fightProp.FIGHT_PROP_ELEMENT_MASTERY, fightProp.FIGHT_PROP_VAPORIZE_ADD_HURT)
                        targetNonCritical.vaporizeDamage = amplication.forward
                        targetNonCritical.reversevaporizeDamage = amplication.reverse
                        forward = getCriticalDamageInfo(damage=amplication.forward, critical=critical, criticalHurt=criticalHurt)
                        reverse = getCriticalDamageInfo(damage=amplication.reverse, critical=critical, criticalHurt=criticalHurt)
                        targetNonCritical.vaporizeDamage = forward.nonCriticalDamage
                        targetNonCritical.reversevaporizeDamage = reverse.nonCriticalDamage
                        targetCritical.vaporizeDamage = forward.criticalDamage
                        targetCritical.reversevaporizeDamage = reverse.criticalDamage
                        targetExpected.vaporizeDamage = forward.expectedDamage
                        targetExpected.reversevaporizeDamage = reverse.expectedDamage
                    case "촉진":
                        aggravate = getCriticalDamageInfo(
                            damage=catalyzeReaction(
                                characterInfo.level, fightProp.FIGHT_PROP_ELEMENT_MASTERY, fightProp.FIGHT_PROP_AGGRAVATE_ADD_HURT, totalElementalAddHurt, 1.15
                            ),
                            critical=critical,
                            criticalHurt=criticalHurt,
                        )
                        damageResult.aggravateDamageNonCritical = aggravate.nonCriticalDamage
                        damageResult.aggravateDamageCritical = aggravate.criticalDamage
                        damageResult.aggravateDamage = aggravate.expectedDamage
                    case "발산":
                        aggravate = getCriticalDamageInfo(
                            damage=catalyzeReaction(
                                characterInfo.level, fightProp.FIGHT_PROP_ELEMENT_MASTERY, fightProp.FIGHT_PROP_AGGRAVATE_ADD_HURT, totalElementalAddHurt, 1.25
                            ),
                            critical=critical,
                            criticalHurt=criticalHurt,
                        )
                        damageResult.aggravateDamageNonCritical = aggravate.nonCriticalDamage
                        damageResult.aggravateDamageCritical = aggravate.criticalDamage
                        damageResult.aggravateDamage = aggravate.expectedDamage
                    case "감전":
                        damageResult.electroChargedDamage = transformativeReaction(
                            characterInfo.level,
                            fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                            fightProp.FIGHT_PROP_ELECTROCHARGED_ADD_HURT,
                            getToleranceCoefficient(decrease=fightProp.FIGHT_PROP_ELEC_RES_MINUS),
                            1.2,
                        )
                    case "달감전":
                        # 달감전에 대해 좀 더 조사 필요
                        a = 0
                    case "과부하":
                        damageResult.overloadedDamage = transformativeReaction(
                            characterInfo.level,
                            fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                            fightProp.FIGHT_PROP_OVERLOADED_ADD_HURT,
                            getToleranceCoefficient(decrease=fightProp.FIGHT_PROP_FIRE_RES_MINUS),
                            2.0,
                        )
                    case "초전도":
                        damageResult.superconductDamage = transformativeReaction(
                            characterInfo.level,
                            fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                            fightProp.FIGHT_PROP_SUPERCONDUCT_ADD_HURT,
                            getToleranceCoefficient(decrease=fightProp.FIGHT_PROP_ICE_RES_MINUS),
                            0.5,
                        )
                    case "확산":
                        swirlList = ["fire", "water", "ice", "elec"]
                        for swirl in swirlList:
                            setattr(
                                damageResult,
                                f"{swirl}SwirlDamage",
                                transformativeReaction(
                                    characterInfo.level,
                                    fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                    fightProp.FIGHT_PROP_SWIRL_ADD_HURT,
                                    getToleranceCoefficient(decrease=getattr(fightProp, f"FIGHT_PROP_{swirl.upper()}_RES_MINUS")),
                                    0.5,
                                ),
                            )
                    case "개화":
                        damageResult.bloomDamage = transformativeReaction(
                            characterInfo.level,
                            fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                            fightProp.FIGHT_PROP_BLOOM_ADD_HURT,
                            getToleranceCoefficient(decrease=fightProp.FIGHT_PROP_GRASS_RES_MINUS),
                            2.0,
                        )
                    case "만개":
                        damageResult.hyperBloomDamage = transformativeReaction(
                            characterInfo.level,
                            fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                            fightProp.FIGHT_PROP_HYPERBLOOM_ADD_HURT,
                            getToleranceCoefficient(decrease=fightProp.FIGHT_PROP_GRASS_RES_MINUS),
                            3.0,
                        )
                    case "연소":
                        damageResult.burningDamage = transformativeReaction(
                            characterInfo.level,
                            fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                            fightProp.FIGHT_PROP_BURGEON_ADD_HURT,
                            getToleranceCoefficient(decrease=fightProp.FIGHT_PROP_FIRE_RES_MINUS),
                            0.25,
                        )
                    case "발화":
                        damageResult.burgeonDamage = transformativeReaction(
                            characterInfo.level,
                            fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                            fightProp.FIGHT_PROP_BURGEON_ADD_HURT,
                            getToleranceCoefficient(decrease=fightProp.FIGHT_PROP_FIRE_RES_MINUS),
                            3.0,
                        )

    return {"damage": {}, "totalFightProps": {}}

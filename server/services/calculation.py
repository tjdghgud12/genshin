from services.ambrApi import getAmbrApi
from services.character import getFightProp
from schemas.calculation import requestCharacterInfoSchema, responseDamageResult, responseFightPropSchema, damageResultSchema
from schemas.fightProp import fightPropSchema
from data.globalVariable import levelCoefficientMap
from ambr import AmbrAPI
from typing import Literal
from pydantic import BaseModel
from functools import partial
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


def amplificationReaction(attackPoint: float, elementalMastery: float, amplicationBonus: float, coefficient: float):
    # 증폭: 2.78 * 원마/(원마+1400)
    # AM=RM×(1+EM+RB)
    masteryBonus = 2.78 * elementalMastery / (elementalMastery + 1400)
    return attackPoint * coefficient * (1 + masteryBonus + amplicationBonus)


def catalyzeReaction(attackPoint: float, elementalMastery: float, catalyzeBonus: float, coefficient: float):
    # EM = 5 * 원마/(원마+1200)
    masteryBonus = 5 * elementalMastery / (elementalMastery + 1200)
    return attackPoint * coefficient * (1 + masteryBonus + catalyzeBonus)


def transformativeReaction(level: int, elementalMastery: float, transformativeBonus: float, resMinus: float, coefficient: float, finalAddHurt: float = 0.0):
    # EM = 16 * 원마/(원마+2000)
    masteryBonus = 16 * elementalMastery / (elementalMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=resMinus)
    return levelCoefficientMap[level] * coefficient * (1 + masteryBonus + transformativeBonus) * toleranceCoefficient * (1 + finalAddHurt)


async def damageCalculation(characterInfo: requestCharacterInfoSchema, additionalFightProp: fightPropSchema):
    # 몬스터 레벨은 100, 모든 내성은 10%로 고정
    ambrApi: AmbrAPI = await getAmbrApi()
    ambrCharacterDetail = await ambrApi.fetch_character_detail(str(characterInfo.id))
    getTotalFightProp = getFightProp.get(characterInfo.name)
    damageResult = responseDamageResult()
    element = ambrCharacterDetail.element
    reactions = {
        "Fire": ["역융해", "증발", "연소", "발화", "과부하"],
        "Elec": ["촉진", "만개", "과부하", "감전", "초전도"],
        "Water": ["역증발", "개화", "감전"],
        "Grass": ["발산", "개화", "연소"],
        "Wind": ["확산"],
        "Rock": [],
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

    roopReactionHandlerMap = {
        "융해": (partial(amplificationReaction, amplicationBonus=fightProp.FIGHT_PROP_MELT_ADD_HURT, coefficient=1.5), "meltDamage"),
        "역융해": (partial(amplificationReaction, amplicationBonus=fightProp.FIGHT_PROP_MELT_ADD_HURT, coefficient=2.0), "reverseMeltDamage"),
        "증발": (partial(amplificationReaction, amplicationBonus=fightProp.FIGHT_PROP_VAPORIZE_ADD_HURT, coefficient=1.5), "vaporizeDamage"),
        "역증발": (partial(amplificationReaction, amplicationBonus=fightProp.FIGHT_PROP_VAPORIZE_ADD_HURT, coefficient=2.0), "reverseVaporizeDamage"),
        "촉진": (partial(catalyzeReaction, catalyzeBonus=fightProp.FIGHT_PROP_MELT_ADD_HURT, coefficient=1.15), "aggravateDamage"),
        "발산": (partial(catalyzeReaction, catalyzeBonus=fightProp.FIGHT_PROP_MELT_ADD_HURT, coefficient=1.25), "spreadDamage"),
    }

    transformativeReactionHandlerMap = {
        "감전": (
            partial(transformativeReaction, transformativeBonus=fightProp.FIGHT_PROP_ELECTROCHARGED_ADD_HURT, resMinus=fightProp.FIGHT_PROP_ELEC_RES_MINUS, coefficient=1.2),
            "electroChargedDamage",
        ),
        "과부하": (
            partial(transformativeReaction, transformativeBonus=fightProp.FIGHT_PROP_OVERLOADED_ADD_HURT, resMinus=fightProp.FIGHT_PROP_FIRE_RES_MINUS, coefficient=2.0),
            "overloadedDamage",
        ),
        "초전도": (
            partial(transformativeReaction, transformativeBonus=fightProp.FIGHT_PROP_SUPERCONDUCT_ADD_HURT, resMinus=fightProp.FIGHT_PROP_ICE_RES_MINUS, coefficient=0.5),
            "superconductDamage",
        ),
        "쇄빙": (
            partial(transformativeReaction, transformativeBonus=fightProp.FIGHT_PROP_SHATTER_ADD_HURT, resMinus=fightProp.FIGHT_PROP_PHYSICAL_RES_MINUS, coefficient=1.5),
            "shatterDamage",
        ),
        "개화": (
            partial(transformativeReaction, transformativeBonus=fightProp.FIGHT_PROP_BLOOM_ADD_HURT, resMinus=fightProp.FIGHT_PROP_GRASS_RES_MINUS, coefficient=2.0),
            "bloomDamage",
        ),
        "만개": (
            partial(transformativeReaction, transformativeBonus=fightProp.FIGHT_PROP_HYPERBLOOM_ADD_HURT, resMinus=fightProp.FIGHT_PROP_GRASS_RES_MINUS, coefficient=3.0),
            "hyperBloomDamage",
        ),
        "발화": (
            partial(transformativeReaction, transformativeBonus=fightProp.FIGHT_PROP_BURGEON_ADD_HURT, resMinus=fightProp.FIGHT_PROP_FIRE_RES_MINUS, coefficient=3.0),
            "burgeonDamage",
        ),
        "연소": (
            partial(transformativeReaction, transformativeBonus=fightProp.FIGHT_PROP_BURNING_ADD_HURT, resMinus=fightProp.FIGHT_PROP_FIRE_RES_MINUS, coefficient=0.25),
            "burningDamage",
        ),
    }

    lunarReactionHandlerMap = {
        "달감전": (
            partial(
                transformativeReaction,
                transformativeBonus=fightProp.FIGHT_PROP_LUNARCHARGED_ADD_HURT,
                resMinus=fightProp.FIGHT_PROP_ELEC_RES_MINUS,
                coefficient=1.8,
                finalAddHurt=fightProp.FIGHT_PROP_FINAL_LUNARCHARGED_ADD_HURT,
            ),
            "lunarChargedDamage",
        )
    }

    # 최종 기반스텟 연산
    setattr(fightProp, "FIGHT_PROP_HP_FINAL", getFinalProp(fightProp, "HP"))
    setattr(fightProp, "FIGHT_PROP_ATTACK_FINAL", getFinalProp(fightProp, "ATTACK"))
    setattr(fightProp, "FIGHT_PROP_DEFENSE_FINAL", getFinalProp(fightProp, "DEFENSE"))

    # 중간 연산 값(내성 계수, 방어력 계수)
    monsterLevel = 100
    defensCoefficient = (characterInfo.level + 100) / (
        ((monsterLevel + 100) * (1 - fightProp.FIGHT_PROP_DEFENSE_MINUS) * (1 - fightProp.FIGHT_PROP_DEFENSE_IGNORE)) + (characterInfo.level + 100)
    )
    elementToleranceCoefficient = getToleranceCoefficient(decrease=getattr(fightProp, f"FIGHT_PROP_{element.upper()}_RES_MINUS"))
    physicalToleranceCoefficient = getToleranceCoefficient(decrease=fightProp.FIGHT_PROP_PHYSICAL_RES_MINUS)

    enableReaction = reactions[element]
    if characterInfo.name == "이네파":
        enableReaction.append("달감전")

    for skill in characterInfo.activeSkill:
        for attackType, baseFightProp in {k: v for k, v in skill.baseFightProp.model_dump().items() if v is not None}.items():
            # 차스카의 경우 별도로 처리 필요!
            # 커스텀 영역에 대해서 처리 필요!
            key = attackTypeKey[attackType]
            targetNonCritical = getattr(damageResult, f"{attackType}NonCritical")
            targetCritical = getattr(damageResult, f"{attackType}Critical")
            targetExpected = getattr(damageResult, attackType)
            finalAttackPoint = sum(getattr(fightProp, f"FIGHT_PROP_{key}_FINAL") * value for key, value in baseFightProp.items() if value is not None)
            critical = fightProp.FIGHT_PROP_CRITICAL + getattr(fightProp, f"FIGHT_PROP_{key}_CRITICAL")
            criticalHurt = fightProp.FIGHT_PROP_CRITICAL_HURT + getattr(fightProp, f"FIGHT_PROP_{key}_CRITICAL_HURT")

            addHurt = fightProp.FIGHT_PROP_ATTACK_ADD_HURT + getattr(fightProp, f"FIGHT_PROP_{key}_ATTACK_ADD_HURT")
            elementAddHurt = getattr(fightProp, f"FIGHT_PROP_{key}_{element.upper()}_ADD_HURT") + getattr(fightProp, f"FIGHT_PROP_{element.upper()}_ADD_HURT")
            physicalAddHurt = fightProp.FIGHT_PROP_PHYSICAL_ADD_HURT

            finalElementalAddHurt = (1 + elementAddHurt + addHurt) * elementToleranceCoefficient * defensCoefficient

            targetNonCritical.physicalDamage = finalAttackPoint * (1 + physicalAddHurt + addHurt) * physicalToleranceCoefficient * defensCoefficient
            elementalDamage = finalAttackPoint * finalElementalAddHurt

            for reaction in enableReaction:  # 증폭 격변 반응 연산
                attackPoints = getCriticalDamageInfo(
                    damage=levelCoefficientMap[characterInfo.level] * finalElementalAddHurt if reaction == "촉진" or reaction == "발산" else elementalDamage,
                    critical=critical,
                    criticalHurt=criticalHurt,
                )
                if reaction in roopReactionHandlerMap:
                    reactionHandler, attr = roopReactionHandlerMap[reaction]
                    setattr(targetNonCritical, attr, reactionHandler(attackPoints.nonCriticalDamage, fightProp.FIGHT_PROP_ELEMENT_MASTERY))
                    setattr(targetCritical, attr, reactionHandler(attackPoints.criticalDamage, fightProp.FIGHT_PROP_ELEMENT_MASTERY))
                    setattr(targetExpected, attr, reactionHandler(attackPoints.expectedDamage, fightProp.FIGHT_PROP_ELEMENT_MASTERY))

    # 격변 반응 별도 처리 진행
    for reaction in enableReaction:
        if reaction in transformativeReactionHandlerMap:
            reactionHandler, attr = transformativeReactionHandlerMap[reaction]
            setattr(damageResult, attr, reactionHandler(characterInfo.level, fightProp.FIGHT_PROP_ELEMENT_MASTERY))

    # 달반응 별도 처리 진행
    for reaction in enableReaction:
        if reaction in lunarReactionHandlerMap:
            reactionHandler, attr = lunarReactionHandlerMap[reaction]
            lunarDamage = getCriticalDamageInfo(
                damage=reactionHandler(characterInfo.level, fightProp.FIGHT_PROP_ELEMENT_MASTERY),
                critical=critical,
                criticalHurt=criticalHurt,
            )
            setattr(damageResult, f"{attr}NonCritical", lunarDamage.nonCriticalDamage)
            setattr(damageResult, f"{attr}Critical", lunarDamage.criticalDamage)
            setattr(damageResult, attr, lunarDamage.expectedDamage)

    # 확산
    if "확산" in enableReaction:
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

    return {"damage": {}, "totalFightProps": {}}

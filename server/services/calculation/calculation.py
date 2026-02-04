from ambr import AmbrAPI
from itertools import chain
from typing import Literal
from services.ambrApi import getAmbrApi
from schemas.calculation import requestCharacterInfoSchema, responseDamageResult, responseFightPropSchema, damageResultSchema, responseCalculationResult
from data.globalVariable import levelCoefficientMap, fightPropMap
from services.calculation.utils import getFinalProp, getToleranceCoefficient, getCriticalDamageInfo, baseFightPropKeyMap
from services.calculation.reaction import (
    getVaporizeDamage,
    getMeltDamage,
    getElectroChargedDamage,
    getSuperconductDamage,
    getOverloadedDamage,
    getSwirlDamage,
    getBloomDamage,
    getHyperBloomDamage,
    getBurgeonDamage,
    getBurningDamage,
    getAggravateDamage,
    getSpreadDamage,
    getShatterDamage,
    getLunarBloomDamage,
    getLunarChargedDamage,
    getLunarCrystallizeDamage,
)
from services.character import getFightProp
from services.character.commonData import CharacterFightPropReturnData
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema

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


lunarReactionMap = {
    "lunarBloom": {"reaction": getLunarBloomDamage, "resMinus": fightPropMap.GRASS_RES_MINUS.value},
    "lunarCharged": {"reaction": getLunarChargedDamage, "resMinus": fightPropMap.ELEC_RES_MINUS.value},
    "lunarCrystallize": {"reaction": getLunarCrystallizeDamage, "resMinus": fightPropMap.ROCK_RES_MINUS.value},
}


def getLunarDamage(
    attackTypeKey: Literal["lunarBloom", "lunarCharged", "lunarCrystallize"],
    fightProp: responseFightPropSchema,
    critical: float,
    criticalHurt: float,
    finalAttackPoint: float,
    reaction: bool = False,
):
    getLunarReaction = lunarReactionMap[attackTypeKey]["reaction"]
    lunarAdditionalCriticalDamage = None
    lunarExtraCriticalDamage = None
    resMinus = getattr(fightProp, lunarReactionMap[attackTypeKey]["resMinus"], 0.0)
    lunarType = attackTypeKey.upper()
    lunarAdditionalPoint = getattr(fightProp, f"FIGHT_PROP_{lunarType}_ADD_POINT", 0.0)
    lunarExtraDamage = getattr(fightProp, f"FIGHT_PROP_{lunarType}_EXTRA_DAMAGE", 0.0)
    lunarBaseAddHurt = 1 + fightProp.FIGHT_PROP_LUNAR_BASE_ADD_HURT + getattr(fightProp, f"FIGHT_PROP_{lunarType}_BASE_ADD_HURT", 0.0)
    lunarAddHurt = 1 + fightProp.FIGHT_PROP_LUNAR_ADD_HURT + getattr(fightProp, f"FIGHT_PROP_{lunarType}_ADD_HURT", 0.0)
    lunarPromotion = 1 + fightProp.FIGHT_PROP_LUNAR_PROMOTION + getattr(fightProp, f"FIGHT_PROP_{lunarType}_PROMOTION", 0.0)
    lunarCritical = critical + getattr(fightProp, "FIGHT_PROP_LUNAR_CRITICAL", 0.0) + getattr(fightProp, f"FIGHT_PROP_{lunarType}_CRITICAL", 0.0)
    lunarCriticalHurt = criticalHurt + getattr(fightProp, "FIGHT_PROP_LUNAR_CRITICAL_HURT", 0.0) + getattr(fightProp, f"FIGHT_PROP_{lunarType}_CRITICAL_HURT", 0.0)

    lunarDamage = getLunarReaction(
        attackPoint=finalAttackPoint,
        elementMastery=fightProp.FIGHT_PROP_ELEMENT_MASTERY,
        lunarBaseAddHurt=lunarBaseAddHurt,
        lunarPromotion=lunarPromotion,
        resMinus=resMinus,
        lunarAddHurt=lunarAddHurt,
        reaction=reaction,
    )
    lunarCriticalDamage = getCriticalDamageInfo(
        damage=lunarDamage,
        critical=lunarCritical,
        criticalHurt=lunarCriticalHurt,
    )
    if lunarAdditionalPoint > 0:
        lunarAdditionalDamage = getLunarReaction(
            attackPoint=finalAttackPoint,
            elementMastery=fightProp.FIGHT_PROP_ELEMENT_MASTERY,
            lunarBaseAddHurt=lunarBaseAddHurt,
            lunarPromotion=lunarPromotion,
            resMinus=resMinus,
            lunarAddHurt=lunarAddHurt,
            reaction=reaction,
        )
        lunarAdditionalCriticalDamage = getCriticalDamageInfo(
            damage=lunarAdditionalDamage,
            critical=lunarCritical,
            criticalHurt=lunarCriticalHurt,
        )
    if lunarExtraDamage > 0:
        # ex) 라우마 Q 스텍
        # 라우마의 Q 스텍은 각종 피증 및 원마보너스가 적용되지 않음.
        lunarExtraDamage = getLunarReaction(
            attackPoint=lunarExtraDamage,
            elementMastery=0,
            lunarBaseAddHurt=0,
            lunarPromotion=lunarPromotion,
            resMinus=resMinus,
            lunarAddHurt=0,
            reaction=reaction,
        )
        lunarExtraCriticalDamage = getCriticalDamageInfo(
            damage=lunarExtraDamage,
            critical=lunarCritical,
            criticalHurt=lunarCriticalHurt,
        )

    return lunarCriticalDamage, lunarAdditionalCriticalDamage, lunarExtraCriticalDamage


async def damageCalculation(characterInfo: requestCharacterInfoSchema, additionalFightProp: fightPropSchema) -> responseCalculationResult:
    # 몬스터 레벨은 100, 모든 내성은 10%로 고정
    ambrApi: AmbrAPI = await getAmbrApi()
    ambrCharacterDetail = await ambrApi.fetch_character_detail(str(characterInfo.id))
    getTotalFightProp = getFightProp.get(characterInfo.name)
    damageResult = responseDamageResult()
    reactionMap = {
        "physical": [],
        "fire": ["역융해", "증발", "연소", "발화", "과부하"],
        "elec": ["촉진", "만개", "과부하", "감전", "초전도"],
        "water": ["역증발", "개화", "감전"],
        "grass": ["발산", "개화", "연소"],
        "wind": ["확산"],
        "rock": [],
        "ice": ["융해", "초전도"],
    }
    attackTypeKeyMap = {
        "nomal": "NOMAL_ATTACK",
        "charge": "CHARGED_ATTACK",
        "falling": "FALLING_ATTACK",
        "elementalSkill": "ELEMENT_SKILL",
        "elementalBurst": "ELEMENT_BURST",
    }

    # ------------------------------------ 공격 종류 입력 ------------------------------------
    attacks = []
    for skill in characterInfo.activeSkill:
        attacks.extend((k, v, False) for k, v in skill.baseFightProp.model_dump().items() if v is not None)
        if skill.additionalAttack is not None:
            for additional in skill.additionalAttack:
                damageResult.customNonCritical[additional.name] = damageResultSchema()
                damageResult.customCritical[additional.name] = damageResultSchema()
                damageResult.custom[additional.name] = damageResultSchema()
                attacks.append((additional.type, additional.baseFightProp.model_dump(), additional.name))

    for data in chain(characterInfo.passiveSkill, characterInfo.constellations):
        if data.unlocked:
            if data.additionalAttack is not None:
                for additional in data.additionalAttack:
                    damageResult.customNonCritical[additional.name] = damageResultSchema()
                    damageResult.customCritical[additional.name] = damageResultSchema()
                    damageResult.custom[additional.name] = damageResultSchema()
                    attacks.append((additional.type, additional.baseFightProp.model_dump(), additional.name))
    # -----------------------------------------------------------------------------------

    # 캐릭터 자체 스텟 연산
    if getTotalFightProp is not None:
        result: CharacterFightPropReturnData = await getTotalFightProp(ambrCharacterDetail, characterInfo)
        fightProp: responseFightPropSchema = responseFightPropSchema(**result.fightProp.model_dump())
        for key, value in additionalFightProp.model_dump().items():
            fightProp.add(key, value)

    # 최종 기반스텟 연산
    setattr(fightProp, "FIGHT_PROP_HP_FINAL", getFinalProp(fightProp, "HP"))
    setattr(fightProp, "FIGHT_PROP_ATTACK_FINAL", getFinalProp(fightProp, "ATTACK"))
    setattr(fightProp, "FIGHT_PROP_DEFENSE_FINAL", getFinalProp(fightProp, "DEFENSE"))

    # 방어력 계수
    monsterLevel = 100
    defensCoefficient = (characterInfo.level + 100) / (
        ((monsterLevel + 100) * (1 - fightProp.FIGHT_PROP_DEFENSE_MINUS) * (1 - fightProp.FIGHT_PROP_DEFENSE_IGNORE)) + (characterInfo.level + 100)
    )

    # 차스카의 경우 별도로 처리 필요
    for attackType, baseFightProp, customName in attacks:
        attackTypeKey = attackTypeKeyMap.get(attackType, "")
        if isinstance(customName, str):
            targetNonCritical = damageResult.customNonCritical[customName]
            targetCritical = damageResult.customCritical[customName]
            targetExpected = damageResult.custom[customName]
        else:
            targetNonCritical = getattr(damageResult, f"{attackType}NonCritical")
            targetCritical = getattr(damageResult, f"{attackType}Critical")
            targetExpected = getattr(damageResult, attackType)

        baseValues = [(getattr(fightProp, base.value), value) for base in baseFightPropKeyMap if (value := baseFightProp.get(base.name)) is not None]
        finalAttackPoint = sum(prop * val for prop, val in baseValues) if baseValues else None

        if finalAttackPoint:
            elements = baseFightProp.get("element", [])

            for element in elements:
                reactions = reactionMap.get(element, [])
                toleranceCoefficient = getToleranceCoefficient(decrease=getattr(fightProp, f"FIGHT_PROP_{element.upper()}_RES_MINUS"))
                additionalAttackPoint = (
                    fightProp.FIGHT_PROP_ATTACK_ADD_POINT
                    + getattr(fightProp, f"FIGHT_PROP_{attackTypeKey}_ATTACK_ADD_POINT", 0.0)
                    + getattr(fightProp, f"FIGHT_PROP_{element.upper()}_ADD_POINT", 0.0)
                    + getattr(fightProp, f"FIGHT_PROP_{attackTypeKey}_{element.upper()}_ADD_POINT", 0.0)
                )

                if customName:
                    targetCustomPoint = fightProp.FIGHT_PROP_ADDITIONAL_ATTACK.get(customName, additionalAttackFightPropSchema())
                    additionalAttackPoint += getattr(targetCustomPoint, "FIGHT_PROP_ATTACK_ADD_POINT", 0.0)

                critical = fightProp.FIGHT_PROP_CRITICAL + getattr(fightProp, f"FIGHT_PROP_{attackTypeKey}_CRITICAL", 0.0)
                criticalHurt = (
                    fightProp.FIGHT_PROP_CRITICAL_HURT
                    + getattr(fightProp, f"FIGHT_PROP_{key}_CRITICAL_HURT", 0.0)
                    + getattr(fightProp, f"FIGHT_PROP_{element.upper()}_CRITICAL_HURT", 0.0)
                )
                addHurt = (
                    1
                    + fightProp.FIGHT_PROP_ATTACK_ADD_HURT
                    + getattr(fightProp, f"FIGHT_PROP_{attackTypeKey}_ATTACK_ADD_HURT", 0.0)
                    + getattr(fightProp, f"FIGHT_PROP_{element.upper()}_ADD_HURT", 0.0)
                )
                finalDamageAddHurt = 1 + getattr(fightProp, f"FIGHT_PROP_FINAL_{attackTypeKey}_ATTACK_ADD_HURT", 0.0)  # 최종 피해 증가(곱연산, 피해증가 옵션 X)

                # 직접 달 반응 연산
                if attackType in ["lunarBloom", "lunarCharged", "lunarCrystallize"]:
                    lunarCriticalDamage, lunarAdditionalCriticalDamage, lunarExtraCriticalDamage = getLunarDamage(
                        attackTypeKey=attackType,
                        fightProp=fightProp,
                        critical=critical,
                        criticalHurt=criticalHurt,
                        finalAttackPoint=finalAttackPoint,
                    )
                    setattr(targetCritical, f"{attackType}Damage", lunarCriticalDamage.criticalDamage)
                    setattr(targetNonCritical, f"{attackType}Damage", lunarCriticalDamage.nonCriticalDamage)
                    setattr(targetExpected, f"{attackType}Damage", lunarCriticalDamage.expectedDamage)
                    if lunarAdditionalCriticalDamage:
                        setattr(targetNonCritical, f"{attackType}DamageAdditional", lunarAdditionalCriticalDamage.nonCriticalDamage)
                        setattr(targetCritical, f"{attackType}DamageAdditional", lunarAdditionalCriticalDamage.criticalDamage)
                        setattr(targetExpected, f"{attackType}DamageAdditional", lunarAdditionalCriticalDamage.expectedDamage)
                    if lunarExtraCriticalDamage:
                        setattr(targetNonCritical, f"{attackType}DamageExtra", lunarExtraCriticalDamage.nonCriticalDamage)
                        setattr(targetCritical, f"{attackType}DamageExtra", lunarExtraCriticalDamage.criticalDamage)
                        setattr(targetExpected, f"{attackType}DamageExtra", lunarExtraCriticalDamage.expectedDamage)

                    continue

                # 데미지 연산
                totalMultiplyDamage = (1 + addHurt) * toleranceCoefficient * defensCoefficient * finalDamageAddHurt
                damages = finalAttackPoint * totalMultiplyDamage
                finalDamage = getCriticalDamageInfo(
                    damage=damages,
                    critical=critical,
                    criticalHurt=criticalHurt,
                )

                damageType = "physicalDamage" if element == "physical" else "elementalDamage"
                setattr(targetNonCritical, damageType, finalDamage.nonCriticalDamage)
                setattr(targetCritical, damageType, finalDamage.criticalDamage)
                setattr(targetExpected, damageType, finalDamage.expectedDamage)

                if additionalAttackPoint > 0:  # 추가 계수 영역
                    additionalDamages = additionalAttackPoint * totalMultiplyDamage
                    finalAdditionalDamage = getCriticalDamageInfo(
                        damage=additionalDamages,
                        critical=critical,
                        criticalHurt=criticalHurt,
                    )
                    additionalDamageType = f"{damageType}Additional"
                    setattr(targetNonCritical, additionalDamageType, finalAdditionalDamage.nonCriticalDamage)
                    setattr(targetCritical, additionalDamageType, finalAdditionalDamage.criticalDamage)
                    setattr(targetExpected, additionalDamageType, finalAdditionalDamage.expectedDamage)

                # 원소 반응 연산
                damageList = [(finalDamage.nonCriticalDamage, targetNonCritical), (finalDamage.criticalDamage, targetCritical), (finalDamage.expectedDamage, targetExpected)]
                for reaction in reactions:
                    # 증폭 및 격화 반응
                    for damage, target in damageList:
                        match reaction:
                            case "증발":
                                vaporizeDamages = getVaporizeDamage(
                                    attackPoint=damage,
                                    elementMastery=fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                    vaporizeAddHurt=fightProp.FIGHT_PROP_VAPORIZE_ADD_HURT,
                                )
                                setattr(target, "vaporizeDamage", vaporizeDamages)
                            case "역증발":
                                reverseVaporizeDamages = getVaporizeDamage(
                                    attackPoint=damage,
                                    elementMastery=fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                    vaporizeAddHurt=fightProp.FIGHT_PROP_VAPORIZE_ADD_HURT,
                                    reverse=True,
                                )
                                setattr(target, "reverseVaporizeDamage", reverseVaporizeDamages)
                            case "융해":
                                meltDamages = getMeltDamage(
                                    attackPoint=damage,
                                    elementMastery=fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                    meltAddHurt=fightProp.FIGHT_PROP_MELT_ADD_HURT,
                                )
                                setattr(target, "meltDamage", meltDamages)
                            case "역융해":
                                reverseMeltDamages = getMeltDamage(
                                    attackPoint=damage,
                                    elementMastery=fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                    meltAddHurt=fightProp.FIGHT_PROP_MELT_ADD_HURT,
                                    reverse=True,
                                )
                                setattr(target, "reverseMeltDamage", reverseMeltDamages)

                            # 격화 반응
                            case "촉진":
                                aggravateDamages = getAggravateDamage(
                                    level=characterInfo.level,
                                    elementMastery=fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                    aggravateAddHurt=fightProp.FIGHT_PROP_AGGRAVATE_ADD_HURT,
                                    totalAddHurt=totalMultiplyDamage,
                                )
                                setattr(target, "aggravateDamage", aggravateDamages)
                            case "발산":
                                spreadDamages = getSpreadDamage(
                                    level=characterInfo.level,
                                    elementMastery=fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                    spreadAddHurt=fightProp.FIGHT_PROP_SPREAD_ADD_HURT,
                                    totalAddHurt=totalMultiplyDamage,
                                )
                                setattr(target, "spreadDamage", spreadDamages)

                    # 격변 반응
                    match reaction:
                        case "과부하":
                            overloadedDamages = getOverloadedDamage(
                                characterInfo.level,
                                fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                fightProp.FIGHT_PROP_OVERLOADED_ADD_HURT,
                                fightProp.FIGHT_PROP_FIRE_RES_MINUS,
                            )
                            setattr(targetExpected, "overloadedDamage", overloadedDamages)
                        case "감전":
                            electroChargedDamages = getElectroChargedDamage(
                                characterInfo.level,
                                fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                fightProp.FIGHT_PROP_ELECTROCHARGED_ADD_HURT,
                                fightProp.FIGHT_PROP_ELEC_RES_MINUS,
                            )
                            setattr(targetExpected, "electroChargedDamage", electroChargedDamages)
                        case "초전도":
                            superconductDamages = getSuperconductDamage(
                                characterInfo.level,
                                fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                fightProp.FIGHT_PROP_SUPERCONDUCT_ADD_HURT,
                                fightProp.FIGHT_PROP_ICE_RES_MINUS,
                            )
                            setattr(targetExpected, "superconductDamage", superconductDamages)
                        case "쇄빙":
                            shatterDamages = getShatterDamage(
                                characterInfo.level,
                                fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                fightProp.FIGHT_PROP_SHATTER_ADD_HURT,
                                fightProp.FIGHT_PROP_PHYSICAL_RES_MINUS,
                            )
                            setattr(targetExpected, "shatterDamage", shatterDamages)
                        case "개화":
                            bloomDamages = getBloomDamage(
                                characterInfo.level,
                                fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                fightProp.FIGHT_PROP_BLOOM_ADD_HURT,
                                fightProp.FIGHT_PROP_GRASS_RES_MINUS,
                            )
                            setattr(targetExpected, "bloomDamage", bloomDamages)
                        case "만개":
                            hyperBloomDamages = getHyperBloomDamage(
                                characterInfo.level,
                                fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                fightProp.FIGHT_PROP_HYPERBLOOM_ADD_HURT,
                                fightProp.FIGHT_PROP_GRASS_RES_MINUS,
                            )
                            setattr(targetExpected, "hyperBloomDamage", hyperBloomDamages)
                        case "발화":
                            burgeonDamages = getBurgeonDamage(
                                characterInfo.level,
                                fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                fightProp.FIGHT_PROP_BURGEON_ADD_HURT,
                                fightProp.FIGHT_PROP_FIRE_RES_MINUS,
                            )
                            setattr(targetExpected, "burgeonDamage", burgeonDamages)
                        case "연소":
                            burningDamages = getBurningDamage(
                                characterInfo.level,
                                fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                fightProp.FIGHT_PROP_BURNING_ADD_HURT,
                                fightProp.FIGHT_PROP_FIRE_RES_MINUS,
                            )
                            setattr(targetExpected, "burningDamage", burningDamages)
                        case "확산":
                            swirlDamages = getSwirlDamage(
                                characterInfo.level,
                                fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                                fightProp.FIGHT_PROP_SWIRL_ADD_HURT,
                                fightProp.FIGHT_PROP_FIRE_RES_MINUS,
                                fightProp.FIGHT_PROP_WATER_RES_MINUS,
                            )
                            setattr(targetExpected, "fireSwirlDamage", swirlDamages.fire)
                            setattr(targetExpected, "waterSwirlDamage", swirlDamages.water)
                            setattr(targetExpected, "iceSwirlDamage", swirlDamages.ice)
                            setattr(targetExpected, "elecSwirlDamage", swirlDamages.elec)
                        # 반응 달반응 연산(달감전, 달결정)
                        # case "달감전":
                        #     lunarChargedDamages = getLunarChargedDamage(
                        #         attackPoint=damage,
                        #         elementMastery=fightProp.FIGHT_PROP_ELEMENT_MASTERY,
                        #         elecResMinus=fightProp.FIGHT_PROP_ELEC_RES_MINUS,
                        #         lunarAddHurt=fightProp.FIGHT_PROP_LUNAR_ADD_HURT,
                        #         lunarBaseAddHurt=fightProp.FIGHT_PROP_LUNAR_BASE_ADD_HURT,
                        #         lunarPromotion=fightProp.FIGHT_PROP_LUNAR_PROMOTION,
                        #     )
                        #     setattr(target, "lunarChargedDamage", lunarChargedDamages)
                        case "달결정":
                            lunarCriticalDamage, lunarAdditionalCriticalDamage, lunarExtraCriticalDamage = getLunarDamage(
                                attackTypeKey="lunarCrystallize",
                                fightProp=fightProp,
                                critical=critical,
                                criticalHurt=criticalHurt,
                                finalAttackPoint=levelCoefficientMap[characterInfo.level],
                            )
                            setattr(targetExpected, "lunarCrystallizeDamage", lunarCriticalDamage.expectedDamage)
                            setattr(targetCritical, "lunarCrystallizeDamage", lunarCriticalDamage.criticalDamage)
                            setattr(targetNonCritical, "lunarCrystallizeDamage", lunarCriticalDamage.nonCriticalDamage)
                            if lunarAdditionalCriticalDamage:
                                setattr(targetExpected, "lunarCrystallizeDamageAdditional", lunarAdditionalCriticalDamage.expectedDamage)
                                setattr(targetCritical, "lunarCrystallizeDamageAdditional", lunarAdditionalCriticalDamage.criticalDamage)
                                setattr(targetNonCritical, "lunarCrystallizeDamageAdditional", lunarAdditionalCriticalDamage.nonCriticalDamage)
                            if lunarExtraCriticalDamage:
                                setattr(targetExpected, "lunarCrystallizeExtraDamage", lunarExtraCriticalDamage.expectedDamage)
                                setattr(targetCritical, "lunarCrystallizeExtraDamage", lunarExtraCriticalDamage.criticalDamage)
                                setattr(targetNonCritical, "lunarCrystallizeExtraDamage", lunarExtraCriticalDamage.nonCriticalDamage)

    return responseCalculationResult(damage=damageResult, characterInfo=responseCalculationResult.responseCharacterInfo(**characterInfo.model_dump(), totalStat=fightProp))

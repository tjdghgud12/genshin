from services.calculation.utils import getToleranceCoefficient, swirlDamageSchema
from data.globalVariable import levelCoefficientMap


# 증발
def getVaporizeDamage(attackPoint: float, elementMastery: float, vaporizeAddHurt: float, reverse: bool = False):
    masteryBonus = 2.78 * elementMastery / (elementMastery + 1400)
    return attackPoint * (2 if reverse else 1.5) * (1 + masteryBonus + vaporizeAddHurt)


# 융해
def getMeltDamage(attackPoint: float, elementMastery: float, meltAddHurt: float, reverse: bool = False):
    masteryBonus = 2.78 * elementMastery / (elementMastery + 1400)
    return attackPoint * (2 if reverse else 1.5) * (1 + masteryBonus + meltAddHurt)


# 감전
def getElectroChargedDamage(level: int, elementMastery: float, electroChargedAddHurt: float, elecResMinus: float):
    masteryBonus = 16 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=elecResMinus)

    return levelCoefficientMap[level] * 1.2 * (1 + masteryBonus + electroChargedAddHurt) * toleranceCoefficient


# 초전도
def getSuperconductDamage(level: int, elementMastery: float, superconductAddHurt: float, iceResMinus: float):
    masteryBonus = 16 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=iceResMinus)

    return levelCoefficientMap[level] * 0.5 * (1 + masteryBonus + superconductAddHurt) * toleranceCoefficient


# 과부하
def getOverloadedDamage(level: int, elementMastery: float, overloadedAddHurt: float, fireResMinus: float):
    masteryBonus = 16 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=fireResMinus)

    return levelCoefficientMap[level] * 2.0 * (1 + masteryBonus + overloadedAddHurt) * toleranceCoefficient


# 확산
def getSwirlDamage(level: int, elementMastery: float, swirlAddHurt: float, fireResMinus: float, waterResMinus: float, iceResMinus: float, elecResMinus: float) -> swirlDamageSchema:
    masteryBonus = 16 * elementMastery / (elementMastery + 2000)
    result = swirlDamageSchema()

    for swirl in ["fire", "water", "ice", "elec"]:
        toleranceCoefficient = getToleranceCoefficient(decrease=locals()[f"{swirl}ResMinus"])
        setattr(result, swirl, levelCoefficientMap[level] * 0.5 * (1 + masteryBonus + swirlAddHurt) * toleranceCoefficient)

    return result


# 개화
def getBloomDamage(level: int, elementMastery: float, bloomAddHurt: float, grassResMinus: float):
    masteryBonus = 16 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=grassResMinus)

    return levelCoefficientMap[level] * 2.0 * (1 + masteryBonus + bloomAddHurt) * toleranceCoefficient


# 만개
def getHyperBloomDamage(level: int, elementMastery: float, hyperBloomAddHurt: float, grassResMinus: float):
    masteryBonus = 16 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=grassResMinus)

    return levelCoefficientMap[level] * 3.0 * (1 + masteryBonus + hyperBloomAddHurt) * toleranceCoefficient


# 연소
def getBurningDamage(level: int, elementMastery: float, burningAddHurt: float, fireResMinus: float):
    masteryBonus = 16 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=fireResMinus)

    return levelCoefficientMap[level] * 0.25 * (1 + masteryBonus + burningAddHurt) * toleranceCoefficient


# 발화
def getBurgeonDamage(level: int, elementMastery: float, burgeonAddHurt: float, fireResMinus: float):
    masteryBonus = 16 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=fireResMinus)

    return levelCoefficientMap[level] * 3.0 * (1 + masteryBonus + burgeonAddHurt) * toleranceCoefficient


# 촉진
def getAggravateDamage(level: int, elementMastery: float, aggravateAddHurt: float, totalAddHurt: float):
    masteryBonus = 5 * elementMastery / (elementMastery + 1200)
    return levelCoefficientMap[level] * 1.15 * (1 + masteryBonus + aggravateAddHurt) * totalAddHurt


# 발산
def getSpreadDamage(level: int, elementMastery: float, spreadAddHurt: float, totalAddHurt: float):
    masteryBonus = 5 * elementMastery / (elementMastery + 1200)
    return levelCoefficientMap[level] * 1.25 * (1 + masteryBonus + spreadAddHurt) * totalAddHurt


# 쇄빙
def getShatterDamage(level: int, elementMastery: float, shatterAddHurt: float, physicalResMinus: float):
    masteryBonus = 16 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=physicalResMinus)

    return levelCoefficientMap[level] * 1.5 * (1 + masteryBonus + shatterAddHurt) * toleranceCoefficient


# 달개화
def getLunarBloomDamage(attackPoint: float, elementMastery: float, resMinus: float, lunarAddHurt: float, lunarBaseAddHurt: float, lunarPromotion: float, reaction: bool = False):
    # ((계수 * (원마보너스 + 달피증) * 달 개화 기본 피증) + 달 개화 계수 추가(라우마 버프)) * 승격 * 치명 * 내성
    masteryBonus = 6 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=resMinus)

    return (attackPoint * (1 + masteryBonus + lunarAddHurt) * (1 + lunarBaseAddHurt)) * toleranceCoefficient * lunarPromotion


# 달감전
def getLunarChargedDamage(attackPoint: float, elementMastery: float, resMinus: float, lunarAddHurt: float, lunarBaseAddHurt: float, lunarPromotion: float, reaction: bool = False):
    # ((계수 * (원마보너스 + 달피증) * 달 감전 기본 피증)) * 승격 * 치명 * 내성
    # reaction은 1.8 / directs는 3
    masteryBonus = 6 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=resMinus)

    return (1.8 if reaction else 3) * (attackPoint * (1 + masteryBonus + lunarAddHurt) * (1 + lunarBaseAddHurt)) * toleranceCoefficient * lunarPromotion


# 달결정
def getLunarCrystallizeDamage(
    attackPoint: float, elementMastery: float, resMinus: float, lunarAddHurt: float, lunarBaseAddHurt: float, lunarPromotion: float, reaction: bool = False
):
    # ((계수 * (원마보너스 + 달피증) * 달 결정 기본 피증) + 달 결정 계수 추가(일루가 버프)) * 승격 * 치명 * 내성
    # reaction은 0.96 / directs는 1.6
    masteryBonus = 6 * elementMastery / (elementMastery + 2000)
    toleranceCoefficient = getToleranceCoefficient(decrease=resMinus)

    return (0.96 if reaction else 1.6) * (attackPoint * (1 + masteryBonus + lunarAddHurt) * (1 + lunarBaseAddHurt)) * toleranceCoefficient * lunarPromotion

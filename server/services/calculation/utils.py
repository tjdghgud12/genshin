from schemas.calculation import responseFightPropSchema
from typing import Literal
from pydantic import BaseModel
from enum import Enum


class swirlDamageSchema(BaseModel):
    fire: float
    water: float
    ice: float
    elec: float


class baseFightPropKeyMap(str, Enum):
    HP = "FIGHT_PROP_HP_FINAL"
    ATTACK = "FIGHT_PROP_ATTACK_FINAL"
    DEFENSE = "FIGHT_PROP_DEFENSE_FINAL"
    ELEMENT_MASTERY = "FIGHT_PROP_ELEMENT_MASTERY"


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

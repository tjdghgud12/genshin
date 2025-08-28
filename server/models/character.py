from __future__ import annotations
from typing import TypedDict
from enum import Enum
from pydantic import BaseModel


class skillConstellationType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"
    none = None


class damageBaseFightPropModel(BaseModel):
    HP: float | None = None
    ATTACK: float | None = None
    DEFENSE: float | None = None
    ELEMENTAL_MASTARY: float | None = None


class skillBaseFightPropModel(BaseModel):

    class customDict(TypedDict):
        name: str
        fightProp: damageBaseFightPropModel

    nomal: damageBaseFightPropModel | None = None
    charge: damageBaseFightPropModel | None = None
    falling: damageBaseFightPropModel | None = None
    elementalSkill: damageBaseFightPropModel | None = None
    elementalBurst: damageBaseFightPropModel | None = None
    customs: list[customDict] | None = None


class skillConstellationOptionModel(BaseModel):
    type: skillConstellationType = skillConstellationType.always
    maxStack: int = 0
    label: str = ""


class passiveSkillModel(BaseModel):
    unlockLevel: int
    description: str
    options: list[skillConstellationOptionModel]


class activeSkillModel(BaseModel):
    description: str = ""
    baseFightProp: skillBaseFightPropModel = skillBaseFightPropModel()
    options: list[skillConstellationOptionModel] = []


class contellationModel(BaseModel):
    name: str
    description: str
    options: list[skillConstellationOptionModel]

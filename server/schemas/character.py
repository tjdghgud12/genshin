from __future__ import annotations
from typing import TypedDict
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class skillConstellationType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"
    none = None


class damageBaseFightPropSchema(BaseModel):
    HP: float | None = None
    ATTACK: float | None = None
    DEFENSE: float | None = None
    ELEMENTAL_MASTARY: float | None = None


class skillBaseFightPropSchema(BaseModel):

    class customDict(TypedDict):
        name: str
        type: Literal["nomal", "charge", "falling", "elementalSkill", "elementalBurst"] | None
        fightProp: damageBaseFightPropSchema

    nomal: damageBaseFightPropSchema | None = None
    charge: damageBaseFightPropSchema | None = None
    falling: damageBaseFightPropSchema | None = None
    elementalSkill: damageBaseFightPropSchema | None = None
    elementalBurst: damageBaseFightPropSchema | None = None
    customs: list[customDict] | None = None


class skillConstellationOptionSchema(BaseModel):
    type: skillConstellationType = skillConstellationType.always
    maxStack: int = 0
    label: str = ""


class passiveSkillSchema(BaseModel):
    unlockLevel: int
    description: str
    options: list[skillConstellationOptionSchema]


class activeSkillSchema(BaseModel):
    description: str = ""
    baseFightProp: skillBaseFightPropSchema = skillBaseFightPropSchema()
    options: list[skillConstellationOptionSchema] = []


class contellationSchema(BaseModel):
    name: str
    description: str
    options: list[skillConstellationOptionSchema]

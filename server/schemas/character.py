from __future__ import annotations
from typing import TypedDict
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class skillConstellationType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"
    select = "select"
    none = None


class damageBaseFightPropSchema(BaseModel):
    element: list[Literal["fire", "water", "grass", "elec", "rock", "wind", "ice", "physical"]] | None = None
    HP: float | None = None
    ATTACK: float | None = None
    DEFENSE: float | None = None
    ELEMENT_MASTERY: float | None = None


class additionalAttackSchema(BaseModel):
    name: str
    type: Literal["nomal", "charge", "falling", "elementalSkill", "elementalBurst", "fire", "water", "grass", "elec", "rock", "wind", "ice"] | None
    baseFightProp: damageBaseFightPropSchema


class skillBaseFightPropSchema(BaseModel):
    nomal: damageBaseFightPropSchema | None = None
    charge: damageBaseFightPropSchema | None = None
    falling: damageBaseFightPropSchema | None = None
    elementalSkill: damageBaseFightPropSchema | None = None
    elementalBurst: damageBaseFightPropSchema | None = None


class skillConstellationOptionSchema(BaseModel):
    type: skillConstellationType = skillConstellationType.always
    selectList: list[str | None] = []
    maxStack: int = 0
    label: str = ""


class passiveSkillSchema(BaseModel):
    unlockLevel: int
    description: str
    additionalAttack: list[additionalAttackSchema] | None = None
    options: list[skillConstellationOptionSchema] = []


class activeSkillSchema(BaseModel):
    description: str = ""
    baseFightProp: skillBaseFightPropSchema = skillBaseFightPropSchema()
    additionalAttack: list[additionalAttackSchema] | None = None
    options: list[skillConstellationOptionSchema] = []


class contellationSchema(BaseModel):
    name: str
    description: str
    additionalAttack: list[additionalAttackSchema] | None = None
    options: list[skillConstellationOptionSchema] = []


class characterDataSchema(BaseModel):
    passiveSkill: dict[str, passiveSkillSchema]
    activeSkill: dict[str, activeSkillSchema]
    constellation: list[contellationSchema]

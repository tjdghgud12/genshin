from __future__ import annotations

from enum import Enum
from pydantic import BaseModel


class skillConstellationType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"
    none = None


class skillConstellationOptionModel(BaseModel):
    type: skillConstellationType
    maxStack: int
    label: str


class passiveSkillModel(BaseModel):
    unlockLevel: int
    description: str
    options: list[skillConstellationOptionModel]


class activeSkillModel(BaseModel):
    description: str
    options: list[skillConstellationOptionModel]


class contellationModel(BaseModel):
    name: str
    description: str
    options: list[skillConstellationOptionModel]

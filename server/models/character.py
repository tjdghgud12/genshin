from enum import Enum
from pydantic import BaseModel


class skillConstellationType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"
    none = None


class skillConstellationOptionType(BaseModel):
    type: skillConstellationType
    maxStack: int
    label: str


class passiveSkillType(BaseModel):
    unlockLevel: int
    description: str
    options: list[skillConstellationOptionType]


class activeSkillType(BaseModel):
    description: str
    options: list[skillConstellationOptionType]


class contellationType(BaseModel):
    name: str
    description: str
    options: list[skillConstellationOptionType]

from enum import Enum
from pydantic import BaseModel
from models.weapon import weaponDataModel
from models.artifact import artifactSetOptionModel


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


class characterInfoModel(BaseModel):
    level: int
    constellations: list[contellationModel]
    activeSkill: list[activeSkillModel]
    passiveSkill: list[passiveSkillModel]
    weapon: weaponDataModel
    artifact: artifactSetOptionModel

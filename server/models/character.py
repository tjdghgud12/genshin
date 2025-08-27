from enum import Enum
from pydantic import BaseModel
from models.weapon import weaponDataModel
from models.artifact import artifactDataModel


class skillConstellationType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"
    none = None


class StatusMixin(BaseModel):
    active: bool
    stack: int


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


class requestCharacterInfoModel(BaseModel):
    level: int
    constellations: list[contellationModel]
    activeSkill: list[activeSkillModel]
    passiveSkill: list[passiveSkillModel]
    weapon: weaponDataModel
    artifact: artifactDataModel

    model_config = {"extra": "ignore"}

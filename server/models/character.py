from __future__ import annotations
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
    class requestSkillConstellationOptionModel(skillConstellationOptionModel, StatusMixin):
        pass

    class requestPassiveSkillModel(passiveSkillModel):
        options: list[requestCharacterInfoModel.requestSkillConstellationOptionModel]

    class requestActiveSkillModel(activeSkillModel):
        level: int
        options: list[requestCharacterInfoModel.requestSkillConstellationOptionModel]

    class requestContellationModel(contellationModel):
        unlocked: bool
        options: list[requestCharacterInfoModel.requestSkillConstellationOptionModel]

    level: int
    passiveSkill: list[requestPassiveSkillModel]
    activeSkill: list[requestActiveSkillModel]
    constellations: list[requestContellationModel]
    weapon: weaponDataModel
    artifact: artifactDataModel

    model_config = {"extra": "ignore"}

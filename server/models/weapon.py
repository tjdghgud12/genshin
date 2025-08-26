from pydantic import BaseModel
from enum import Enum


class weaponOptionType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"


class weaponOptionModel(BaseModel):
    type: weaponOptionType = weaponOptionType.always
    maxStack: int = 1
    description: str = ""
    label: str = ""


class weaponDataModel(BaseModel):
    id: int
    name: str
    level: int
    refinement: int
    options: list[weaponOptionModel]

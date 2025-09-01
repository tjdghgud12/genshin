from pydantic import BaseModel
from enum import Enum


class weaponOptionType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"


class StatusMixin(BaseModel):
    active: bool
    stack: int


class weaponOptionSchema(BaseModel):
    type: weaponOptionType = weaponOptionType.always
    maxStack: int = 1
    description: str = ""
    label: str = ""


class weaponDataSchema(BaseModel):
    class extendedWeaponOptionSchema(weaponOptionSchema, StatusMixin):
        pass

    id: int
    name: str
    level: int
    refinement: int
    options: list[extendedWeaponOptionSchema]

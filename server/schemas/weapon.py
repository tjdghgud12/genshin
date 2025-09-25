from pydantic import BaseModel, model_validator
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

    @model_validator(mode="before")
    def convert_value_to_enum(cls, values):
        if isinstance(values, dict) and isinstance(values.get("type"), str):
            try:
                values["type"] = WeaponType(values["type"])
            except ValueError:
                raise ValueError(f"Invalid WeaponType value: {values['type']}")
        return values

    id: int
    type: WeaponType
    name: str
    level: int
    refinement: int
    options: list[extendedWeaponOptionSchema]

    model_config = {"extra": "ignore"}

from enum import Enum
from pydantic import BaseModel


class artifactSetOptionType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"


class artifactSetOptionModel(BaseModel):
    type: artifactSetOptionType = artifactSetOptionType.always
    maxStack: int = 1
    description: str = ""
    label: str = ""
    requiredParts: int = 0

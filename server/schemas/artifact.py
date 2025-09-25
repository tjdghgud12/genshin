from data.globalVariable import fightPropKeys, fightPropTypes
from enum import Enum
from pydantic import BaseModel, field_validator


class artifactSetOptionType(Enum):
    always = "always"
    toggle = "toggle"
    stack = "stack"


class StatusMixin(BaseModel):
    active: bool = False
    stack: int = 0


class artifactSetOptionSchema(BaseModel):
    type: artifactSetOptionType = artifactSetOptionType.always
    maxStack: int = 1
    description: str = ""
    label: str = ""
    requiredParts: int = 0


class artifactSetDataSchema(BaseModel):
    class extendedArtifactSetOptionSchema(artifactSetOptionSchema, StatusMixin):
        pass

    name: str
    numberOfParts: int
    options: list[extendedArtifactSetOptionSchema]


class artifactPartsDataSchema(BaseModel):
    setName: str
    type: str
    mainStat: dict[str, float]
    subStat: list[dict[str, float]]

    @field_validator("mainStat")
    @classmethod
    def validateMainStat(cls, v: dict[str, float]) -> dict[str, float]:
        if not v:
            raise ValueError("mainStat은 비어있을 수 없습니다")
        if len(v) != 1:
            raise ValueError("mainStat은 정확히 하나의 키-값 쌍만 가져야 합니다")

        key, value = next(iter(v.items()))

        if key not in fightPropKeys:
            raise ValueError(f"허용되지 않는 전투 속성: {key}. " f"CharacterFightPropSchema에 정의된 필드만 사용 가능합니다. ")

        # 값 타입 검증
        if not isinstance(value, (int, float)):
            raise ValueError(f"{key}의 값은 숫자({fightPropTypes[key]})여야 합니다. 받은 타입: {type(value)}")
        # 값 범위 검증 (선택사항)
        if value < 0:
            raise ValueError(f"{key}의 값은 음수일 수 없습니다: {value}")

        return v

    @field_validator("subStat")
    @classmethod
    def validate_sub_stats(cls, v: list[dict[str, float]]) -> list[dict[str, float]]:
        if not isinstance(v, list):
            raise ValueError("subStat은 리스트여야 합니다")

        for i, stat in enumerate(v):
            if not isinstance(stat, dict):
                raise ValueError(f"subStat[{i}]는 딕셔너리여야 합니다")
            if not stat:
                raise ValueError(f"subStat[{i}]는 비어있을 수 없습니다")
            for key, value in stat.items():
                # 키 검증 (동적)
                if key not in fightPropKeys:
                    raise ValueError(f"subStat[{i}]에 허용되지 않는 전투 속성: {key}. " f"CharacterFightPropSchema에 정의된 필드만 사용 가능합니다.")
                # 값 타입 검증
                if not isinstance(value, (int, float)):
                    raise ValueError(f"subStat[{i}][{key}]의 값은 숫자({{fightPropTypes[key]}})여야 합니다. 받은 타입: {type(value)}")
                # 값 범위 검증
                if value < 0:
                    raise ValueError(f"subStat[{i}][{key}]의 값은 음수일 수 없습니다: {value}")

        return v


class artifactDataSchema(BaseModel):
    parts: list[artifactPartsDataSchema]
    setInfo: list[artifactSetDataSchema]

    model_config = {"extra": "ignore"}

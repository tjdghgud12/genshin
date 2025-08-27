from __future__ import annotations
from models.artifact import artifactDataModel
from models.character import skillConstellationOptionModel, passiveSkillModel, activeSkillModel, contellationModel
from models.fightProp import fightPropModel
from models.weapon import weaponDataModel
from pydantic import BaseModel


class StatusMixin(BaseModel):
    active: bool
    stack: int


class requestCharacterInfoModel(BaseModel):
    class requestSkillConstellationOptionModel(skillConstellationOptionModel, StatusMixin):
        pass

    class requestPassiveSkillModel(passiveSkillModel):
        name: str
        unlocked: bool
        options: list[requestCharacterInfoModel.requestSkillConstellationOptionModel]

    class requestActiveSkillModel(activeSkillModel):
        name: str
        level: int
        options: list[requestCharacterInfoModel.requestSkillConstellationOptionModel]

    class requestContellationModel(contellationModel):
        name: str
        unlocked: bool
        options: list[requestCharacterInfoModel.requestSkillConstellationOptionModel]

    name: str
    id: int
    level: int
    passiveSkill: list[requestPassiveSkillModel]
    activeSkill: list[requestActiveSkillModel]
    constellations: list[requestContellationModel]
    weapon: weaponDataModel
    artifact: artifactDataModel

    model_config = {"extra": "ignore"}


class responseFightPropModel(fightPropModel):
    FIGHT_PROP_HP_FINAL: float = 0.0
    FIGHT_PROP_ATTACK_FINAL: float = 0.0
    FIGHT_PROP_DEFENSE_FINAL: float = 0.0


class responseDamageResult(BaseModel):
    # 기본
    physicalDamage: float = 0.0
    elementalDamage: float = 0.0

    # 증폭
    meltDamage: float | None = 0.0  # 융해
    reverseMeltDamage: float | None = 0.0  # 역융해
    evaporationDamage: float | None = 0.0  # 증발
    reverseEvaporationDamage: float | None = 0.0  # 증발

    # 격화
    aggravateDamage: float | None = 0.0  # 촉진
    spreadDamage: float | None = 0.0  # 발산

    # 격변
    overloadedDamage: float | None = 0.0  # 과부하
    electricShockDamage: float | None = 0.0  # 감전
    moonElectricShockDamage: float | None = 0.0  # 달감전
    superconductDamage: float | None = 0.0  # 초전도
    shatterDamage: float | None = 0.0  # 쇄빙
    bloomDamage: float | None = 0.0  # 개화
    hyperBloomDamage: float | None = 0.0  # 만개
    ignitionDamage: float | None = 0.0  # 발화
    combusionDamage: float | None = 0.0  # 연소

    swirlDamage: float | None = 0.0  # 확산

    def add(self, field_name: str, value: float):
        if not hasattr(self, field_name):
            raise KeyError(f"{field_name} is not a valid field")
        setattr(self, field_name, getattr(self, field_name) + value)

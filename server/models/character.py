from enum import Enum
from pydantic import BaseModel
from models.weapon import weaponOptionModel
from models.artifact import artifactSetOptionModel


class CharacterFightPropModel(BaseModel):
    # 공통
    FIGHT_PROP_BASE_HP: float = 0.0
    FIGHT_PROP_HP: float = 0.0
    FIGHT_PROP_HP_PERCENT: float = 0.0
    FIGHT_PROP_BASE_ATTACK: float = 0.0
    FIGHT_PROP_ATTACK: float = 0.0
    FIGHT_PROP_ATTACK_PERCENT: float = 0.0
    FIGHT_PROP_BASE_DEFENSE: float = 0.0
    FIGHT_PROP_DEFENSE: float = 0.0
    FIGHT_PROP_DEFENSE_PERCENT: float = 0.0
    FIGHT_PROP_ELEMENT_MASTERY: float = 0.0
    FIGHT_PROP_CHARGE_EFFICIENCY: float = 1.0
    FIGHT_PROP_CRITICAL: float = 0.05
    FIGHT_PROP_CRITICAL_HURT: float = 0.5
    FIGHT_PROP_PHYSICAL_ADD_HURT: float = 0.0
    FIGHT_PROP_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_PHYSICAL_RES_MINUS: float = 0.0
    FIGHT_PROP_FIRE_RES_MINUS: float = 0.0
    FIGHT_PROP_WATER_RES_MINUS: float = 0.0
    FIGHT_PROP_ICE_RES_MINUS: float = 0.0
    FIGHT_PROP_ELEC_RES_MINUS: float = 0.0
    FIGHT_PROP_GRASS_RES_MINUS: float = 0.0
    FIGHT_PROP_WIND_RES_MINUS: float = 0.0
    FIGHT_PROP_ROCK_RES_MINUS: float = 0.0
    FIGHT_PROP_DEFENSE_MINUS: float = 0.0
    FIGHT_PROP_DEFENSE_IGNORE: float = 0.0
    FIGHT_PROP_HEAL_ADD: float = 0.0

    # 일반공격 관련
    FIGHT_PROP_NOMAL_ATTACK_CRITICAL: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_ATTACK_ADD_HURT: float = 0.0

    # 강공격 관련
    FIGHT_PROP_CHARGED_ATTACK_CRITICAL: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_ATTACK_ADD_HURT: float = 0.0

    # 낙하공격 관련
    FIGHT_PROP_FALLING_ATTACK_CRITICAL: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_ATTACK_ADD_HURT: float = 0.0

    # 원소 전투 스킬 관련
    FIGHT_PROP_ELEMENT_SKILL_CRITICAL: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_ATTACK_ADD_HURT: float = 0.0

    # 원소 폭발 관련
    FIGHT_PROP_ELEMENT_BURST_CRITICAL: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_ATTACK_ADD_HURT: float = 0.0

    # 원소 반응 관련
    FIGHT_PROP_OVERLOADED_ADD_HURT: float = 0.0  # 과부하
    FIGHT_PROP_ELECTRICSHOCK_ADD_HURT: float = 0.0  # 감전
    FIGHT_PROP_SUPERCONDUCT_ADD_HURT: float = 0.0  # 초전도
    FIGHT_PROP_HYPERBLOOM_ADD_HURT: float = 0.0  # 만개
    FIGHT_PROP_AGGRAVATE_ADD_HURT: float = 0.0  # 촉진
    FIGHT_PROP_EVAPORATION_ADD_HURT: float = 0.0  # 증발
    FIGHT_PROP_MELT_ADD_HURT: float = 0.0  # 융해
    FIGHT_PROP_COMBUSTION_ADD_HURT: float = 0.0  # 연소
    FIGHT_PROP_IGNITION_ADD_HURT: float = 0.0  # 발화

    def add(self, field_name: str, value: float):
        if not hasattr(self, field_name):
            raise KeyError(f"{field_name} is not a valid field")
        setattr(self, field_name, getattr(self, field_name) + value)


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

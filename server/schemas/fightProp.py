from pydantic import BaseModel


class finalAddHurtSchema(BaseModel):
    FIGHT_PROP_LUNARCHARGED_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_ATTACK_ADD_HURT: float = 0.0

    def add(self, field_name: str, value: float):
        if not hasattr(self, field_name):
            raise KeyError(f"{field_name} is not a valid field")
        setattr(self, field_name, getattr(self, field_name) + value)


class fightPropSchema(BaseModel):
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
    FIGHT_PROP_CHARGE_EFFICIENCY: float = 0.0
    FIGHT_PROP_CRITICAL: float = 0.0
    FIGHT_PROP_CRITICAL_HURT: float = 0.0
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
    FIGHT_PROP_ELECTROCHARGED_ADD_HURT: float = 0.0  # 감전
    FIGHT_PROP_SUPERCONDUCT_ADD_HURT: float = 0.0  # 초전도
    FIGHT_PROP_SHATTER_ADD_HURT: float = 0.0  # 쇄빙
    FIGHT_PROP_BLOOM_ADD_HURT: float = 0.0  # 개화
    FIGHT_PROP_HYPERBLOOM_ADD_HURT: float = 0.0  # 만개
    FIGHT_PROP_AGGRAVATE_ADD_HURT: float = 0.0  # 촉진
    FIGHT_PROP_SPREAD_ADD_HURT: float = 0.0  # 발산
    FIGHT_PROP_VAPORIZE_ADD_HURT: float = 0.0  # 증발
    FIGHT_PROP_MELT_ADD_HURT: float = 0.0  # 융해
    FIGHT_PROP_BURNING_ADD_HURT: float = 0.0  # 연소
    FIGHT_PROP_BURGEON_ADD_HURT: float = 0.0  # 발화
    FIGHT_PROP_SWIRL_ADD_HURT: float = 0.0  # 확산
    FIGHT_PROP_LUNARCHARGED_ADD_HURT: float = 0.0  # 달감전

    # 추가적인 최종데미지 곱연산 항목이 들어가야해
    FIGHT_PROP_FINAL: finalAddHurtSchema = finalAddHurtSchema()

    def add(self, field_name: str, value: float):
        if not hasattr(self, field_name):
            raise KeyError(f"{field_name} is not a valid field")
        setattr(self, field_name, getattr(self, field_name) + value)

    @classmethod
    def extractFightPropKeys(cls) -> frozenset[str]:
        try:
            return frozenset(cls.model_fields.keys())
        except AttributeError:
            return frozenset(cls.__dict__.keys())

    @classmethod
    def extractFightPropTypes(cls) -> dict[str, type | None]:
        return {name: getattr(field, "annotation", None) for name, field in cls.model_fields.items()}

    model_config = {"extra": "ignore"}

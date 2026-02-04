from pydantic import BaseModel


class additionalAttackFightPropSchema(BaseModel):
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
    FIGHT_PROP_ATTACK_ADD_POINT: float = 0.0

    FIGHT_PROP_LUNAR_ADD_HURT: float = 0.0  # 달빛 반응 피해

    FIGHT_PROP_LUNARCHARGED_CRITICAL: float = 0.0
    FIGHT_PROP_LUNARCHARGED_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_LUNARCHARGED_ADD_HURT: float = 0.0  # 달감전
    FIGHT_PROP_LUNARCHARGED_BASE_ADD_HURT: float = 0.0  # 달감전 기본 피증
    FIGHT_PROP_LUNARCHARGED_ADD_POINT: float = 0.0  # 달감전 계수 추가

    FIGHT_PROP_LUNARBLOOM_CRITICAL: float = 0.0
    FIGHT_PROP_LUNARBLOOM_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_LUNARBLOOM_ADD_HURT: float = 0.0  # 달개화
    FIGHT_PROP_LUNARBLOOM_BASE_ADD_HURT: float = 0.0  # 달개화 기본 피증
    FIGHT_PROP_LUNARBLOOM_ADD_POINT: float = 0.0  # 달개화 계수 추가

    # 최종데미지 곱연산
    FIGHT_PROP_FINAL_LUNARCHARGED_ADD_HURT: float = 0.0
    FIGHT_PROP_FINAL_NOMAL_ATTACK_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_FINAL_CHARGED_ATTACK_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_FINAL_ELEMENT_BURST_ATTACK_ADD_HURT: float = 0.0

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
    FIGHT_PROP_ATTACK_ADD_POINT: float = 0.0  # 계수 추가
    FIGHT_PROP_ELEC_ADD_POINT: float = 0.0  # 계수 추가
    FIGHT_PROP_ICE_CRITICAL_HURT: float = 0.0  # 얼음 원소 전용 치명타 피해 증가
    FIGHT_PROP_ICE_ADD_POINT: float = 0.0  # 얼음 원소 전용 계수 추가
    FIGHT_PROP_WATER_CRITICAL_HURT: float = 0.0  # 물 원소 전용 치명타 피해 증가
    FIGHT_PROP_ELEC_CRITICAL_HURT: float = 0.0  # 번개 원소 전용 치명타 피해 증가
    FIGHT_PROP_GRASS_CRITICAL_HURT: float = 0.0  # 풀 원소 전용 치명타 피해 증가
    FIGHT_PROP_ROCK_CRITICAL_HURT: float = 0.0  # 바위 원소 전용 치명타 피해 증가

    # 일반공격 관련
    FIGHT_PROP_NOMAL_ATTACK_CRITICAL: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_PHYSICAL_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_NOMAL_ATTACK_ATTACK_ADD_POINT: float = 0.0  # 계수 추가
    FIGHT_PROP_NOMAL_ATTACK_ELEC_ADD_POINT: float = 0.0  # 계수 추가

    # 강공격 관련
    FIGHT_PROP_CHARGED_ATTACK_CRITICAL: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_PHYSICAL_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_CHARGED_ATTACK_ATTACK_ADD_POINT: float = 0.0  # 계수 추가
    FIGHT_PROP_CHARGED_ATTACK_ELEC_ADD_POINT: float = 0.0  # 계수 추가

    # 낙하공격 관련
    FIGHT_PROP_FALLING_ATTACK_CRITICAL: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_PHYSICAL_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_FALLING_ATTACK_ATTACK_ADD_POINT: float = 0.0  # 계수 추가
    FIGHT_PROP_FALLING_ATTACK_ELEC_ADD_POINT: float = 0.0  # 계수 추가

    # 원소 전투 스킬 관련
    FIGHT_PROP_ELEMENT_SKILL_CRITICAL: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_PHYSICAL_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_SKILL_ATTACK_ADD_POINT: float = 0.0  # 계수 추가
    FIGHT_PROP_ELEMENT_SKILL_ELEC_ADD_POINT: float = 0.0  # 계수 추가
    FIGHT_PROP_ELEMENT_SKILL_DEFENSE_IGNORE: float = 0.0

    # 원소 폭발 관련
    FIGHT_PROP_ELEMENT_BURST_CRITICAL: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_PHYSICAL_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_FIRE_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_ELEC_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_WATER_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_GRASS_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_WIND_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_ROCK_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_ICE_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_ELEMENT_BURST_ATTACK_ADD_POINT: float = 0.0  # 계수 추가
    FIGHT_PROP_ELEMENT_BURST_ELEC_ADD_POINT: float = 0.0  # 계수 추가

    # 추가 공격 전용 fight prop
    FIGHT_PROP_ADDITIONAL_ATTACK: dict[str, additionalAttackFightPropSchema] = {}

    # 원소 반응 관련
    FIGHT_PROP_OVERLOADED_ADD_HURT: float = 0.0  # 과부하
    FIGHT_PROP_ELECTROCHARGED_ADD_HURT: float = 0.0  # 감전
    FIGHT_PROP_SUPERCONDUCT_ADD_HURT: float = 0.0  # 초전도
    FIGHT_PROP_SHATTER_ADD_HURT: float = 0.0  # 쇄빙
    FIGHT_PROP_AGGRAVATE_ADD_HURT: float = 0.0  # 촉진
    FIGHT_PROP_SPREAD_ADD_HURT: float = 0.0  # 발산
    FIGHT_PROP_VAPORIZE_ADD_HURT: float = 0.0  # 증발
    FIGHT_PROP_MELT_ADD_HURT: float = 0.0  # 융해
    FIGHT_PROP_SWIRL_ADD_HURT: float = 0.0  # 확산

    # 개별 치명타 옵션 보유 반응
    FIGHT_PROP_HYPERBLOOM_CRITICAL: float = 0.0
    FIGHT_PROP_HYPERBLOOM_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_HYPERBLOOM_ADD_HURT: float = 0.0  # 만개
    FIGHT_PROP_HYPERBLOOM_ADD_POINT: float = 0.0  # 만개 계수 추가

    FIGHT_PROP_BLOOM_CRITICAL: float = 0.0
    FIGHT_PROP_BLOOM_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_BLOOM_ADD_HURT: float = 0.0  # 개화
    FIGHT_PROP_BLOOM_ADD_POINT: float = 0.0  # 개화 계수 추가

    FIGHT_PROP_BURNING_CRITICAL: float = 0.0
    FIGHT_PROP_BURNING_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_BURNING_ADD_HURT: float = 0.0  # 연소

    FIGHT_PROP_BURGEON_CRITICAL: float = 0.0
    FIGHT_PROP_BURGEON_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_BURGEON_ADD_HURT: float = 0.0  # 발화
    FIGHT_PROP_BURGEON_ADD_POINT: float = 0.0  # 발화 계수 추가

    # 달 반응 관련
    FIGHT_PROP_LUNAR_ADD_HURT: float = 0.0  # 달빛 반응 피해
    FIGHT_PROP_LUNAR_BASE_ADD_HURT: float = 0.0  # 달빛 반응 기본 피증
    FIGHT_PROP_LUNAR_PROMOTION: float = 0.0  # 달빛 반응 승격
    FIGHT_PROP_LUNAR_CRITICAL_HURT: float = 0.0  # 달빛 반응 치명타 피해 증가

    FIGHT_PROP_LUNARCHARGED_CRITICAL: float = 0.0
    FIGHT_PROP_LUNARCHARGED_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_LUNARCHARGED_ADD_HURT: float = 0.0  # 달감전
    FIGHT_PROP_LUNARCHARGED_BASE_ADD_HURT: float = 0.0  # 달감전 기본 피증
    FIGHT_PROP_LUNARCHARGED_ADD_POINT: float = 0.0  # 달감전 계수 추가
    FIGHT_PROP_LUNARCHARGED_PROMOTION: float = 0.0  # 달감전 승격

    FIGHT_PROP_LUNARBLOOM_CRITICAL: float = 0.0
    FIGHT_PROP_LUNARBLOOM_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_LUNARBLOOM_ADD_HURT: float = 0.0  # 달개화
    FIGHT_PROP_LUNARBLOOM_BASE_ADD_HURT: float = 0.0  # 달개화 기본 피증
    FIGHT_PROP_LUNARBLOOM_ADD_POINT: float = 0.0  # 달개화 계수 추가
    FIGHT_PROP_LUNARBLOOM_PROMOTION: float = 0.0  # 달개화 승격
    FIGHT_PROP_LUNARBLOOM_EXTRA_DAMAGE: float = 0.0  # 달개화 extra 데미지(라우마 Q)

    FIGHT_PROP_LUNARCRYSTALLIZE_CRITICAL: float = 0.0
    FIGHT_PROP_LUNARCRYSTALLIZE_CRITICAL_HURT: float = 0.0
    FIGHT_PROP_LUNARCRYSTALLIZE_ADD_HURT: float = 0.0  # 달결정
    FIGHT_PROP_LUNARCRYSTALLIZE_BASE_ADD_HURT: float = 0.0  # 달결정 기본 피증
    FIGHT_PROP_LUNARCRYSTALLIZE_ADD_POINT: float = 0.0  # 달결정 계수 추가
    FIGHT_PROP_LUNARCRYSTALLIZE_PROMOTION: float = 0.0  # 달결정 승격
    FIGHT_PROP_LUNARCRYSTALLIZE_EXTRA_DAMAGE: float = 0.0  # 달결정 extra 데미지(일루가 Q)

    # 최종데미지 곱연산
    FIGHT_PROP_FINAL_LUNARCHARGED_ADD_HURT: float = 0.0
    FIGHT_PROP_FINAL_NOMAL_ATTACK_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_FINAL_CHARGED_ATTACK_ATTACK_ADD_HURT: float = 0.0
    FIGHT_PROP_FINAL_ELEMENT_BURST_ATTACK_ADD_HURT: float = 0.0

    def add(self, field_name: str, value: float, additionalAttackName: str = ""):
        if not hasattr(self, field_name):
            raise KeyError(f"{field_name} is not a valid field")
        if field_name == "FIGHT_PROP_ADDITIONAL_ATTACK":
            target = self.FIGHT_PROP_ADDITIONAL_ATTACK.get(additionalAttackName, None)
            if target:
                setattr(target, field_name, getattr(target, field_name) + value)
        else:
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

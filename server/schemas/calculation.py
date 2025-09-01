from __future__ import annotations
from schemas.artifact import artifactDataSchema
from schemas.character import skillConstellationOptionSchema, passiveSkillSchema, activeSkillSchema, contellationSchema
from schemas.fightProp import fightPropSchema
from schemas.weapon import weaponDataSchema
from pydantic import BaseModel


class StatusMixin(BaseModel):
    active: bool
    stack: int


class requestCharacterInfoSchema(BaseModel):
    class requestSkillConstellationOptionSchema(skillConstellationOptionSchema, StatusMixin):
        pass

    class requestPassiveSkillSchema(passiveSkillSchema):
        name: str
        unlocked: bool
        options: list[requestCharacterInfoSchema.requestSkillConstellationOptionSchema]

    class requestActiveSkillSchema(activeSkillSchema):
        name: str
        level: int
        options: list[requestCharacterInfoSchema.requestSkillConstellationOptionSchema] = []

    class requestContellationSchema(contellationSchema):
        name: str
        unlocked: bool
        options: list[requestCharacterInfoSchema.requestSkillConstellationOptionSchema]

    name: str
    id: int
    level: int
    passiveSkill: list[requestPassiveSkillSchema]
    activeSkill: list[requestActiveSkillSchema]
    constellations: list[requestContellationSchema]
    weapon: weaponDataSchema
    artifact: artifactDataSchema

    model_config = {"extra": "ignore"}


class responseFightPropSchema(fightPropSchema):
    FIGHT_PROP_HP_FINAL: float = 0.0
    FIGHT_PROP_ATTACK_FINAL: float = 0.0
    FIGHT_PROP_DEFENSE_FINAL: float = 0.0


class damageResultSchema(BaseModel):
    # 기본
    physicalDamage: float = 0.0
    elementalDamage: float = 0.0

    # 증폭
    meltDamage: float | None = 0.0  # 융해
    reverseMeltDamage: float | None = 0.0  # 역융해
    vaporizeDamage: float | None = 0.0  # 증발
    reversevaporizeDamage: float | None = 0.0  # 증발


class responseDamageResult(BaseModel):
    # 일반 공격
    nomal: damageResultSchema = damageResultSchema()
    nomalCritical: damageResultSchema = damageResultSchema()
    nomalNonCritical: damageResultSchema = damageResultSchema()
    # 강 공격
    charge: damageResultSchema = damageResultSchema()
    chargeCritical: damageResultSchema = damageResultSchema()
    chargeNonCritical: damageResultSchema = damageResultSchema()
    # 낙하 공격
    falling: damageResultSchema = damageResultSchema()
    fallingCritical: damageResultSchema = damageResultSchema()
    fallingNonCritical: damageResultSchema = damageResultSchema()
    # 원소 전투 스킬
    elementalSkill: damageResultSchema = damageResultSchema()
    elementalSkillCritical: damageResultSchema = damageResultSchema()
    elementalSkillNonCritical: damageResultSchema = damageResultSchema()
    # 원소 폭발
    elementalBurst: damageResultSchema = damageResultSchema()
    elementalBurstCritical: damageResultSchema = damageResultSchema()
    elementalBurstNonCritical: damageResultSchema = damageResultSchema()
    # 커스텀
    custom: list[damageResultSchema] = []
    customCritical: list[damageResultSchema] = []
    customNonCritical: damageResultSchema = damageResultSchema()

    # 격화
    aggravateDamage: float | None = 0.0  # 촉진 기대값
    aggravateDamageCritical: float | None = 0.0  # 촉진 치명타
    aggravateDamageNonCritical: float | None = 0.0  # 촉진 논치명타
    spreadDamage: float | None = 0.0  # 발산 기대값
    spreadDamageCritical: float | None = 0.0  # 발산 치명타
    spreadDamageNonCritical: float | None = 0.0  # 발산 논치명타

    # 격변
    overloadedDamage: float | None = 0.0  # 과부하
    electroChargedDamage: float | None = 0.0  # 감전
    superconductDamage: float | None = 0.0  # 초전도
    shatterDamage: float | None = 0.0  # 쇄빙
    bloomDamage: float | None = 0.0  # 개화
    hyperBloomDamage: float | None = 0.0  # 만개
    burgeonDamage: float | None = 0.0  # 발화
    burningDamage: float | None = 0.0  # 연소

    moonElectroChargedDamage: float | None = 0.0  # 달감전 기대값
    moonElectroChargedDamageCritical: float | None = 0.0  # 달감전 치명타
    moonElectroChargedDamageNonCritical: float | None = 0.0  # 달감전 논치명타

    # 확산
    swirlDamage: float | None = 0.0

    def add(self, field_name: str, value: float):
        if not hasattr(self, field_name):
            raise KeyError(f"{field_name} is not a valid field")
        setattr(self, field_name, getattr(self, field_name) + value)

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
    meltDamage: float | None = None  # 융해
    reverseMeltDamage: float | None = None  # 역융해
    vaporizeDamage: float | None = None  # 증발
    reversevaporizeDamage: float | None = None  # 역증발

    # 격화
    aggravateDamage: float | None = None  # 촉진
    spreadDamage: float | None = None  # 발산


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
    customNonCritical: list[damageResultSchema] = []

    # 격변
    overloadedDamage: float | None = None  # 과부하
    electroChargedDamage: float | None = None  # 감전
    superconductDamage: float | None = None  # 초전도
    shatterDamage: float | None = None  # 쇄빙
    bloomDamage: float | None = None  # 개화
    hyperBloomDamage: float | None = None  # 만개
    burgeonDamage: float | None = None  # 발화
    burningDamage: float | None = None  # 연소

    # 달반응
    lunarChargedDamage: float | None = None  # 달감전 기대값
    lunarChargedDamageCritical: float | None = None  # 달감전 치명타
    lunarChargedDamageNonCritical: float | None = None  # 달감전 논치명타

    # 확산
    fireSwirlDamage: float | None = None
    waterSwirlDamage: float | None = None
    iceSwirlDamage: float | None = None
    elecSwirlDamage: float | None = None

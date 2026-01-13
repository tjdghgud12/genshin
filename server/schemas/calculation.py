from __future__ import annotations
from schemas.artifact import artifactDataSchema
from schemas.character import skillConstellationOptionSchema, passiveSkillSchema, activeSkillSchema, contellationSchema
from schemas.fightProp import fightPropSchema
from schemas.weapon import weaponDataSchema
from pydantic import BaseModel
from enka.gi import Icon


class StatusMixin(BaseModel):
    active: bool
    stack: int
    select: str | None


class requestCharacterInfoSchema(BaseModel):
    class requestSkillConstellationOptionSchema(skillConstellationOptionSchema, StatusMixin):
        model_config = {"extra": "ignore"}
        pass

    class requestPassiveSkillSchema(passiveSkillSchema):
        name: str
        icon: Icon | str
        unlocked: bool
        options: list[requestCharacterInfoSchema.requestSkillConstellationOptionSchema] = []
        model_config = {"extra": "ignore"}

    class requestActiveSkillSchema(activeSkillSchema):
        name: str
        icon: Icon | str
        level: int
        options: list[requestCharacterInfoSchema.requestSkillConstellationOptionSchema] = []
        model_config = {"extra": "ignore"}

    class requestContellationSchema(contellationSchema):
        unlocked: bool
        icon: Icon | str
        options: list[requestCharacterInfoSchema.requestSkillConstellationOptionSchema] = []
        model_config = {"extra": "ignore"}

    name: str
    icon: Icon | str
    element: str
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
    physicalDamage: float | None = None
    elementalDamage: float | None = None

    # 증폭
    meltDamage: float | None = None  # 융해
    reverseMeltDamage: float | None = None  # 역융해
    vaporizeDamage: float | None = None  # 증발
    reverseVaporizeDamage: float | None = None  # 역증발

    # 격화
    aggravateDamage: float | None = None  # 촉진
    spreadDamage: float | None = None  # 발산

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
    lunarBloomDamage: float | None = None  # 달개화 기대값
    lunarBloomDamageAdditional: float | None = None  # 달개화 추가 계수 기대값

    # 확산
    fireSwirlDamage: float | None = None  # 불확산
    waterSwirlDamage: float | None = None  # 물확산
    iceSwirlDamage: float | None = None  # 얼음확산
    elecSwirlDamage: float | None = None  # 번개확산

    # 추가 계수
    physicalDamageAdditional: float | None = None  # 계수 추가 물리 데미지
    elementalDamageAdditional: float | None = None  # 계수 추가 원소 데미지
    meltDamageAdditional: float | None = None  # 계수 추가 융해
    reverseMeltDamageAdditional: float | None = None  # 계수 추가 역융해
    vaporizeDamageAdditional: float | None = None  # 계수 추가 증발
    reversevaporizeDamageAdditional: float | None = None  # 계수 추가 역증발


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
    # 추가 타격
    custom: dict[str, damageResultSchema] = {}
    customCritical: dict[str, damageResultSchema] = {}
    customNonCritical: dict[str, damageResultSchema] = {}


class responseCalculationResult(BaseModel):
    class responseCharacterInfo(requestCharacterInfoSchema):
        totalStat: responseFightPropSchema
        pass

    damage: responseDamageResult
    characterInfo: responseCharacterInfo

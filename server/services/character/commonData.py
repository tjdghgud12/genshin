from data import character as characterData
from services.artifact import getArtifactFightProp, getArtifactSetData
from services.weapon import getTotalWeaponFightProp
from schemas.artifact import artifactDataSchema
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema, additionalAttackFightPropSchema
from schemas.weapon import weaponDataSchema
from ambr import CharacterDetail, CharacterPromote
from itertools import chain
from typing import Protocol, Coroutine, Any
from pydantic import BaseModel


class CharacterFightPropReturnData(BaseModel):
    fightProp: fightPropSchema
    characterInfo: requestCharacterInfoSchema


class CharacterFightPropGetter(Protocol):
    def __call__(
        self, ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False
    ) -> Coroutine[Any, Any, CharacterFightPropReturnData]: ...


# ----------------------------------- Fucntion -----------------------------------
def genCharacterBaseStat(ambrCharacterDetail: CharacterDetail, level: int) -> fightPropSchema:
    fightProp = fightPropSchema(FIGHT_PROP_CRITICAL=0.05, FIGHT_PROP_CRITICAL_HURT=0.5, FIGHT_PROP_CHARGE_EFFICIENCY=1.0)

    curveInfo = characterData.ambrCharacterCurve[str(level)]["curveInfos"]
    promoteStat = max(
        (promote for promote in ambrCharacterDetail.upgrade.promotes if promote.unlock_max_level <= level),
        key=lambda x: x.unlock_max_level,
        default=CharacterPromote,
    )

    # itertools.chain으로 모든 스탯을 하나의 스트림으로 통합
    allStats = chain(
        ((s.prop_type, s.init_value * curveInfo[s.growth_type]) for s in ambrCharacterDetail.upgrade.base_stats), ((s.id, s.value) for s in (promoteStat.add_stats or []))
    )

    # 메모리 효율적인 적용
    for propType, value in allStats:
        fightProp.add(propType, value)

    return fightProp


def getConstellationData():
    constellationData = []
    return constellationData


async def getWeaponArtifactFightProp(fightProp: fightPropSchema, weapon: weaponDataSchema, artifact: artifactDataSchema, characterInfo: requestCharacterInfoSchema | None = None):
    # ----------------------- Artifact -----------------------
    artifactFightProp = getArtifactFightProp(artifact)
    artifactSetData = getArtifactSetData(artifact.setInfo, fightProp, weapon.type, characterInfo)
    artifactSetFightProp = artifactSetData["fightProp"]
    if artifactSetData["afterAddProps"] != None:
        for key in artifactSetData["afterAddProps"]:
            setattr(artifactSetFightProp, key, 0.0)

    # ----------------------- weapon -----------------------
    getWeaponFightProp = getTotalWeaponFightProp[weapon.name]
    weaponData = await getWeaponFightProp(weapon.id, weapon.level, weapon.refinement, weapon.options, fightProp)
    weaponFightProp = weaponData["fightProp"]
    if weaponData["afterAddProps"] != None:
        for key in weaponData["afterAddProps"]:
            setattr(weaponFightProp, key, 0.0)

    # ----------------------- 성유물 + 무기 데이터 합산 -----------------------
    for fightPropKey, value in artifactFightProp.model_dump().items():
        if fightPropKey == "FIGHT_PROP_ADDITIONAL_ATTACK":
            newAdditionalAttack: dict[str, additionalAttackFightPropSchema] = {}
            s = getattr(artifactSetFightProp, fightPropKey)
            w = getattr(weaponFightProp, fightPropKey)

            for name in {**s, **w, **value}:
                sTarget = s.get(name, additionalAttackFightPropSchema())
                wTarget = w.get(name, additionalAttackFightPropSchema())
                valueTarget = value.get(name, additionalAttackFightPropSchema())
                for key, v in sTarget.items():
                    valueTarget.add(key, v)
                    valueTarget.add(key, getattr(wTarget, v))
                    newAdditionalAttack[name] = valueTarget
            fightProp.FIGHT_PROP_ADDITIONAL_ATTACK = newAdditionalAttack

        else:
            fightProp.add(fightPropKey, value + getattr(artifactSetFightProp, fightPropKey) + getattr(weaponFightProp, fightPropKey))

    return {"fightProp": fightProp, "weaponAfterProps": weaponData["afterAddProps"], "artifactAfterProps": artifactSetData["afterAddProps"]}


async def getAfterWeaponArtifactFightProp(
    fightProp: fightPropSchema, weapon: weaponDataSchema, artifact: artifactDataSchema, weaponAfterProps: list | None, artifactAfterProps: list | None
):
    getWeaponFightProp = getTotalWeaponFightProp[weapon.name]

    if weaponAfterProps != None:
        finallyWeaponData = await getWeaponFightProp(weapon.id, weapon.level, weapon.refinement, weapon.options, fightProp)
        for key in finallyWeaponData["afterAddProps"]:
            fightProp.add(key, getattr(finallyWeaponData["fightProp"], key))

    if artifactAfterProps != None:
        finallyArtifactSetData = getArtifactSetData(artifact.setInfo, fightProp, weapon.type)
        for key in finallyArtifactSetData["afterAddProps"] or []:
            fightProp.add(key, getattr(finallyArtifactSetData["fightProp"], key))

    return fightProp

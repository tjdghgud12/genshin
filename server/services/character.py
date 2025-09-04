from data import character as characterData
from data.globalVariable import fightPropMpa
from services.artifact import getArtifactFightProp, getArtifactSetData
from services.weapon import getTotalWeaponFightProp
from schemas.artifact import artifactDataSchema
from schemas.calculation import requestCharacterInfoSchema
from schemas.fightProp import fightPropSchema
from schemas.weapon import weaponDataSchema
from ambr import CharacterDetail, CharacterPromote
from copy import deepcopy
from dataclasses import dataclass
from itertools import chain
from typing import Protocol, Coroutine, Any
from pydantic import BaseModel


# ----------------------------------- Class -----------------------------------
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


async def getWeaponArtifactFightProp(fightProp: fightPropSchema, weapon: weaponDataSchema, artifact: artifactDataSchema):
    # ----------------------- Artifact -----------------------
    artifactFightProp = getArtifactFightProp(artifact)
    artifactSetData = getArtifactSetData(artifact.setInfo, fightProp)
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
        finallyArtifactSetData = getArtifactSetData(artifact.setInfo, fightProp)
        for key in finallyArtifactSetData["afterAddProps"] or []:
            fightProp.add(key, getattr(finallyArtifactSetData["fightProp"], key))

    return fightProp


async def getGanyuFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    # ----------------------- Base Fight Prop -----------------------
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 획린(獲麟), 구름 여행, 잡초 근절, 살생의 발걸음의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "이슬 먹는 신수":
                    if constellation.options[0].active:  # pyright: ignore[reportIndexIssue]
                        newFightProp.add(fightPropMpa.ICE_RES_MINUS.value, 0.15)
                case "서수(西狩)":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, constellation.options[0].stack * 0.05)
                case "구름 여행":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "잡초 근절":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 감우의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "단 하나의 마음":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.CHARGED_ATTACK_CRITICAL.value, 0.2)
                case "천지교태":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.ICE_ADD_HURT.value, 0.2)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getKamisatoAyakaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # # 서리에 검게 물든 벚꽃, 삼중 서리 관문, 흩날리는 카미후부키, 화운종월경의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "삼중 서리 관문":  # 최종 데미지 기준 추가 피해
                    newFightProp.add(fightPropMpa.FINAL_ELEMENT_BURST_ATTACK_ADD_HURT.value, 1.4)
                case "영고성쇠":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.DEFENSE_MINUS.value, 0.3)
                case "물에 비친 달":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_HURT.value, 2.98)
                case "흩날리는 카미후부키":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "화운종월경":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 아야카의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "천죄국죄 진사":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_HURT.value, 0.3)
                        newFightProp.add(fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_HURT.value, 0.3)
                case "한천선명 축사":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.ICE_ADD_HURT.value, 0.18)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getKeqingFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # # 가연, 등루, 이등의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "계뢰":  # 원소 전투 스킬 추가 피해
                    description = "뇌설이 존재하는 동안 다시 원소 전투 스킬 발동 시 공격력의 50%의 번개 원소 피해 추가"
                case "조율":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.25)
                case "염정":
                    newFightProp.add(fightPropMpa.ELEC_ADD_HURT.value, constellation.options[0].stack * 0.06)
                case "등루":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "이등":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 각청의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "옥형의 품격":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.CRITICAL.value, 0.15)
                        newFightProp.add(fightPropMpa.CHARGE_EFFICIENCY.value, 0.15)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getNahidaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # # 지혜를 머금은 씨앗, 감화된 성취의 싹, 달변으로 맺은 열매, 깨달음을 주는 잎의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "올곧은 선견의 뿌리":
                    # 연소, 개화, 만개, 발화의 치명타 발생
                    # 활성, 촉진, 발산 반응 시 방어력 감소만 적용
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.DEFENSE_MINUS.value, 0.3)
                        newFightProp.add(fightPropMpa.BLOOM_CRITICAL.value, 0.2)
                        newFightProp.add(fightPropMpa.BLOOM_CRITICAL_HURT.value, 1.0)
                        newFightProp.add(fightPropMpa.HYPERBLOOM_CRITICAL.value, 0.2)
                        newFightProp.add(fightPropMpa.HYPERBLOOM_CRITICAL_HURT.value, 1.0)
                        newFightProp.add(fightPropMpa.BURGEON_CRITICAL.value, 0.2)
                        newFightProp.add(fightPropMpa.BURGEON_CRITICAL_HURT.value, 1.0)
                        newFightProp.add(fightPropMpa.BURNING_CRITICAL.value, 0.2)
                        newFightProp.add(fightPropMpa.BURNING_CRITICAL_HURT.value, 1.0)

                case "추론으로 드러난 줄기":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ELEMENT_MASTERY.value, constellation.options[0].stack * 20 + 80)
                case "감화된 성취의 싹":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "깨달음을 주는 잎":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    activeSkillLevelMap = {
        "마음이 그리는 환상": [
            (14.9, 22.3),
            (16.0, 24.0),
            (17.1, 25.7),
            (18.6, 27.9),
            (19.7, 29.6),
            (20.8, 31.2),
            (22.3, 33.5),
            (23.8, 35.7),
            (25.3, 37.9),
            (26.8, 40.2),
            (28.3, 42.4),
            (29.8, 44.6),
            (31.6, 47.4),
            (33.5, 50.2),
            (35.3, 53.0),
        ]
    }

    for active in characterInfo.activeSkill:
        match active.name:
            case "마음이 그리는 환상":  # 번개, 물의 경우 fightProp에 영향 X. 각 쿨감 및 지속시간 증가.
                option = active.options[0]  #  0번지가 불
                if option.active:
                    addElementalBurstLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "깨달음을 주는 잎"))
                    seedsOfWisdom = next((constellation for constellation in characterInfo.constellations if constellation.name == "지혜를 머금은 씨앗"))
                    addLevel = 3 if addElementalBurstLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    stack = min(option.stack + (1 if seedsOfWisdom.unlocked else 0), 2)
                    newFightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value, skillValue[stack - 1])

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "정선으로 포용한 명론":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.ELEMENT_MASTERY.value, min(getattr(newFightProp, fightPropMpa.ELEMENT_MASTERY.value) * 0.25, 250))
                case "지혜로 깨우친 지론":
                    if passive.options[0].active:
                        val = min(getattr(newFightProp, fightPropMpa.ELEMENT_MASTERY.value) - 200, 800)
                        if val > 0:
                            newFightProp.add(fightPropMpa.ELEMENT_SKILL_CRITICAL.value, val * 0.03)
                            newFightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value, val * 0.1)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getRaidenShogunFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 악요 명문(銘文), 진영의 과거, 진리의 맹세, 쇼군의 현형, 염원의 대행인의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "강철 절단":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.DEFENSE_IGNORE.value, 0.6)
                # case "진영의 과거":
                #     characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                # case "쇼군의 현형":
                #     characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    activeSkillLevelMap = {
        "초월·악요개안": [
            0.0022,  # Level 1
            0.0023,  # Level 2
            0.0024,  # Level 3
            0.0025,  # Level 4
            0.0026,  # Level 5
            0.0027,  # Level 6
            0.0028,  # Level 7
            0.0029,  # Level 8
            0.0030,  # Level 9
            0.0030,  # Level 10
            0.0030,  # Level 11
            0.0030,  # Level 12
            0.0030,  # Level 13
            0.0030,  # Level 14
            0.0030,  # Level 15
        ]
    }

    for active in characterInfo.activeSkill:
        match active.name:
            case "초월·악요개안":
                if active.options[0].active:
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "쇼군의 현형"))
                    addLevel = 3 if addElementalSkillLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    newFightProp.add(fightPropMpa.ELEMENT_BURST_ATTACK_ADD_HURT.value, 90 * skillValue)  # 90은 라이덴의 원소 에너지

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "비범한 옥체":
                    if passive.options[0].active:
                        val = getattr(newFightProp, fightPropMpa.CHARGE_EFFICIENCY.value) - 1
                        if val > 0:
                            newFightProp.add(fightPropMpa.ELEC_ADD_HURT.value, val * 0.4)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getHuTaoFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 진홍의 꽃다발, 비처럼 내리는 불안, 적색 피의 의식, 영원한 안식의 정원, 꽃잎 향초의 기도는 호두의 fightProp에 영향 X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "나비 잔향":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.CRITICAL.value, 1.00)
                case "적색 피의 의식":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "꽃잎 향초의 기도":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0

    # ----------------------- passive -----------------------
    # 모습을 감춘 나비는 호두의 fightProp에 영향X
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "핏빛 분장":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.FIRE_ADD_HURT.value, 0.33)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    # ----------------------- active -----------------------
    # 가장 마지막 최대HP기준으로 적용되어야 하기 때문에 해당 위치로 이동
    activeSkillLevelMap = {
        "나비의 서": [
            0.0384,  # Level 1
            0.0407,  # Level 2
            0.0430,  # Level 3
            0.0460,  # Level 4
            0.0483,  # Level 5
            0.0506,  # Level 6
            0.0536,  # Level 7
            0.0566,  # Level 8
            0.0596,  # Level 9
            0.0626,  # Level 10
            0.0656,  # Level 11
            0.0685,  # Level 12
            0.0715,  # Level 13
            0.0745,  # Level 14
            0.0775,  # Level 15
        ]
    }

    for active in characterInfo.activeSkill:
        match active.name:
            case "나비의 서":
                if active.options[0].active:
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "적색 피의 의식"))
                    addLevel = 3 if addElementalSkillLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    baseHp = getattr(newFightProp, fightPropMpa.BASE_HP.value)
                    hpPercent = getattr(newFightProp, fightPropMpa.HP_PERCENT.value)
                    hp = getattr(newFightProp, fightPropMpa.HP.value)
                    totalHp = baseHp * (hpPercent + 1) + hp
                    newFightProp.add(fightPropMpa.ATTACK.value, totalHp * skillValue)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getFurinaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalAttackPoints = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 6돌을 제외한 모든 돌파 옵션은 fightProp에 영향 없거나 active에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "「모두 사랑의 축배를 들렴!」":
                    if constellation.options[0].active:
                        # 평타 계수 추가이기 때문에 2025-08-05기준 미개발 상태
                        description = "원소 전투 스킬 발동 시 일반공격, 강공격, 낙하공격이 hp최대치의 18%만큼 증가하는 물 원소 피해로 변경. 프뉴마 상태일 때 일반공격, 강공격, 낙하공격의 추락충격으로 주는 피해가 hp최대치의 25%만큼 증가"
                        additionalAttackPoints.append({"key": fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_POINT.value, "value": ("HP", 0.43)})
                        additionalAttackPoints.append({"key": fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_POINT.value, "value": ("HP", 0.43)})
                        additionalAttackPoints.append({"key": fightPropMpa.FALLING_ATTACK_ATTACK_ADD_POINT.value, "value": ("HP", 0.43)})
                case "「내 이름은 그 누구도 모르리라」":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "「난 알았노라, 그대의 이름은…!」":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    activeSkillLevelMap = {
        "성대한 카니발": [
            [0.0007, 0.0001],  # Level 1
            [0.0009, 0.0002],  # Level 2
            [0.0011, 0.0003],  # Level 3
            [0.0013, 0.0004],  # Level 4
            [0.0015, 0.0005],  # Level 5
            [0.0017, 0.0006],  # Level 6
            [0.0019, 0.0007],  # Level 7
            [0.0021, 0.0008],  # Level 8
            [0.0023, 0.0009],  # Level 9
            [0.0025, 0.0010],  # Level 10
            [0.0027, 0.0011],  # Level 11
            [0.0029, 0.0012],  # Level 12
            [0.0031, 0.0013],  # Level 13
            [0.0033, 0.0014],  # Level 14
            [0.0035, 0.0015],  # Level 15
        ]
    }

    for active in characterInfo.activeSkill:
        match active.name:
            case "성대한 카니발":
                option = active.options[0]
                if option.active:
                    addElementalBurstLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "「내 이름은 그 누구도 모르리라」"))
                    firstConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "「사랑은 애걸해도 길들일 수 없는 새」"))
                    secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "「여자의 마음은 흔들리는 부평초」"))
                    addLevel = 3 if addElementalBurstLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]

                    if firstConstellation.unlocked:
                        option.stack = min(option.stack + 150, 400)
                    if secondConstellation.unlocked:
                        newFightProp.add(fightPropMpa.HP_PERCENT.value, 0.0035 * option.stack)

                    newFightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, skillValue[0] * option.stack)
                    # newFightProp[fightPropMpa.ATTACK_ADD_HURT.value] += skillValue[1] * active.stack # 치유 보너스

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    # ----------------------- passive -----------------------
    # 가장 마지막 최대HP기준으로 적용되어야 하기 때문에 해당 위치로 이동
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "고독한 독백":
                    if passive.options[0].active:
                        baseHp = getattr(newFightProp, fightPropMpa.BASE_HP.value)
                        hpPercent = getattr(newFightProp, fightPropMpa.HP_PERCENT.value)
                        hp = getattr(newFightProp, fightPropMpa.HP.value)
                        totalHp = baseHp * (hpPercent + 1) + hp
                        newFightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value, min(totalHp / 1000 * 0.007, 0.28))

    # 추가 계수 입력부
    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMpa, f"BASE_{pointKey}").value) * (
            1 + getattr(newFightProp, getattr(fightPropMpa, f"{pointKey}_PERCENT").value)
        ) + getattr(newFightProp, getattr(fightPropMpa, pointKey).value)
        newFightProp.add(key, finalPoint * value)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getSkirkFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 심연, 악연, 소망, 멸류는 fightProp에 영향 없거나 각 스킬 연산 시 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "요원":  # 스킬 계수 추가
                    description = "허계 균열 1개 흡수할 때 마다 스커크 공격력의 500%에 해당하는 얼음 원소 피해 추가"
                case "심연":  # 스킬 계수 추가
                    description = "원소 전투 스킬 발동 시 뱀의 계략 10pt 획득. 원소 폭발 사용 시 뱀의 계략 최대치 10pt 증가."
                case "근원":  # 스킬 계수 추가
                    description = "흡수한 허계 균열 수 당 극악기 · 참 스택 획득. 극악기 · 참 스택 마다 원소 폭발 발동 시 공격력의 750%에 해당하는 얼음 원소 피해 추가. 일곱빛 섬광 모드에서는 일반공격 또는 피격 시 협동 공격"
                case "악연":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "소망":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    activeSkillLevelMap = {
        "극악기·멸": [
            [0.035, 0.066, 0.088, 0.110],
            [0.040, 0.072, 0.096, 0.120],
            [0.045, 0.078, 0.104, 0.130],
            [0.050, 0.084, 0.112, 0.140],
            [0.055, 0.090, 0.120, 0.150],
            [0.060, 0.096, 0.128, 0.160],
            [0.065, 0.102, 0.136, 0.170],
            [0.070, 0.108, 0.144, 0.180],
            [0.075, 0.114, 0.152, 0.190],
            [0.080, 0.120, 0.160, 0.200],
            [0.085, 0.126, 0.168, 0.210],
            [0.090, 0.132, 0.176, 0.220],
            [0.095, 0.138, 0.184, 0.230],
            [0.100, 0.144, 0.192, 0.240],
            [0.105, 0.150, 0.200, 0.250],
        ]
    }
    for active in characterInfo.activeSkill:
        match active.name:
            case "극악기·멸":
                option = active.options[0]
                if option.active:
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.name == "악연"))
                    secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "심연"))
                    addLevel = 3 if addElementalSkillLevel.unlocked else 0
                    skillValue = activeSkillLevelMap[active.name][active.level + addLevel - 1]
                    if secondConstellation.unlocked:
                        newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.7)

                    newFightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, skillValue[option.stack])

    # ----------------------- passive -----------------------
    # 이치 너머의 이치는 원소전투스킬과 원소폭발의 계수 추가. 계수 추가는 미개발 상태
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "흐름의 적멸":
                    if passive.options[0].active:
                        normal = [0, 1.1, 1.2, 1.7]
                        burst = [0, 1.05, 1.15, 1.6]
                        newFightProp.add(fightPropMpa.FINAL_NOMAL_ATTACK_ATTACK_ADD_HURT.value, normal[passive.options[0].stack])
                        newFightProp.add(fightPropMpa.FINAL_ELEMENT_BURST_ATTACK_ADD_HURT.value, burst[passive.options[0].stack])

                        fourthConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "멸류"))
                        if fourthConstellation.unlocked:
                            addAttackPercent = [0, 0.1, 0.2, 0.4]
                            newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, addAttackPercent[passive.options[0].stack])

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getEscoffierFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalAttackPoints = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 로즈마리 비밀 레시피는 fightProp에 영향X
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "미각을 깨우는 식전 공연":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.CRITICAL_HURT.value, 0.6)
                case "예술의 경지에 이른 스튜":  # 스킬 계수 추가
                    description = "원소 전투 스킬 발동 시 피해를 에스코피에의 공격력의 240%만큼 증가시키는 즉석 요리 스텍 획득(신학 깃털 효과)"
                    additionalAttackPoints.append({"key": fightPropMpa.ATTACK_ADD_POINT.value, "value": ("ATTACK", 2.4)})
                case "무지갯빛 티타임":  # 스킬 계수 추가
                    description = "현재 필드 위에 있는 파티 내 자신의 캐릭터의 일반공격, 강공격, 낙하공격이 명중 시 에스코피에의 공격력의 500%에 해당하는 얼음 원소 추가 피해"
                case "캐러멜화의 마법":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "다채로운 소스의 교향곡":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 에스코피에의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    # 밥이 보약은 fightProp에 영향X
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "영감의 조미료":
                    option = passive.options[0]
                    if option.active:
                        addIceWarterResMinus = [0, 0.05, 0.1, 0.15, 0.55]
                        newFightProp.add(fightPropMpa.ICE_RES_MINUS.value, addIceWarterResMinus[option.stack])
                        newFightProp.add(fightPropMpa.WATER_RES_MINUS.value, addIceWarterResMinus[option.stack])

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMpa, f"BASE_{pointKey}").value) * (
            1 + getattr(newFightProp, getattr(fightPropMpa, f"{pointKey}_PERCENT").value)
        ) + getattr(newFightProp, getattr(fightPropMpa, pointKey).value)
        newFightProp.add(key, finalPoint * value)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getCitlaliFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalAttackPoints = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 구름뱀의 깃털 왕관, 불길한 닷새의 저주은 fightProp에 영향 없거나 스킬에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "사백 개의 별빛":  # 스킬 계수 추가
                    description = "파티 내 캐릭터가 공격 시 소모되는 별빛 검 스텍을 10개 획득. 별빛 검은 시틀라리의 원소 마스터리의 200%만큼 피해 증가"
                    additionalAttackPoints.append({"key": fightPropMpa.ATTACK_ADD_POINT.value, "value": ("ELEMENT_MASTERY", 2)})
                case "심장을 삼키는 자의 순행":
                    newFightProp.add(fightPropMpa.ELEMENT_MASTERY.value, 125)
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ELEMENT_MASTERY.value, 250)
                case "죽음을 거부하는 자의 영혼 해골":  # 추가 피해
                    if constellation.options[0].active:
                        description = "서리 운석 폭풍 명중 시 시틀라리의 원소 마스터리의 1800%만큼의 추가 피해."
                case "아홉 번째 하늘의 계약":
                    newFightProp.add(fightPropMpa.FIRE_ADD_HURT.value, 0.015 * constellation.options[0].stack)
                    newFightProp.add(fightPropMpa.WATER_ADD_HURT.value, 0.015 * constellation.options[0].stack)
                    newFightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, 0.025 * constellation.options[0].stack)
                case "구름뱀의 깃털 왕관":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0
                case "불길한 닷새의 저주":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
    # ----------------------- active -----------------------
    # active: 시틀라리의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "다섯 번째 하늘의 서리비":
                    if passive.options[0].active:
                        secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "심장을 삼키는 자의 순행"))
                        if secondConstellation.unlocked:
                            newFightProp.add(fightPropMpa.FIRE_RES_MINUS.value, 0.2)
                            newFightProp.add(fightPropMpa.WATER_RES_MINUS.value, 0.2)
                        newFightProp.add(fightPropMpa.FIRE_RES_MINUS.value, 0.2)
                        newFightProp.add(fightPropMpa.WATER_RES_MINUS.value, 0.2)
                case "하얀 불나비의 별옷":  # 스킬 계수 추가
                    # 원소전투 스킬 검은 서리별의 이즈파파가 일으킨 서리운석 폭풍이 주는 피해가 시틀라리 원소 마스터리의 90%만큼 증가
                    # 원소폭발 반짝이는 칙령의 얼음 폭풍이 주는 피해가 시틀라리 원소 마스터리의 1200%만큼 증가
                    additionalAttackPoints.append({"key": fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_POINT, "value": ("ELEMENT_MASTERY", 0.9)})
                    additionalAttackPoints.append({"key": fightPropMpa.ELEMENT_BURST_ATTACK_ADD_POINT, "value": ("ELEMENT_MASTERY", 12)})

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMpa, pointKey).value)
        newFightProp.add(key, finalPoint * value)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getNeuvilletteFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 위대한 제정, 법의 계율, 고대의 의제, 연민의 왕관, 정의의 판결 fightProp에 영향 없거나 스킬에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "분노의 보상":  # 스킬 계수 추가
                    description = "강공격 명중 시 hp최대치의 10% 물 원소 피해를 주는 격류 2개 소환"
                case "고대의 의제":
                    characterInfo.activeSkill[0].level -= 3 if enkaDataFlag else 0
                case "정의의 판결":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 느비예트의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "생존한 고대바다의 계승자":
                    option = passive.options[0]
                    if option.active:
                        finalCharged = [0, 0.10, 1.25, 1.60]  # 최종 데미지 곱연산(강공격)
                        newFightProp.add(fightPropMpa.FINAL_CHARGED_ATTACK_ATTACK_ADD_HURT.value, finalCharged[option.stack])

                        firstConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "위대한 제정"))
                        secondConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "법의 계율"))
                        if firstConstellation.unlocked:
                            option.stack = min(option.stack + 1, 3)
                        if secondConstellation.unlocked:
                            newFightProp.add(fightPropMpa.CHARGED_ATTACK_CRITICAL_HURT.value, 0.14 * option.stack)
                case "드높은 중재의 규율":
                    option = passive.options[0]
                    if option.active:
                        newFightProp.add(fightPropMpa.WATER_ADD_HURT.value, 0.6 * option.stack)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


async def getMavuikaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag: bool = False) -> CharacterFightPropReturnData:
    newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    additionalAttackPoints = []

    # -----------------------weapon & Artifact -----------------------
    weaponArtifactData = await getWeaponArtifactFightProp(deepcopy(newFightProp), characterInfo.weapon, characterInfo.artifact)
    newFightProp = weaponArtifactData["fightProp"]

    # ----------------------- constellations -----------------------
    # 타오르는 태양, 진정한 의미, 「지도자」의 각오는 fightProp에 영향 없거나 다른 곳에서 처리
    for constellation in characterInfo.constellations:
        if constellation.unlocked:
            match constellation.name:
                case "밤 주인의 계시":
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.4)
                case "잿더미의 대가":  # 스킬 계수 추가(일반공격, 강공격, 원소폭발의 석양 베기로 주는 피해가 마비카 공격력의 60%/90%/120%만큼 증가)
                    newFightProp.add(fightPropMpa.BASE_ATTACK.value, 200)
                    additionalAttackPoints.append({"key": fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_POINT.value, "value": ("ATTACK", 0.6)})
                    additionalAttackPoints.append({"key": fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_POINT.value, "value": ("ATTACK", 0.9)})
                    additionalAttackPoints.append({"key": fightPropMpa.ELEMENT_BURST_ATTACK_ADD_POINT.value, "value": ("ATTACK", 1.2)})
                case "「인간의 이름」 해방":  # 스킬 계수 추가
                    if constellation.options[0].active:
                        newFightProp.add(fightPropMpa.DEFENSE_MINUS.value, 0.2)
                    description = "불볕 고리: 공격 적중 시 공격력의 200%에 해당하는 밤혼 성질의 불 원소 피해 추가. 바이크 : 주변 적 방어력 20% 감소 및 3초마다 공격력의 500%에 해당하는 밤혼 성질의 불 원소 피해 추가"
                case "타오르는 태양":
                    characterInfo.activeSkill[2].level -= 3 if enkaDataFlag else 0
                case "진정한 의미":
                    characterInfo.activeSkill[1].level -= 3 if enkaDataFlag else 0

    # ----------------------- active -----------------------
    # active: 마비카의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive.unlocked:
            match passive.name:
                case "타오르는 꽃의 선물":
                    if passive.options[0].active:
                        newFightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.3)
                case "「키온고지」":
                    option = passive.options[0]
                    if option.active:
                        fourthConstellation = next((constellation for constellation in characterInfo.constellations if constellation.name == "「지도자」의 각오"))
                        if fourthConstellation.unlocked:
                            option.stack = option.maxStack
                            newFightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, 0.1)
                        newFightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, 0.002 * option.stack)

    # ----------------------- 추후 연산 진행부 -----------------------
    newFightProp = await getAfterWeaponArtifactFightProp(
        weaponArtifactData["fightProp"], characterInfo.weapon, characterInfo.artifact, weaponArtifactData["weaponAfterProps"], weaponArtifactData["artifactAfterProps"]
    )

    for additionalAttackPoint in additionalAttackPoints:
        key = additionalAttackPoint["key"]
        pointKey, value = additionalAttackPoint["value"]
        finalPoint = getattr(newFightProp, getattr(fightPropMpa, f"BASE_{pointKey}").value) * (
            1 + getattr(newFightProp, getattr(fightPropMpa, f"{pointKey}_PERCENT").value)
        ) + getattr(newFightProp, getattr(fightPropMpa, pointKey).value)
        newFightProp.add(key, finalPoint * value)

    return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


# async def getYelanFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: requestCharacterInfoSchema, enkaDataFlag:bool = False) -> CharacterFightPropReturnData:
#     newFightProp: fightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
#     return CharacterFightPropReturnData(fightProp=newFightProp, characterInfo=characterInfo)


getFightProp: dict[str, CharacterFightPropGetter] = {
    "감우": getGanyuFightProp,
    "카미사토 아야카": getKamisatoAyakaFightProp,
    "각청": getKeqingFightProp,
    "나히다": getNahidaFightProp,
    "라이덴 쇼군": getRaidenShogunFightProp,
    "호두": getHuTaoFightProp,
    "푸리나": getFurinaFightProp,
    "시틀라리": getCitlaliFightProp,
    "마비카": getMavuikaFightProp,
    "느비예트": getNeuvilletteFightProp,
    "에스코피에": getEscoffierFightProp,
    "스커크": getSkirkFightProp,
    # "야란": getYelanFightProp,
}

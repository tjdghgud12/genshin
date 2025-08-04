from typing import cast, List, Protocol, Coroutine, Any
from ambr import CharacterDetail, CharacterPromote
from pydantic import BaseModel
from data.character import CharacterFightPropSchema
from data import character as characterData
from services.weapon import getTotalWeaponFightProp
from services.artifact import getArtifactFightProp, getArtifactSetData
from data.globalVariable import fightPropKeys, baseFightProps


# ----------------------------------- Class -----------------------------------
class CharacterInfo(BaseModel):
    name: str
    level: int | str
    weapon: dict
    artifact: dict[str, list[dict]]
    passiveSkill: List[dict]
    activeSkill: List[dict]
    constellations: List[dict]


class CharacterFightPropGetter(Protocol):
    def __call__(self, ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> Coroutine[Any, Any, CharacterFightPropSchema]: ...


# ----------------------------------- Fucntion -----------------------------------
def genCharacterBaseStat(ambrCharacterDetail: CharacterDetail, level: int) -> CharacterFightPropSchema:
    fightProp: CharacterFightPropSchema = cast(
        CharacterFightPropSchema,
        {
            key: (
                0.05 if key == fightPropKeys.CRITICAL.value else 0.5 if key == fightPropKeys.CRITICAL_HURT.value else 1.0 if key == fightPropKeys.CHARGE_EFFICIENCY.value else 0.0
            )
            for key in list(CharacterFightPropSchema.__annotations__.keys())
        },
    )

    curveInfo = characterData.ambrCharacterCurve[str(level)]["curveInfos"]
    promoteStat = max(
        (promote for promote in ambrCharacterDetail.upgrade.promotes if promote.unlock_max_level <= level),
        key=lambda x: x.unlock_max_level,
        default=CharacterPromote,
    )

    for baseStat in ambrCharacterDetail.upgrade.base_stats:
        fightProp[baseStat.prop_type] += baseStat.init_value * curveInfo[baseStat.growth_type]
    for addStat in promoteStat.add_stats or []:
        fightProp[addStat.id] += addStat.value

    return fightProp


def getConstellationData():
    constellationData = []
    return constellationData


async def getGanyuFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    # ----------------------- Base Fight Prop -----------------------
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # ----------------------- Artifact -----------------------
    artifactFightProp = getArtifactFightProp(characterInfo.artifact)
    artifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
    artifactSetFightProp = artifactSetData["fightProp"]
    if artifactSetData["afterAddProps"] != None:
        for key in artifactSetData["afterAddProps"]:
            artifactSetFightProp[key] = 0.0

    # ----------------------- weapon -----------------------
    getWeaponFightProp = getTotalWeaponFightProp[characterInfo.weapon["name"]]
    weaponData = await getWeaponFightProp(
        characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
    )
    weaponFightProp = weaponData["fightProp"]
    if weaponData["afterAddProps"] != None:
        for key in weaponData["afterAddProps"]:
            weaponFightProp[key] = 0.0

    # ----------------------- 성유물 + 무기 데이터 합산 -----------------------
    for fightPropKey, value in artifactFightProp.items():
        newFightProp[fightPropKey] += value + artifactSetFightProp[fightPropKey] + weaponFightProp[fightPropKey]

    # ----------------------- active -----------------------
    # active: 감우의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive["unlocked"] and passive["active"]:
            match passive["name"]:
                case "단 하나의 마음":
                    newFightProp[fightPropKeys.CHARGED_ATTACK_CRITICAL.value] += 0.2
                case "천지교태":
                    newFightProp[fightPropKeys.ICE_ADD_HURT.value] += 0.2

    # ----------------------- constellations -----------------------
    # 획린(獲麟), 구름 여행, 잡초 근절, 살생의 발걸음의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation["unlocked"] and constellation["active"]:
            match constellation["name"]:
                case "이슬 먹는 신수":
                    newFightProp[fightPropKeys.ICE_RES_MINUS.value] += 0.15
                case "서수(西狩)":
                    newFightProp[fightPropKeys.ATTACK_ADD_HURT.value] += constellation["stack"] * 0.05

    # ----------------------- 추후 연산 진행부 -----------------------
    if weaponData["afterAddProps"] != None:
        finallyWeaponData = await getWeaponFightProp(
            characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
        )
        for key in finallyWeaponData["afterAddProps"]:
            newFightProp[key] += finallyWeaponData["fightProp"][key]

    if artifactSetData["afterAddProps"] != None:
        finallyArtifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
        for key in artifactSetData["afterAddProps"]:
            newFightProp[key] += finallyArtifactSetData["fightProp"][key]

    return newFightProp


async def getKamisatoAyakaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # ----------------------- Artifact -----------------------
    artifactFightProp = getArtifactFightProp(characterInfo.artifact)
    artifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
    artifactSetFightProp = artifactSetData["fightProp"]
    if artifactSetData["afterAddProps"] != None:
        for key in artifactSetData["afterAddProps"]:
            artifactSetFightProp[key] = 0.0

    # ----------------------- weapon -----------------------
    getWeaponFightProp = getTotalWeaponFightProp[characterInfo.weapon["name"]]
    weaponData = await getWeaponFightProp(
        characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
    )
    weaponFightProp = weaponData["fightProp"]
    if weaponData["afterAddProps"] != None:
        for key in weaponData["afterAddProps"]:
            weaponFightProp[key] = 0.0

    # ----------------------- 성유물 + 무기 데이터 합산 -----------------------
    for fightPropKey, value in artifactFightProp.items():
        newFightProp[fightPropKey] += value + artifactSetFightProp[fightPropKey] + weaponFightProp[fightPropKey]

    # ----------------------- active -----------------------
    # active: 아야카의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive["unlocked"] and passive["active"]:
            match passive["name"]:
                case "천죄국죄 진사":
                    newFightProp[fightPropKeys.NOMAL_ATTACK_ATTACK_ADD_HURT.value] += 0.3
                    newFightProp[fightPropKeys.CHARGED_ATTACK_ATTACK_ADD_HURT.value] += 0.3
                case "한천선명 축사":
                    newFightProp[fightPropKeys.ICE_ADD_HURT.value] += 0.18

    # ----------------------- constellations -----------------------
    # # 서리에 검게 물든 벚꽃, 삼중 서리 관문, 흩날리는 카미후부키, 화운종월경의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation["unlocked"] and constellation["active"]:
            match constellation["name"]:
                case "영고성쇠":
                    newFightProp[fightPropKeys.DEFENSE_MINUS.value] += 0.3
                case "물에 비친 달":
                    newFightProp[fightPropKeys.CHARGED_ATTACK_ATTACK_ADD_HURT.value] += 2.98

    # ----------------------- 추후 연산 진행부 -----------------------
    if weaponData["afterAddProps"] != None:
        finallyWeaponData = await getWeaponFightProp(
            characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
        )
        for key in finallyWeaponData["afterAddProps"]:
            newFightProp[key] += finallyWeaponData["fightProp"][key]

    if artifactSetData["afterAddProps"] != None:
        finallyArtifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
        for key in artifactSetData["afterAddProps"]:
            newFightProp[key] += finallyArtifactSetData["fightProp"][key]

    return newFightProp


async def getKeqingFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # ----------------------- Artifact -----------------------
    artifactFightProp = getArtifactFightProp(characterInfo.artifact)
    artifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
    artifactSetFightProp = artifactSetData["fightProp"]
    if artifactSetData["afterAddProps"] != None:
        for key in artifactSetData["afterAddProps"]:
            artifactSetFightProp[key] = 0.0

    # ----------------------- weapon -----------------------
    getWeaponFightProp = getTotalWeaponFightProp[characterInfo.weapon["name"]]
    weaponData = await getWeaponFightProp(
        characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
    )
    weaponFightProp = weaponData["fightProp"]
    if weaponData["afterAddProps"] != None:
        for key in weaponData["afterAddProps"]:
            weaponFightProp[key] = 0.0

    # ----------------------- 성유물 + 무기 데이터 합산 -----------------------
    for fightPropKey, value in artifactFightProp.items():
        newFightProp[fightPropKey] += value + artifactSetFightProp[fightPropKey] + weaponFightProp[fightPropKey]

    # ----------------------- active -----------------------
    # active: 각청의 active에는 버프 효과 존재 X

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive["unlocked"] and passive["active"]:
            match passive["name"]:
                case "옥형의 품격":
                    newFightProp[fightPropKeys.CRITICAL.value] += 0.15
                    newFightProp[fightPropKeys.CHARGE_EFFICIENCY.value] += 0.15

    # ----------------------- constellations -----------------------
    # # 계뢰, 가연, 등루, 이등의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation["unlocked"] and constellation["active"]:
            match constellation["name"]:
                case "조율":
                    newFightProp[fightPropKeys.ATTACK_PERCENT.value] += 0.25
                case "염정":
                    newFightProp[fightPropKeys.ELEC_ADD_HURT.value] += constellation["stack"] * 0.06

    # ----------------------- 추후 연산 진행부 -----------------------
    if weaponData["afterAddProps"] != None:
        finallyWeaponData = await getWeaponFightProp(
            characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
        )
        for key in finallyWeaponData["afterAddProps"]:
            newFightProp[key] += finallyWeaponData["fightProp"][key]

    if artifactSetData["afterAddProps"] != None:
        finallyArtifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
        for key in artifactSetData["afterAddProps"]:
            newFightProp[key] += finallyArtifactSetData["fightProp"][key]

    return newFightProp


async def getNahidaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # ----------------------- Artifact -----------------------
    artifactFightProp = getArtifactFightProp(characterInfo.artifact)
    artifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
    artifactSetFightProp = artifactSetData["fightProp"]
    if artifactSetData["afterAddProps"] != None:
        for key in artifactSetData["afterAddProps"]:
            artifactSetFightProp[key] = 0.0

    # ----------------------- weapon -----------------------
    getWeaponFightProp = getTotalWeaponFightProp[characterInfo.weapon["name"]]
    weaponData = await getWeaponFightProp(
        characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
    )
    weaponFightProp = weaponData["fightProp"]
    if weaponData["afterAddProps"] != None:
        for key in weaponData["afterAddProps"]:
            weaponFightProp[key] = 0.0

    # ----------------------- 성유물 + 무기 데이터 합산 -----------------------
    for fightPropKey, value in artifactFightProp.items():
        newFightProp[fightPropKey] += value + artifactSetFightProp[fightPropKey] + weaponFightProp[fightPropKey]

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

    # ----------------------- active -----------------------
    for active in characterInfo.activeSkill:
        if active["active"]:
            match active["name"]:
                case "마음이 그리는 환상":  # 번개, 물의 경우 fightProp에 영향 X. 각 쿨감 및 지속시간 증가
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.get("name") == "깨달음을 주는 잎"), {})
                    seedsOfWisdom = next((constellation for constellation in characterInfo.constellations if constellation.get("name") == "지혜를  머금은 씨앗"), {})
                    addLevel = 3 if addElementalSkillLevel.get("unlock", False) else 0
                    skillValue = activeSkillLevelMap[active["name"]][active["level"] + addLevel - 1]
                    stack = min(active["stack"] + (1 if seedsOfWisdom.get("unlock", False) else 0), 2)
                    newFightProp[fightPropKeys.ELEMENT_SKILL_ATTACK_ADD_HURT.value] += skillValue[stack - 1]

    # ----------------------- constellations -----------------------
    # # 지혜를 머금은 씨앗, 감화된 성취의 싹, 달변으로 맺은 열매, 깨달음을 주는 잎의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation["unlocked"] and constellation["active"]:
            match constellation["name"]:
                case "올곧은 선견의 뿌리":
                    # 연소, 개화, 만개, 발화의 치명타 효과는 일단 무시
                    # 활성, 촉진, 발산 반응 시 방어력 감소만 적용
                    newFightProp[fightPropKeys.DEFENSE_MINUS.value] += 0.3
                case "추론으로 드러난 줄기":
                    newFightProp[fightPropKeys.ELEMENT_MASTERY.value] += constellation["stack"] * 20 + 80

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive["unlocked"] and passive["active"]:
            match passive["name"]:
                case "정선으로 포용한 명론":
                    newFightProp[fightPropKeys.ELEMENT_MASTERY.value] += min(newFightProp[fightPropKeys.ELEMENT_MASTERY.value] * 0.25, 250)
                case "지혜로 깨우친 지론":
                    val = min(newFightProp[fightPropKeys.ELEMENT_MASTERY.value] - 200, 800)
                    if val > 0:
                        newFightProp[fightPropKeys.ELEMENT_SKILL_CRITICAL.value] += val * 0.03
                        newFightProp[fightPropKeys.ELEMENT_SKILL_ATTACK_ADD_HURT.value] += val * 0.1

    # ----------------------- 추후 연산 진행부 -----------------------
    if weaponData["afterAddProps"] != None:
        finallyWeaponData = await getWeaponFightProp(
            characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
        )
        for key in finallyWeaponData["afterAddProps"]:
            newFightProp[key] += finallyWeaponData["fightProp"][key]

    if artifactSetData["afterAddProps"] != None:
        finallyArtifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
        for key in artifactSetData["afterAddProps"]:
            newFightProp[key] += finallyArtifactSetData["fightProp"][key]

    return newFightProp


async def getRaidenShogunFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    # ----------------------- Artifact -----------------------
    artifactFightProp = getArtifactFightProp(characterInfo.artifact)
    artifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
    artifactSetFightProp = artifactSetData["fightProp"]
    if artifactSetData["afterAddProps"] != None:
        for key in artifactSetData["afterAddProps"]:
            artifactSetFightProp[key] = 0.0

    # ----------------------- weapon -----------------------
    getWeaponFightProp = getTotalWeaponFightProp[characterInfo.weapon["name"]]
    weaponData = await getWeaponFightProp(
        characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
    )
    weaponFightProp = weaponData["fightProp"]
    if weaponData["afterAddProps"] != None:
        for key in weaponData["afterAddProps"]:
            weaponFightProp[key] = 0.0

    # ----------------------- 성유물 + 무기 데이터 합산 -----------------------
    for fightPropKey, value in artifactFightProp.items():
        newFightProp[fightPropKey] += value + artifactSetFightProp[fightPropKey] + weaponFightProp[fightPropKey]

    activeSkillLevelMap = {
        "초월·악요개안": [
            0.22,  # Level 1
            0.23,  # Level 2
            0.24,  # Level 3
            0.25,  # Level 4
            0.26,  # Level 5
            0.27,  # Level 6
            0.28,  # Level 7
            0.29,  # Level 8
            0.30,  # Level 9
            0.30,  # Level 10
            0.30,  # Level 11
            0.30,  # Level 12
            0.30,  # Level 13
            0.30,  # Level 14
            0.30,  # Level 15
        ]
    }

    # ----------------------- active -----------------------
    for active in characterInfo.activeSkill:
        if active["active"]:
            match active["name"]:
                case "초월·악요개안":
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.get("name") == "쇼군의 현형"), {})
                    addLevel = 3 if addElementalSkillLevel.get("unlock", False) else 0
                    skillValue = activeSkillLevelMap[active["name"]][active["level"] + addLevel - 1]
                    newFightProp[fightPropKeys.ELEMENT_BURST_ATTACK_ADD_HURT.value] += 90 * skillValue / 100  # 90은 라이덴의 원소 에너지

    # ----------------------- constellations -----------------------
    # 악요 명문(銘文), 진영의 과거, 진리의 맹세, 쇼군의 현형, 염원의 대행인의 경우 fightProp에 영행 X
    for constellation in characterInfo.constellations:
        if constellation["unlocked"] and constellation["active"]:
            match constellation["name"]:
                case "강철 절단":
                    newFightProp[fightPropKeys.DEFENSE_IGNORE.value] += 0.6

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive["unlocked"] and passive["active"]:
            match passive["name"]:
                case "비범한 옥체":
                    val = newFightProp[fightPropKeys.CHARGE_EFFICIENCY.value] - 1
                    if val > 0:
                        newFightProp[fightPropKeys.ELEC_ADD_HURT.value] += val * 0.4

    # ----------------------- 추후 연산 진행부 -----------------------
    if weaponData["afterAddProps"] != None:
        finallyWeaponData = await getWeaponFightProp(
            characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
        )
        for key in finallyWeaponData["afterAddProps"]:
            newFightProp[key] += finallyWeaponData["fightProp"][key]

    if artifactSetData["afterAddProps"] != None:
        finallyArtifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
        for key in artifactSetData["afterAddProps"]:
            newFightProp[key] += finallyArtifactSetData["fightProp"][key]

    return newFightProp


async def getHuTaoFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))

    # ----------------------- Artifact -----------------------
    artifactFightProp = getArtifactFightProp(characterInfo.artifact)
    artifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
    artifactSetFightProp = artifactSetData["fightProp"]
    if artifactSetData["afterAddProps"] != None:
        for key in artifactSetData["afterAddProps"]:
            artifactSetFightProp[key] = 0.0

    # ----------------------- weapon -----------------------
    getWeaponFightProp = getTotalWeaponFightProp[characterInfo.weapon["name"]]
    weaponData = await getWeaponFightProp(
        characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
    )
    weaponFightProp = weaponData["fightProp"]
    if weaponData["afterAddProps"] != None:
        for key in weaponData["afterAddProps"]:
            weaponFightProp[key] = 0.0

    # ----------------------- 성유물 + 무기 데이터 합산 -----------------------
    for fightPropKey, value in artifactFightProp.items():
        newFightProp[fightPropKey] += value + artifactSetFightProp[fightPropKey] + weaponFightProp[fightPropKey]

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

    # ----------------------- active -----------------------
    for active in characterInfo.activeSkill:
        if active["active"]:
            match active["name"]:
                case "나비의 서":
                    addElementalSkillLevel = next((constellation for constellation in characterInfo.constellations if constellation.get("name") == "적색 피의 의식"), {})
                    addLevel = 3 if addElementalSkillLevel.get("unlock", False) else 0
                    skillValue = activeSkillLevelMap[active["name"]][active["level"] + addLevel - 1]
                    baseHp = newFightProp[fightPropKeys.BASE_HP.value]
                    hpPercent = newFightProp[fightPropKeys.HP_PERCENT.value]
                    hp = newFightProp[fightPropKeys.HP.value]
                    totalHp = baseHp * (hpPercent + 1) + hp
                    newFightProp[fightPropKeys.ATTACK.value] += totalHp * skillValue

    # ----------------------- constellations -----------------------
    for constellation in characterInfo.constellations:
        if constellation["unlocked"] and constellation["active"]:
            match constellation["name"]:
                case "":
                    newFightProp[fightPropKeys.DEFENSE_IGNORE.value] += 0.6

    # ----------------------- passive -----------------------
    for passive in characterInfo.passiveSkill:
        if passive["unlocked"] and passive["active"]:
            match passive["name"]:
                case "":
                    val = newFightProp[fightPropKeys.CHARGE_EFFICIENCY.value] - 1
                    if val > 0:
                        newFightProp[fightPropKeys.ELEC_ADD_HURT.value] += val * 0.4

    # ----------------------- 추후 연산 진행부 -----------------------
    if weaponData["afterAddProps"] != None:
        finallyWeaponData = await getWeaponFightProp(
            characterInfo.weapon["id"], characterInfo.weapon["level"], characterInfo.weapon["refinement"], characterInfo.weapon["option"], newFightProp
        )
        for key in finallyWeaponData["afterAddProps"]:
            newFightProp[key] += finallyWeaponData["fightProp"][key]

    if artifactSetData["afterAddProps"] != None:
        finallyArtifactSetData = getArtifactSetData(characterInfo.artifact["setInfo"], newFightProp)
        for key in artifactSetData["afterAddProps"]:
            newFightProp[key] += finallyArtifactSetData["fightProp"][key]

    return newFightProp


async def getFurinaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    return newFightProp


async def getSkirkFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    return newFightProp


async def getEscoffierFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    return newFightProp


async def getCitlaliFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    return newFightProp


async def getNeuvilletteFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    return newFightProp


async def getMavuikaFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
    newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
    return newFightProp


# async def getYelanFightProp(ambrCharacterDetail: CharacterDetail, characterInfo: CharacterInfo) -> CharacterFightPropSchema:
#     newFightProp: CharacterFightPropSchema = genCharacterBaseStat(ambrCharacterDetail, int(characterInfo.level))
#     return newFightProp


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

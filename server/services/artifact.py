from data.artifact import artifactSetOptions
from data.character import fightPropTemplate
from data.globalVariable import fightPropMpa, fightPropKeys
from schemas.artifact import artifactDataSchema, artifactSetDataSchema
from schemas.fightProp import fightPropSchema
from typing import cast, TypedDict
from copy import deepcopy
from ambr import WeaponType
import inspect


# characterFightProp: fightPropSchema
class ArtifactDataReturnSchema(TypedDict, total=True):
    fightProp: fightPropSchema
    afterAddProps: list[str] | None


def getMarechausseeHunterSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)

    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_HURT.value, 0.15)
                    fightProp.add(fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_HURT.value, 0.15)
                case 1:
                    fightProp.add(fightPropMpa.CRITICAL.value, 0.12 * info.stack)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getBlizzardStrayerSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)

    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ICE_ADD_HURT.value, 0.15)
                case 1:
                    if info.active:
                        fightProp.add(fightPropMpa.CRITICAL.value, 0.2)
                case 2:
                    if info.active:
                        fightProp.add(fightPropMpa.CRITICAL.value, 0.2)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getThunderingFurySetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ELEC_ADD_HURT.value, 0.15)
                case 1:
                    fightProp.add(fightPropMpa.OVERLOADED_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropMpa.ELECTROCHARGED_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropMpa.SUPERCONDUCT_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropMpa.HYPERBLOOM_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropMpa.AGGRAVATE_ADD_HURT.value, 0.2)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getDeepwoodMemoriesSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.GRASS_ADD_HURT.value, 0.15)
                case 1:
                    fightProp.add(fightPropMpa.GRASS_RES_MINUS.value, 0.3)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getEmblemOfSeveredFateSetOption(
    numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema], characterFightProp: fightPropSchema
) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.CHARGE_EFFICIENCY.value, 0.2)
                case 1:
                    fightProp.add(fightPropMpa.ELEMENT_BURST_ATTACK_ADD_HURT.value, getattr(characterFightProp, fightPropMpa.CHARGE_EFFICIENCY.value) * 0.25)

    return {"fightProp": fightProp, "afterAddProps": [fightPropMpa.ELEMENT_BURST_ATTACK_ADD_HURT.value]}


def getCrimsonWitchOfFlamesSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.FIRE_ADD_HURT.value, 0.15)
                case 1:
                    fightProp.add(fightPropMpa.OVERLOADED_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropMpa.BURGEON_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropMpa.BURNING_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropMpa.VAPORIZE_ADD_HURT.value, 0.15)
                    fightProp.add(fightPropMpa.MELT_ADD_HURT.value, 0.15)
                    fightProp.add(fightPropMpa.FIRE_ADD_HURT.value, 0.075 * info.stack)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getGoldenTroupeSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value, 0.20)
                case 1:
                    fightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value, 0.25)
                case 2:
                    if info.active:
                        fightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_HURT.value, 0.25)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getFinaleOfTheDeepGalleriesSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ICE_ADD_HURT.value, 0.15)
                case 1:
                    if info.active:
                        fightProp.add(fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_HURT.value, 0.60)
                        fightProp.add(fightPropMpa.ELEMENT_BURST_ATTACK_ADD_HURT.value, 0.60)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getScrollOfTheHeroOfCinderCitySetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 1:
                    if info.active:
                        fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, 0.12)
                case 2:
                    if info.active:
                        fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, 0.28)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getObsidianCodexSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    if info.active:
                        fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, 0.15)
                case 1:
                    if info.active:
                        fightProp.add(fightPropMpa.CRITICAL.value, 0.40)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getFragmentOfHarmonicWhimsySetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    if info.active:
                        fightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.18)
                case 1:
                    if info.active:
                        fightProp.add(fightPropMpa.ATTACK_ADD_HURT.value, 0.18 * info.stack)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getSongOfDaysPastSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.HEAL_ADD.value, 0.15)
                case 1:
                    if info.active:
                        fightProp.add(fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_POINT.value, info.stack * 0.08)
                        fightProp.add(fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_POINT.value, info.stack * 0.08)
                        fightProp.add(fightPropMpa.FALLING_ATTACK_ATTACK_ADD_POINT.value, info.stack * 0.08)
                        fightProp.add(fightPropMpa.ELEMENT_SKILL_ATTACK_ADD_POINT.value, info.stack * 0.08)
                        fightProp.add(fightPropMpa.ELEMENT_BURST_ATTACK_ADD_POINT.value, info.stack * 0.08)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getNighttimeWhispersInTheEchoingWoodsSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.18)
                case 1:
                    if info.active:
                        fightProp.add(fightPropMpa.ROCK_ADD_HURT.value, 0.20)
                case 2:
                    if info.active and optionInfo[1].active:
                        fightProp.add(fightPropMpa.ROCK_ADD_HURT.value, 0.30)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getShimenawasReminiscenceSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.18)
                case 1:
                    if info.active:
                        fightProp.add(fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_HURT.value, 0.50)
                        fightProp.add(fightPropMpa.CHARGED_ATTACK_ATTACK_ADD_HURT.value, 0.50)
                        fightProp.add(fightPropMpa.FALLING_ATTACK_ATTACK_ADD_HURT.value, 0.50)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getPaleFlameSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema]) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.PHYSICAL_ADD_HURT.value, 0.25)
                case 1:
                    if info.active:
                        fightProp.add(fightPropMpa.ATTACK_PERCENT.value, info.stack * 0.09)
                        if info.stack >= info.maxStack:
                            fightProp.add(fightPropMpa.PHYSICAL_ADD_HURT.value, 0.25)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getGladiatorsFinaleSetOption(numberOfParts: int, optionInfo: list[artifactSetDataSchema.extendedArtifactSetOptionSchema], weaponType: WeaponType) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info.requiredParts:
            match i:
                case 0:
                    fightProp.add(fightPropMpa.ATTACK_PERCENT.value, 0.18)
                case 1:
                    # 조건에 한손검 양손검 장병기를 알아야함.
                    # fightProp이 아니라 캐릭터의 옵션 자체를 알아야하네
                    weaponList = [WeaponType.CLAYMORE, WeaponType.SWORD, WeaponType.POLE]
                    if weaponType in weaponList:
                        fightProp.add(fightPropMpa.NOMAL_ATTACK_ATTACK_ADD_HURT.value, 0.35)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


getArtifactSetsFightProp = {
    "그림자 사냥꾼": getMarechausseeHunterSetOption,
    "얼음바람 속에서 길잃은 용사": getBlizzardStrayerSetOption,
    "번개 같은 분노": getThunderingFurySetOption,
    "숲의 기억": getDeepwoodMemoriesSetOption,
    "절연의 기치": getEmblemOfSeveredFateSetOption,
    "불타오르는 화염의 마녀": getCrimsonWitchOfFlamesSetOption,
    "황금 극단": getGoldenTroupeSetOption,
    "깊은 회랑의 피날레": getFinaleOfTheDeepGalleriesSetOption,
    "잿더미성 용사의 두루마리": getScrollOfTheHeroOfCinderCitySetOption,
    "흑요석 비전": getObsidianCodexSetOption,
    "조화로운 공상의 단편": getFragmentOfHarmonicWhimsySetOption,
    "지난날의 노래": getSongOfDaysPastSetOption,
    "메아리숲의 야화": getNighttimeWhispersInTheEchoingWoodsSetOption,
    "추억의 시메나와": getShimenawasReminiscenceSetOption,
    "창백의 화염": getPaleFlameSetOption,
    "검투사의 피날레": getGladiatorsFinaleSetOption,
}


def getArtifactFightProp(artifactInfo: artifactDataSchema) -> fightPropSchema:
    fightProp = deepcopy(fightPropTemplate)
    artifacts = artifactInfo.parts

    # 성유물 부위별 옵션 연산
    for artifact in artifacts:
        mainFightPropKey, mainValue = next(iter(artifact.mainStat.items()))
        #
        if not mainFightPropKey in fightPropKeys:
            setattr(fightProp, mainFightPropKey, 0.0)
        fightProp.add(mainFightPropKey, mainValue)
        for subStat in artifact.subStat:
            subFightPropKey, subValue = next(iter(subStat.items()))
            if not subFightPropKey in fightPropKeys:
                setattr(fightProp, subFightPropKey, 0)
            fightProp.add(subFightPropKey, subValue)

    return fightProp


def getArtifactSetData(setInfos: list[artifactSetDataSchema], characterFightProp: fightPropSchema, weaponType: WeaponType) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for setInfo in setInfos:
        getSetFightProp = getArtifactSetsFightProp[setInfo.name]
        variableList = inspect.signature(getSetFightProp).parameters
        variables = {"numberOfParts": setInfo.numberOfParts, "optionInfo": setInfo.options}
        if "characterFightProp" in variableList:
            variables["characterFightProp"] = characterFightProp
        if "weaponType" in variableList:
            variables["weaponType"] = weaponType

        setOptionFightProp = getSetFightProp(**variables)
        afterAddProps = setOptionFightProp["afterAddProps"]
        for fightPropKey, value in setOptionFightProp["fightProp"].model_dump().items():
            fightProp.add(fightPropKey, value)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=afterAddProps)


def getArtifactSetInfo(artifacts: list[dict]):
    setList = set()
    setInfo = []
    for artifact in artifacts:
        setList.add(artifact["setName"])  # 여기서 세트를 알 수 있어야함.

    for setName in setList:
        numberOfParts = sum(1 for artifact in artifacts if artifact.get("setName") == setName)
        if numberOfParts > 2:
            setInfo.append({"name": setName, "options": artifactSetOptions.get(setName), "numberOfParts": numberOfParts})

    return setInfo

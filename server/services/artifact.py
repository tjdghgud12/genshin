from typing import cast, TypedDict
from data.character import fightPropTemplate
from models.character import CharacterFightPropModel
from data.artifact import artifactSetOptions
from data.globalVariable import fightPropKeys
from copy import deepcopy


# characterFightProp: CharacterFightPropModel
class ArtifactDataReturnSchema(TypedDict, total=True):
    fightProp: CharacterFightPropModel
    afterAddProps: list[str] | None


def getMarechausseeHunterSetOption(numberOfParts: int, optionInfo: list[dict], _characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)

    for i, info in enumerate(optionInfo):
        if numberOfParts >= info["requiredParts"]:
            match i:
                case 0:
                    fightProp.add(fightPropKeys.NOMAL_ATTACK_ATTACK_ADD_HURT.value, 0.15)
                    fightProp.add(fightPropKeys.CHARGED_ATTACK_ATTACK_ADD_HURT.value, 0.15)
                case 1:
                    fightProp.add(fightPropKeys.CRITICAL.value, 0.12 * info["stack"])

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getBlizzardStrayerSetOption(numberOfParts: int, optionInfo: list[dict], _characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)

    for i, info in enumerate(optionInfo):
        if numberOfParts >= info["requiredParts"]:
            match i:
                case 0:
                    fightProp.add(fightPropKeys.ICE_ADD_HURT.value, 0.15)
                case 1:
                    if info["active"]:
                        fightProp.add(fightPropKeys.CRITICAL.value, 0.2)
                case 2:
                    if info["active"]:
                        fightProp.add(fightPropKeys.CRITICAL.value, 0.2)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getThunderingFurySetOption(numberOfParts: int, optionInfo: list[dict], _characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info["requiredParts"]:
            match i:
                case 0:
                    fightProp.add(fightPropKeys.ELEC_ADD_HURT.value, 0.15)
                case 1:
                    fightProp.add(fightPropKeys.OVERLOADED_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropKeys.ELECTRICSHOCK_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropKeys.SUPERCONDUCT_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropKeys.HYPERBLOOM_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropKeys.AGGRAVATE_ADD_HURT.value, 0.2)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getDeepwoodMemoriesSetOption(numberOfParts: int, optionInfo: list[dict], _characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info["requiredParts"]:
            match i:
                case 0:
                    fightProp.add(fightPropKeys.GRASS_ADD_HURT.value, 0.15)
                case 1:
                    fightProp.add(fightPropKeys.GRASS_RES_MINUS.value, 0.3)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getEmblemOfSeveredFateSetOption(numberOfParts: int, optionInfo: list[dict], characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info["requiredParts"]:
            match i:
                case 0:
                    fightProp.add(fightPropKeys.CHARGE_EFFICIENCY.value, 0.2)
                case 1:
                    fightProp.add(fightPropKeys.ELEMENT_BURST_ATTACK_ADD_HURT.value, getattr(characterFightProp, fightPropKeys.CHARGE_EFFICIENCY.value) * 0.25)

    return {"fightProp": fightProp, "afterAddProps": [fightPropKeys.ELEMENT_BURST_ATTACK_ADD_HURT.value]}


def getCrimsonWitchOfFlamesSetOption(numberOfParts: int, optionInfo: list[dict], _characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info["requiredParts"]:
            match i:
                case 0:
                    fightProp.add(fightPropKeys.FIRE_ADD_HURT.value, 0.15)
                case 1:
                    fightProp.add(fightPropKeys.OVERLOADED_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropKeys.IGNITION_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropKeys.COMBUSTION_ADD_HURT.value, 0.4)
                    fightProp.add(fightPropKeys.EVAPORATION_ADD_HURT.value, 0.15)
                    fightProp.add(fightPropKeys.MELT_ADD_HURT.value, 0.15)
                    fightProp.add(fightPropKeys.FIRE_ADD_HURT.value, 0.075 * info["stack"])

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getGoldenTroupeSetOption(numberOfParts: int, optionInfo: list[dict], _characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info["requiredParts"]:
            match i:
                case 0:
                    fightProp.add(fightPropKeys.ELEMENT_SKILL_ATTACK_ADD_HURT.value, 0.20)
                case 1:
                    fightProp.add(fightPropKeys.ELEMENT_SKILL_ATTACK_ADD_HURT.value, 0.25)
                case 2:
                    if info["active"]:
                        fightProp.add(fightPropKeys.ELEMENT_SKILL_ATTACK_ADD_HURT.value, 0.25)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getFinaleOfTheDeepGalleriesSetOption(numberOfParts: int, optionInfo: list[dict], _characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info["requiredParts"]:
            match i:
                case 0:
                    fightProp.add(fightPropKeys.ICE_ADD_HURT.value, 0.15)
                case 1:
                    if info["active"]:
                        fightProp.add(fightPropKeys.NOMAL_ATTACK_ATTACK_ADD_HURT.value, 0.60)
                        fightProp.add(fightPropKeys.ELEMENT_BURST_ATTACK_ADD_HURT.value, 0.60)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getScrollOfTheHeroOfCinderCitySetOption(numberOfParts: int, optionInfo: list[dict], _characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info["requiredParts"]:
            match i:
                case 1:
                    if info["active"]:
                        fightProp.add(fightPropKeys.ATTACK_ADD_HURT.value, 0.12)
                case 2:
                    if info["active"]:
                        fightProp.add(fightPropKeys.ATTACK_ADD_HURT.value, 0.28)

    return ArtifactDataReturnSchema(fightProp=fightProp, afterAddProps=None)


def getObsidianCodexSetOption(numberOfParts: int, optionInfo: list[dict], _characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for i, info in enumerate(optionInfo):
        if numberOfParts >= info["requiredParts"]:
            match i:
                case 0:
                    if info["active"]:
                        fightProp.add(fightPropKeys.ATTACK_ADD_HURT.value, 0.15)
                case 1:
                    if info["active"]:
                        fightProp.add(fightPropKeys.CRITICAL.value, 0.40)

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
}


def getArtifactFightProp(artifactInfo: dict) -> CharacterFightPropModel:
    fightProp = deepcopy(fightPropTemplate)
    artifacts: list[dict] = artifactInfo["parts"]

    # 성유물 부위별 옵션 연산
    for artifact in artifacts:
        mainFightPropKey, mainValue = next(iter(artifact["mainStat"].items()))
        if not mainFightPropKey in fightProp:
            setattr(fightProp, mainFightPropKey, 0.0)
        fightProp.add(mainFightPropKey, mainValue)
        for subStat in artifact["subStat"]:
            subFightPropKey, subValue = next(iter(subStat.items()))
            if not subFightPropKey in fightProp:
                setattr(fightProp, subFightPropKey, 0)
            fightProp.add(subFightPropKey, subValue)

    return fightProp


def getArtifactSetData(setInfos: list[dict], characterFightProp: CharacterFightPropModel) -> ArtifactDataReturnSchema:
    fightProp = deepcopy(fightPropTemplate)
    for setInfo in setInfos:
        getSetFightProp = getArtifactSetsFightProp[setInfo["name"]]
        setOptionFightProp = getSetFightProp(setInfo["numberOfParts"], setInfo.get("options") or [], characterFightProp)
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

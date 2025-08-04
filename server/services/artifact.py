from typing import cast
from data.character import CharacterFightPropSchema, fightPropTemplate
from data.artifact import artifactSetOptions
from data.globalVariable import fightPropKeys


def getMarechausseeHunterSetOption(numberOfParts: int, optionInfo: list[dict]):
    fightProp: CharacterFightPropSchema = {**fightPropTemplate}

    for i, info in enumerate(optionInfo):
        if info["active"]:
            match i:
                case 0:
                    if numberOfParts >= 2:
                        fightProp[fightPropKeys.NOMAL_ATTACK_ATTACK_ADD_HURT.value] += 0.15
                        fightProp[fightPropKeys.CHARGED_ATTACK_ATTACK_ADD_HURT.value] += 0.15
                case 1:
                    if numberOfParts >= 4:
                        fightProp[fightPropKeys.CRITICAL.value] += 0.12 * info["stack"]

    return fightProp


def getBlizzardStrayerSetOption(numberOfParts: int, optionInfo: list[dict]):
    fightProp: CharacterFightPropSchema = {**fightPropTemplate}

    for i, info in enumerate(optionInfo):
        if info["active"]:
            match i:
                case 0:
                    if numberOfParts >= 2:
                        fightProp[fightPropKeys.ICE_ADD_HURT.value] += 0.15
                case 1:
                    if numberOfParts >= 4:
                        fightProp[fightPropKeys.CRITICAL.value] += 0.2 * info["stack"]

    return fightProp


def getThunderingFurySetOption(numberOfParts: int, optionInfo: list[dict]):
    fightProp: CharacterFightPropSchema = {**fightPropTemplate}
    for i, info in enumerate(optionInfo):
        if info["active"]:
            match i:
                case 0:
                    if numberOfParts >= 2:
                        fightProp[fightPropKeys.ELEC_ADD_HURT.value] += 0.15
                case 1:
                    if numberOfParts >= 4:
                        fightProp[fightPropKeys.OVERLOADED_ADD_HURT.value] += 0.4
                        fightProp[fightPropKeys.ELECTRICSHOCK_ADD_HURT.value] += 0.4
                        fightProp[fightPropKeys.SUPERCONDUCT_ADD_HURT.value] += 0.4
                        fightProp[fightPropKeys.HYPERBLOOM_ADD_HURT.value] += 0.4
                        fightProp[fightPropKeys.AGGRAVATE_ADD_HURT.value] += 0.2

    return fightProp


def getDeepwoodMemoriesSetOption(numberOfParts: int, optionInfo: list[dict]):
    fightProp: CharacterFightPropSchema = {**fightPropTemplate}
    for i, info in enumerate(optionInfo):
        if info["active"]:
            match i:
                case 0:
                    if numberOfParts >= 2:
                        fightProp[fightPropKeys.GRASS_ADD_HURT.value] += 0.15
                case 1:
                    if numberOfParts >= 4:
                        fightProp[fightPropKeys.GRASS_RES_MINUS.value] += 0.3

    return fightProp


def getEmblemOfSeveredFateSetOption(numberOfParts: int, optionInfo: list[dict]):
    fightProp: CharacterFightPropSchema = {**fightPropTemplate}
    for i, info in enumerate(optionInfo):
        if info["active"]:
            match i:
                case 0:
                    if numberOfParts >= 2:
                        fightProp[fightPropKeys.CHARGE_EFFICIENCY.value] += 0.2
                case 1:
                    if numberOfParts >= 4:
                        fightProp[fightPropKeys.ELEMENT_BURST_ATTACK_ADD_HURT.value] += 0.3

    return fightProp


getArtifactSetFightProp = {
    "그림자 사냥꾼": getMarechausseeHunterSetOption,
    "얼음바람 속에서 길잃은 용사": getBlizzardStrayerSetOption,
    "번개 같은 분노": getThunderingFurySetOption,
    "숲의 기억": getDeepwoodMemoriesSetOption,
    "절연의 기치": getEmblemOfSeveredFateSetOption,
}


def getArtifactData(artifactInfo: dict) -> CharacterFightPropSchema:
    fightProp: CharacterFightPropSchema = {**fightPropTemplate}
    artifacts: list[dict] = artifactInfo["parts"]
    setInfos: list[dict] = artifactInfo["setInfo"]

    # 성유뮬 부위별 옵션 연산
    for artifact in artifacts:
        mainFightPropKey, mainValue = next(iter(artifact["mainStat"].items()))
        if not mainFightPropKey in fightProp:
            fightProp[mainFightPropKey] = 0
        fightProp[mainFightPropKey] += mainValue
        for subStat in artifact["subStat"]:
            subFightPropKey, subValue = next(iter(subStat.items()))
            if not subFightPropKey in fightProp:
                fightProp[subFightPropKey] = 0
            fightProp[subFightPropKey] += subValue

    # 세트옵션으로 증가하는 fightProp 연산
    for setInfo in setInfos:
        getSetFightProp = getArtifactSetFightProp[setInfo["name"]]
        setOptionFightProp = getSetFightProp(setInfo["numberOfParts"], setInfo.get("option") or [])
        for fightPropKey, value in setOptionFightProp.items():
            fightProp[fightPropKey] += value

    return fightProp


def getArtifactSetInfo(artifacts: list[dict]):
    setList = set()
    setInfo = []
    for artifact in artifacts:
        setList.add(artifact["setName"])  # 여기서 세트를 알 수 있어야함.

    for setName in setList:
        numberOfParts = sum(1 for artifact in artifacts if artifact.get("setName") == setName)
        if numberOfParts > 2:
            setInfo.append({"name": setName, "option": artifactSetOptions.get(setName), "numberOfParts": numberOfParts})

    return setInfo

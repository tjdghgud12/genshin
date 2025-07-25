from typing import cast
from data.character import CharacterFightPropType, fightPropTemplate
from data.artifact import artifactSetOptions


def getMarechausseeHunterSetOption(numberOfParts: int, optionInfo: list[dict]):
    fightProp: CharacterFightPropType = {**fightPropTemplate}

    for i, info in enumerate(optionInfo):
        if info["active"]:
            match i:
                case 0:
                    if numberOfParts >= 2:
                        fightProp["FIGHT_PROP_NOMAL_ATTACK_ATTACK_ADD_HURT"] += 0.15
                        fightProp["FIGHT_PROP_CHARGED_ATTACK_ATTACK_ADD_HURT"] += 0.15
                case 1:
                    if numberOfParts >= 4:
                        fightProp["FIGHT_PROP_CRITICAL"] += 0.12 * info["stack"]

    return fightProp


def getBlizzardStrayerSetOption(numberOfParts: int, optionInfo: list[dict]):
    fightProp: CharacterFightPropType = {**fightPropTemplate}

    for i, info in enumerate(optionInfo):
        if info["active"]:
            match i:
                case 0:
                    if numberOfParts >= 2:
                        fightProp["FIGHT_PROP_ICE_ADD_HURT"] += 0.15
                case 1:
                    if numberOfParts >= 4:
                        fightProp["FIGHT_PROP_CRITICAL"] += 0.2 * info["stack"]

    return fightProp


def getThunderingFurySetOption(numberOfParts: int, optionInfo: list[dict]):
    fightProp: CharacterFightPropType = {**fightPropTemplate}
    for i, info in enumerate(optionInfo):
        if info["active"]:
            match i:
                case 0:
                    if numberOfParts >= 2:
                        fightProp["FIGHT_PROP_ELEC_ADD_HURT"] += 0.15
                case 1:
                    if numberOfParts >= 4:
                        fightProp["FIGHT_PROP_OVERLOADED_ADD_HURT"] += 0.4
                        fightProp["FIGHT_PROP_ELECTRICSHOCK_ADD_HURT"] += 0.4
                        fightProp["FIGHT_PROP_SUPERCONDUCT_ADD_HURT"] += 0.4
                        fightProp["FIGHT_PROP_HYPERBLOOM_ADD_HURT"] += 0.4
                        fightProp["FIGHT_PROP_AGGRAVATE_ADD_HURT"] += 0.2

    return fightProp


getArtifactSetFightProp = {
    "그림자 사냥꾼": getMarechausseeHunterSetOption,
    "얼음바람 속에서 길잃은 용사": getBlizzardStrayerSetOption,
    "번개 같은 분노": getThunderingFurySetOption,
}


def getArtifactData(artifactInfo: dict) -> CharacterFightPropType:
    fightProp: CharacterFightPropType = {**fightPropTemplate}
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

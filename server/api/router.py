import data.artifact as artifactData
from data.character import characterData
import data.weapon as weaponData
from services.artifact import getArtifactSetInfo
from services.ambrApi import getAmbrApi
from services.calculation import damageCalculation
from services.character import getFightProp
from schemas.calculation import requestCharacterInfoSchema
from schemas.character import passiveSkillSchema, activeSkillSchema, skillConstellationOptionSchema, skillConstellationType
from schemas.fightProp import fightPropSchema
from ambr import CharacterDetail, AmbrAPI, Talent, Constellation
import enka
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()


# 2025-07-23 기준(genshin impact 5.7)
# ambrCharacters = await ambrApi.fetch_characters() # 여행자 빼고 100개, 각 속성별 여행자 포함 시 106개
# ambrWeapons = await ambrApi.fetch_weapons() # 4성 이상은 186개, 1성 이상은 220개
# ambrArtifacts = await ambrApi.fetch_artifact_sets() # 55개
class calculationBody(BaseModel):
    additionalFightProp: fightPropSchema
    characterInfo: requestCharacterInfoSchema


@router.get("/weapons/{id}")
async def getWeaponDetail(id: int, ambrApi: AmbrAPI = Depends(getAmbrApi)):
    if ambrApi is None:
        raise HTTPException(status_code=503, detail="ambrApi is not initialized yet")
    try:
        return await ambrApi.fetch_weapon_detail(id)
    except:
        raise HTTPException(status_code=404, detail="weapon detail is not found")


@router.get("/weapons")
async def genWeaponList(ambrApi: AmbrAPI = Depends(getAmbrApi)):
    if ambrApi is None:
        raise HTTPException(status_code=503, detail="ambrApi is not initialized yet")
    weaponInfo = weaponData.weaponInfo
    ambrWeapons = await ambrApi.fetch_weapons()  # 4성 이상은 186개, 1성 이상은 220개

    return list(map(lambda weapon: {**vars(weapon), "options": weaponInfo.get(weapon.name, None)}, filter(lambda weapon: weaponInfo.get(weapon.name, None) != None, ambrWeapons)))


@router.get("/artifactsets/{id}")
async def getArtifactSetDetail(id: int, ambrApi: AmbrAPI = Depends(getAmbrApi)):
    if ambrApi is None:
        raise HTTPException(status_code=503, detail="ambrApi is not initialized yet")

    try:
        return await ambrApi.fetch_artifact_set_detail(id)
    except:
        raise HTTPException(status_code=404, detail="artifactsets detail is not found")


@router.get("/artifactsets")
async def genArtifactSetList(ambrApi: AmbrAPI = Depends(getAmbrApi)):
    if ambrApi is None:
        raise HTTPException(status_code=503, detail="ambrApi is not initialized yet")
    setOptions = artifactData.artifactSetOptions
    ambrArtifactSets = await ambrApi.fetch_artifact_sets()

    return list(map(lambda set: {**vars(set), "options": setOptions.get(set.name, None)}, filter(lambda set: setOptions.get(set.name, None) != None, ambrArtifactSets)))


@router.get("/user/{uid}")
async def getUserData(uid: int, ambrApi: AmbrAPI = Depends(getAmbrApi)):
    if ambrApi is None:
        raise HTTPException(status_code=503, detail="ambrApi is not initialized yet")

    async with enka.GenshinClient(lang="ko") as client:
        await client.update_assets()
        rawRes = await client.fetch_showcase(uid, raw=True)
        characterInfoList = client.parse_showcase(rawRes).characters

        parsedCharacters = []
        for i, avatar in enumerate(characterInfoList):
            # 해당 위치에서 해야할 것 : front에서 사용 예정인 데이터 구조를 enka데이터를 통해 제작 후
            #                         draw에 필요한 데이터 및 최종 연산 결과를 리턴
            # draw 필요 데이터 : 이름, 레벨, icon, 성유물 정보, 운명의 자리, 스킬 정보, 무기 정보
            # 최종 연산 필요 데이터 : 이름, 레벨, ambrCharacterDetail, 성유물 정보, 운명의 자리, 스킬 정보, 무기 정보, 최종 연산 완료 후 fightProp

            if characterData.get(avatar.name):
                artifacts = avatar.artifacts
                weapon = avatar.weapon
                ambrCharacterDetail: CharacterDetail = await ambrApi.fetch_character_detail(str(avatar.id))
                # Draw를 위한 데이터 제작
                characterInfo = {
                    "id": avatar.id,
                    "name": avatar.name,
                    "element": avatar.element.value,
                    "level": avatar.level,
                    "moonsign": characterData[avatar.name].moonsign,
                    "ascension": avatar.ascension,
                    "icon": avatar.costume.icon if getattr(avatar, "costume", None) else avatar.icon,  # type: ignore
                    "weaponType": ambrCharacterDetail.weapon_type,
                    "weapon": {},
                    "artifact": {"parts": [], "setInfo": []},
                    "passiveSkill": [],
                    "activeSkill": [],
                    "constellations": [],
                    "totalStat": {},
                }

                # --------------------------- 스킬 및 운명의 자리 ---------------------------
                characterConstellation = characterData[avatar.name].constellation
                ambrConstellation: dict[str, Constellation] = {c.name: c for c in ambrCharacterDetail.constellations}
                enkaConstellation: dict[str, enka.gi.Constellation] = {c.name: c for c in avatar.constellations}
                characterPassive = characterData[avatar.name].passiveSkill
                characterActive = characterData[avatar.name].activeSkill
                defaultFalseConstellation = ["잿더미의 대가"]

                passive = list(filter(lambda talent: talent.type.name == "ULTIMATE" and characterPassive.get(talent.name), ambrCharacterDetail.talents))
                for i, skill in enumerate(passive):
                    skillOption = characterPassive.get(skill.name) or passiveSkillSchema(unlockLevel=1, description="")
                    unlocked = avatar.ascension >= skillOption.unlockLevel
                    characterInfo["passiveSkill"].append(
                        {
                            **skillOption.model_dump(),
                            "name": skill.name,
                            "icon": skill.icon,
                            "description": skill.description,
                            "unlocked": unlocked,
                            "unlockLevel": skillOption.unlockLevel,
                            "options": [
                                {**vars(option), "active": True if unlocked else False, "stack": option.maxStack, "select": option.selectList[0] if option.selectList else None}
                                for option in skillOption.options
                            ],
                        }
                    )
                for i, skillDetail in enumerate(ambrCharacterDetail.talents):
                    skill = next((t for t in avatar.talents if t.name == skillDetail.name), None)
                    if skill and skill.name in characterActive:
                        skillOption = characterActive.get(skill.name) or activeSkillSchema(description="")
                        characterInfo["activeSkill"].append(
                            {
                                **skillOption.model_dump(),
                                "name": skill.name,
                                "level": skill.level,
                                "icon": skill.icon,
                                "description": skillDetail.description,
                                "unlocked": unlocked,
                                "options": [
                                    {**vars(option), "active": True, "stack": option.maxStack if skillOption else 0, "select": option.selectList[0] if option.selectList else None}
                                    for option in skillOption.options
                                ],
                                "baseFightProp": skillOption.baseFightProp,
                            }
                        )

                for i, defaultConstellation in enumerate(characterConstellation):
                    name = defaultConstellation.name
                    characterInfo["constellations"].append(
                        {
                            **vars(defaultConstellation),
                            "icon": enkaConstellation[name].icon,
                            "unlocked": enkaConstellation[name].unlocked,
                            # "unlocked": False,  # 테스트를 위한 모든 캐릭터 명함 처리
                            # "unlocked": True,  # 테스트를 위한 모든 캐릭터 풀돌 처리
                            "description": ambrConstellation[name].description,
                            "options": [
                                {**vars(option), "active": True, "stack": option.maxStack, "select": option.selectList[0] if option.selectList else None}
                                for option in defaultConstellation.options
                            ],
                        }
                    )

                # ---------------------------------------------------------------------

                # --------------------------- 무기 ---------------------------
                characterInfo["weapon"] = {
                    "id": weapon.item_id,
                    "name": weapon.name,
                    "type": ambrCharacterDetail.weapon_type,
                    "refinement": weapon.refinement,
                    "level": weapon.level,
                    "icon": weapon.icon,
                    "options": [],
                    "stat": {stat.type.value: stat.value / 100 if stat.is_percentage else stat.value for stat in weapon.stats},
                }
                weaponOption = weaponData.weaponInfo.get(weapon.name)
                if weaponOption is not None:
                    for option in weaponOption:
                        characterInfo["weapon"]["options"].append(
                            {**vars(option), "active": True, "stack": option.maxStack, "select": option.selectList[0] if option.selectList else None}
                        )
                # ---------------------------------------------------------------------

                # -------------------------- 성유물 --------------------------
                for artifact in artifacts:
                    characterInfo["artifact"]["parts"].append(
                        {
                            "setName": artifact.set_name,
                            "type": artifact.equip_type.value,
                            "mainStat": {artifact.main_stat.type.value: artifact.main_stat.value / 100 if artifact.main_stat.is_percentage else artifact.main_stat.value},
                            "subStat": [{subStat.type.value: subStat.value / 100 if subStat.is_percentage else subStat.value} for subStat in artifact.sub_stats],
                            "icon": artifact.icon,
                        }
                    )
                artifactSetInfo = getArtifactSetInfo(characterInfo["artifact"]["parts"])
                for setInfo in artifactSetInfo:
                    options = setInfo.get("options") if setInfo.get("options") else []
                    characterInfo["artifact"]["setInfo"].append(
                        {
                            **setInfo,
                            "options": [
                                {**vars(option), "active": True, "stack": option.maxStack, "select": option.selectList[0] if option.selectList else None} for option in options
                            ],
                        }
                    )
                # ---------------------------------------------------------------------

                # 2. 최종 Fight Prop 데이터 계산
                getTotalFightProp = getFightProp.get(avatar.name)
                if getTotalFightProp is not None:
                    newFightProp = await getTotalFightProp(ambrCharacterDetail, requestCharacterInfoSchema(**characterInfo), enkaDataFlag=True)
                    characterInfo["activeSkill"] = [{**active, "level": newFightProp.characterInfo.activeSkill[i].level} for i, active in enumerate(characterInfo["activeSkill"])]

                    # 3. 최종 캐릭터 스텟 및 데미지 계산
                    damageCalculationResult = await damageCalculation(characterInfo=requestCharacterInfoSchema(**characterInfo), additionalFightProp=fightPropSchema())

                parsedCharacters.append(damageCalculationResult)
        return {"characters": parsedCharacters}


@router.post("/calculation")
async def calculation(characterInfo: requestCharacterInfoSchema, additionalFightProp: fightPropSchema, ambrApi: AmbrAPI = Depends(getAmbrApi)):
    if ambrApi is None:
        raise HTTPException(status_code=503, detail="ambrApi is not initialized yet")
    result = await damageCalculation(characterInfo=characterInfo, additionalFightProp=additionalFightProp)
    return result


@router.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

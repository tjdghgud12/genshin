from fastapi import APIRouter, HTTPException, Depends
from ambr import CharacterDetail, WeaponDetail, AmbrAPI, Talent, Constellation
import enka
from data.character import passiveSkill, activeSkill, constellation
import data.weapon as weaponInfo
from services.ambrApi import getAmbrApi
from services.character import getFightProp, CharacterInfo
from services.artifact import getArtifactSetInfo

router = APIRouter()

# 2025-07-23 기준(genshin impact 5.7)
# ambrCharacters = await ambrApi.fetch_characters() # 여행자 빼고 100개, 각 속성별 여행자 포함 시 106개
# ambrWeapons = await ambrApi.fetch_weapons() # 4성 이상은 186개, 1성 이상은 220개
# ambrArtifacts = await ambrApi.fetch_artifact_sets() # 55개


@router.get("/user/{uid}")
async def getUserData(uid: int, ambrApi: AmbrAPI = Depends(getAmbrApi)):
    if ambrApi is None:
        raise HTTPException(status_code=503, detail="ambrApi is not initialized yet")

    async with enka.GenshinClient(lang="ko") as client:
        rawRes = await client.fetch_showcase(uid, raw=True)
        characterInfoList = client.parse_showcase(rawRes).characters

        parsedCharacters = []
        for i, avatar in enumerate(characterInfoList):
            # 해당 위치에서 해야할 것 : front에서 사용 예정인 데이터 구조를 enka데이터를 통해 제작 후
            #                         draw에 필요한 데이터 및 최종 연산 결과를 리턴
            # draw 필요 데이터 : 이름, 레벨, icon, 성유물 정보, 운명의 자리, 스킬 정보, 무기 정보
            # 최종 연산 필요 데이터 : 이름, 레벨, ambrCharacterDetail, 성유물 정보, 운명의 자리, 스킬 정보, 무기 정보, 최종 연산 완료 후 fightProp

            artifacts = avatar.artifacts
            weapon = avatar.weapon
            ambrCharacterDetail: CharacterDetail = await ambrApi.fetch_character_detail(str(avatar.id))

            # Draw를 위한 데이터 제작
            characterInfo = {
                "name": avatar.name,
                "level": avatar.level,
                "ascension": avatar.ascension,
                "icon": avatar.costume.icon if getattr(avatar, "costume", None) else avatar.icon,  # type: ignore
                "weapon": {},
                "artifact": {"parts": [], "setInfo": []},
                "passiveSkill": [],
                "activeSkill": [],
                "constellations": [],
                "totalStat": {},
            }

            # --------------------------- 스킬 및 운명의 자리 ---------------------------
            characterConstellation = constellation.get(avatar.name, {})
            ambrConstellation: dict[str, Constellation] = {c.name: c for c in ambrCharacterDetail.constellations}
            enkaConstellation: dict[str, enka.gi.Constellation] = {c.name: c for c in avatar.constellations}
            characterPassive = passiveSkill.get(avatar.name, {})
            characterActive = activeSkill.get(avatar.name, {})
            defaultFalseConstellation = ["잿더미의 대가"]

            passive = list(filter(lambda talent: talent.type.name == "ULTIMATE" and characterPassive.get(talent.name), ambrCharacterDetail.talents))
            for i, skill in enumerate(passive):
                unlocked = avatar.ascension >= (1 if i == 0 else 4)
                skillOption = characterPassive.get(skill.name) or {}
                characterInfo["passiveSkill"].append(
                    {
                        **skillOption,
                        "name": skill.name,
                        "icon": skill.icon,
                        "description": skill.description,
                        "unlocked": unlocked,
                        "active": True if unlocked else False,
                        "stack": skillOption.get("maxStack"),
                    }
                )
            for i, skill in enumerate(avatar.talents):
                skillOption = characterActive.get(skill.name)
                skillDetail = next((t for t in ambrCharacterDetail.talents if t.name == skill.name), Talent)
                characterInfo["activeSkill"].append(
                    {
                        "name": skill.name,
                        "level": skill.level,
                        "type": skillOption.get("type") if skillOption else "always",
                        "icon": skill.icon,
                        "description": skillDetail.description,
                        "active": True,
                        "stack": skillOption.get("maxStack") if skillOption else 0,
                    }
                )

            for i, defaultConstellation in enumerate(characterConstellation):
                name = defaultConstellation["name"]
                characterInfo["constellations"].append(
                    {
                        **defaultConstellation,
                        "icon": enkaConstellation[name].icon,
                        "unlocked": enkaConstellation[name].unlocked,
                        "description": ambrConstellation[name].description,
                        "active": False if skill.name in defaultFalseConstellation else True,
                        "stack": defaultConstellation.get("maxStack"),
                    }
                )

            # ---------------------------------------------------------------------

            # --------------------------- 무기 ---------------------------
            characterInfo["weapon"] = {
                "id": weapon.item_id,
                "name": weapon.name,
                "refinement": weapon.refinement,
                "level": weapon.level,
                "icon": weapon.icon,
                "option": [],
                "stat": {stat.type.value: stat.value / 100 if stat.is_percentage else stat.value for stat in weapon.stats},
            }
            weaponOption = weaponInfo.weaponType.get(weapon.name)
            if weaponOption is not None:
                for option in weaponOption:
                    characterInfo["weapon"]["option"].append({**option, "active": True, "stack": option.get("maxStack")})
            # ---------------------------------------------------------------------

            # -------------------------- 성유물 --------------------------
            for artifact in artifacts:
                characterInfo["artifact"]["parts"].append(
                    {
                        "name": artifact.name,
                        "setName": artifact.set_name,
                        "id": artifact.id,
                        "type": artifact.equip_type.name,
                        "mainStat": {artifact.main_stat.type.value: artifact.main_stat.value / 100 if artifact.main_stat.is_percentage else artifact.main_stat.value},
                        "subStat": [{subStat.type.value: subStat.value / 100 if subStat.is_percentage else subStat.value} for subStat in artifact.sub_stats],
                        "icon": artifact.icon,
                    }
                )
            artifactSetInfo = getArtifactSetInfo(characterInfo["artifact"]["parts"])
            for setInfo in artifactSetInfo:
                options = setInfo.get("option") if setInfo.get("option") else []
                characterInfo["artifact"]["setInfo"].append({**setInfo, "option": [{**option, "active": True, "stack": option["maxStack"]} for option in options]})
                # ---------------------------------------------------------------------

                # 2. 최종 Fight Prop 데이터 계산
            getTotalFightProp = getFightProp.get(avatar.name)
            avatarRawData = rawRes["avatarInfoList"][i]
            if getTotalFightProp is not None:
                totalFightProp = await getTotalFightProp(ambrCharacterDetail, CharacterInfo(**characterInfo))

            # 3. 최종 캐릭터 스텟 및 데미지 계산

            parsedCharacters.append({"info": characterInfo, "result": {}})
        return {"characters": parsedCharacters}


@router.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

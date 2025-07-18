
from fastapi import APIRouter
import ambr
from services.parseEnka import parseFightProps
from data.globalVariable import characterStats
import enka
import data.weapon as weaponInfo

router = APIRouter()

ENKA_API_URL = "https://enka.network/api/uid/{uid}"  # uid는 유저 ID


@router.get("/user/{uid}")
async def getUserData(uid: int):
    async with enka.GenshinClient(lang='ko') as client:
        rawRes = await client.fetch_showcase(uid, raw=True)
        avatar_info_list = client.parse_showcase(rawRes).characters

        # 필요한 정보만 추출 예시
        parsed_avatars = []
        for i, avatar in enumerate(avatar_info_list):
            avatarRawData = rawRes['avatarInfoList'][i]
            name = avatar.name
            artifacts = avatar.artifacts
            weapon = avatar.weapon
            fightProps = parseFightProps(avatarRawData.get("fightPropMap"))
            characterInfo = {
                "name": name,
                "level": avatar.level,
                "icon": avatar.costume.icon if getattr(avatar, "costume", None) else avatar.icon,
                "baseStat":{**characterStats, **{key: value for key, value in fightProps.items() if "BASE" in key}},
                "weapon": {},
                "artifact": {},
                "activeSkill": {},
                "passiveSkill": {},
                "totalStat":{},
            }

            # ----------------------- 캐릭터 Base Stat 제작 -----------------------
            # 캐릭터 레벨에 따른 추가 stat 까지 적용
            async with ambr.AmbrAPI(lang=ambr.Language.KR) as ambrApi:
                ambrCharacterDetail = await ambrApi.fetch_character_detail(avatar.id)
            promoteStat = max(
                (promote for promote in ambrCharacterDetail.upgrade.promotes 
                if promote.unlock_max_level <= int(characterInfo["level"])),
                key=lambda x: x.unlock_max_level,
                default=0
            )
            if promoteStat:
                for addStat in promoteStat.add_stats:
                    if addStat.id == ambrCharacterDetail.special_stat.value:
                        characterInfo["baseStat"][addStat.id] += addStat.value
            # ---------------------------------------------------------------------

            # --------------------------- 무기 stat 제작 ---------------------------
            # 여기서 무기
            # 주옵, 부옵 적용. 무기 옵션은 front에서 on/off 적용
            # 1. 주옵 부옵은 그냥 연산 진행
            # 2. 무기 옵션의 경우 함수 리턴 불가능이기 때문에 type만 지정해서 넘기고, front에서는 on/off or stack값만 넘겨서 back에서 연산 진행
            # 즉, 무기별 각 옵션은 back에서 보관.
            # front는 사용자 설정값만 받아서 back로 이동 시키기
            # 1. 무기 옵션은 일단 오늘은 불가능. 무기별로 전부 함수 별도로 만들어야 하기 때문에
            # 2. 주옵 부옵만 적용하기
            # 무기에 담아야 하는 값: name, refinement(재련), stat
            characterInfo['weapon']['name'] = weapon.name
            characterInfo['weapon']['refinement'] = weapon.refinement
            characterInfo['weapon']['level'] = weapon.level
            characterInfo['weapon']['icon'] = weapon.icon
            characterInfo['weapon']['option'] = weaponInfo.weaponType[weapon.name] if getattr(weaponInfo.weaponType, weapon.name, None) else []
            characterInfo['weapon']['stat'] = {}
            for stat in weapon.stats:
                characterInfo['weapon']['stat'][stat.type.value] = stat.value

            # 이제 각 무기별 option에 대한 리턴값은 별도로 보관하는게 좋겠다.
            # 1차적으로 무기 옵션의 type 지정 완료
            # ---------------------------------------------------------------------

            # -------------------------- 성유물 stat 제작 --------------------------
            # 여기서 성유물
            # 주옵, 부옵 적용. 셋옵 중 조건없이 스텟 증가하는 경우는 적용. 아닌 경우는 front에서 on/off 적용
            # 여기서 담아야 하는 항목들 : 주옵, 부옵
            # ---------------------------------------------------------------------

            # --------------------------- 스킬 stat 제작 ---------------------------
            # 여기서 스킬(패시브 액티브 on/off에 따라 적용 해야함)
            # 음...이건 애매하네??? 깡 스텟이 증가하는 경우가 있단말이지?
            # 액티브의 경우 무조건 front에서 on/off 적용
            # 패시브의 경우 조건없이 스텟 증가할 경우 적용. 아닌 경우는 front에서 on/off 적용
            # ---------------------------------------------------------------------

            
            parsed_avatars.append(characterInfo)
        return {"avatars": parsed_avatars}

@router.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

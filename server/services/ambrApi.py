import ambr
from ambr import Language

ambrApi = None


async def initAmbrApi():
    global ambrApi
    from data import character
    from data import weapon

    if ambrApi is None:
        ambrApi = ambr.AmbrAPI(lang=Language.KR)
        await ambrApi.start()
        character.ambrCharacterCurve = await ambrApi.fetch_avatar_curve()
        weapon.ambrWeaponCurve = await ambrApi.fetch_weapon_curve()
    return ambrApi


async def closeAmbrApi():
    global ambrApi
    from data import character
    from data import weapon

    if ambrApi is not None:
        await ambrApi.close()
        ambrApi = None
        character.ambrCharacterCurve = {}
        weapon.ambrWeaponCurve = {}


async def getAmbrApi():
    if ambrApi is None:
        raise RuntimeError("ambrApi is not initialized yet")
    return ambrApi

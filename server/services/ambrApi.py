import ambr
from ambr import Language

ambrApi = None


async def initAmbrApi():
    global ambrApi
    from data import globalVariable

    if ambrApi is None:
        ambrApi = ambr.AmbrAPI(lang=Language.KR)
        await ambrApi.start()
        globalVariable.ambrCharacterCurve = await ambrApi.fetch_avatar_curve()
    return ambrApi


async def closeAmbrApi():
    global ambrApi
    from data import globalVariable

    if ambrApi is not None:
        await ambrApi.close()
        ambrApi = None
        globalVariable.ambrCharacterCurve = None


async def getAmbrApi():
    if ambrApi is None:
        raise RuntimeError("ambrApi is not initialized yet")
    return ambrApi

from .mondstadt import info as mondstadtInfo
from .liyue import info as liyueInfo
from .inazuma import info as inazumaInfo
from .sumeru import info as sumeruInfo
from .fontaine import info as fontaineInfo
from .natlan import info as natlanInfo
from .omniScourge import info as omniScourgeInfo
from schemas.fightProp import fightPropSchema


ambrCharacterCurve: dict[str, dict] = {}
fightPropTemplate = fightPropSchema()

characterData = {
    **mondstadtInfo,
    **liyueInfo,
    **inazumaInfo,
    **sumeruInfo,
    **fontaineInfo,
    **natlanInfo,
    **omniScourgeInfo,
}

__all__ = ["characterData", "ambrCharacterCurve", "fightPropTemplate"]

from .mondstadt import getFightProp as mondstadtGetFightProp
from .liyue import getFightProp as liyueGetFightProp
from .inazuma import getFightProp as inazumaGetFightProp
from .sumeru import getFightProp as sumeruGetFightProp
from .fontaine import getFightProp as fontaineGetFightProp
from .natlan import getFightProp as natlanGetFightProp
from .omniScourge import getFightProp as omniScourgeGetFightProp
from .snezhnaya import getFightProp as snezhnayaGetFightProp

getFightProp = {
    **mondstadtGetFightProp,
    **liyueGetFightProp,
    **inazumaGetFightProp,
    **sumeruGetFightProp,
    **fontaineGetFightProp,
    **natlanGetFightProp,
    **omniScourgeGetFightProp,
    **snezhnayaGetFightProp,
}

__all__ = ["getFightProp"]

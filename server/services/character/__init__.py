from .mondstadt import getFightProp as mondstadtGetFightProp
from .liyue import getFightProp as liyueGetFightProp
from .inazuma import getFightProp as inazumaGetFightProp
from .sumeru import getFightProp as sumeruGetFightProp
from .fontaine import getFightProp as fontaineGetFightProp
from .natlan import getFightProp as natlanGetFightProp
from .omniScourge import getFightProp as omniScourgeGetFightProp

getFightProp = {
    **mondstadtGetFightProp,
    **liyueGetFightProp,
    **inazumaGetFightProp,
    **sumeruGetFightProp,
    **fontaineGetFightProp,
    **natlanGetFightProp,
    **omniScourgeGetFightProp,
}

__all__ = ["getFightProp"]

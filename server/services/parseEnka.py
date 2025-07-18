from data.globalVariable import fightPropMap


def parseFightProps(characterFightPropMap: dict):
    stats = {}
    for id, value in characterFightPropMap.items():
        name = fightPropMap.get(id, f"Unknown({id})")
        if("Unknown" not in name):
            stats[name] = value
    return stats



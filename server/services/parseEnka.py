from data.globalVariable import enkaFightPropMap


def parseFightProps(characterFightPropMap: dict):
    stats = {}
    for id, value in characterFightPropMap.items():
        name = enkaFightPropMap.get(id, f"Unknown({id})")
        if "Unknown" not in name:
            stats[name] = value
    return stats

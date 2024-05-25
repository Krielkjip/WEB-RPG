def collect_resource(interact, player_state, region_map):
    if interact == "Cut Tree":
        player_state["inventory"]["logs_amount"] += 1
        region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Grass"
    elif interact == "Mine Rock":
        player_state["inventory"]["rocks_amount"] += 1
        region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Dirt"
    return player_state, region_map

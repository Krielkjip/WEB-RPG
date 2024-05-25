def collect_resource(interact, player_state, region_map):
    message = ""
    fail_message = ""

    if interact == "Cut Tree":
        if player_state["inventory"]["stone_axe_uses"] > 0:
            player_state["inventory"]["logs_amount"] += 2
            player_state["inventory"]["stone_axe_uses"] -= 1
            region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Grass"
            message = "You have cut the tree and got 2 logs, you lost 1 stone axe use"
        elif player_state["inventory"]["wooden_axe_uses"] > 0:
            player_state["inventory"]["logs_amount"] += 1
            player_state["inventory"]["wooden_axe_uses"] -= 1
            region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Grass"
            message = "You have cut the tree and got 1 log, you lost 1 wooden axe use"
        else:
            fail_message = "You don't have an axe use left"

    elif interact == "Mine Rock":
        if player_state["inventory"]["stone_pickaxe_uses"] > 0:
            player_state["inventory"]["rocks_amount"] += 2
            player_state["inventory"]["stone_pickaxe_uses"] -= 1
            region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Dirt"
            message = "You have mined the rock and got 2 rocks, you lost 1 stone pickaxe use"
        elif player_state["inventory"]["wooden_pickaxe_uses"] > 0:
            player_state["inventory"]["rocks_amount"] += 1
            player_state["inventory"]["wooden_pickaxe_uses"] -= 1
            region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Dirt"
            message = "You have mined the rock and got 1 rock, you lost 1 wooden pickaxe use"
        else:
            fail_message = "You don't have a pickaxe use left"

    return player_state, region_map, message, fail_message

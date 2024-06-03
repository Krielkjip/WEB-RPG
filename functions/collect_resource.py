def collect_resource(interact, player_state, region_map):
    """
    Handles resource collection (e.g. cutting trees, mining rocks) based on player's inventory and location.

    Args:
        interact (str): The type of interaction (e.g. "Cut Tree", "Mine Rock")
        player_state (dict): The player's current state (inventory, location, etc.)
        region_map (list of lists): The game world's region map

    Returns:
        tuple: (updated player_state, updated region_map, success message, failure message)
    """
    message = ""
    fail_message = ""

    # Handle tree cutting
    if interact == "Cut Tree":
        # Check if player has a stone axe with uses left
        if player_state["inventory"]["stone_axe_uses"] > 0:
            # Cut the tree, gain 2 logs, and lose 1 stone axe use
            player_state["inventory"]["logs_amount"] += 2
            player_state["inventory"]["stone_axe_uses"] -= 1
            region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Grass"
            message = "You have cut the tree and got 2 logs, you lost 1 stone axe use"
        # Check if player has a wooden axe with uses left
        elif player_state["inventory"]["wooden_axe_uses"] > 0:
            # Cut the tree, gain 1 log, and lose 1 wooden axe use
            player_state["inventory"]["logs_amount"] += 1
            player_state["inventory"]["wooden_axe_uses"] -= 1
            region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Grass"
            message = "You have cut the tree and got 1 log, you lost 1 wooden axe use"
        else:
            # No axe uses left, fail to cut tree
            fail_message = "You don't have an axe use left"

    # Handle rock mining
    elif interact == "Mine Rock":
        # Check if player has a stone pickaxe with uses left
        if player_state["inventory"]["stone_pickaxe_uses"] > 0:
            # Mine the rock, gain 2 rocks, and lose 1 stone pickaxe use
            player_state["inventory"]["rocks_amount"] += 2
            player_state["inventory"]["stone_pickaxe_uses"] -= 1
            region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Dirt"
            message = "You have mined the rock and got 2 rocks, you lost 1 stone pickaxe use"
        # Check if player has a wooden pickaxe with uses left
        elif player_state["inventory"]["wooden_pickaxe_uses"] > 0:
            # Mine the rock, gain 1 rock, and lose 1 wooden pickaxe use
            player_state["inventory"]["rocks_amount"] += 1
            player_state["inventory"]["wooden_pickaxe_uses"] -= 1
            region_map[player_state["region_location"][1]][player_state["region_location"][0]] = "Dirt"
            message = "You have mined the rock and got 1 rock, you lost 1 wooden pickaxe use"
        else:
            # No pickaxe uses left, fail to mine rock
            fail_message = "You don't have a pickaxe use left"

    return player_state, region_map, message, fail_message

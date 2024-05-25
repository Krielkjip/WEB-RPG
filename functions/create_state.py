def create_player_state():
    return {"location": [0, 0], "region_location": [0, 0],
            "inventory": {"logs_amount": 100, "rocks_amount": 100, "planks_amount": 0, "sticks_amount": 0,
                          "wooden_pickaxe_uses": 10, "wooden_axe_uses": 10, "stone_pickaxe_uses": 0,
                          "stone_axe_uses": 0}}


def create_map():
    return {"world_map": [], "region_map": {}}

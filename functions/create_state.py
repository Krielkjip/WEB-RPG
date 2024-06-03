def create_player_state():
    """
    Creates a new player state with default values.

    Returns:
        dict: The initial player state
    """
    return {
        "location": [0, 0],  # Initial location (x, y) coordinates
        "region_location": [0, 0],  # Initial region location (x, y) coordinates
        "inventory": {
            "logs_amount": 100,  # Initial logs amount
            "rocks_amount": 100,  # Initial rocks amount
            "planks_amount": 0,  # Initial planks amount
            "sticks_amount": 0,  # Initial sticks amount
            "wooden_pickaxe_uses": 10,  # Initial wooden pickaxe uses
            "wooden_axe_uses": 10,  # Initial wooden axe uses
            "stone_pickaxe_uses": 0,  # Initial stone pickaxe uses
            "stone_axe_uses": 0  # Initial stone axe uses
        }
    }


def create_map():
    """
    Creates a new game map with default values.

    Returns:
        dict: The initial game map
    """
    return {
        "world_map": [],  # The overall world map (empty at start)
        "region_map": {}  # The current region map (empty at start)
    }

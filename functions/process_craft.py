def process_craft(craft, player_state):
    """
    Process a crafting command and update the player's inventory accordingly.

    Args:
        craft (str): The crafting command (e.g. "craft planks")
        player_state (dict): The current player state

    Returns:
        player_state (dict): The updated player state
        message (str): A success message if the craft was successful
        fail_message (str): An error message if the craft failed
    """
    print(craft)
    # Convert the craft command to lowercase and strip any whitespace
    craft = craft.lower()
    # Remove the "craft " prefix from the command
    craft = craft[6:]
    print(craft)

    # Initialize success and failure messages
    message = ""
    fail_message = ""

    # Handle different crafting commands
    if craft == "planks":
        # Check if the player has enough logs to craft planks
        if player_state["inventory"]["logs_amount"] > 0:
            # Consume a log and add 4 planks to the inventory
            player_state["inventory"]["logs_amount"] -= 1
            player_state["inventory"]["planks_amount"] += 4
            message = "You crafted 4 planks"
        else:
            fail_message = "You didn't have a log to craft planks"

    elif craft == "sticks":
        # Check if the player has enough planks to craft sticks
        if player_state["inventory"]["planks_amount"] > 1:
            # Consume 2 planks and add 4 sticks to the inventory
            player_state["inventory"]["planks_amount"] -= 2
            player_state["inventory"]["sticks_amount"] += 4
            message = "You crafted 4 sticks"
        else:
            fail_message = "You didn't have planks to craft sticks"

    elif craft == "wooden pickaxe uses":
        # Check if the player has enough planks and sticks to craft a wooden pickaxe
        has_enough_planks = player_state["inventory"]["planks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_planks and has_enough_sticks:
            # Consume 3 planks and 2 sticks, and add 10 wooden pickaxe uses to the inventory
            player_state["inventory"]["planks_amount"] -= 3
            player_state["inventory"]["sticks_amount"] -= 2
            player_state["inventory"]["wooden_pickaxe_uses"] += 10
            message = "You crafted 10 wooden pickaxe uses"
        elif not has_enough_planks and not has_enough_sticks:
            fail_message = "You didn't have enough planks and sticks to craft a wooden pickaxe"
        elif not has_enough_planks:
            fail_message = "You didn't have enough planks to craft a wooden pickaxe"
        elif not has_enough_sticks:
            fail_message = "You didn't have enough sticks to craft a wooden pickaxe"

    elif craft == "wooden axe uses":
        # Check if the player has enough planks and sticks to craft a wooden axe
        has_enough_planks = player_state["inventory"]["planks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_planks and has_enough_sticks:
            # Consume 3 planks and 2 sticks, and add 10 wooden axe uses to the inventory
            player_state["inventory"]["planks_amount"] -= 3
            player_state["inventory"]["sticks_amount"] -= 2
            player_state["inventory"]["wooden_axe_uses"] += 10
            message = "You crafted 10 wooden axe uses"
        elif not has_enough_planks and not has_enough_sticks:
            fail_message = "You didn't have enough planks and sticks to craft a wooden axe"
        elif not has_enough_planks:
            fail_message = "You didn't have enough planks to craft a wooden axe"
        elif not has_enough_sticks:
            fail_message = "You didn't have enough sticks to craft a wooden axe"

    elif craft == "stone pickaxe uses":
        # Check if the player has enough rocks and sticks to craft a stone pickaxe
        has_enough_rocks = player_state["inventory"]["rocks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_rocks and has_enough_sticks:
            # Consume 3 rocks and 2 sticks, and add 20 stone pickaxe uses to the inventory
            player_state["inventory"]["rocks_amount"] -= 3
            player_state["inventory"]["sticks_amount"] -= 2
            player_state["inventory"]["stone_pickaxe_uses"] += 20
            message = "You crafted 20 stone pickaxe uses"
        elif not has_enough_rocks and not has_enough_sticks:
            fail_message = "You didn't have enough rocks and sticks to craft a stone pickaxe"
        elif not has_enough_rocks:
            fail_message = "You didn't have enough rocks to craft a stone pickaxe"
        elif not has_enough_sticks:
            fail_message = "You didn't have enough sticks to craft a stone pickaxe"

    elif craft == "stone axe uses":
        # Check if the player has enough rocks and sticks to craft a stone axe
        has_enough_rocks = player_state["inventory"]["rocks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_rocks and has_enough_sticks:
            # Consume 3 rocks and 2 sticks, and add 20 stone axe uses to the inventory
            player_state["inventory"]["rocks_amount"] -= 3
            player_state["inventory"]["sticks_amount"] -= 2
            player_state["inventory"]["stone_axe_uses"] += 20
            message = "You crafted 20 stone axe uses"
        elif not has_enough_rocks and not has_enough_sticks:
            fail_message = "You didn't have enough rocks and sticks to craft a stone axe"
        elif not has_enough_rocks:
            fail_message = "You didn't have enough rocks to craft a stone axe"
        elif not has_enough_sticks:
            fail_message = "You didn't have enough sticks to craft a stone axe"

    return player_state, message, fail_message

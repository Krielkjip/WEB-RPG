def process_craft(craft, player_state):
    print(craft)
    craft = craft.lower()
    craft = craft[6:]
    message = ""
    fail_message = ""
    print(craft)

    if craft == "planks":
        if player_state["inventory"]["logs_amount"] > 0:
            player_state["inventory"]["logs_amount"] -= 1
            player_state["inventory"]["planks_amount"] += 4
            message = "You crafted 4 planks"
        else:
            fail_message = "You didn't have a log to craft planks"

    elif craft == "sticks":
        if player_state["inventory"]["planks_amount"] > 1:
            player_state["inventory"]["planks_amount"] -= 2
            player_state["inventory"]["sticks_amount"] += 4
            message = "You crafted 4 sticks"
        else:
            fail_message = "You didn't have planks to craft sticks"

    elif craft == "wooden pickaxe uses":
        has_enough_planks = player_state["inventory"]["planks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_planks and has_enough_sticks:
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
        has_enough_planks = player_state["inventory"]["planks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_planks and has_enough_sticks:
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
        has_enough_rocks = player_state["inventory"]["rocks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_rocks and has_enough_sticks:
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
        has_enough_rocks = player_state["inventory"]["rocks_amount"] > 2
        has_enough_sticks = player_state["inventory"]["sticks_amount"] > 1

        if has_enough_rocks and has_enough_sticks:
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

from .tile_text import get_tile_text
from region_map_gen import run_region_gen
from .move import move_player, move_mobs
from .collect_resource import collect_resource


def process_interact(interact, region_map_size, map_size, region_map, map, player_state, mobs_data):
    message = ""
    fail_message = ""
    current_biome = map["world_map"][player_state["location"][0]][player_state["location"][1]]
    biome_data = get_tile_text(current_biome)
    print(biome_data)
    print(interact)
    print(player_state["location"])
    if interact == "Interact Get Region":
        try:
            region_map = map["region_map"][f"{player_state['location'][0]}_{player_state['location'][1]}"]
        except KeyError:
            current_biome = map["world_map"][player_state["location"][0]][player_state["location"][1]]
            region_map = run_region_gen(region_map_size, region_map_size, current_biome)
            # map["region_map"][f"{player_state["location"][0]}_{player_state["location"][1]}"] = region_map

        # print(region_map)
        # region_map = run_region_gen(region_map_size, region_map_size, current_biome)
        # print("Gen Region Map")
        player_state["region_location"] = [0, 0]
    elif interact[:4].lower() == "move":
        player_state, world_change = move_player(interact, map_size, region_map_size, player_state, "Region")
        if world_change:
            try:
                current_biome = map["world_map"][player_state["location"][0]][player_state["location"][1]]
                biome_data = get_tile_text(current_biome)
                region_map = map["region_map"][f"{player_state['location'][0]}_{player_state['location'][1]}"]
            except KeyError:
                current_biome = map["world_map"][player_state["location"][0]][player_state["location"][1]]
                biome_data = get_tile_text(current_biome)
                region_map = run_region_gen(region_map_size, region_map_size, current_biome)
        mobs_data = move_mobs(mobs_data, region_map_size, map_size)
    else:
        player_state, region_map, message, fail_message = collect_resource(interact, player_state, region_map)
    map["region_map"][f"{player_state['location'][0]}_{player_state['location'][1]}"] = region_map
    # make writable map
    writable_map = []
    for y in range(len(region_map)):
        writable_map_row = []
        for x in range(len(region_map[y])):
            tile = region_map[y][x]
            mob = False
            # print(mobs_data)
            for item in mobs_data:
                data = mobs_data[item]
                if data["location"][0] == player_state["location"][0] and data["location"][1] == \
                        player_state["location"][1]:
                    if data["region_location"][0] == x and data["region_location"][1] == y:
                        # print(data)
                        mob = True
                        mob_name = data["name"]
                        break
            if mob:
                writable_map_row.append([tile, True, mob_name])
            else:
                writable_map_row.append([tile, False, None])
        writable_map.append(writable_map_row)
    # print(writable_map)

    return writable_map, region_map, player_state, biome_data, message, fail_message

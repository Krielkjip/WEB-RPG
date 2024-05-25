import random
import json
from pathlib import Path


def generate_terrain(height, width, biome):
    file_path = Path(__file__).absolute().parent
    with open(file_path / "region_gen_data.json", 'r') as json_file:
        data = json.load(json_file)
        terrain_weights = data[biome]

    terrain_types = list(terrain_weights.keys())
    weighted_terrain = []
    for x in range(width):
        row = []
        for y in range(height):
            row.append(random.choices(terrain_types, weights=list(terrain_weights.values()))[0])
        weighted_terrain.append(row)
    return weighted_terrain


region_characters = {
    "Tree": "T",
    "Grass": "G",
    "Pebble": "P",
    "Flower": "F",
    "Bush": "B",
    "Water": "~",
    "Rock": "R",
    "Moss": "M",
    "Dead Tree": "T",
    "Fungi Tree": "T",
    "Fungi": "F",
    "Iron Ore": "I",
    "Snow": "S",
    "Deep Snow": "D",
    "Ice": "I",
    "Sandstone": "S",
    "Sand": "~",
    "Cactus": "C",
    "Empty": "#",
    "Coal Ore": "C",
    "Mud": "M",
    "Dead Bush": "B",
    "Magma": "~",
    "Ash": "~",
    "Ash Rock": "A",
    "Sulfur": "S"
}


def count(neighbors, what_region):
    return sum(1 for neighbor in neighbors if neighbor == what_region)


def check_modify_region(new_region, neighbors):
    biome_count = count(neighbors, new_region)
    if biome_count > 0:
        probability = 100
        random_number = random.randint(1, 100)
        if random_number <= probability:
            return True


def modify_terrain(terrain_grid, height, width, biome):
    file_path = Path(__file__).absolute().parent
    with open(file_path / "region_gen_data.json", 'r') as json_file:
        data = json.load(json_file)
    for x in range(width):
        for y in range(height):
            current_region = terrain_grid[x][y]
            regions = data["Regions in Biomes"][biome]
            neighbors = [
                terrain_grid[(x + 1) % width][y],
                terrain_grid[(x - 1) % width][y],
                terrain_grid[x][(y + 1) % height],
                terrain_grid[x][(y - 1) % height]
            ]

            # Check conditions for each biome
            num_regions = len(regions)
            for i, region in enumerate(regions):
                if current_region == region:
                    new_region_index = (i + 1) % num_regions
                    new_region = regions[new_region_index]
                    if check_modify_region(new_region, neighbors):
                        terrain_grid[x][y] = new_region
                    break


# Main function to generate region
def main(height, width, biome):
    terrain_grid = generate_terrain(height, width, biome)
    # display_terrain(terrain_grid, height, width)
    # print(" ")
    for x in range(1):
        modify_terrain(terrain_grid, height, width, biome)
        # print("\nTerrain Map after Modification:")
        # display_terrain(terrain_grid, height, width)
        # print(" ")
        # print("\nTerrain Map as a List:")

    return terrain_grid


def run_region_gen(height, width, biome):
    # print(biome)
    region_map = main(height, width, biome)
    # print(region_map)
    return region_map

# run_region_gen(8, 8, "Volcano")
# input("Press any key to exit...")

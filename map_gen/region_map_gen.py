import random
import json
from pathlib import Path


# Function to generate a 2D grid of terrain types based on biome data
def generate_terrain(height, width, biome):
    """
    Generates a 2D grid of terrain types based on biome data.

    Args:
        height (int): The height of the grid.
        width (int): The width of the grid.
        biome (str): The biome type.

    Returns:
        list: A 2D list of terrain types.
    """
    # Get the file path of the current script
    file_path = Path(__file__).absolute().parent

    # Load the biome data from a JSON file
    with open(file_path / "region_gen_data.json", 'r') as json_file:
        data = json.load(json_file)
        # Get the terrain weights for the specified biome
        terrain_weights = data[biome]

    # Get the list of terrain types and their corresponding weights
    terrain_types = list(terrain_weights.keys())
    weighted_terrain = []
    for x in range(width):
        row = []
        for y in range(height):
            # Randomly select a terrain type based on the weights
            row.append(random.choices(terrain_types, weights=list(terrain_weights.values()))[0])
        weighted_terrain.append(row)
    return weighted_terrain


# Function to count the number of neighbors that match a certain region
def count(neighbors, what_region):
    """
    Counts the number of neighbors that match a certain region.

    Args:
        neighbors (list): A list of neighboring regions.
        what_region (str): The region to count.

    Returns:
        int: The count of neighboring regions that match what_region.
    """
    return sum(1 for neighbor in neighbors if neighbor == what_region)


# Function to check if a region should be modified based on its neighbors
def check_modify_region(new_region, neighbors):
    """
    Checks if a region should be modified based on its neighbors.

    Args:
        new_region (str): The new region to check.
        neighbors (list): A list of neighboring regions.

    Returns:
        bool: True if the region should be modified, False otherwise.
    """
    # Count the number of neighbors that match the new region
    biome_count = count(neighbors, new_region)
    # If the count is greater than 0, there's a chance to modify the region
    if biome_count > 0:
        # Set a probability for modification (e.g. 10%)
        probability = 10
        # Generate a random number between 1 and 100
        random_number = random.randint(1, 100)
        # If the random number is less than the probability, modify the region
        if random_number <= probability:
            return True
    return False


# Function to modify the terrain grid based on biome data
def modify_terrain(terrain_grid, height, width, biome):
    """
    Modifies the terrain grid based on biome data.

    Args:
        terrain_grid (list): The 2D list of terrain types.
        height (int): The height of the grid.
        width (int): The width of the grid.
        biome (str): The biome type.
    """
    file_path = Path(__file__).absolute().parent
    with open(file_path / "region_gen_data.json", 'r') as json_file:
        data = json.load(json_file)
    for x in range(width):
        for y in range(height):
            # Get the current region
            current_region = terrain_grid[x][y]
            # Get the list of regions in the biome
            regions = data["Regions in Biomes"][biome]
            # Get the neighboring regions
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
                    # Get the index of the current region in the list
                    new_region_index = (i + 1) % num_regions
                    new_region = regions[new_region_index]
                    # Check if the region should be modified based on its neighbors
                    if check_modify_region(new_region, neighbors):
                        # Modify the region
                        terrain_grid[x][y] = new_region
                    break


# Main function to generate a region
def main(height, width, biome):
    """
    Generates a region.

    Args:
        height (int): The height of the grid.
        width (int): The width of the grid.
        biome (str): The biome type.

    Returns:
        list: The modified terrain grid.
    """
    # Generate the terrain grid
    terrain_grid = generate_terrain(height, width, biome)
    # Modify the terrain grid
    for x in range(1):
        modify_terrain(terrain_grid, height, width, biome)
    return terrain_grid


# Run the region generation function
def run_region_gen(height, width, biome):
    """
    Runs the region generation function.

    Args:
        height (int): The height of the grid.
        width (int): The width of the grid.
        biome (str): The biome type.

    Returns:
        list: The modified terrain grid.
    """
    region_map = main(height, width, biome)
    return region_map

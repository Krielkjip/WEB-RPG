import gc
import os
import shutil
import tempfile
from typing import Annotated
import json
from pathlib import Path
from world_map_gen import run_world_gen
import time

import uvicorn
from fastapi import FastAPI, Request, Response, UploadFile, File, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from starlette.responses import HTMLResponse

map_size = 16
player_state = [0, 0]
map = []
last_interaction = 0

# Get the directory of the current Python script
current_dir = Path(__file__).resolve().parent

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

app.mount("/statics", StaticFiles(directory="statics"), name="statics")


def save_game(command, map, player_state):
    file_location = "save_data/" + command[5:] + ".json"
    with open(file_location, 'w') as json_file:
        json.dump([map, player_state], json_file)
        print("SAVED DATA")


def load_game(command, map, player_state):
    if command == "load current":
        return map, player_state
    elif command == "load fresh":
        map = run_world_gen(map_size, map_size)
        player_state = [0, 0]
        return map, player_state
    else:
        file_location = "save_data/" + command[5:]
        with open(file_location, 'r') as json_file:
            data = json.load(json_file)
            map = data[0]
            player_state = data[1]
            return map, player_state


def process_command(command, map, player_state):
    if command[:4].lower() == "save":
        save_game(command, map, player_state)
        print("Saving")
    elif command[:4].lower() == "load":
        map, player_state = load_game(command, map, player_state)
        print("Loading")
    move_player(command.lower())
    state = {"command_len": len(command)}
    if command == "":
        state['error_msg'] = "Please enter a command"
    state['command'] = command
    print(state)
    return state, map, player_state


def move_player(move):
    if move == "down":
        print("Moving down")
        if player_state[1] < map_size - 1:
            player_state[1] += 1
    elif move == "up":
        print("Moving up")
        if player_state[1] > 0:
            player_state[1] -= 1
    elif move == "right":
        print("Moving right")
        if player_state[0] < map_size - 1:
            player_state[0] += 1
    elif move == "left":
        print("Moving left")
        if player_state[0] > 0:
            player_state[0] -= 1


def get_tile_text(current_tile):
    biome_descriptions = {
        "Taiga Forest": ["Taiga Forest", "You are in a Taiga Forest",
                         "A vast expanse of cold coniferous forest, primarily spruce, fir, and pine, blanketed in snow with frozen lakes and occasional clearings. Home to wolves, foxes, and polar bears adapted to the harsh northern wilderness.",
                         ["Wolves", "Foxes", "Polar Bears"],
                         ["Tree", "Grass"]],
        "Taiga": ["Taiga", "You are in a Taiga",
                  "A cold, snowy landscape dotted with coniferous trees like spruce, fir, and pine. The ground is often covered in snow, with occasional clearings and frozen lakes.",
                  ["Wolves", "Foxes", "Polar Bears"],
                  ["Tree", "Grass"]],
        "Rainforest": ["Rainforest", "You are in a Rainforest",
                       "Lush and dense vegetation with towering trees, vibrant foliage, and a diverse array of wildlife. The air is humid, and sunlight filters through the thick canopy, creating dappled shadows on the forest floor.",
                       ["Jaguars", "Toucans", "Anacondas"],
                       ["Tree", "Grass"]],
        "Grassland": ["Grassland", "You are in the Grasslands",
                      "Wide expanses of rolling grasses, occasionally interspersed with low shrubs and scattered trees. The terrain is relatively flat, with open skies and a sense of vastness.",
                      ["Bison", "Lions", "Hawks"],
                      ["Grass"]],
        "Mountain": ["Mountain", "You are on a Mountain",
                     "Towering peaks, rocky slopes, and rugged terrain. Snow-capped summits, deep valleys, and alpine meadows characterize this biome, with breathtaking views and challenging landscapes.",
                     ["Mountain Goats", "Eagles", "Snow Leopards"],
                     ["Rock", "Snow"]],
        "Forest": ["Forest", "You are in a Forest",
                   "Dense growth of trees, both deciduous and coniferous, with a rich underbrush of shrubs, ferns, and mosses. Sunlight filters through the canopy, casting a greenish hue on the forest floor.",
                   ["Deer", "Bears", "Wolves"],
                   ["Tree", "Grass"]],
        "Volcano": ["Volcano", "You are inside a Volcano",
                    "A dramatic landscape dominated by the presence of a volcano, with steaming vents, rugged lava fields, and occasional eruptions. The air is often filled with ash and the ground may be hot to the touch in some areas.",
                    ["Fire Elementals", "Lava Slimes", "Magma Golems"],
                    ["Lava"]],
        "Desert": ["Desert", "You are in a Desert",
                   "Arid expanses of sand dunes, rocky outcrops, and sparse vegetation adapted to extreme dryness. The landscape is characterized by intense sunlight, high temperatures during the day, and cold nights.",
                   ["Scorpions", "Vultures", "Camels"],
                   ["Sand"]],
        "Ocean": ["Ocean", "You are in a Ocean",
                  "Vast stretches of open water, with varying depths, currents, and marine life. Waves crash against rocky cliffs or gently lap against sandy shores, while seabirds soar overhead and marine mammals swim beneath the surface.",
                  ["Sharks", "Dolphins", "Sea Turtles"],
                  ["Water"]],
        "Temperate Forest": ["Temperate Forest", "You are in a Temperate Forest",
                             "Similar to a forest biome but with a more moderate climate, characterized by a mix of deciduous and evergreen trees. The ground may be covered in a carpet of fallen leaves, and there are clear seasonal changes in foliage color.",
                             ["Squirrels", "Owls", "Raccoons"],
                             ["Tree"]],
        "Tundra": ["Tundra", "You are in a Tundra",
                   "A cold and treeless biome with vast expanses of low-lying vegetation, such as mosses, lichens, and hardy grasses. Permafrost underlies much of the landscape, and there are few trees due to the harsh conditions.",
                   ["Polar Bears", "Arctic Foxes", "Caribou"],
                   ["Snow"]],
        "Savanna": ["Savanna", "You are in a Savanna",
                    "Open grasslands dotted with scattered trees and shrubs, characterized by a dry climate with seasonal rainfall. The landscape may include occasional rocky outcrops and grazing herds of animals like zebras and antelope.",
                    ["Lions", "Giraffes", "Elephants"],
                    ["Grass"]]
    }

    return biome_descriptions.get(current_tile, None)


@app.get("/index")
async def command(request: Request, command: str):
    global player_state
    global map
    print(command)
    state, map, player_state = process_command(command, map, player_state)
    return templates.TemplateResponse('game/game.j2',
                                      {"request": request, "player_state": player_state, "map": map, "state": {}})


@app.post("/index")
async def command(request: Request, command: str = Form(default="")):
    global player_state
    global map
    print(command)
    state, map, player_state = process_command(command, map, player_state)
    return templates.TemplateResponse('game/game.j2',
                                      {"request": request, "player_state": player_state, "map": map, "state": state})


@app.post("/interact")
async def interact(request: Request, interact: str = Form(default="")):
    global last_interaction
    current_tile = map[player_state[0]][player_state[1]]
    tile_data = get_tile_text(current_tile)
    print(tile_data)
    print(interact)
    print(last_interaction)
    print(time.time() - last_interaction)
    if last_interaction == 0:
        last_interaction = time.time()
        interaction_succeeded = True
    elif time.time() - last_interaction > 5:
        last_interaction = time.time()
        interaction_succeeded = True
    else:
        interaction_succeeded = False
    return templates.TemplateResponse('game/interact.j2', {"request": request, "tile_data": tile_data, "interaction_succeeded": interaction_succeeded})


@app.get("/interact")
async def interact(request: Request):
    return templates.TemplateResponse('game/interact.j2', {"request": request})


@app.post("/")
async def root(request: Request, ):
    return templates.TemplateResponse('game/game.j2', {"request": request, "state": {}})


@app.get("/")
async def root(request: Request):
    """
    Handle initial landing page with nothing on the url, render index.j2
    :param request: request from client
    :return: rendered index.j2
    """
    folder_path = 'save_data'
    items = os.listdir(folder_path)
    items.remove(".gitkeep")
    return templates.TemplateResponse("index.j2", {"request": request, "items": items})


@app.get("/{path:path}")
async def handle_request(path: str, request: Request):
    """
    Handle all not specified requests from client
    :param path: requested path
    :param request: full request from client
    :return: processed template at path,
            if not found: return the file from the static folder
            if not found: return the 404-error.html (Not Found)
    """
    # TODO: Convert print statements to proper logging
    print(path, current_dir)
    # Try to serve the requested file from /templates folder
    template_file = current_dir / "templates" / path
    print('template_file:', template_file)
    if template_file.exists():
        if template_file.is_file():
            # We got an exact match
            return templates.TemplateResponse(path, {"request": request})
        else:
            # It is a folder, check for index.j2 in this folder
            path = path + '/index.j2'
            template_file = current_dir / "templates" / path
            if template_file.exists() and template_file.is_file():
                # We got an index.j2
                return templates.TemplateResponse(path, {"request": request})
    # No template, check for static
    static_file = current_dir / "statics" / path
    if static_file.exists():
        return HTMLResponse(static_file.read_text())
    # No Template, No Static, return error
    return HTMLResponse(Path('statics/errors/404-error.html').read_text())


if __name__ == "__main__":
    uvicorn.run(app, port=8000)

import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from functions import *

map_size = 16
region_map_size = 8
mobs_data = []
region_map = []
last_interaction = 0
map = create_map()
player_state = create_player_state()
save_location = ""

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


@app.get("/index")
async def command(request: Request, command: str):
    global player_state
    global map
    global mobs_data
    global save_location
    print(command)
    state, map, player_state, mobs_data, save_location = process_command(command, map_size, region_map_size, map,
                                                                         player_state, mobs_data, save_location)
    world_map = map["world_map"]
    print(player_state)
    return templates.TemplateResponse('game/game.j2',
                                      {"request": request, "player_state": player_state, "map": world_map,
                                       "state": state, "save_location": save_location, "command": command.lower()})


@app.post("/index")
async def command(request: Request, command: str = Form(default="")):
    global player_state
    global map
    global mobs_data
    global save_location
    print(command)
    state, map, player_state, mobs_data, save_location = process_command(command, map_size, region_map_size, map,
                                                                         player_state, mobs_data, save_location)
    world_map = map["world_map"]
    print(player_state)
    return templates.TemplateResponse('game/game.j2',
                                      {"request": request, "player_state": player_state, "map": world_map,
                                       "state": state, "save_location": save_location, "command": command.lower()})


@app.post("/interact")
async def interact(request: Request, interact: str = Form(default="")):
    global player_state
    global writable_map
    global region_map
    global mobs_data
    writable_map, region_map, player_state, biome_data = process_interact(interact, region_map_size, map_size,
                                                                          region_map, map, player_state, mobs_data)
    print(player_state)
    return templates.TemplateResponse('game/interact.j2',
                                      {"request": request, "biome_data": biome_data, "writable_map": writable_map,
                                       "player_state": player_state})


@app.post("/inventory")
async def inventory(request: Request):
    global player_state
    return templates.TemplateResponse('game/inventory.j2', {'request': request, "player_state": player_state})


@app.get("/inventory")
async def inventory(request: Request):
    global player_state
    return templates.TemplateResponse('game/inventory.j2', {'request': request, "player_state": player_state})


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

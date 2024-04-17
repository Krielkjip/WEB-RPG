import gc
import os
import shutil
import tempfile
from typing import Annotated
import json
from pathlib import Path
from world_map_gen import run_world_gen

import uvicorn
from fastapi import FastAPI, Request, Response, UploadFile, File, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from starlette.responses import HTMLResponse


map_size = 16
player_location = [0, 0]
map = run_world_gen(map_size, map_size)
print(map)
# map = None


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

def process_command(command):
    move_player(command.lower())
    state = { "command_len": len(command) }
    if command == "":
        state['error_msg'] = "Please enter a command"
    state['command'] = command
    print(state)
    return state

def move_player(move):
    if move == "down":
        print("Moving down")
        if player_location[1] < map_size - 1:
            player_location[1] += 1
    elif move == "up":
        print("Moving up")
        if player_location[1] > 0:
            player_location[1] -= 1
    elif move == "right":
        print("Moving right")
        if player_location[0] < map_size - 1:
            player_location[0] += 1
    elif move == "left":
        print("Moving left")
        if player_location[0] > 0:
            player_location[0] -= 1

@app.get("/index")
async def command(request: Request):
    return templates.TemplateResponse('game/index.j2', {"request": request, "player_location": player_location, "map": map, "state": {}})


@app.post("/index")
async def command(request: Request, command: str = Form(default = ""), move: str = Form(default = "")):
    print(command)
    state = process_command(command)
    return templates.TemplateResponse('game/index.j2', {"request": request, "player_location": player_location, "map": map, "state": state})

@app.post("/")
async def move(request: Request,):
    return templates.TemplateResponse('game/index.j2', {"request": request, "state": {}})


@app.get("/")
async def root(request: Request):
    """
    Handle initial landing page with nothing on the url, render index.j2
    :param request: request from client
    :return: rendered index.j2
    """
    return await handle_request('index.j2', request)


@app.get("/{path:path}")
async def handle_request(path:str, request: Request):
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

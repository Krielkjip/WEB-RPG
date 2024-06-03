# Import necessary modules
import os
from pathlib import Path

# Import FastAPI and related modules
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

# Import custom functions from another file
from functions import *

# Set up game constants
map_size = 16
region_map_size = 8

# Initialize game state variables
mobs_data = {}
region_map = []
writable_map = []
last_interaction = 0
maps_server = create_map()
player_state = create_player_state()
save_location = ""

# Get the directory of the current Python script
current_dir = Path(__file__).resolve().parent

# Create a FastAPI app
app = FastAPI()

# Set up CORS middleware to allow cross-origin requests
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/statics", StaticFiles(directory="statics"), name="statics")


# Define a function to handle commands
def handle_command(command: str, request: Request):
    """
    Handle a command from the user
    :param command: The command to process
    :param request: The request object
    :return: A rendered template response
    """
    global player_state
    global maps_server
    global mobs_data
    global save_location
    print(command)
    state, maps_server, player_state, mobs_data, save_location = process_command(
        command, map_size, region_map_size, maps_server, player_state, mobs_data, save_location
    )
    world_map = maps_server["world_map"]
    print(player_state)
    return templates.TemplateResponse(
        'game/game.j2',
        {
            "request": request,
            "player_state": player_state,
            "map": world_map,
            "state": state,
            "save_location": save_location,
            "command": command.lower()
        }
    )


# Define routes for the app
@app.get("/index")
async def get_index(request: Request, command: str):
    """
    Handle GET requests to /index
    :param request: The request object
    :param command: The command to process
    :return: A rendered template response
    """
    return handle_command(command, request)


@app.post("/index")
async def post_index(request: Request, command: str = Form(default="")):
    """
    Handle POST requests to /index
    :param request: The request object
    :param command: The command to process
    :return: A rendered template response
    """
    return handle_command(command, request)


@app.post("/interact")
async def post_interact(request: Request, interact: str = Form(default="")):
    """
    Handle POST requests to /interact
    :param request: The request object
    :param interact: The interaction to process
    :return: A rendered template response
    """
    global player_state
    global writable_map
    global region_map
    global mobs_data
    writable_map, region_map, player_state, biome_data, message, fail_message = process_interact(
        interact, region_map_size, map_size, region_map, maps_server, player_state, mobs_data
    )
    print(player_state)
    return templates.TemplateResponse(
        'game/interact.j2',
        {
            "request": request,
            "biome_data": biome_data,
            "writable_map": writable_map,
            "player_state": player_state,
            "interact": interact.lower(),
            "message": message,
            "fail_message": fail_message
        }
    )


@app.post("/inventory")
async def post_inventory(request: Request, craft: str = Form(default="")):
    """
    Handle POST requests to /inventory
    :param request: The request object
    :param craft: The crafting action to process
    :return: A rendered template response
    """
    global player_state
    print(craft)
    player_state, message, fail_message = process_craft(craft, player_state)
    return templates.TemplateResponse(
        'game/inventory.j2',
        {
            'request': request,
            "player_state": player_state,
            "message": message,
            "fail_message": fail_message
        }
    )


@app.get("/inventory")
async def get_inventory(request: Request):
    """
    Handle GET requests to /inventory
    :param request: The request object
    :return: A rendered template response
    """
    global player_state
    return templates.TemplateResponse('game/inventory.j2', {'request': request, "player_state": player_state})


@app.get("/")
async def root(request: Request):
    """
    Handle GET requests to the root URL
    :param request: The request object
    :return: A rendered template response
    """
    folder_path = 'save_data'
    items = os.listdir(folder_path)
    items.remove(".gitkeep")
    return templates.TemplateResponse("index.j2", {"request": request, "items": items})


@app.get("/{path:path}")
async def handle_request(path: str, request: Request):
    """
    Handle GET requests to any other URL
    :param path: The requested path
    :param request: The request object
    :return: A rendered template response or a static file
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
    # Run the app with uvicorn
    uvicorn.run(app, port=8000)

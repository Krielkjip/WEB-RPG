import gc
import os
import shutil
import tempfile
from typing import Annotated
import json
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Response, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from starlette.responses import HTMLResponse


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


@app.get("/api_data/{path_var}")
async def api_data(request: Request, path_var: str):
    print("path_var:", path_var)
    return path_var


@app.get("/api_template/{path_var}")
async def api_template(request: Request, path_var: str):
    print("path_var:", path_var)
    return templates.TemplateResponse('for_api/' + path_var + '.template', {"request": request})


@app.get("/")
async def root(request: Request):
    """
    Handle initial landing page with nothing on the url, render index.html
    :param request: request from client
    :return: rendered index.html
    """
    return await handle_request('index.html', request)


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
            # It is a folder, check for index.html in this folder
            path = path + '/index.html'
            template_file = current_dir / "templates" / path
            if template_file.exists() and template_file.is_file():
                # We got an index.html
                return templates.TemplateResponse(path, {"request": request})
    # No template, check for static
    static_file = current_dir / "statics" / path
    if static_file.exists():
        return HTMLResponse(static_file.read_text())
    # No Template, No Static, return error
    return HTMLResponse(Path('statics/errors/404-error.html').read_text())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
import shutil

from aiofiles.os import path as aiopath
from auth.authentication import JWTDict, check_authorized_dirs, require_jwt
from sanic import Blueprint
from sanic.exceptions import Forbidden, InvalidUsage, NotFound
from sanic.request import Request
from sanic.response import HTTPResponse, json
from utils import BunshoConfig, getmimetype, parsebytes

blueprint = Blueprint("api_core", url_prefix="/core")


@blueprint.get("/ls/<index:int>/<folder:path>")
@require_jwt(return_value=True)
@check_authorized_dirs
async def api_core_ls(request: Request, index: int, folder: str, jwt: JWTDict) -> HTTPResponse:
    body = []
    try:
        folder_path = os.path.join(
            request.app.config.LOCATIONS[int(index)]["dir"], folder
        )
        dirlist = os.listdir(folder_path)
    except (FileNotFoundError, IndexError, NotADirectoryError):
        raise InvalidUsage("Bad argument values were provided.", 400)

    for item in dirlist:
        is_directory = await aiopath.isdir(os.path.join(folder_path, item))
        size = None
        if not is_directory:
            size = parsebytes(await aiopath.getsize(os.path.join(folder_path, item)))
        body.append(
            {
                "name": item,
                "mimetype": await getmimetype(os.path.join(folder_path, item)),
                "size": size,
                "created": int(await aiopath.getctime(os.path.join(folder_path, item))),
                "is_directory": is_directory,
            }
        )

    return json({"listing": body})


@blueprint.patch("/mv/<index:int>/<filepath:path>")
@require_jwt(return_value=True)
@check_authorized_dirs
async def api_core_mv(
    request: Request, index: int, filepath: str, jwt: JWTDict
) -> HTTPResponse:
    if not jwt["permissions"]["move"]:
        raise Forbidden("Insufficient permissions to move files.", 403)

    try:
        location = request.app.config.LOCATIONS[int(index)]["dir"]
        file_path = os.path.join(location, filepath)
        full_path = os.path.normpath(os.path.join(location, request.json["new_path"]))
        full_path += (
            "/" if (not full_path.endswith("/") and not request.json["rename"]) else ""
        )
    except (IndexError, KeyError):
        raise InvalidUsage("Bad argument values were provided.", 400)

    if not await aiopath.exists(file_path) or (
        not await aiopath.exists(full_path) and not request.json["rename"]
    ):
        raise NotFound("File or folder was not found.", 404)
    if not full_path.startswith(location):
        raise InvalidUsage(
            "Directory traversal outside of the root location is not allowed.", 400
        )
    if await aiopath.exists(os.path.join(full_path, os.path.basename(filepath))):
        raise InvalidUsage(
            "There is already a file with the same name at the destination.", 400
        )

    if not request.json["rename"]:
        os.rename(file_path, os.path.join(full_path, os.path.basename(filepath)))
    else:
        os.rename(file_path, full_path)
    return json({"status": "OK"})


@blueprint.delete("/rm/<index:int>/<filepath:path>")
@require_jwt(return_value=True)
@check_authorized_dirs
async def api_core_rm(
    request: Request, index: int, filepath: str, jwt: JWTDict
) -> HTTPResponse:
    if not jwt["permissions"]["delete"]:
        raise Forbidden("Insufficient permissions to delete files.", 403)

    path = os.path.join(request.app.config.LOCATIONS[int(index)]["dir"], filepath)
    if not await aiopath.exists(path):
        raise NotFound("File or folder was not found.", 404)

    if await aiopath.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)
    return json({"status": "OK"})


@blueprint.post("/update-cfg")
@require_jwt(return_value=True)
async def api_core_update_cfg(request: Request, jwt: JWTDict) -> HTTPResponse:
    if jwt["permissions"]["admin"]:
        request.app.update_config(BunshoConfig())
        return json({"status": "OK"})

    raise Forbidden("Insufficient permissions to perform administrator actions.", 403)

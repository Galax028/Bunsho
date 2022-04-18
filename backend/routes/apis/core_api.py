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
async def api_core_ls(
    request: Request, index: int, folder: str, jwt: JWTDict
) -> HTTPResponse:
    """
    List Directory Endpoint

    This endpoint lists the contents of a directory.

    openapi:
    ---
    tags:
        - filesystem
    security:
        - token: []
    parameters:
        - in: path
          name: index
          schema:
              type: integer
              example: 0
          required: true
          description: Index of a location from the config array of locations.
        - in: path
          name: folder
          schema:
              type: string
              example: /path/to/folder
          required: true
          description: The folder path to list.
    responses:
        "200":
            description: The folder's content.
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            listing:
                                type: array
                                items:
                                    type: object
                                    properties:
                                        name:
                                            type: string
                                        mimetype:
                                            type: string
                                            nullable: true
                                        size:
                                            type: string
                                            nullable: true
                                        created:
                                            type: integer
                                        is_directory:
                                            type: boolean
                        example:
                            listing:
                                - name: essay.txt
                                  mimetype: text/plain
                                  size: 1024
                                  is_directory: false
                                - name: work
                                  mimetype: null
                                  size: null
                                  is_directory: true
    """
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
    """
    Move File/Folder Endpoint

    This endpoint moves the specified file or folder. If the request JSON has
    the `rename` key set to `true`, it will rename the file or folder instead.

    openapi:
    ---
    tags:
        - filesystem
    security:
        - token: []
    parameters:
        - in: path
          name: index
          schema:
              type: integer
              example: 0
          required: true
          description: Index of a location from the config array of locations.
        - in: path
          name: filepath
          schema:
              type: string
              example: /path/to/file_or_folder
          required: true
          description: The path to the file or folder to move/rename.
    requestBody:
        description: Configuration.
        required: true
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        new_path:
                            type: string
                        rename:
                            type: boolean
                    example:
                        new_path: ./other/folder
                        rename: false
    responses:
        "200":
            description: File/folder was moved/renamed successfully.
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            status:
                                type: string
                        example:
                            status: OK
    """
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
            "There is already a file/folder with the same name at the destination.", 400
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
    """
    Delete File/Folder Endpoint

    This endpoint deletes the specified file or folder.

    openapi:
    ---
    tags:
        - filesystem
    security:
        - token: []
    parameters:
        - in: path
          name: index
          schema:
              type: integer
              example: 0
          required: true
          description: Index of a location from the config array of locations.
        - in: path
          name: filepath
          schema:
              type: string
              example: /path/to/file_or_folder
          required: true
          description: The path to the file or folder to delete.
    responses:
        "200":
            description: File/folder was deleted successfully.
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            status:
                                type: string
                        example:
                            status: OK
    """
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
    """
    Update Configuration Endpoint

    This endpoint when requested, will update the server's configuration from
    the `config.json` file. Requires admin permissions.

    openapi:
    ---
    tags:
        - config
    security:
        - token: []
    responses:
        "200":
            description: Config was updated successfully.
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            status:
                                type: string
                        example:
                            status: OK
    """
    if jwt["permissions"]["admin"]:
        request.app.update_config(BunshoConfig())
        return json({"status": "OK"})

    raise Forbidden("Insufficient permissions to perform administrator actions.", 403)

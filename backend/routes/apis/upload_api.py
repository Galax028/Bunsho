import os

import aiofiles
from aiofiles.os import path as aiopath
from auth.authentication import JWTDict, require_jwt
from database import TempDBInterface
from sanic import Blueprint
from sanic.exceptions import Forbidden, InvalidUsage, NotFound
from sanic.request import Request
from sanic.response import HTTPResponse, json

blueprint = Blueprint("api_upload", url_prefix="/upload")


@blueprint.post("/file-metadata")
@require_jwt(return_value=True)
async def api_upload_file_metadata(request: Request, jwt: JWTDict) -> HTTPResponse:
    """
    Upload File Endpoint (Part 1)

    This endpoint requires the request to send the location, destination folder,
    and the filename. It will then return a UUID to be used in the uploading
    process.

    openapi:
    ---
    tags:
        - upload
    security:
        - token: []
    requestBody:
        description: Configuration.
        required: true
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        location:
                            type: string
                        folder:
                            type: string
                        filename:
                            type: string
                    example:
                        location: Pictures
                        folder: screenshots/
                        filename: funny-game-bug.jpeg
    responses:
        "200":
            description: The UUID to be used for file uploading.
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            uuid:
                                type: string
    """
    if not jwt["permissions"]["write"]:
        raise Forbidden("Insufficient permissions to write files.", 403)

    cfg = request.app.config
    valid_locations = [l["name"] for l in cfg.LOCATIONS]
    authorized = False
    try:
        location = request.json["location"]
        folder = request.json["folder"]
        filename = request.json["filename"]
    except KeyError:
        raise InvalidUsage("Bad argument values were provided.", 400)

    if location not in valid_locations:
        raise NotFound("The provided location was not found.", 404)

    if jwt["authorized_locations"] == "all":
        authorized = True
    for authorized_location in jwt["authorized_locations"]:
        if authorized_location in valid_locations:
            authorized = True

    if authorized:
        location_dir = next((i for i in cfg.LOCATIONS if i["name"] == location))["dir"]
        full_location = os.path.normpath(
            os.path.join(location_dir, folder, os.path.basename(filename))
        )
        if not full_location.startswith(location_dir) or not await aiopath.exists(
            os.path.dirname(full_location)
        ):
            raise InvalidUsage(
                "Directory traversal outside of the root location is not allowed.", 400
            )
        if await aiopath.exists(full_location):
            raise InvalidUsage(
                "There is already a file/folder with the same name at the destination.",
                400,
            )

        return json(
            {
                "uuid": await request.app.ctx.tempdb.insert_uuid(
                    jwt["uname"], full_location
                ),
            }
        )

    raise Forbidden("Insufficient permissions to access this location.", 403)


@blueprint.put("/file", stream=True)
@require_jwt(return_value=True)
async def api_upload_file(
    request: Request, tempdb: TempDBInterface, jwt: JWTDict
) -> HTTPResponse:
    """
    Upload File Endpoint (Part 2)

    This endpoint requires will allow you to upload the file. The UUID from the
    part 1 upload endpoint is required.

    openapi:
    ---
    tags:
        - upload
    security:
        - token: []
    parameters:
        - in: query
          name: uuid
          schema:
              type: string
          required: true
          description: The UUID from the part 1 upload endpoint.
    requestBody:
        description: The file to be uploaded.
        content:
            application/octet-stream:
                schema:
                    type: string
                    format: binary
    responses:
        "200":
            description: The file was uploaded successfully.
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
    if not jwt["permissions"]["write"]:
        raise Forbidden("Insufficient permissions to write files.", 403)

    entry: tuple = await tempdb.find_uuid(request.args.get("uuid"))
    if entry:
        async with aiofiles.open(entry[2], "wb") as filepath:
            while True:
                body = await request.stream.read()  # type: ignore
                if body is None:
                    break

                await filepath.write(body)

        await tempdb.delete_uuid(request.args.get("uuid"))
        return json({"status": "OK"})

    raise NotFound("The specified UUID was not found.", 404)

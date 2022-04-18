import asyncio
import os
import shutil

from aiofiles.os import path as aiopath
from aiofiles.os import stat
from auth.authentication import JWTDict, check_authorized_dirs, require_jwt
from sanic import Blueprint
from sanic.exceptions import InvalidUsage, NotFound
from sanic.request import Request
from sanic.response import ResponseStream, file_stream
from utils import getmimetype

blueprint = Blueprint("api_download", url_prefix="/download")


@blueprint.get("/single/<index:int>/<filepath:path>")
@require_jwt(return_value=True)
@check_authorized_dirs
async def api_download_single(
    request: Request, index: int, filepath: str, jwt: JWTDict
) -> ResponseStream:
    """
    Download Single File Endpoint

    This endpoint will stream the file requested by the user to be downloaded.

    openapi:
    ---
    tags:
        - download
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
          description: The path to the file to download.
    responses:
        "200":
            description: The requested file.
            content:
                application/octet-stream:
                    schema:
                        type: string
                        format: binary
    """
    path = os.path.join(request.app.config.LOCATIONS[int(index)]["dir"], filepath)
    if not await aiopath.exists(path):
        raise NotFound("File or folder was not found.", 404)
    if not await aiopath.isfile(path):
        raise InvalidUsage("Folders cannot be downloaded by this endpoint.", 400)

    return await file_stream(
        location=path,
        chunk_size=1048576,
        mime_type=await getmimetype(path),
        headers={
            "Content-Disposition": f'Attachment; filename="{os.path.basename(path)}"',
            "Content-Length": str((await stat(path)).st_size),
        },
    )


@blueprint.get("/folder/<index:int>/<folder:path>")
@require_jwt(return_value=True)
@check_authorized_dirs
async def api_download_folder(
    request: Request, index: int, folder: str, jwt: JWTDict
) -> ResponseStream:
    """
    Download Compressed Folder Endpoint

    This endpoint will stream the folder requested by the user to be downloaded.
    The user can specify wheather to use Zip compression or Tar with GZip.

    openapi:
    ---
    tags:
        - download
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
          description: The path to the folder to download.
        - in: query
          name: ext
          schema:
              type: string
              enum: [zip, tar.gz]
          required: true
          description: The file compression type. Accepts "zip" or "tar.gz".
    responses:
        "200":
            description: The requested folder.
            content:
                application/octet-stream:
                    schema:
                        type: string
                        format: binary
    """
    path = os.path.join(request.app.config.LOCATIONS[int(index)]["dir"], folder)
    archive_path = f"{os.path.join(request.app.ctx.tmp_folder, path.replace('/', '_'))}"
    ext = request.args.get("ext")
    if not await aiopath.exists(path):
        raise NotFound("File or folder was not found.", 404)
    if not await aiopath.isdir(path):
        raise InvalidUsage("Files cannot be downloaded by this endpoint.", 400)
    if ext not in ("zip", "tar.gz"):
        raise InvalidUsage("Invalid archive type was requested.", 400)
    if not await aiopath.exists(f"{archive_path}.{ext}"):
        await asyncio.get_running_loop().run_in_executor(
            None,
            shutil.make_archive,
            archive_path,
            ext if ext != "tar.gz" else "gztar",
            path,
        )

    return await file_stream(
        location=f"{archive_path}.{ext}",
        chunk_size=1048576,
        mime_type=await getmimetype(f"{archive_path}.{ext}"),
        headers={
            "Content-Disposition": f'Attachment; filename="{os.path.basename(archive_path)}.{ext}"',
            "Content-Length": str((await stat(f"{archive_path}.{ext}")).st_size),
        },
    )

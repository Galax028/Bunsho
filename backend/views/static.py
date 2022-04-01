from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, file

blueprint = Blueprint("static")
blueprint.static("/assets", "../frontend/dist/assets", name="static_assets")


@blueprint.get("/")  # type: ignore
@blueprint.get(r"/<path:[^/api].*?>")
async def static_root(_request: Request, path: str = None) -> HTTPResponse:
    return await file("../frontend/dist/index.html")

from sanic import Sanic
from sanic.exceptions import Forbidden, InvalidUsage, Unauthorized, NotFound
from sanic.request import Request
from sanic.response import HTTPResponse, json


class ExceptionHandlers:
    def __init__(self, app: Sanic):
        app.error_handler.add(InvalidUsage, self.bad_request_handler)
        app.error_handler.add(Forbidden, self.forbidden_handler)
        app.error_handler.add(NotFound, self.not_found_handler)
        app.error_handler.add(Unauthorized, self.unauthorized_handler)

    async def bad_request_handler(
        self, _request: Request, exception: InvalidUsage
    ) -> HTTPResponse:
        return json({"error": "Bad Request", "error_msg": str(exception)}, 400)

    async def forbidden_handler(
        self, _request: Request, exception: Forbidden
    ) -> HTTPResponse:
        return json({"error": "Forbidden", "error_msg": str(exception)}, 403)

    async def not_found_handler(
        self, _request: Request, exception: NotFound
    ) -> HTTPResponse:
        return json({"error": "Not Found", "error_msg": str(exception)}, 404)

    async def unauthorized_handler(
        self, _request: Request, exception: Unauthorized
    ) -> HTTPResponse:
        return json({"error": "Unauthorized", "error_msg": str(exception)}, 401)

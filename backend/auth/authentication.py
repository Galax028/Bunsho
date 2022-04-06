from functools import wraps
from typing import Awaitable, Callable, Coroutine, TypedDict, Union

import jwt
from sanic.exceptions import Forbidden, InvalidUsage, Unauthorized
from sanic.request import Request

PermissionsDict = TypedDict(
    "PermissionsDict",
    {
        "admin": bool,
        "write": bool,
        "move": bool,
        "delete": bool,
        "share": bool,
    },
)


JWTDict = TypedDict(
    "JWTDict",
    {
        "iat": int,
        "exp": int,
        "iss": str,
        "uname": str,
        "authorized_locations": Union[str, list],
        "permissions": PermissionsDict,
    },
)


async def _decode_token(
    request: Request, return_value: bool = False
) -> Union[bool, str, JWTDict]:
    if not request.token:
        raise Unauthorized("Bearer authorization is required.", 401, "Bearer")

    try:
        decoded: JWTDict = jwt.decode(  # type: ignore
            request.token, request.app.config.SECRET, algorithms=["HS256"]
        )
        blacklist: bool = await request.app.ctx.tempdb.verify_jwt_blacklist(
            decoded["uname"], decoded["iat"]
        )
        if decoded["iss"] != "Bunsho":
            raise Unauthorized("Invalid token issuer.", 401)
        if blacklist:
            raise Unauthorized("This token has been invalidated.", 401)
        if return_value:
            return decoded
    except jwt.exceptions.DecodeError:
        raise Unauthorized("An error occurred while trying to decode the token.", 401)
    except jwt.exceptions.ExpiredSignatureError:
        raise Unauthorized("This token has expired.", 401)

    return True


def require_jwt(wrapped: Callable[..., Awaitable] = None, return_value: bool = False):
    def decorator(func: Callable[..., Awaitable]):
        @wraps(func)
        async def decorated_function(request: Request, *args, **kwargs):
            auth_result = await _decode_token(request, return_value)
            if auth_result is True:
                return await func(request, *args, **kwargs)
            if isinstance(auth_result, dict):
                return await func(request, *args, **kwargs, jwt=auth_result)

        return decorated_function

    return decorator(wrapped) if wrapped else decorator


def check_authorized_dirs(wrapped: Callable[..., Coroutine]):
    def decorator(func: Callable[..., Coroutine]):
        @wraps(func)
        async def decorated_function(request: Request, *args, **kwargs):
            try:
                location = request.app.config.LOCATIONS[int(kwargs["index"])]
            except IndexError as err:
                raise InvalidUsage("Location index was not provided.", 400)

            jwt = kwargs["jwt"]
            if (
                isinstance(jwt["authorized_locations"], str)
                and jwt["authorized_locations"] != "all"
            ) or (
                isinstance(jwt["authorized_locations"], list)
                and location["name"] not in jwt["authorized_locations"]
            ):
                raise Forbidden(
                    "Insufficient permissions to access this location.", 403
                )

            return await func(request, *args, **kwargs)

        return decorated_function

    return decorator(wrapped)

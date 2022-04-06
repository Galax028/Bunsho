from datetime import datetime, timedelta, timezone

import jwt
from auth.authentication import JWTDict, require_jwt
from auth.passwd import hash_passwd, verify_passwd
from database import SQLiteInterface, TempDBInterface
from sanic import Blueprint
from sanic.exceptions import Forbidden, InvalidUsage, NotFound, Unauthorized
from sanic.request import Request
from sanic.response import HTTPResponse, json

blueprint = Blueprint("api_auth", url_prefix="/auth")


@blueprint.post("/login")
async def api_auth_login(request: Request, db: SQLiteInterface) -> HTTPResponse:
    """
    Login Endpoint

    This endpoint takes in the username and password and returns a JWT token.

    openapi:
    ---
    tags:
        - authentication
    requestBody:
        description: User credentials.
        required: true
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        uname:
                          type: string
                        passwd:
                          type: string
                example:
                  uname: admin
                  passwd: admin
    responses:
        "200":
            description: The JWT access token.
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            token:
                                type: string
    """
    credentials: dict = request.json
    if not credentials or ["uname", "passwd"] != list(credentials.keys()):
        raise InvalidUsage("Credentials were not provided.", 400)

    fetched_credentials = await db.find_user(credentials["uname"])
    if not fetched_credentials:
        raise Unauthorized("Could not find the user with the provided username.", 401)

    verification: list[bool] = await verify_passwd(
        fetched_credentials[1], credentials["passwd"]
    )
    if verification[0]:
        if verification[1]:
            await db.update_user(
                uname=credentials["uname"],
                passwd=await hash_passwd(credentials["passwd"]),
            )

        cfg = request.app.config
        return json(
            {
                "token": jwt.encode(
                    {
                        "iat": datetime.now(tz=timezone.utc),
                        "exp": datetime.now(tz=timezone.utc)
                        + timedelta(minutes=cfg.JWT_EXPIRY_MINUTES),
                        "iss": "Bunsho",
                        "uname": fetched_credentials[0],
                        "authorized_locations": fetched_credentials[2],
                        "permissions": fetched_credentials[3],
                    },
                    cfg.SECRET,
                    algorithm="HS256",
                ),
            }
        )

    raise Unauthorized("Given credentials were invalid.", 401)


@blueprint.post("/logout-all")
@require_jwt(return_value=True)
async def api_auth_logout_all(
    request: Request, tempdb: TempDBInterface, jwt: JWTDict
) -> HTTPResponse:
    """
    Force Logout Endpoint

    This endpoint forces all the user's devices to logout by blacklisting tokens.

    openapi:
    ---
    tags:
        - authentication
    security:
        - token: []
    responses:
        "200":
            description: The user was forced to logout from all devices successfully.
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
    await tempdb.blacklist_jwt(
        jwt["uname"], int(datetime.now(tz=timezone.utc).timestamp())
    )
    return json({"status": "OK"})


@blueprint.get("/get-user")
@require_jwt(return_value=True)
async def api_auth_get_user(
    request: Request, db: SQLiteInterface, jwt: JWTDict
) -> HTTPResponse:
    """
    Get User Endpoint

    This endpoint replies with a user's data stored in the database. Requires
    admin permissions if the query username is not the same as the username in
    the provided JWT token.

    openapi:
    ---
    tags:
        - authentication
    security:
        - token: []
    parameters:
        - name: uname
          in: query
          description: The username to query the database.
          required: true
          schema:
              type: string
              example: admin
    responses:
        "200":
            description: The requested user's data.
            content:
                application/json:
                    schema:
                    type: object
                    properties:
                        body:
                            type: object
                            properties:
                                uname:
                                    type: string
                                authorized_locations:
                                    type: string
                                permissions:
                                    type: object
                                    properties:
                                        admin:
                                            type: boolean
                                        write:
                                            type: boolean
                                        move:
                                            type: boolean
                                        delete:
                                            type: boolean
                                        share:
                                            type: boolean
                    example:
                        body:
                            uname: john
                            authorized_locations: all
                            permissions:
                                admin: false
                                write: true
                                move: true
                                delete: true
                                share: true
    """
    uname: str = request.args.get("uname")
    if not uname:
        raise InvalidUsage("Username was not specified.", 400)

    if jwt["uname"] != uname and not jwt["permissions"]["admin"]:
        raise Forbidden(
            "Insufficient permissions to perform administrator actions.", 403
        )

    user: list = await db.find_user(uname)
    if user:
        return json(
            {
                "body": {
                    "uname": user[0],
                    "authorized_locations": user[2],
                    "permissions": user[3],
                },
            }
        )

    raise NotFound("Requested user was not found.", 404)

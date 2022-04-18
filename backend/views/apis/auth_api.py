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


@blueprint.post("/access-token")
async def api_auth_access_token(
    request: Request, db: SQLiteInterface, tempdb: TempDBInterface
) -> HTTPResponse:
    """
    Access Token Endpoint

    This endpoint verifies the refresh token provided in the cookie and returns
    an access token.

    openapi:
    ---
    tags:
        - authentication
    parameters:
        - in: cookie
          name: rt
          description: The refresh token.
          required: true
          schema:
              type: string
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
    rt_cookie = request.cookies.get("rt")
    if not rt_cookie:
        raise Unauthorized("Refresh token was not provided.", 401)

    fetched_rt = await db.find_refresh_token("token", rt_cookie)
    if not fetched_rt or fetched_rt[0] != rt_cookie:
        raise Unauthorized(
            "Could not find the provided refresh token in the database.", 401
        )
    try:
        decoded: JWTDict = jwt.decode(
            jwt=rt_cookie,
            key=request.app.config.REFRESH_TOKEN_SECRET,
            algorithms=["HS256"],
        )
        is_blacklisted: bool = await tempdb.verify_jwt_blacklist(
            decoded["uname"], decoded["iat"]
        )
        if decoded["iss"] != "Bunsho":
            raise Unauthorized("Invalid token issuer.", 401)
        if is_blacklisted:
            raise Unauthorized("This token has been invalidated.", 401)
    except jwt.exceptions.DecodeError:
        raise Unauthorized("An error occurred while trying to decode the token.", 401)
    except jwt.exceptions.ExpiredSignatureError:
        raise Unauthorized("This token has expired.", 401)

    try:
        refresh_token = jwt.decode(
            jwt=rt_cookie,
            key=request.app.config.REFRESH_TOKEN_SECRET,
            algorithms=["HS256"],
        )
        if refresh_token["iss"] != "Bunsho":
            raise Unauthorized("Invalid token issuer.", 401)
    except jwt.exceptions.DecodeError:
        raise Unauthorized("An error occurred while trying to decode the token.", 401)
    except jwt.exceptions.ExpiredSignatureError:
        raise Unauthorized("This token has expired.", 401)

    fetched_credentials = await db.find_user(fetched_rt[2])
    return json(
        {
            "access-token": jwt.encode(
                {
                    "iat": datetime.now(tz=timezone.utc),
                    "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=15),
                    "iss": "Bunsho",
                    "uname": fetched_credentials[0],
                    "authorized_locations": fetched_credentials[2],
                    "permissions": fetched_credentials[3],
                },
                request.app.config.ACCESS_TOKEN_SECRET,
                algorithm="HS256",
            ),
        }
    )


@blueprint.post("/refresh-token")
async def api_auth_refresh_token(request: Request, db: SQLiteInterface) -> HTTPResponse:
    """
    Refresh Token Endpoint

    This endpoint takes in the username and password and sets a refresh token as
    a cookie and also returns an access token for the user.

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

        fetched_rt = await db.find_refresh_token("uname", credentials["uname"])
        if fetched_rt:
            refresh_token_expiry = datetime.fromtimestamp(fetched_rt[1])
            refresh_token = fetched_rt[0]
        else:
            refresh_token_expiry = datetime.now(tz=timezone.utc) + timedelta(days=1)
            refresh_token = jwt.encode(
                {
                    "iat": datetime.now(tz=timezone.utc),
                    "exp": refresh_token_expiry,
                    "iss": "Bunsho",
                    "uname": fetched_credentials[0],
                },
                request.app.config.REFRESH_TOKEN_SECRET,
                algorithm="HS256",
            )
            await db.insert_refresh_token(
                token=refresh_token,
                expiry=int(refresh_token_expiry.timestamp()),
                uname=credentials["uname"],
            )

        response = json(
            {
                "access-token": jwt.encode(
                    {
                        "iat": datetime.now(tz=timezone.utc),
                        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=15),
                        "iss": "Bunsho",
                        "uname": fetched_credentials[0],
                        "authorized_locations": fetched_credentials[2],
                        "permissions": fetched_credentials[3],
                    },
                    request.app.config.ACCESS_TOKEN_SECRET,
                    algorithm="HS256",
                ),
            }
        )
        response.cookies["rt"] = refresh_token
        response.cookies["rt"]["expires"] = refresh_token_expiry
        response.cookies["rt"]["path"] = "/api/auth/refresh-token"
        response.cookies["rt"]["httponly"] = True
        response.cookies["rt"]["samesite"] = "Strict"
        return response

    raise Unauthorized("Given credentials were invalid.", 401)


@blueprint.post("/logout-all")
@require_jwt(return_value=True)
async def api_auth_logout_all(
    request: Request, tempdb: TempDBInterface, jwt: JWTDict
) -> HTTPResponse:
    """
    Force Logout Endpoint

    This endpoint forces all the user's devices to logout by blacklisting both
    access tokens and refresh tokens that are created before the logout time.

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

import asyncio
import os
from datetime import datetime, timezone
from sqlite3 import Row
from typing import Union

import aiofiles
import aiosqlite
import ujson
from aiofiles.os import path as aiopath

from .firstrun import generate_db


class SQLiteInterface:
    def __init__(self, db):
        self._db: aiosqlite.Connection = db
        self._lock = asyncio.Lock()

    @classmethod
    async def init(cls):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bunsho.db")
        if not await aiopath.exists(path):
            await (await aiofiles.open(path, "x")).close()
            await generate_db(path)

        return SQLiteInterface(await aiosqlite.connect(path))

    async def insert_user(
        self,
        uname: str,
        passwd: str,
        authorized_locations: Union[str, list],
        permissions: dict,
    ) -> None:
        async with self._lock:
            authorized_locations = (
                authorized_locations
                if isinstance(authorized_locations, str)
                else ujson.dumps(authorized_locations)
            )
            await self._db.execute(
                """
                INSERT INTO auth (uname, passwd, authorized_locations, permissions)
                VALUES (?, ?, ?, ?);
                """,
                (
                    uname,
                    passwd,
                    ujson.dumps(authorized_locations),
                    ujson.dumps(permissions),
                ),
            )
            await self._db.commit()

    async def update_user(
        self,
        uname: str,
        new_uname: str = None,
        passwd: str = None,
        authorized_locations: Union[str, list] = None,
        permissions: dict = None,
    ) -> None:
        async with self._lock:
            if new_uname:
                await self._db.execute(
                    "UPDATE auth SET uname=(?) WHERE uname=(?);", (new_uname, uname)
                )
            elif passwd:
                await self._db.execute(
                    "UPDATE auth SET passwd=(?) WHERE uname=(?);", (passwd, uname)
                )
            elif authorized_locations:
                authorized_locations = (
                    authorized_locations
                    if isinstance(authorized_locations, str)
                    else ujson.dumps(authorized_locations)
                )
                await self._db.execute(
                    "UPDATE auth SET authorized_locations=(?) WHERE uname=(?);",
                    (authorized_locations, uname),
                )
            elif permissions:
                await self._db.execute(
                    "UPDATE auth SET permissions=(?) WHERE uname=(?);",
                    (ujson.dumps(permissions), uname),
                )

            await self._db.commit()

    async def delete_user(self, uname: str) -> None:
        async with self._lock:
            await self._db.execute("DELETE FROM auth WHERE uname=(?);", (uname,))
            await self._db.commit()

    async def find_user(self, uname: str) -> Union[list, None]:
        user = []
        async with self._db.execute(
            "SELECT * FROM auth WHERE uname=(?);", (uname,)
        ) as cursor:
            result = await cursor.fetchone()
            if not result:
                return None

            user = [*result]
            user[2] = ujson.loads(user[2])
            user[3] = ujson.loads(user[3])

        return user

    async def find_all_users(self) -> list:
        users = []
        async with self._db.execute("SELECT * FROM auth;") as cursor:
            async for user in cursor:
                user = [*user]  # type: ignore
                user[2] = ujson.loads(user[2])  # type: ignore
                user[3] = ujson.loads(user[3])  # type: ignore
                users.append(user)

        return users

    async def insert_refresh_token(self, token: str, expiry: int, uname: str) -> None:
        async with self._lock:
            await self._db.execute(
                """
                INSERT INTO refresh_tokens (token, expiry, uname)
                VALUES (?, ?, ?);
                """,
                (token, expiry, uname),
            )
            await self._db.commit()

    async def find_refresh_token(self, by: str, value: str) -> Union[Row, None]:
        async with self._db.execute(
            f"SELECT * FROM refresh_tokens WHERE {by}=(?);", (value,)
        ) as cursor:
            return await cursor.fetchone()

    async def delete_refresh_token(self, uname: str) -> None:
        async with self._lock:
            await self._db.execute(
                "DELETE FROM refresh_tokens WHERE uname=(?);", (uname,)
            )
            await self._db.commit()

    async def refresh_tokens_cleanup_task(self) -> None:
        while True:
            async with self._db.execute("SELECT * FROM refresh_tokens;") as cursor:
                async for row in cursor:
                    if row[1] < int(datetime.now(tz=timezone.utc).timestamp()):
                        await self.delete_refresh_token(row[2])

            await asyncio.sleep(60)

    async def stop(self) -> None:
        await self._db.close()

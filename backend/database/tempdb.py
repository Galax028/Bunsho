import asyncio
import os
from textwrap import dedent
from typing import Union
from uuid import uuid4

import aiosqlite


class TempDBInterface:
    def __init__(self, db, path):
        self._path: str = path
        self._db: aiosqlite.Connection = db
        self._lock = asyncio.Lock()

    @classmethod
    async def init(cls):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp.db")
        conn = await aiosqlite.connect(path)
        await conn.execute(
            dedent(
                """
            CREATE TABLE IF NOT EXISTS upload_uuids (
                uuid TEXT NOT NULL UNIQUE,
                user TEXT NOT NULL,
                path TEXT NOT NULL
            );
        """
            )
        )
        await conn.execute(
            dedent(
                """
            CREATE TABLE IF NOT EXISTS jwt_blacklist (
                uname TEXT NOT NULL UNIQUE,
                iat INTEGER NOT NULL
            );
        """
            )
        )
        await conn.commit()
        return TempDBInterface(conn, path)

    async def insert_uuid(self, user: str, path: str) -> str:
        async with self._lock:
            uuid = str(uuid4())
            await self._db.execute(
                "INSERT INTO upload_uuids (uuid, user, path) VALUES (?, ?, ?);",
                (uuid, user, path),
            )
            await self._db.commit()
            return uuid

    async def find_uuid(self, uuid: str) -> Union[aiosqlite.Row, None]:
        async with self._db.execute(
            "SELECT * FROM upload_uuids WHERE uuid=(?);", (uuid,)
        ) as cursor:
            result = await cursor.fetchone()
            if not result:
                return None
            return result

    async def delete_uuid(self, uuid: str) -> None:
        async with self._lock:
            await self._db.execute("DELETE FROM upload_uuids WHERE uuid=(?);", (uuid,))
            await self._db.commit()

    async def blacklist_jwt(self, uname: str, iat: int) -> None:
        async with self._lock:
            await self._db.execute(
                "INSERT INTO jwt_blacklist (uname, iat) VALUES (?, ?);", (uname, iat)
            )
            await self._db.commit()

    async def verify_jwt_blacklist(self, uname: str, iat: int) -> bool:
        async with self._db.execute(
            "SELECT * FROM jwt_blacklist WHERE uname=(?);", (uname,)
        ) as cursor:
            result = await cursor.fetchone()
            if not result:
                return False
            if result[1] > iat:
                return True
        return False

    async def stop(self) -> None:
        await self._db.close()
        try:
            os.remove(self._path)
        except FileNotFoundError:
            pass

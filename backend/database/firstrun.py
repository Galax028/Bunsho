from textwrap import dedent

import aiosqlite
import ujson
from auth.passwd import hash_passwd  # type: ignore


async def generate_db(path: str):
    async with aiosqlite.connect(path) as db:
        await db.execute(
            dedent(
                """
            CREATE TABLE IF NOT EXISTS auth (
                uname TEXT NOT NULL UNIQUE,
                passwd TEXT NOT NULL,
                authorized_locations TEXT NOT NULL,
                permissions TEXT NOT NULL
            );
        """
            )
        )
        await db.commit()
        await db.execute(
            """
            INSERT INTO auth (uname, passwd, authorized_locations, permissions)
            VALUES (?, ?, ?, ?);
        """,
            (
                "admin",
                await hash_passwd("admin"),
                ujson.dumps("all"),
                ujson.dumps(
                    {
                        "admin": True,
                        "write": True,
                        "move": True,
                        "delete": True,
                        "share": True,
                    }
                ),
            ),
        )
        await db.commit()

from textwrap import dedent

import aiosqlite
import ujson
from auth.passwd import hash_passwd


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
        await db.execute(
            dedent(
                """
                CREATE TABLE IF NOT EXISTS refresh_tokens (
                    token TEXT NOT NULL UNIQUE,
                    expiry INTEGER NOT NULL,
                    uname TEXT NOT NULL,
                    FOREIGN KEY (uname)
                    REFERENCES auth (uname)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
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

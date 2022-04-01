import asyncio
import os

import uvloop
from sanic import Sanic
from sanic.log import logger

from database import SQLiteInterface, TempDBInterface
from exceptions import ExceptionHandlers
from utils import BunshoConfig
from views import load_views


class BunshoApp(Sanic):
    def __init__(self):
        super().__init__("bunsho", config=BunshoConfig())

        load_views(self)
        ExceptionHandlers(self)
        logger.info("[App]: Loaded views, APIs, and error handlers")
        self.extend(
            config={
                "cors_origins": "*",
                "oas": self.config.DEV_MODE,
                "oas_ui_default": "swagger",
                "oas_ui_redoc": False,
            }
        )

        self.register_listener(self.init_app, "main_process_start")
        self.register_listener(self.stop_app, "main_process_stop")
        self.register_listener(self.init_db, "before_server_start")
        self.register_listener(self.stop_db, "before_server_stop")

        logger.info("[App]: Starting main server process...")
        self.run(
            host=self.config.HOST,
            port=self.config.PORT,
            debug=self.config.DEV_MODE,
            ssl=self.config.get("SSL_CERTS_FOLDER"),
            fast=not self.config.DEV_MODE,
            access_log=self.config.DEV_MODE,
        )

    async def init_app(self, _app, _) -> None:
        self.ctx.tmp_folder = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "tmp"
        )
        os.mkdir(self.ctx.tmp_folder)
        logger.info("[App]: Created temporary download cache directory")

    async def stop_app(self, _app, _) -> None:
        for archive in os.listdir(self.ctx.tmp_folder):
            os.remove(os.path.join(self.ctx.tmp_folder, archive))
        os.rmdir(self.ctx.tmp_folder)
        logger.info("[App]: Deleted temporary download cache directory")

    async def init_db(self, _app, _) -> None:
        self.ctx.db = await SQLiteInterface.init()
        self.ext.dependency(self.ctx.db)
        logger.info("[Worker]: Connected to SQLite database")
        self.ctx.tempdb = await TempDBInterface.init()
        self.ext.dependency(self.ctx.tempdb)
        logger.info("[Worker]: Connected to temporary database")

    async def stop_db(self, _app, _) -> None:
        await self.ctx.db.stop()
        logger.info("[Worker]: Disconnected from SQLite database")
        await self.ctx.tempdb.stop()
        logger.info("[Worker]: Disconnected from temporary database")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    BunshoApp()

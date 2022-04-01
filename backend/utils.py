import asyncio
import math
import random
from typing import Union

import magic
import ujson
from aiofiles.os import path as aiopath
from sanic.config import Config


class BunshoConfig(Config):
    def __init__(self):
        super().__init__()

        with open("./config.json", "r", encoding="utf8") as f:
            self.update_config(ujson.load(f))


def generateshare() -> str:
    return "".join(
        random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        for _ in range(6)
    )


async def getmimetype(file: str) -> Union[str, None]:
    def _getmimetype(file: str) -> str:
        return magic.from_file(file, mime=True)

    if not await aiopath.isdir(file):
        return await asyncio.get_running_loop().run_in_executor(
            None, _getmimetype, file
        )
    return None


def parsebytes(b: int) -> str:
    multiple = math.trunc(math.log2(b) / math.log2(1000))
    value = b / math.pow(1000, multiple)
    return (
        f'{value:.2f} {["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"][multiple]}'
    )

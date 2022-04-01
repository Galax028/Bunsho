import asyncio

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


async def hash_passwd(passwd: str) -> str:
    def _hash_passwd(passwd: str) -> str:
        return PasswordHasher(salt_len=32).hash(passwd)

    return await asyncio.get_running_loop().run_in_executor(None, _hash_passwd, passwd)


async def verify_passwd(hash_passwd: str, passwd: str) -> list[bool]:
    def _verify_passwd(hash_passwd: str, passwd: str) -> list[bool]:
        try:
            PasswordHasher(salt_len=32).verify(hash_passwd, passwd)
            return [True, PasswordHasher(salt_len=32).check_needs_rehash(hash_passwd)]
        except VerifyMismatchError:
            return [False, False]

    return await asyncio.get_running_loop().run_in_executor(
        None, _verify_passwd, hash_passwd, passwd
    )

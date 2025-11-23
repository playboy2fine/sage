import asyncio

from discord.ext.commands import Bot


class Client(Bot):
    pass


async def amain() -> None:
    print("I'm working!")
    await asyncio.sleep(10)
    print("Bye!")


def main() -> None:
    asyncio.run(amain())
from typing import Any

import nonebot
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.params import ShellCommandArgs, State
from nonebot.rule import ArgumentParser
from nonebot.typing import T_State

from .idalon import idalon

parser = ArgumentParser(add_help=False)

parser.add_argument("name")

idalon_night = nonebot.on_shell_command("idalon", parser=parser)

@idalon_night.handle()
async def _(bot: Bot, event: Event, command: Any = ShellCommandArgs()):
    image = await idalon.nights(command.name)
    if image:
        try:
            await idalon_night.send(MessageSegment.image(image))
        except:
            await idalon_night.finish("未知错误.")
    else:
        idalon_night.finish("未知错误.")
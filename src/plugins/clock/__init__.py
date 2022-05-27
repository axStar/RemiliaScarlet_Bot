import nonebot
from .data_source import wfClock
from nonebot.adapters.onebot.v11 import Event, Bot, MessageSegment


eidolon = nonebot.on_command("平原")





@eidolon.handle()
async def _(bot: Bot, event: Event):
    image = await wfClock.eidolon()
    if image:
        await eidolon.finish(MessageSegment.image(image))
    else:
        await eidolon.finish("出现未知错误，请稍后再试。")
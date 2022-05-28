import nonebot
from .data_source import wfClock
from nonebot.adapters.onebot.v11 import Event, Bot, MessageSegment


eidolon = nonebot.on_command("平原")
earth = nonebot.on_command("地球")
vallis = nonebot.on_command("金星")
cambion = nonebot.on_command("火卫二")

@eidolon.handle()
async def _(bot: Bot, event: Event):
    image = await wfClock.eidolon()
    if image:
        await eidolon.finish(MessageSegment.image(image))
    else:
        await eidolon.finish("出现未知错误，请稍后再试。")


@earth.handle()
async def _(bot: Bot, event: Event):
    image = wfClock.earth()
    await earth.finish(MessageSegment.image(image))


@vallis.handle()
async def _(bot: Bot, event: Event):
    image = wfClock.vallis()
    await vallis.finish(MessageSegment.image(image))

@cambion.handle()
async def _(bot: Bot, event: Event):
    image = await wfClock.cambion()
    if image:
        await eidolon.finish(MessageSegment.image(image))
    else:
        await eidolon.finish("出现未知错误，请稍后再试。")
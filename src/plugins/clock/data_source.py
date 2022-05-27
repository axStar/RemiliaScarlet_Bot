from io import BytesIO
from typing import Union

import arrow
import httpx
from PIL import Image, ImageDraw, ImageFont


class wfClock():
    """获取各个开放地图的时间状态。"""

    def __init__(self) -> None:
        pass

    @classmethod
    async def eidolon(cls) -> Union[BytesIO, None]:
        """获取夜灵平野的状态。"""

        async with httpx.AsyncClient() as client:
            try:
                worldState = await client.get("http://content.warframe.com/dynamic/worldState.php")
                if worldState.status_code != 200:
                    raise Exception(f"错误代码：{worldState.status_code}")
            except:
                return None
            else:
                worldState = worldState.json()

        for item in worldState["SyndicateMissions"]:
            if item["Tag"] == "CetusSyndicate":
                jobStart = arrow.get(
                    (int(item["Activation"]["$date"]["$numberLong"])) / 1000, tzinfo="Asia/Shanghai")
                jobEnd = arrow.get(
                    (int(item["Expiry"]["$date"]["$numberLong"])) / 1000, tzinfo="Asia/Shanghai")
                break

        toNight = jobStart.shift(minutes=100)
        isDay = arrow.now() < toNight
        mShift = 0 if isDay else 150
        toNext = toNight if isDay else jobEnd
        nightList = []
        for _ in range(5):
            nightList.append(
                toNight.shift(minutes=mShift).format("HH:mm | hh:mm A")
            )
            mShift += 150

        stateStr = f"当前状态：{'白天' if isDay else '夜晚'}\n\n距离切换：{toNext.humanize(locale='zh-cn', only_distance=True, granularity=['hour', 'minute'])}"
        nightStr = "\n\n".join(nightList)
        timeImage = BytesIO()
        img = Image.open("./src/plugins/clock/data/背景.png")
        draw = ImageDraw.ImageDraw(img)
        tfont = ImageFont.truetype("./src/plugins/clock/data/font1.ttf", 42)
        textW, textH = draw.textsize(stateStr, tfont)
        draw.text(((800-textW)/2, (368-textH)/2), stateStr, font=tfont)
        textW, textH = draw.textsize(nightStr, tfont)
        draw.text(((800-textW)/2, (788-textH)/2 + 368), nightStr, font=tfont)
        img.save(timeImage, "png")
        return timeImage

    @classmethod
    def earth(cls) -> BytesIO:
        now = arrow.now().int_timestamp % 28800
        isDay = now < 14400
        leftSeconds = 14400 - (now % 14400)
        toNext = arrow.now().shift(seconds=leftSeconds)
        earthState = "{}\n\n距离结束：{}".format("白天" if isDay else '夜晚', toNext.humanize(locale='zh-cn', only_distance=True, granularity=['hour', 'minute']))
        earthImage =BytesIO()
        img = Image.open("./src/plugins/clock/data/地球背景.png")
        draw = ImageDraw.ImageDraw(img)
        tfont = ImageFont.truetype("./src/plugins/clock/data/font1.ttf", 32)
        textW, textH = draw.textsize(earthState, tfont)
        draw.text(((400-textW)/2, (400-textH)/2), earthState, font=tfont, align="center")
        img.save(earthImage, "png")
        return earthImage
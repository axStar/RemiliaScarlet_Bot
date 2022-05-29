
import asyncio
from io import BytesIO
from re import T

import httpx
from PIL import Image, ImageDraw, ImageFont


class idalon():
    pass

    def __init__(self) -> None:
        pass

    @classmethod
    def __get_run(cls, data: dict) -> list:
        lastHydrolystLimbBreakTime = cls.__calculate_time(
            data["lastHydrolystLimbBreakTime"])
        extractionTime = cls.__calculate_time(data["extractionTime"])
        loadTime = cls.__calculate_time(data["loadTime"])
        host = data["host"]
        clients = ["匿名" if x == "$anonymous" else x for x in data["clients"]]
        return [lastHydrolystLimbBreakTime, extractionTime, loadTime, host, clients]

    @classmethod
    def __get_eidolon(cls, data: dict) -> list:
        firstLimbBreakTime = cls.__calculate_time(data["firstLimbBreakTime"])
        medianLimbBreakTime = cls.__calculate_time(data["medianLimbBreakTime"])
        lastLimbBreakTime = cls.__calculate_time(data["lastLimbBreakTime"])
        capshotTime = cls.__calculate_time(data["capshotTime"])
        shrineTime = cls.__calculate_time(data["shrineTime"])
        result = data["result"]
        return [firstLimbBreakTime, medianLimbBreakTime, lastLimbBreakTime, capshotTime, shrineTime, result]

    @staticmethod
    def __calculate_time(second) -> str:
        if not second:
            return ""
        minute, second = divmod(second, 60)
        hour, minute = divmod(minute, 60)
        hour, minute, second = int(hour), int(minute), round(second, 3)
        return f'{f"{hour}h " if hour else ""}{f"{minute}m " if minute else ""}{f"{second}s" if second else ""}'

    @classmethod
    async def nights(cls, hunter) -> BytesIO:
        """
        - hunter 查询用户的ID
        - orderby 根据什么进行排序
            - createdAt 创建时间
            - averageLastHydrolystLimbBreakTime 平均水力使倒地
            - averageRealTime 平均结算时间
            - averageExtractionTime 平均撤离时间
            - activeTime 活动时间
        - orderDirection 排序方式
            - desc 倒序
            - asc 顺序
        - capturedHydrolystsCount 只查询指定水力使捕获数量的夜晚
        - squadSize 只查询指定大小的队伍
        """

        # 146
        # Run信息区域 x 0-180 y 0-400

        url = "https://api.idalon.com/v1/nights"  # API链接
        #firstX, firstY = (143, 118)  # (1, 1)切片坐标
        #areaW, areaH = (130.5, 83.5)  # (1, 1)切片范围
        # API参数
        params = {
            "hunter": hunter,
            "orderBy": "createdAt",
            "orderDirection": "desc",
            "withRuns": "true",
            "withEidolons": "true",
            "limit": 1
        }

        # 向API发送异步请求
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                result = await client.get(url, params=params)
                if result.status_code != 200:
                    raise
            except:
                return None

        night = result.json()   # 获取字典

        # 检测数据不为空
        if not night["items"]:
            return None

        # 创建一个新的图片，用来拼接Run图片。图片宽1200，高为400xRun。
        all_image = Image.new(
            "RGB", (1200, 400*len(night["items"][0]["runs"])), (204, 204, 204))

        # for循环读取run
        for count, run in enumerate(night["items"][0]["runs"]):

            # 通过__get_run方法获取Run中所需的信息。
            runData = cls.__get_run(run)

            # 将所需信息处理为字符串。
            runC = f"Run{count+1}"
            hunters = f"{runData[3]}\n" + "\n".join(runData[4])
            loadtime = f"加载耗时：{runData[2]}"
            lastHydrolystLimbBreakTime = f"水力倒地：{runData[0]}"
            extractionTime = f"结算时间：{runData[1]}"
            string = "\n\n".join(
                [runC, hunters, loadtime, lastHydrolystLimbBreakTime, extractionTime])

            # 打开Run背景图片
            img = Image.open("./src/PIL/idalon_run.png")

            # 写入Run信息
            draw = ImageDraw.ImageDraw(img)
            Tfont = ImageFont.truetype("./src/PIL/font2.TTF", 16)
            textW, textH = draw.textsize(string, Tfont)
            draw.text((0, (400-textH)/2), string, "#FFFFFF", Tfont)

            # 逐个读取eidolon信息。
            for ecount, eidolon in enumerate(run["eidolons"]):

                # 通过__get_eidolon获取eidolon中所需信息。
                eidolonData = cls.__get_eidolon(eidolon)

                # 读取eidolonData列表的数据写入图片。
                for tcount, t in enumerate(eidolonData):
                    textW, textH = draw.textsize(t, Tfont)
                    draw.text((((130.5 - textW) / 2) + (143 + (130.5 * tcount)),
                              146 + (84*ecount)), t, "#FFFFFF", Tfont)

            all_image.paste(img, (0, 0+(400*count)))
        doneimg = BytesIO()
        all_image.save(doneimg, "png")
        return doneimg

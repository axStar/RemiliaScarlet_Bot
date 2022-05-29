str1 = """Aliceresia
匿名

加载耗时：22.18s

水力倒地：7m 3.889s

结算时间：8m 19.325s"""

from PIL import Image, ImageDraw, ImageFont

img = Image.open("./src/PIL/idalon_run.png")
draw = ImageDraw.ImageDraw(img)
font = ImageFont.truetype("./src/PIL/font2.TTF", 14)
textW, textH = draw.textsize(str1, font)
print(str1)
draw.text((0, (400-textH)/2), str1, font=font)
img.show()
from PIL import Image, ImageDraw, ImageFont




image = Image.open('bg.jpg')

draw = ImageDraw.Draw(image)

font = ImageFont.truetype('Roboto-Regular.ttf', size=10)


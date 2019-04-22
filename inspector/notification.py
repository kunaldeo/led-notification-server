import json
import subprocess

from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse

from inspector.icon_utilities import get_icon
from plexobject import settings
from wrap import split_lines


def process_notification(request):
    data = json.loads(request.body)
    # Get title and message
    title = data['title']
    message = ''
    app_name = data['appName']
    if data['bigText']:
        message = data['bigText']

    elif data['text']:
        message = data['text']

    elif data['tickerText']:
        message = data['tickerText']
    if data['subText']:
        message = '{} {}'.format(message, data['subText'])
    message = message.replace('\n', ' ').replace('\r', ' ')
    large_icon_data = data['largeIcon']['data'].encode('utf-8')
    app_icon_data = data['appIcon']['data'].encode('utf-8')
    # small_icon_data = data['smallIcon']['data'].encode('utf-8')
    image = Image.open('bg.jpg')
    (x, y) = (1, 1)
    icon_x = x
    if app_icon_data:
        icon_path = get_icon(app_icon_data)
        icon_image = Image.open(icon_path)
        icon_image.thumbnail((28, 28), Image.ANTIALIAS)
        image.paste(icon_image, (icon_x, y))
        icon_x += 32
    if large_icon_data:
        icon_path = get_icon(large_icon_data)
        icon_image = Image.open(icon_path)
        icon_image.thumbnail((28, 28), Image.ANTIALIAS)
        image.paste(icon_image, (icon_x, y))
        icon_x += 32
    # if small_icon_data:
    #     icon_path = get_icon(small_icon_data)
    #     icon_image = Image.open(icon_path)
    #     icon_image.thumbnail((28, 28), Image.ANTIALIAS)
    #     image.paste(icon_image, (icon_x, y))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('noto-sans.ttf', size=11, )
    draw.text((icon_x - 2, y + 10), app_name, fill='rgb(34,139,34)', font=font)
    title_lines = split_lines(title)
    message_lines = split_lines(message)
    line_height = 11  # Todo take this from font properties
    y = y + 29
    for line in title_lines:
        draw.text((x, y), line, fill='rgb(178,34,34)', font=font)
        y += line_height
    for line in message_lines:
        draw.text((x, y), line, fill='rgb(255,165,0)', font=font)
        y += line_height
    image.save(settings.NOTIFICATION_OUTPUT_IMAGE_PATH)
    subprocess.run([settings.SCREEN_CLEAR_COMMAND, "-C", "-g", "128x128"])
    subprocess.run(["./notify.sh"])
    return HttpResponse("Displayed")

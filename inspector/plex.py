import json
import subprocess
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse

from plexobject import settings


def process_plex(request):
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])

        metadata = payload.get('Metadata')
        event = payload.get('event')
        # player = payload.get('Player').get('title')

        if event == 'media.stop':
            subprocess.run([settings.SCREEN_CLEAR_COMMAND, "-C", "-g", "128x128"])

        elif event is not 'media.stop':
            info = {}

            image = Image.open(settings.IMAGE_BACKGROUND)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(settings.FONT_NAME, size=settings.FONT_SIZE)

            (x, y) = (1, 0)

            if metadata.get('librarySectionType') == 'show':
                info['show'] = metadata.get('grandparentTitle')
                info['season'] = metadata.get('parentTitle')
                info['thumb'] = metadata.get('parentThumb')

            elif metadata.get('librarySectionType') == 'movie':
                info['show'] = metadata.get('Genre')[0].get('tag')
                info['season'] = metadata.get('Director')[0].get('tag')
                info['rating'] = metadata.get('rating')
                info['thumb'] = metadata.get('thumb')
                info['ratingImage'] = metadata.get('ratingImage')

                rating_image_file = ""
                if info['ratingImage'].startswith('imdb'):
                    rating_image_file = 'imdb.png'
                elif info['ratingImage'].startswith('rottentomatoes'):
                    if info['ratingImage'] == 'rottentomatoes://image.rating.ripe':
                        rating_image_file = 'ripe.png'
                    elif info['ratingImage'] == 'rottentomatoes://image.rating.rotten':
                        rating_image_file = 'rotten.png'

                if metadata.get('audienceRating'):
                    audience_rating_image_file = ""
                    info['audienceRating'] = metadata.get('audienceRating')
                    info['audienceRatingImage'] = metadata.get('audienceRatingImage')
                    if info['audienceRatingImage'] == 'rottentomatoes://image.rating.upright':
                        audience_rating_image_file = "upright.png"
                    elif info['audienceRatingImage'] == 'rottentomatoes://image.rating.spilled':
                        audience_rating_image_file = "spilled.png"

                    audience_rating_image = Image.open(audience_rating_image_file)
                    image.paste(audience_rating_image, (x + 60 + 16 + 14, y + 13))
                    draw.text((x + 60 + 16 + 16 + 14, y + 13), str(info['audienceRating']), fill='rgb(255,105,180)',
                              font=font)

                rating_image = Image.open(rating_image_file)
                image.paste(rating_image, (x + 56, y + 13))
                draw.text((x + 15 + 60, y + 13), str(info['rating']), fill='rgb(255,105,180)', font=font)

            info['title'] = metadata.get('title')
            info['content_date'] = metadata.get('originallyAvailableAt')
            thumb_url = settings.PLEX_SERVER_URL + info[
                'thumb'] + "?checkFiles=1&includeExtras=1&includeBandwidths=1&X-Plex-Token=" + settings.PLEX_TOKEN
            thumb_url_response = requests.get(thumb_url)

            thumb_image = Image.open(BytesIO(thumb_url_response.content))
            thumb_image.thumbnail((128, 88), Image.ANTIALIAS)

            image.paste(thumb_image, (x + 69, y + 40))

            # color = 'rgb(255,165,0)'

            draw.text((x, y), info['title'], fill='rgb(255,165,0)', font=font)
            draw.text((x, y + 13), info['show'], fill='rgb(178,34,34)', font=font)
            draw.text((x, y + 27), info['season'], fill='rgb(34,139,34)', font=font)
            draw.text((x + 71, y + 27), info['content_date'], fill='rgb(255,105,180)', font=font)

            # Display File Info
            rating_key = metadata.get("ratingKey")
            localuri = settings.PLEX_SERVER_URL + "/library/metadata/" + rating_key + "?checkFiles=1&includeExtras=0&includeBandwidths=1&X-Plex-Token=" + settings.PLEX_TOKEN
            headers = {'Accept': 'application/json'}
            local_response = requests.get(localuri, headers=headers).json()
            file_info = local_response.get('MediaContainer').get('Metadata')[0].get('Media')[0]

            video_resolution = file_info.get('videoResolution').upper()
            video_codec = file_info.get('videoCodec').upper()
            video_profile = file_info.get('videoProfile').upper().replace('MAIN 10', 'HDR 10')
            audio_codec = file_info.get('audioCodec').upper()
            audio_channels = str(file_info.get('audioChannels'))

            draw.text((x, y + 40), video_resolution, fill='rgb(255,105,180)', font=font)
            draw.text((x, y + 55), video_codec, fill='rgb(255,105,180)', font=font)
            draw.text((x, y + 70), video_profile, fill='rgb(255,105,180)', font=font)
            draw.text((x, y + 85), audio_codec, fill='rgb(255,105,180)', font=font)
            draw.text((x + 50, y + 85), audio_channels, fill='rgb(255,105,180)', font=font)

            image.save(settings.PLEX_OUTPUT_IMAGE_PATH)

            subprocess.run([settings.PLEX_OUTPUT_SCRIPT_PATH])
    return HttpResponse("Handled Webhook & generated image")

import base64
import hashlib
import os

from plexobject.settings import ICON_CACHE_DIR


def get_icon(icon_data):
    icon = icon_data
    icon_path = os.path.join(ICON_CACHE_DIR,
                             hashlib.md5(icon_data).hexdigest())

    if not os.path.exists(icon_path):
        with open(icon_path, 'wb') as f:
            f.write(base64.decodebytes(icon))

    return icon_path

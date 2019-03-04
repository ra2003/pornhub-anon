import os
from pathlib import Path

STOP_TAGS = {
    'cartoon',
    'animation',
    'drawn',
    'hentai'
    'alien',
    '3d',
    'famous',
}

HOME_DIR = Path.home()
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

FIND_LINK_LOCK = 2
DOWNLOAD_LOCK = 10
SOURCE_PATH = str(HOME_DIR.joinpath('pornanon-sources'))
FACES_PATH = str(HOME_DIR.joinpath('pornanon-faces'))
TMP_PATH = '/tmp/pornanon'
FIND_LINK_TIMEOUT = 15
DOWNLOAD_TIMEOUT = 65

HAAR_CASCADE_XML = os.path.join(CURRENT_DIR, '..', 'data', 'haarcascade_frontalface_default.xml')
LBP_CASCADE_XML = os.path.join(CURRENT_DIR, '..', 'data', 'lbpcascade_frontalface_improved.xml')
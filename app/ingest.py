from pathlib import Path
from app.logger import logger
from app.metadata import read_metadata
from app.normalize import normalize
from app.musicbrainz import enrich
from app.language import detect_language
from app.scoring import score
from app.hash import sha256
from app.pipeline import process

SUPPORTED_EXTENSIONS = {
    ".mp3",
    ".flac",
    ".m4a",
    ".ogg",
    ".aac",
    ".wma",
}


#def find_audio_files(root: str):

#    root = Path(root)

#    for file in root.rglob("*"):
#        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
#            yield file

def find_audio_files(root: str):

    root = Path(root)

    if root.is_file():

        if root.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield root

        return

    for file in root.rglob("*"):

        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield file



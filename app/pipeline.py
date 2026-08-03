from app.metadata import read_metadata
from app.normalize import normalize
from app.musicbrainz import enrich
from app.language import detect_language
from app.scoring import score
from app.hash import sha256
from app.hash import calculate_hash
from app.acoustid import enrich as acoustid
from app.logger import logger
from app.publisher import publish
from app.duplicates import check

#def calculate_hash(track):
#    track.file_hash = sha256(track.source_path)
#    return track


PIPELINE = [
    normalize,
    #lookup_track,
    enrich,
    normalize,
    detect_language,
    calculate_hash,
    check,
    score,
    acoustid,
    score,
    publish,
]


def process(filename):

    track = read_metadata(str(filename))

    for stage in PIPELINE:
        track = stage(track)

        if track.status in ("FAILED","DUPLICATE"):
             break

    return track

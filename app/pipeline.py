from app.metadata import read_metadata
from app.normalize import normalize
from app.musicbrainz import lookup_track
from app.language import detect_language
from app.scoring import score
from app.hash import sha256


def calculate_hash(track):
    track.file_hash = sha256(track.source_path)
    return track


PIPELINE = [
    normalize,
    lookup_track,
    detect_language,
    calculate_hash,
    score,
]


def process(filename):

    track = read_metadata(str(filename))

    for stage in PIPELINE:
        track = stage(track)

    return track

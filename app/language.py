from app.models import Track
from app.logger import logger

ARTIST_LANGUAGE = {
    "michael learns to rock": ("English", 100),
    "michael jackson": ("English", 100),
    "a. r. rahman": ("Mixed", 60),
    "lata mangeshkar": ("Mixed", 50),
}


def detect_language(track: Track) -> Track:

    artist = (track.artist or "").strip().lower()

    if artist in ARTIST_LANGUAGE:
        language, confidence = ARTIST_LANGUAGE[artist]

        track.language = language
        track.language_confidence = confidence
        track.language_source = "artist-rule"

    else:
        track.language = "Unknown"
        track.language_confidence = 0
        track.language_source = "unknown"

    return track

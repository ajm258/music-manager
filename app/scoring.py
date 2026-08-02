from app.models import Track
from app.logger import logger

REQUIRED_FIELDS = [
    "title",
    "artist",
    "album",
    "album_artist",
    "year",
    "genre",
    "language",
]


def score(track: Track) -> Track:

    total = len(REQUIRED_FIELDS)
    passed = 0

    for field in REQUIRED_FIELDS:
        value = getattr(track, field)

        if value not in (None, "", "Unknown"):
            passed += 1

    track.metadata_score = round((passed / total) * 100)

    if track.metadata_score < 90:
        track.needs_review = True

    return track

from pathlib import Path
from mutagen import File

from app.models import Track


def _tag(audio, *names):
    """Return the first matching tag value."""
    if audio is None or audio.tags is None:
        return None

    for name in names:
        if name in audio.tags:
            value = audio.tags[name]

            if isinstance(value, list):
                value = value[0]

            return str(value)

    return None


def read_metadata(filename: str) -> Track:

    audio = File(filename, easy=True)

    track = Track(
        source_path=filename,
        filename=Path(filename).name,
    )

    if audio is None:
        return track

    track.title = _tag(audio, "title")
    track.artist = _tag(audio, "artist")
    track.album = _tag(audio, "album")
    track.album_artist = _tag(audio, "albumartist")
    track.genre = _tag(audio, "genre")
    track.year = _tag(audio, "date")

    if audio.info:
        track.duration = round(audio.info.length, 1)

        if hasattr(audio.info, "bitrate"):
            track.bitrate = int(audio.info.bitrate / 1000)

    track.codec = audio.mime[0] if hasattr(audio, "mime") else None

    return track

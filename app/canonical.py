from dataclasses import dataclass


@dataclass
class CanonicalMetadata:

    title: str
    artist: str
    album: str
    year: int | None
    recording_id: str
    release_id: str

def build(recording, release):

    year = None

    if release.get("date"):
        year = int(release["date"][:4])

    return CanonicalMetadata(
        title=recording["title"],
        artist=recording["artist-credit-phrase"],
        album=release["title"],
        year=year,
        recording_id=recording["id"],
        release_id=release["id"],
    )

def compare(track, canonical):

    changes = {}

    if track.title != canonical.title:
        changes["title"] = (track.title, canonical.title)

    if track.artist != canonical.artist:
        changes["artist"] = (track.artist, canonical.artist)

    if track.album != canonical.album:
        changes["album"] = (track.album, canonical.album)

    if track.year != canonical.year:
        changes["year"] = (track.year, canonical.year)

    return changes

def apply(track, canonical):

    # Safe updates
    track.artist = canonical.artist

    # Leave these untouched for now
    # track.title = canonical.title
    # track.album = canonical.album
    # track.year = canonical.year

    return track

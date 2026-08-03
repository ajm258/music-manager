import musicbrainzngs
from app.logger import logger
from app.config import CONFIG
from pprint import pprint
from app.mbresolver import resolve
from app.canonical import build
from app.canonical import apply

musicbrainzngs.set_useragent(
    CONFIG["musicbrainz"]["app_name"],
    CONFIG["musicbrainz"]["version"],
    CONFIG["musicbrainz"]["email"],
)

from app.models import Track


def enrich(track: Track) -> Track:
    try:
        result = musicbrainzngs.search_recordings(
            artist=track.artist,
            recording=track.title,
            release=track.album,
            limit=10,
        )

        recordings = result.get("recording-list", [])

        if not recordings:
            return track

        #recording = recordings[0]
   
        recording, confidence = resolve(
               track,
               recordings,
        )

        track.mb_recording_id = recording.get("id")

        releases = recording.get("release-list", [])
        if releases:
            track.mb_release_id = releases[0].get("id")

    except Exception as e:
        print(f"MusicBrainz lookup failed: {e}")

    #return track
    return canonical(track)


def get_recording(recording_id):
    result = musicbrainzngs.get_recording_by_id(
        recording_id,
        includes=[
            "artists",
            "releases",
        ],
    )

    return result["recording"]
    pprint(result)
    return result

def get_release(release_id):

    result = musicbrainzngs.get_release_by_id(
        release_id,
        includes=[
            "artists",
        ],
    )

    return result["release"]

def canonical(track):

    if not track.mb_recording_id or not track.mb_release_id:
        return track

    recording = get_recording(track.mb_recording_id)
    release = get_release(track.mb_release_id)

    #return build(recording, release)
    canonical = build(recording, release)

    apply(track, canonical)

    return track

def apply(track, canonical):

    if track.title.lower() == canonical.title.lower():
        track.title = canonical.title

    if track.artist.lower() == canonical.artist.lower():
        track.artist = canonical.artist

    if track.album.lower() == canonical.album.lower():
        track.album = canonical.album

    # Don't update year automatically

    return track

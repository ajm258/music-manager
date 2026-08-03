import musicbrainzngs
from app.logger import logger
from app.config import CONFIG
from pprint import pprint
from app.mbresolver import resolve
from app.canonical import build
from app.canonical import apply
import logging

#logging.getLogger("musicbrainzngs.mbxml").setLevel(logging.ERROR)
#logging.getLogger("musicbrainzngs.musicbrainz").setLevel(logging.ERROR)

logging.getLogger("music-manager").setLevel(logging.ERROR)
logging.getLogger("musicbrainzngs").setLevel(logging.ERROR)


#import logging

#for name in logging.root.manager.loggerDict:
#    print(name)

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

        if recording is None or confidence < 80:
             return track

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

def same(a, b):
    return (a or "").casefold() == (b or "").casefold()


def apply(track, canonical):

    if not same(track.title, canonical.title):
        track.title = canonical.title

    if not same(track.artist, canonical.artist):
        track.artist = canonical.artist

    if not same(track.album, canonical.album):
        track.album = canonical.album

    if track.year != canonical.year:
        track.year = canonical.year

    track.mb_recording_id = canonical.recording_id
    track.mb_release_id = canonical.release_id

    return track

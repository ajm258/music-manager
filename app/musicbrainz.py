import logging
import time

import musicbrainzngs

from app.canonical import apply, build
from app.config import CONFIG
from app.logger import logger
from app.mbresolver import resolve
from app.models import Track

logging.getLogger("music-manager").setLevel(logging.ERROR)
logging.getLogger("musicbrainzngs").setLevel(logging.ERROR)

musicbrainzngs.set_useragent(
    CONFIG["musicbrainz"]["app_name"],
    CONFIG["musicbrainz"]["version"],
    CONFIG["musicbrainz"]["email"],
)


def enrich(track: Track) -> Track:

    try:

        start = time.perf_counter()

        result = musicbrainzngs.search_recordings(
            artist=track.artist,
            recording=track.title,
            release=track.album,
            limit=10,
        )

        print(f"search_recordings : {time.perf_counter() - start:.3f}s")

        recordings = result.get("recording-list", [])

        if not recordings:
            return track

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

        logger.exception("MusicBrainz lookup failed")

        return track

    return canonical(track)


def get_recording(recording_id):

    start = time.perf_counter()

    result = musicbrainzngs.get_recording_by_id(
        recording_id,
        includes=[
            "artists",
            "releases",
        ],
    )

    print(f"get_recording    : {time.perf_counter() - start:.3f}s")

    return result["recording"]


def get_release(release_id):

    start = time.perf_counter()

    result = musicbrainzngs.get_release_by_id(
        release_id,
        includes=[
            "artists",
        ],
    )

    print(f"get_release      : {time.perf_counter() - start:.3f}s")

    return result["release"]


def canonical(track):

    if not track.mb_recording_id or not track.mb_release_id:
        return track
    start = time.perf_counter()
    recording = get_recording(track.mb_recording_id)
    print(f"get_recording: {time.perf_counter() - start:.3f}s")

    start = time.perf_counter()
    release = get_release(track.mb_release_id)
    print(f"get_release: {time.perf_counter() - start:.3f}s")

    canonical = build(recording, release)

    apply(track, canonical)

    return track

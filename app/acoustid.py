import subprocess
import acoustid
from app.logger import logger

from app.config import CONFIG
from app.resolver import resolve


def fingerprint(filename):

    result = subprocess.run(
        ["fpcalc", filename],
        capture_output=True,
        text=True,
        check=True,
    )

    duration = None
    fingerprint = None

    for line in result.stdout.splitlines():

        if line.startswith("DURATION="):
            duration = int(line.split("=")[1])

        elif line.startswith("FINGERPRINT="):
            fingerprint = line.split("=", 1)[1]

    return duration, fingerprint


def identify(duration, fingerprint):

    api_key = CONFIG["acoustid"]["api_key"]

    return acoustid.lookup(
        api_key,
        fingerprint,
        duration,
        meta="recordings",
    )


from app.resolver import resolve


def enrich(track):

    if track.metadata_score >= 95:
        return track

    duration, fp = fingerprint(track.source_path)

    result = identify(duration, fp)

    candidates = []

    for r in result["results"]:
        candidates.extend(r.get("recordings", []))

    if not candidates:
        return track

    # resolved = resolve(track, candidates)

    # track.mb_recording_id = resolved["candidate"]["id"]
    # track.identification_confidence = resolved["score"]
    # track.review_reason = resolved["review_reason"]

    best, score = resolve(track, candidates)

    track.mb_recording_id = best["id"]
    track.identification_confidence = score

    return track

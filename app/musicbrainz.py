import musicbrainzngs

from app.models import Track

musicbrainzngs.set_useragent("music-manager", "0.1", "amit@example.com")


def lookup_track(track: Track) -> Track:
    try:
        result = musicbrainzngs.search_recordings(
            artist=track.artist,
            recording=track.title,
            release=track.album,
            limit=1,
        )

        recordings = result.get("recording-list", [])

        if not recordings:
            return track

        recording = recordings[0]

        track.mb_recording_id = recording.get("id")

        releases = recording.get("release-list", [])
        if releases:
            track.mb_release_id = releases[0].get("id")

    except Exception as e:
        print(f"MusicBrainz lookup failed: {e}")

    return track

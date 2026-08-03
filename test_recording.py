from pprint import pprint
from app.musicbrainz import get_recording

recording = get_recording(
    "92e3c9b3-34a0-4f66-b519-29817f5325df"
)

pprint(recording)

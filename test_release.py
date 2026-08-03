from pprint import pprint
from app.musicbrainz import get_release

release = get_release(
    "2246c2e9-d6dc-41a5-a374-83ab84625aed"
)

pprint(release)

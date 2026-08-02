# test_acoustid.py

from pprint import pprint

from app.acoustid import identify

result = identify(
    "/srv/pool/media/music/work/MLTR/06.( Colours ) MLTR - 25 Minutes.mp3"
)

pprint(result)

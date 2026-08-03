from pprint import pprint

from app.pipeline import process
from app.musicbrainz import canonical
from app.canonical import compare

track = process("/srv/pool/media/music/work/MLTR/06.( Colours ) MLTR - 25 Minutes.mp3")

changes = compare(track, canonical(track))

print(changes)
#pprint(canonical(track))

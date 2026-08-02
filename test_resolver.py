from pprint import pprint

from app.acoustid import identify
from app.metadata import read_metadata
from app.normalize import normalize
from app.resolver import resolve

filename = "/srv/pool/media/music/work/MLTR/06.( Colours ) MLTR - 25 Minutes.mp3"

track = normalize(read_metadata(filename))

result = identify(filename)

# Flatten all recordings returned by AcoustID
candidates = []

for acoustid_result in result["results"]:
    candidates.extend(acoustid_result.get("recordings", []))

best, score = resolve(track, candidates)

print(f"Resolver score: {score}")
print()
#print
pprint(best)


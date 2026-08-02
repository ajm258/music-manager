from app.pipeline import process
from app.publisher import destination

track = process(
    "/srv/pool/media/music/work/MLTR/06.( Colours ) MLTR - 25 Minutes.mp3"
)

print(track)

print(destination(track))

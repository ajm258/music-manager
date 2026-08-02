from app.acoustid import fingerprint

duration, fp = fingerprint(
    "/srv/pool/media/music/work/MLTR/06.( Colours ) MLTR - 25 Minutes.mp3"
)

print(duration)
print(len(fp))

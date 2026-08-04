from dataclasses import asdict
import pprint

from app.database import Database
from app.ingest import find_audio_files
from app.pipeline import process

db = Database()

count = 0

for file in find_audio_files("/srv/pool/media/music/work"):

    print(f"Processing: {file.name}")

    try:

        track = process(file)
        start = time.perf_counter()
        db.save_track(track)
        print(time.perf_counter() - start)
        count += 1

    except Exception as e:

        print(f"FAILED: {e}")

db.close()

print()
print(f"Processed {count} tracks.")

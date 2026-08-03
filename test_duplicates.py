from app.database import Database
from app.duplicates import exact_duplicates, recording_duplicates

db = Database()

tracks = db.get_tracks()

print("Exact duplicates")
print("================")
print(exact_duplicates(tracks))

print()

print("Recording duplicates")
print("====================")
print(recording_duplicates(tracks))

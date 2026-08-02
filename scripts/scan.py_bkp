import pprint
import sys
from dataclasses import asdict

from app.database import Database
from app.language import detect_language
from app.metadata import read_metadata
from app.normalize import normalize
from app.scoring import score
from app.musicbrainz import lookup_track
from app.hash import sha256

track = read_metadata(sys.argv[1])
track.file_hash = sha256(track.source_path)
track = normalize(track)
track = lookup_track(track)
track = detect_language(track)
track = score(track)

db = Database()
db.save_track(track)
db.close()

pprint.pp(asdict(track))

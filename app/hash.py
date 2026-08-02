import hashlib
from app.logger import logger

def sha256(filename: str) -> str:

    h = hashlib.sha256()

    with open(filename, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()

def calculate_hash(track):
    track.file_hash = sha256(track.source_path)
    return track

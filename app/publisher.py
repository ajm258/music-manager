from pathlib import Path
from app.logger import logger
from app.config import CONFIG
import shutil
import re
from app.artwork import download

def destination(track):

    language = track.language or "Unknown"

    artist = track.artist or "Unknown Artist"

    title = track.title or track.filename

    filename = f"{title} - {artist}.mp3"

    return Path(language) / filename



def safe(text):

    text = re.sub(r'[<>:"/\\|?*]', "_", text)

    return text.strip()


def publish(track):

    print(f"Publisher status: {track.status}")
    print(f"--------------------------------") 

    if track.status == "DUPLICATE":
         logger.info("Skipping duplicate: %s", track.source_path)
         return track


    destination_path = (
        Path(CONFIG["library"]["publish"])
        / destination(track)
    )

    destination_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        track.source_path,
        destination_path,
    )

    if track.mb_release_id:
        track.artwork = download(
           track.mb_release_id,
       )

    track.library_path = str(destination_path)

    return track

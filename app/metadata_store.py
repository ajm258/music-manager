from pathlib import Path

from app.config import CONFIG


ROOT = Path(CONFIG["library"]["metadata"])


def artwork_path(release_id):

    path = ROOT / "artwork"

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path / f"{release_id}.jpg"


def lyrics_path(recording_id):

    path = ROOT / "lyrics"

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path / f"{recording_id}.lrc"


def replaygain_path(recording_id):

    path = ROOT / "replaygain"

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path / f"{recording_id}.json"

def artwork_exists(release_id):

    artwork = artwork_path(release_id)

    return artwork.exists()

import requests
from app.metadata_store import artwork_path

def download(release_id):

    if not release_id:
        return False

    artwork = artwork_path(release_id)

    if artwork.exists():
        return True

    url = f"https://coverartarchive.org/release/{release_id}/front"

    try:

        response = requests.get(
            url,
            timeout=10,
        )

        if response.status_code != 200:
            return False

        artwork = artwork_path(release_id)

        artwork.write_bytes(response.content)

        return True

    except Exception:
        return False

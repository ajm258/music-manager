from app.models import Track


GENRES = {
    "Classic Rock": "Rock",
    "Classic rock": "Rock",
    "Classic-Rock": "Rock",
    "Pop/Rock": "Rock",
    "Rhythm & Blues": "R&B",
    "Rnb": "R&B",
}


def enrich(track: Track) -> Track:

    if not track.genre:
        return track

    genre = track.genre.strip()

    track.genre = GENRES.get(
        genre,
        genre,
    )

    return track

from app.models import Track

ARTIST_ALIASES = {
    "MLTR": "Michael Learns To Rock",
    "Mltr": "Michael Learns To Rock",
    "MJ": "Michael Jackson",
    "ACDC": "AC/DC",
}


def normalize(track: Track) -> Track:

    #def clean(value):

    #if value is None:
     #   return None

    #return value.strip()
    def clean(value):
        return value.strip() if value else None
    #track.title = track.title.strip()
    #track.artist = track.artist.strip()
    #track.album = track.album.strip()

    if track.artist in ARTIST_ALIASES:
        track.artist = ARTIST_ALIASES[track.artist]

    if track.album_artist in ARTIST_ALIASES:
        track.album_artist = ARTIST_ALIASES[track.album_artist]

    if track.year:
        try:
            track.year = int(str(track.year)[:4])
        except ValueError:
            track.year = None

    return track

from app.models import Track

# Initial artist rules (will grow over time)
ARTIST_LANGUAGE = {
    "Michael Learns To Rock": ("English", 100),
    "Michael Jackson": ("English", 100),
    "A. R. Rahman": ("Mixed", 60),  # many languages
    "Lata Mangeshkar": ("Mixed", 50),
}


def detect_language(track: Track) -> Track:
    if track.artist in ARTIST_LANGUAGE:
        language, confidence = ARTIST_LANGUAGE[track.artist]

        track.language = language
        track.language_confidence = confidence
        track.language_source = "artist-rule"

    else:
        track.language = "Unknown"
        track.language_confidence = 0
        track.language_source = "unknown"

    return track

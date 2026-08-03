from dataclasses import dataclass
from typing import Optional


@dataclass
class Track:
    source_path: str

    filename: str

    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    album_artist: Optional[str] = None

    year: Optional[int] = None
    genre: Optional[str] = None

    duration: Optional[float] = None
    bitrate: Optional[int] = None
    codec: Optional[str] = None

    mb_recording_id: Optional[str] = None
    mb_release_id: Optional[str] = None

    artwork: str | None = None

    language: Optional[str] = None
    language_confidence: int = 0
    language_source: Optional[str] = None

    file_hash: str | None = None

    metadata_score: int = 0
    status: str = "NEW"

    needs_review: bool = False

    acoustid: str | None = None
    mood: str | None = None
    subgenre: str | None = None
    review_reason: str | None = None

    identification_confidence: int = 0

    fingerprint: str | None = None
    library_path: str | None = None

    replaygain_track_gain: float | None = None
    replaygain_track_peak: float | None = None

    replaygain_album_gain: float | None = None
    replaygain_album_peak: float | None = None

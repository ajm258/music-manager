import sqlite3
from dataclasses import asdict
from app.logger import logger
from app.models import Track
from app.config import CONFIG

DB_FILE = CONFIG["database"]["path"]

TRACK_COLUMNS = [
    "source_path",
    "filename",
    "title",
    "artist",
    "album",
    "album_artist",
    "year",
    "genre",
    "language",
    "language_confidence",
    "language_source",
    "duration",
    "bitrate",
    "codec",
    "mb_recording_id",
    "mb_release_id",
    "artwork",
    "replaygain_track_gain",
    "replaygain_track_peak",
    "replaygain_album_gain",
    "replaygain_album_peak",
    "metadata_score",
    "status",
    "file_hash",
    "acoustid",
    "fingerprint",
    "mood",
    "subgenre",
    "review_reason",
    "identification_confidence",
]



class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

    def save_track(self, track: Track):

        data = asdict(track)
        columns = ", ".join(TRACK_COLUMNS)
        placeholders = ", ".join(f":{c}" for c in TRACK_COLUMNS)
        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT id FROM tracks WHERE file_hash = ?",
            (track.file_hash,),
        )

        row = cursor.fetchone()

        if row:

            data["id"] = row["id"]

            cursor.execute(
                """
                UPDATE tracks
                SET
                    source_path=:source_path,
                    filename=:filename,
                    title=:title,
                    artist=:artist,
                    album=:album,
                    album_artist=:album_artist,
                    year=:year,
                    genre=:genre,
                    language=:language,
                    language_confidence=:language_confidence,
                    language_source=:language_source,
                    duration=:duration,
                    bitrate=:bitrate,
                    codec=:codec,
                    mb_recording_id=:mb_recording_id,
                    mb_release_id=:mb_release_id,
                    artwork=:artwork,
                    file_hash=:file_hash,
                    metadata_score=:metadata_score,
                    status=:status,
                    identification_confidence=:identification_confidence
                WHERE id=:id
                """,
                data,
            )

        else:

            cursor.execute(
               f"""
               INSERT INTO tracks
               (
                   {columns}
               )
               VALUES
               (
                   {placeholders}
               )
               """,
               data,
            )

        self.conn.commit()

    #    def close(self):
    #        self.conn.close()

    # from dataclasses import fields

    def get_tracks(self):

        cursor = self.conn.cursor()

        cursor.execute(
              f"""
              SELECT
                 {", ".join(TRACK_COLUMNS)}
              FROM tracks
              """
        )

        rows = cursor.fetchall()

        return [Track(**dict(row)) for row in rows]

    def close(self):
        self.conn.close()

    def get_track_by_hash(self, file_hash):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                file_hash,
                mb_recording_id,
                source_path,
                status
            FROM tracks
            WHERE file_hash = ?
            """,
            (file_hash,),
        )

        return cursor.fetchone()

    def get_track_by_recording(self, recording_id):

        if not recording_id:
            return None

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                filename,
                mb_recording_id,
                file_hash,
                status
            FROM tracks
            WHERE mb_recording_id = ?
            """,
            (recording_id,),
        )

        return cursor.fetchone()

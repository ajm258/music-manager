import sqlite3
from dataclasses import asdict

from app.models import Track

DB_FILE = "/srv/apps/music-manager/database/music.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

    def save_track(self, track: Track):
        data = asdict(track)
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
                    status=:status
                WHERE id=:id
                """,
                data,
            )

        else:
            cursor.execute(
                """
                INSERT INTO tracks
                (
                    source_path,
                    filename,
                    title,
                    artist,
                    album,
                    album_artist,
                    year,
                    genre,
                    language,
                    language_confidence,
                    language_source,
                    duration,
                    bitrate,
                    codec,
                    mb_recording_id,
                    mb_release_id,
                    artwork,
                    file_hash,
                    metadata_score,
                    status
                )
                VALUES
                (
                    :source_path,
                    :filename,
                    :title,
                    :artist,
                    :album,
                    :album_artist,
                    :year,
                    :genre,
                    :language,
                    :language_confidence,
                    :language_source,
                    :duration,
                    :bitrate,
                    :codec,
                    :mb_recording_id,
                    :mb_release_id,
                    :artwork,
                    :file_hash,
                    :metadata_score,
                    :status
                )
                """,
                data,
            )

        self.conn.commit()

    def close(self):
        self.conn.close()

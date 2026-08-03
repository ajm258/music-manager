from app.database import Database


def check(track):

    db = Database()

    # Exact duplicate
    existing = db.get_track_by_hash(track.file_hash)
    print(track.file_hash)
    print(existing)
    if existing:
        db.close()
        track.status = "DUPLICATE"
        track.review_reason = "Exact file already exists"
        return track

    # Same recording
    existing = db.get_track_by_recording(track.mb_recording_id)


    print(existing)

    if existing:
        db.close()
        track.status = "DUPLICATE"
        track.review_reason = "Recording already exists"
        return track

    db.close()

    return track

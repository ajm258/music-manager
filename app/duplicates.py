from collections import defaultdict


def group_by(tracks, field):

    groups = defaultdict(list)

    for track in tracks:

        value = getattr(track, field)

        if not value:
            continue

        groups[value].append(track)

    return {
        key: value
        for key, value in groups.items()
        if len(value) > 1
    }


def exact_duplicates(tracks):
    return group_by(tracks, "file_hash")


def recording_duplicates(tracks):
    return group_by(tracks, "mb_recording_id")

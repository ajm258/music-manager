from difflib import SequenceMatcher


def similarity(a, b):
    if not a or not b:
        return 0

    return SequenceMatcher(
        None,
        str(a).lower(),
        str(b).lower()
    ).ratio()

def score_candidate(track, candidate):

    score = 0

    # Title (40)
    title = candidate.get("title")

    score += similarity(track.title, title) * 40

    # Artist (30)
    artists = candidate.get("artists", [])

    if artists:
        artist = artists[0]["name"]
        score += similarity(track.artist, artist) * 30

    # Duration (20)
    duration = candidate.get("duration")

    if duration:

        diff = abs(track.duration - duration)

        if diff < 1:
            score += 20
        elif diff < 2:
            score += 15
        elif diff < 5:
            score += 10

    return score

def resolve(track, candidates):

    best = None
    best_score = -1

    for candidate in candidates:

        score = score_candidate(track, candidate)

        if score > best_score:
            best = candidate
            best_score = score

    return best, round(best_score, 1)

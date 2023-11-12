KEYS = (
    "C",
    "C♯/D♭",
    "D",
    "D♯/E♭",
    "E",
    "F",
    "F♯/G♭",
    "G",
    "G♯/A♭",
    "A",
    "A♯/B♭",
    "B",
)

MODES = ("minor", "major")


def get_spotify_friendly_key(key: str):
    return KEYS.index(key)


def get_spotify_friendly_mode(mode: str):
    return MODES.index(mode)

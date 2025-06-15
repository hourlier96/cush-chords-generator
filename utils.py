from constants import MODES_DATA, NOTES, ROMAN_DEGREES, CORE_QUALITIES


def get_note_index(note_str):
    note_map = {
        "DB": "C#",
        "EB": "D#",
        "FB": "E",
        "GB": "F#",
        "AB": "G#",
        "BB": "A#",
        "B#": "C",
    }
    clean_note = (
        note_str.upper()
        .replace("♭", "B")
        .split("M")[0]
        .split("m")[0]
        .split("°")[0]
        .split("dim")[0]
        .split("7")[0]
        .split("ø")[0]
    )
    if clean_note == "CB":
        return 11
    if clean_note in note_map:
        clean_note = note_map[clean_note]
    if len(clean_note) > 1 and clean_note[1] in ["#", "B"]:
        return NOTES.index(clean_note[:2])
    return NOTES.index(clean_note[0])


def get_note_from_index(index):
    return NOTES[index % 12]


def parse_chord(chord_name):
    chord_name_c = chord_name.strip()
    root_index = get_note_index(chord_name_c)
    if "maj7" in chord_name_c or "M7" in chord_name_c:
        return root_index, "maj7"
    if "m7b5" in chord_name_c or "ø" in chord_name_c:
        return root_index, "m7b5"
    if "dim7" in chord_name_c or "°7" in chord_name_c:
        return root_index, "dim7"
    if "m7" in chord_name_c:
        return root_index, "m7"
    if "7" in chord_name_c:
        return root_index, "7"
    if "dim" in chord_name_c or "°" in chord_name_c:
        return root_index, "d"
    if "m" in chord_name_c:
        return root_index, "m"
    return root_index, "M"


def get_roman_numeral(chord_name, tonic_index, mode_name):
    chord_index, chord_quality = parse_chord(chord_name)
    interval = (chord_index - tonic_index + 12) % 12
    mode_intervals, mode_qualities, _ = MODES_DATA[mode_name]
    if interval in mode_intervals:
        degree_index = mode_intervals.index(interval)
        base_numeral = ROMAN_DEGREES[degree_index]
        if CORE_QUALITIES.get(mode_qualities[degree_index]) in ["minor", "diminished"]:
            base_numeral = base_numeral.lower()
        quality_map = {"maj7": "maj7", "m7": "m7", "7": "7", "m7b5": "ø7", "dim7": "°7"}
        suffix = quality_map.get(chord_quality, "")
        return base_numeral + suffix
    return f"({chord_name})"


def get_diatonic_7th_chord(degree, key_tonic_index, mode_name="Ionian"):
    mode_intervals, mode_qualities, _ = MODES_DATA[mode_name]
    chord_root_index = (key_tonic_index + mode_intervals[degree - 1]) % 12
    quality = mode_qualities[degree - 1]
    name = get_note_from_index(chord_root_index)
    suffix_map = {
        "maj7": "maj7",
        "m7": "m7",
        "7": "7",
        "m7b5": "m7b5",
    }
    return name + suffix_map.get(quality, "")


def is_chord_compatible(chord_quality, expected_quality):
    """
    Verifie si un accord est compatible avec ce qui est attendu.
    (Cette fonction est correcte et a ete la cle du succès)
    """
    if chord_quality == expected_quality:
        return True
    if chord_quality == "M" and (expected_quality == "maj7" or expected_quality == "7"):
        return True
    if chord_quality == "m" and expected_quality == "m7":
        return True
    if chord_quality == "d" and expected_quality == "m7b5":
        return True
    return False


def format_chords_for_table(chords, width=7):
    if isinstance(chords, str):
        chords_list = chords.split(" - ")
    else:
        chords_list = chords
    formatted = [f"{chord:<{width}}" for chord in chords_list]
    return " ".join(formatted)

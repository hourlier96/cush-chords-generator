# -*- coding: utf-8 -*-
from tabulate import tabulate
from utils import (
    format_chords_for_table,
    get_note_index,
    get_note_from_index,
    get_roman_numeral,
    parse_chord,
    get_diatonic_7th_chord,
    is_chord_compatible,
)
from constants import MODES_DATA, ROMAN_DEGREES


def detect_intelligent_mode(progression, tonic=None):
    """
    Detects the most probable mode of a chord progression.
    Returns the tonic index and the mode name.
    """
    if not progression:
        return get_note_index("C"), "Ionian"

    prog_parsed = [parse_chord(c) for c in progression]
    perfect_matches = []

    for tonic_idx in range(12):
        for mode_name in [
            "Ionian",
            "Dorian",
            "Phrygian",
            "Lydian",
            "Mixolydian",
            "Aeolian",
            "Locrian",
        ]:
            intervals, qualities, _ = MODES_DATA[mode_name]
            is_a_match = True
            chord_degrees = []

            for c_idx, c_qual in prog_parsed:
                interval = (c_idx - tonic_idx + 12) % 12
                if interval not in intervals:
                    is_a_match = False
                    break
                degree_index = intervals.index(interval)
                expected_quality = qualities[degree_index]
                if not is_chord_compatible(c_qual, expected_quality):
                    is_a_match = False
                    break
                chord_degrees.append(degree_index)

            if is_a_match:
                score = 0

                # Criterion 1: First chord is the I chord
                if chord_degrees and chord_degrees[0] == 0:
                    score += 3

                # Criterion 2: V -> I cadence
                for i in range(len(chord_degrees) - 1):
                    if chord_degrees[i] == 4 and chord_degrees[i + 1] == 0:
                        score += 2

                # Criterion 3: Progression ends on I
                if chord_degrees and chord_degrees[-1] == 0:
                    score += 1

                # Criterion 4: Presence of the V chord
                if 4 in chord_degrees:
                    score += 0.5

                # Criterion 5: The first chord root matches the candidate tonic
                if prog_parsed[0][0] == tonic_idx:
                    score += 2

                # Criterion 6: Bonus for 2 - 5 - 1 progression
                if (
                    len(chord_degrees) >= 3
                    and chord_degrees[-3] == 1
                    and chord_degrees[-2] == 4
                    and chord_degrees[-1] == 0
                ):
                    score += 5

                # Criterion 7: Typical Mixolydian signature I7 → IVmaj7 → bVIImaj7
                if (
                    len(prog_parsed) >= 3
                    and chord_degrees[:3] == [0, 3, 6]  # I - IV - bVII
                    and progression[0].endswith("7")  # dominant 7
                    and progression[1].endswith("maj7")
                    and progression[2].endswith("maj7")
                ):
                    score += 5

                # Criterion 8: Presence of an I7 (dominant on the tonic)
                if chord_degrees[0] == 0 and progression[0].endswith("7"):
                    score += 2

                # Criterion 9: Anatole progression I - vi - ii - V
                if len(chord_degrees) >= 4 and chord_degrees[:4] == [0, 5, 1, 4]:
                    score += 4

                perfect_matches.append(
                    {"tonic": tonic_idx, "mode": mode_name, "score": score}
                )
    # If a tonic is provided, we return the first match
    if tonic:
        tonic_index = get_note_index(tonic)
        for match in perfect_matches:
            if match["tonic"] == tonic_index:
                return match["tonic"], match["mode"]

    # for match in perfect_matches:
    #     print(
    #         f"Match: Tonic {get_note_from_index(match['tonic'])}, Mode {match['mode']}, Score {match['score']}"
    #     )
    if not perfect_matches:
        print("No mode found, can't give any substitution.")
        exit(1)

    # Sort by descending score
    best_match = sorted(perfect_matches, key=lambda m: -m["score"])[0]
    return best_match["tonic"], best_match["mode"]


def create_substitution_table(base_progression, tonic=None):
    if tonic and tonic not in base_progression:
        print(
            f"Warning: Tonic '{tonic}' not found in the progression. Using default tonic '{base_progression[0]}'."
        )
        tonic = None

    if not base_progression or len(base_progression) < 2:
        print("The progression is empty or too short.")
        return

    # Use the new intelligent detector
    detected_tonic_index, original_mode = detect_intelligent_mode(
        base_progression, tonic
    )
    print("\nTonic:", tonic if tonic else base_progression[0])
    tonic_name = get_note_from_index(detected_tonic_index)

    # Try to find the exact tonic chord in the progression
    tonic_chord_in_prog = next(
        (c for c in base_progression if get_note_index(c) == detected_tonic_index),
        tonic_name,
    )

    print(f"Analyzing progression '{' -> '.join(base_progression)}'")
    print(f"Most probable mode : {tonic_name} {original_mode}")

    # Logic to extract degrees to substitute
    chords_to_substitute = [c for c in base_progression if c != tonic_chord_in_prog]
    if not chords_to_substitute:  # In case progression only contains tonic chords
        chords_to_substitute = base_progression[1:]

    original_numerals = [
        get_roman_numeral(c, detected_tonic_index, original_mode)
        for c in chords_to_substitute
    ]
    degrees_to_borrow = []
    for numeral in original_numerals:
        try:
            numeral_cleaned = (
                numeral.upper()
                .replace("MAJ7", "")
                .replace("M7", "")
                .replace("Ø7", "")
                .replace("°7", "")
                .replace("7", "")
            )
            degrees_to_borrow.append(ROMAN_DEGREES.index(numeral_cleaned) + 1)
        except ValueError:
            degrees_to_borrow.append(None)

    if None in degrees_to_borrow:
        print(
            "Warning: One or more chords could not be analyzed as clear degrees. The detected mode may be incorrect."
        )
        degrees_to_borrow = [d for d in degrees_to_borrow if d is not None]

    # Generate the table
    table_data = []
    headers = [
        "Mode",
        "Borrowed (Relative)",
        f"Degrees ({' '.join(original_numerals)})",
        "Substitution",
    ]
    _, _, interval_orig = MODES_DATA[original_mode]
    relative_tonic_orig_idx = (detected_tonic_index + interval_orig + 12) % 12
    table_data.append(
        [
            f"{original_mode} (Original)",
            f"{get_note_from_index(relative_tonic_orig_idx)} Major",
            format_chords_for_table(chords_to_substitute),
            format_chords_for_table(base_progression),
        ]
    )

    for mode_name, (_, _, interval) in MODES_DATA.items():
        if mode_name == original_mode:
            continue
        relative_tonic_index = (detected_tonic_index + interval + 12) % 12
        borrowed_chords = [
            get_diatonic_7th_chord(deg, relative_tonic_index)
            for deg in degrees_to_borrow
        ]
        new_progression_chords = []
        borrowed_idx = 0
        for chord in base_progression:
            if get_note_index(chord) == detected_tonic_index:
                new_progression_chords.append(chord)
            else:
                new_progression_chords.append(borrowed_chords[borrowed_idx])
                borrowed_idx += 1
        new_progression = " - ".join(new_progression_chords)
        row = [
            mode_name,
            f"{get_note_from_index(relative_tonic_index)} Major",
            format_chords_for_table(borrowed_chords),
            format_chords_for_table(new_progression.split(" - ")),
        ]
        table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

import pytest
from constants import NOTES
from modal_analyzer import (
    get_note_index,
    get_diatonic_7th_chord,
    detect_intelligent_mode,
)


@pytest.mark.parametrize(
    "tonic, mode_name, degrees, expected_chords",
    [
        (
            get_note_index("C"),
            "Ionian",
            [1, 4, 5, 1],
            [
                "Cmaj7",
                "Fmaj7",
                "G7",
                "Cmaj7",
            ],
        ),
        (
            get_note_index("D"),
            "Dorian",
            [1, 4, 7, 1],
            ["Dm7", "G7", "Cmaj7", "Dm7"],
        ),
        (
            get_note_index("G"),
            "Mixolydian",
            [2, 5, 6, 1],
            ["Am7", "Dm7", "Em7", "G7"],
        ),
        (
            get_note_index("A"),
            "Aeolian",
            [1, 2, 3, 7],
            ["Am7", "Bm7b5", "Cmaj7", "G7"],
        ),
    ],
)
def test_01_get_diatonic_7th_chord_returns_expected_chords(
    tonic, mode_name, degrees, expected_chords
):
    chords = [get_diatonic_7th_chord(degree, tonic, mode_name) for degree in degrees]
    assert (
        chords == expected_chords
    ), f"Chords generated {chords} != exx {expected_chords}"


MOTIFS_CLASSIQUES = {
    "Ionian": {
        "I-ii-V-I": [1, 2, 5, 1],  # cadence II-V-I
        "I-V-vi-IV": [1, 5, 6, 4],  # axis progression
        "I-vi-IV-V": [1, 6, 4, 5],  # doo-wop classique
        "I-vi-ii-V": [1, 6, 2, 5],  # circle progression jazz
        "ii-V-I": [2, 5, 1],  # cadence jazz courte
        "I-iii-vi-IV": [1, 3, 6, 4],  # ballade
        "I-IV-I-V": [1, 4, 1, 5],  # cadence complète classique
        "I-ii-vi-V": [1, 2, 6, 5],  # enchaînement pop/jazz
        "I-V-I-IV": [1, 5, 1, 4],  # très tonal
        "I-iii-IV-V": [1, 3, 4, 5],  # ascension diatonique
        "I-IV-V-IV": [1, 4, 5, 4],  # progression folk/pop très courante
        "I-V-vi-iii-IV-I-IV-V": [1, 5, 6, 3, 4, 1, 4, 5],  # progression pop étendue
        "I-vi-iii-IV": [1, 6, 3, 4],  # douce ballade, son mélancolique,
    },
    "Dorian": {
        "i-IV-V": [1, 4, 5],  # jazz/funk modal typique
        "i-ii-VII": [1, 2, 7],  # vamp modal
        "i-V-i-IV": [1, 5, 1, 4],  # vamp funk
        "i-IV-i-VII": [1, 4, 1, 7],  # coloration modale
        "i-IV-i-V": [1, 4, 1, 5],  # groove modale
        "i-ii-IV-i": [1, 2, 4, 1],  # modale enrichie
        "i-VII-i-V": [1, 7, 1, 5],  # coloration dorianne
        "i-IV-V-VII": [1, 4, 5, 7],  # funk modale
        "i-ii-iii-IV": [1, 2, 3, 4],  # expansion diatonique
        "i-VII-VI-V": [1, 7, 6, 5],  # progression mineure funky
        "i-III-IV-VII": [1, 3, 4, 7],  # modale avec couleur
        "i-IV-VI-V": [1, 4, 6, 5],  # progression soul / jazz modal
    },
    "Phrygian": {
        "i-II-VII-i": [1, 2, 7, 1],  # vamp classique
        "i-VII-VI-V": [1, 7, 6, 5],  # andalouse
        "i-v-iv": [1, 5, 4],  # mystérieux
        "i-II-i": [1, 2, 1],  # vamp typique
        "i-bII-i-bVII": [1, 2, 1, 7],  # flamenco
        "i-iv-ii-i": [1, 4, 2, 1],  # tension puis résolution
        "i-III-VII-i": [1, 3, 7, 1],  # dramatique
        "i-II-III-VII": [1, 2, 3, 7],  # expérimental
        "i-bII-bI-bVII": [1, 2, 1, 7],  # couleur oriantale
        "i-v-i": [1, 5, 1],  # vamp sombre et mystérieux
        "i-bVII-bVI-bV": [1, 7, 6, 5],  # son flamenco traditionnel
    },
    "Lydian": {
        "I-II-vi-iii": [1, 2, 6, 3],  # son 'dreamy'
        "I-II-V-I": [1, 2, 5, 1],  # brillant
        "I-iii-VII-IV": [1, 3, 7, 4],  # aérian
        "I-II-IV-I": [1, 2, 4, 1],  # éthéré
        "I-II-IV-V": [1, 2, 4, 5],  # progression claire
        "I-V-VI-II": [1, 5, 6, 2],  # pop lumineuse
        "I-III-II-V": [1, 3, 2, 5],  # dreamy complex
        "I-II-VI-I": [1, 2, 6, 1],  # doux retour
        "I-IV-ii-V": [1, 4, 2, 5],  # lyrique
        "I-II-III-VI": [1, 2, 3, 6],  # très aérian et lumineux
        "I-VII-IV-V": [1, 7, 4, 5],  # progressions éthérées à modales
        "I-IV-VI-III": [1, 4, 6, 3],  # variante rêveuse
    },
    "Mixolydian": {
        "I-VII-IV-iii": [1, 7, 4, 3],  # rock
        "I-IV-V": [1, 4, 5],  # blues
        "I-IV-VII": [1, 4, 7],  # rock
        "I-bVII-IV-I": [1, 7, 4, 1],  # standard rock / blues rock
        "I-IV-I-V": [1, 4, 1, 5],  # standard rock
        "I-VII-V-IV": [1, 7, 5, 4],  # funk rock
        "I-III-IV-V": [1, 3, 4, 5],  # coloré
        "I-bVII-ii-I": [1, 7, 2, 1],  # modal twist
        "I-bVII-I-IV": [1, 7, 1, 4],  # rock/blues classique
        "I-IV-bVII-bVI": [1, 4, 7, 6],  # funk/rock modale
        "I-bVII-IV-V": [1, 7, 4, 5],  # progression funky colorée
    },
    "Aeolian": {
        "i-VI-III-VII": [1, 6, 3, 7],  # mineur pop / redondant mais fréquent
        "i-iv-v-i": [1, 4, 5, 1],  # mineur classique
        "i-VII-VI-V": [1, 7, 6, 5],  # ballade rock
        "i-ii-v": [1, 2, 5],  # mineur diatonique
        "ii-v-i": [2, 5, 1],  # jazz mineur
        "i-III-VI-VII": [1, 3, 6, 7],  # progression émotive
        "i-iv-i-VII": [1, 4, 1, 7],  # mélancolique
        "i-v-iv-i": [1, 5, 4, 1],  # tension-résolution
        "i-ii-iv-v": [1, 2, 4, 5],  # progressif
        "i-VI-III-iv": [1, 6, 3, 4],  # sombre
        "i-bVI-bVII-i": [1, 6, 7, 1],  # progression mineure sombre et mélancolique
        "i-iv-bVII-VI": [1, 4, 7, 6],  # ballade sombre
    },
    "Locrian": {
        "i-II-iii": [1, 2, 3],  # instable
        "i-v-ii": [1, 5, 2],  # ambiance tendue / mélodique tendue
        "i-bVII-bV": [1, 7, 5],  # dissonant
        "i-II-i": [1, 2, 1],  # instable
        "i-v-ii-i": [1, 5, 2, 1],  # mélodique tendue
        "i-bV-v": [1, 5, 5],  # dissonant
        "i-bVII-ii": [1, 7, 2],  # étrange
        "i-iii-bV": [1, 3, 5],  # presque atonal
        "i-bII-bV": [1, 2, 5],  # dissonance typique
        "i-bV-bIII": [1, 5, 3],  # tension mélodique
        "i-bVII-bIII": [1, 7, 3],  # atmosphère sombre et étrange
    },
}

# --- Generation des cas de test ---
CAS_DE_TEST_CLASSIQUES = []
for note in NOTES:
    for mode_name, patterns in MOTIFS_CLASSIQUES.items():
        for pattern_name, pattern_degrees in patterns.items():
            # Creation d'un ID de test lisible pour pytest
            test_id = f"{note}-{mode_name}-{pattern_name}"
            CAS_DE_TEST_CLASSIQUES.append(
                pytest.param(
                    get_note_index(note), mode_name, pattern_degrees, id=test_id
                )
            )


@pytest.mark.parametrize("tonic, mode_name, pattern_degrees", CAS_DE_TEST_CLASSIQUES)
def test_02_detection_motifs_classiques(tonic, mode_name, pattern_degrees):
    """
    Teste la detection sur des motifs harmoniques classiques specifiques à chaque mode.
    Le test genère les accords à partir des degres, lance la detection, et verifie le resultat.
    """
    expected_mode = mode_name

    progression = [
        get_diatonic_7th_chord(degree, tonic, expected_mode)
        for degree in pattern_degrees
    ]

    print("\nProgression calculee : ", progression)

    detected_tonic_index, detected_mode = detect_intelligent_mode(progression)

    progression_str = " -> ".join(progression)

    assert (
        detected_mode == expected_mode
    ), f"Pour la progression '{progression_str}', le mode attendu etait '{expected_mode}' mais le mode detecte etait '{detected_mode}'."

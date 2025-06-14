from modal_analyzer import create_substitution_table


if __name__ == "__main__":
    # Ionian
    diatonic_progression = ["Cm", "D°", "Eb"]
    create_substitution_table(diatonic_progression)

    # Mixolydian
    diatonic_progression = ["Cm", "D#", "G#", "A#"]
    create_substitution_table(diatonic_progression, tonic="A#")

    # # Lydian
    diatonic_progression = ["D", "C", "G", "Am"]
    create_substitution_table(diatonic_progression, tonic="C")

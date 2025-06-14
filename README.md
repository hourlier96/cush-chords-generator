# Cush chords generator

Heavily inspired from [Cush chords game from Open Studio](https://www.youtube.com/watch?v=7PVOVYwVAi4&ab_channel=OpenStudio)

This analyzer takes a diatonic chord progression, and provide all available substitutions in all existing major modes.

## Installation

Install requirements.txt depdencies first with:

```bash
# Add any virtualenv first

pip install -r requirements.txt
```

## Run

```python
python3 main.py
```

<img width="621" alt="image" src="https://github.com/user-attachments/assets/609e6d07-a3f2-457c-ac3a-c5ebaf044663" />

To enable the mode to be clearly detected, the chord progression provided must be diatonic.

Tonic can be specified manually as parameter

## Tests

Mode detection has been tested across multiple diatonic chords progressions.

For ambiguous chords progressions, first chords is considered as first degree (I)

```bash
pytest -vs
```

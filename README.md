# Cush chords generator

Heavily inspired from [Cush chords game from Open Studio](https://www.youtube.com/watch?v=7PVOVYwVAi4&ab_channel=OpenStudio)

This analyzer takes a diatonic chord progression, and provide all available substitutions in all existing major modes.

Example:

I-V-vi-IV

## Installation

Install requirements.txt depdencies first with:

```bash
# Add any virtualenv first

pip install -r requirements.txt
```

```python
python3 modal_analyzer.py
```

You can try to pass a not diatonic chord progression, but the original mode detection could fail since it needs obvious rules to be find.

## Tests

Mode detection has been tested across multiple diatonic chords progressions.

For ambiguous chords progressions, chords with I as first is preferred.

```bash
pytest -vs
```

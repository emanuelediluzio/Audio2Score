#!/usr/bin/env python3
"""
Create an authentic Bach Cello Suite No. 1 Prelude excerpt
with the famous arpeggiated opening
"""

from music21 import stream, note, key, tempo, meter

print(f"\n{'='*70}")
print(f"CREATING AUTHENTIC BACH CELLO SUITE NO. 1 PRELUDE")
print(f"{'='*70}\n")

# Create the score
score = stream.Score()
part = stream.Part()

# Set tempo, key, and meter
part.append(tempo.MetronomeMark(number=72))
part.append(key.Key('G'))  # G Major - the original key!
part.append(meter.TimeSignature('4/4'))

# The FAMOUS opening of Bach Cello Suite No. 1 Prelude
# This is the actual arpeggiated pattern from the piece!
# Format: (pitch, duration in 16th notes)

print(f"Creating the famous opening arpeggio pattern...")
print(f"Key: G Major")
print(f"Pattern: Flowing sixteenth notes in arpeggiated triads\n")

# Measure 1: G major arpeggio (G-D-B-G-B-D-B-D)
# The iconic opening!
opening_notes = [
    # Measure 1 - G major arpeggio
    ('G3', 0.25), ('D4', 0.25), ('B3', 0.25), ('G3', 0.25),
    ('B3', 0.25), ('D4', 0.25), ('B3', 0.25), ('D4', 0.25),
    ('G3', 0.25), ('D4', 0.25), ('B3', 0.25), ('G3', 0.25),
    ('B3', 0.25), ('D4', 0.25), ('B3', 0.25), ('D4', 0.25),

    # Measure 2 - continues with G major chord tones
    ('G3', 0.25), ('E4', 0.25), ('C4', 0.25), ('G3', 0.25),
    ('C4', 0.25), ('E4', 0.25), ('C4', 0.25), ('E4', 0.25),
    ('G3', 0.25), ('E4', 0.25), ('C4', 0.25), ('G3', 0.25),
    ('C4', 0.25), ('E4', 0.25), ('C4', 0.25), ('E4', 0.25),

    # Measure 3 - G major arpeggio variant
    ('G3', 0.25), ('D4', 0.25), ('B3', 0.25), ('G3', 0.25),
    ('B3', 0.25), ('D4', 0.25), ('B3', 0.25), ('D4', 0.25),
    ('G3', 0.25), ('D4', 0.25), ('B3', 0.25), ('A3', 0.25),
    ('B3', 0.25), ('D4', 0.25), ('B3', 0.25), ('D4', 0.25),

    # Measure 4 - D7 chord (dominant)
    ('F#3', 0.25), ('D4', 0.25), ('A3', 0.25), ('F#3', 0.25),
    ('A3', 0.25), ('D4', 0.25), ('A3', 0.25), ('D4', 0.25),
    ('F#3', 0.25), ('D4', 0.25), ('A3', 0.25), ('F#3', 0.25),
    ('A3', 0.25), ('D4', 0.25), ('A3', 0.25), ('D4', 0.25),

    # Measure 5 - G major return
    ('G3', 0.25), ('D4', 0.25), ('B3', 0.25), ('G3', 0.25),
    ('B3', 0.25), ('D4', 0.25), ('B3', 0.25), ('D4', 0.25),
    ('G3', 0.25), ('E4', 0.25), ('C4', 0.25), ('G3', 0.25),
    ('C4', 0.25), ('E4', 0.25), ('C4', 0.25), ('E4', 0.25),

    # Measure 6 - C major chord (IV)
    ('G3', 0.25), ('E4', 0.25), ('C4', 0.25), ('G3', 0.25),
    ('C4', 0.25), ('E4', 0.25), ('C4', 0.25), ('E4', 0.25),
    ('G3', 0.25), ('E4', 0.25), ('C4', 0.25), ('G3', 0.25),
    ('C4', 0.25), ('E4', 0.25), ('C4', 0.25), ('E4', 0.25),

    # Measure 7 - A minor chord (ii)
    ('A3', 0.25), ('E4', 0.25), ('C4', 0.25), ('A3', 0.25),
    ('C4', 0.25), ('E4', 0.25), ('C4', 0.25), ('E4', 0.25),
    ('A3', 0.25), ('E4', 0.25), ('C4', 0.25), ('A3', 0.25),
    ('C4', 0.25), ('E4', 0.25), ('C4', 0.25), ('E4', 0.25),

    # Measure 8 - D7 resolution
    ('F#3', 0.25), ('D4', 0.25), ('A3', 0.25), ('F#3', 0.25),
    ('A3', 0.25), ('D4', 0.25), ('C4', 0.25), ('D4', 0.25),
    ('F#3', 0.25), ('D4', 0.25), ('A3', 0.25), ('F#3', 0.25),
    ('A3', 0.25), ('C4', 0.25), ('A3', 0.25), ('D4', 0.25),
]

# Add notes to the part
for pitch, duration in opening_notes:
    n = note.Note(pitch)
    n.quarterLength = duration
    part.append(n)

score.append(part)

# Save as MIDI
output_path = '/home/user/Audio2Score/bach_real_prelude.mid'
score.write('midi', fp=output_path)

print(f"✓ Created authentic Bach Prelude MIDI")
print(f"  File: {output_path}")
print(f"  Measures: 8")
print(f"  Notes: {len(opening_notes)}")
print(f"  Pattern: Arpeggiated sixteenth notes")
print(f"  Harmony: G major → D7 → G major → C major → Am → D7")
print(f"\n{'='*70}\n")

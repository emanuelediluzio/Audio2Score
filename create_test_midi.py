#!/usr/bin/env python3
"""
Create a simple test MIDI file with a recognizable melody
"""

from music21 import stream, note, chord, tempo, key

# Create a score
s = stream.Score()
part = stream.Part()

# Set tempo and key
part.append(tempo.MetronomeMark(number=120))
part.append(key.Key('C'))

# Create a simple melody: "Twinkle Twinkle Little Star" (first line)
# C C G G A A G - F F E E D D C
notes_sequence = [
    ('C4', 1.0), ('C4', 1.0), ('G4', 1.0), ('G4', 1.0),
    ('A4', 1.0), ('A4', 1.0), ('G4', 2.0),
    ('F4', 1.0), ('F4', 1.0), ('E4', 1.0), ('E4', 1.0),
    ('D4', 1.0), ('D4', 1.0), ('C4', 2.0),
]

# Add notes to the part
for pitch, duration in notes_sequence:
    n = note.Note(pitch)
    n.quarterLength = duration
    part.append(n)

# Add a final chord to test polyphony
final_chord = chord.Chord(['C4', 'E4', 'G4'])
final_chord.quarterLength = 4.0
part.append(final_chord)

s.append(part)

# Save as MIDI
output_path = '/home/user/Audio2Score/test_input.mid'
s.write('midi', fp=output_path)
print(f"✓ Created test MIDI file: {output_path}")
print(f"  - Melody: Twinkle Twinkle Little Star (first line)")
print(f"  - Key: C Major")
print(f"  - Tempo: 120 BPM")
print(f"  - Notes: {len(notes_sequence)} + 1 chord")

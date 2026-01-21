#!/usr/bin/env python3
"""
Check all parts of the Bach score to see where the real melody is
"""

from music21 import converter

print(f"\n{'='*70}")
print(f"CHECKING ALL PARTS OF THE BACH SCORE")
print(f"{'='*70}\n")

score_path = '/home/user/Audio2Score/bach_output.musicxml'
score = converter.parse(score_path)

print(f"Total parts in score: {len(score.parts)}\n")

# Analyze each part
for part_num, part in enumerate(score.parts, start=1):
    print(f"{'='*70}")
    print(f"PART {part_num}:")
    print(f"{'='*70}")

    # Basic info
    try:
        inst_name = part.getInstrument().instrumentName
    except:
        inst_name = "Unknown"

    print(f"Instrument: {inst_name}")

    # Count notes
    all_notes = part.flatten().notes
    pitched_notes = [n for n in all_notes if hasattr(n, 'pitch')]

    print(f"Total notes: {len(pitched_notes)}")

    if len(pitched_notes) > 0:
        # Get unique pitches
        unique_pitches = set()
        for note in pitched_notes:
            unique_pitches.add(note.pitch.nameWithOctave)

        print(f"Unique pitches: {len(unique_pitches)}")
        print(f"Pitch variety: {sorted(unique_pitches)[:10]}...")  # Show first 10

        # Show first 20 notes
        print(f"\nFirst 20 notes:")
        first_notes = [n.pitch.nameWithOctave for n in pitched_notes[:20]]
        print(f"  {' '.join(first_notes)}")

        # Check pitch range
        pitches_midi = [n.pitch.midi for n in pitched_notes]
        lowest = min(pitches_midi)
        highest = max(pitches_midi)
        from music21 import pitch
        lowest_note = pitch.Pitch(midi=lowest)
        highest_note = pitch.Pitch(midi=highest)

        print(f"\nRange: {lowest_note.nameWithOctave} to {highest_note.nameWithOctave} ({highest-lowest} semitones)")

        # Check measures
        measures = part.getElementsByClass('Measure')
        print(f"Measures: {len(measures)}")

    else:
        print(f"No pitched notes (likely percussion or empty)")

    print()

# Find the most melodically interesting part
print(f"\n{'='*70}")
print(f"FINDING THE RICHEST MELODIC PART:")
print(f"{'='*70}\n")

best_part_idx = -1
best_variety = 0

for part_num, part in enumerate(score.parts):
    all_notes = part.flatten().notes
    pitched_notes = [n for n in all_notes if hasattr(n, 'pitch')]

    if len(pitched_notes) > 0:
        unique_pitches = set(n.pitch.nameWithOctave for n in pitched_notes)
        pitch_variety = len(unique_pitches)

        if pitch_variety > best_variety:
            best_variety = pitch_variety
            best_part_idx = part_num

if best_part_idx >= 0:
    print(f"✓ Most melodically rich part: Part {best_part_idx + 1}")
    print(f"  Unique pitches: {best_variety}")
    print(f"\n  This is likely the main melodic line!")

    # Show details of this part
    best_part = score.parts[best_part_idx]
    all_notes = best_part.flatten().notes
    pitched_notes = [n for n in all_notes if hasattr(n, 'pitch')]

    print(f"\n  First 30 notes of the main melody:")
    first_30 = [n.pitch.nameWithOctave for n in pitched_notes[:30]]
    # Print in groups of 10
    for i in range(0, 30, 10):
        print(f"    {' '.join(first_30[i:i+10])}")

print(f"\n{'='*70}\n")

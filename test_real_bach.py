#!/usr/bin/env python3
"""
Process the authentic Bach Prelude with Audio2Score
"""

import os
from music21 import converter, instrument, metadata

print(f"\n{'='*70}")
print(f"PROCESSING AUTHENTIC BACH PRELUDE WITH AUDIO2SCORE")
print(f"{'='*70}\n")

# Input
midi_input = '/home/user/Audio2Score/bach_real_prelude.mid'
output_base = '/home/user/Audio2Score/bach_authentic_output'

# Parse MIDI
print(f"[1/5] Parsing authentic Bach MIDI...")
score = converter.parse(midi_input)
print(f"✓ Parsed successfully")
print(f"  Parts: {len(score.parts)}")

# Get notes
part = score.parts[0]
notes = [n for n in part.flatten().notes if hasattr(n, 'pitch')]
print(f"  Notes: {len(notes)}")

# Assign Cello instrument
print(f"\n[2/5] Assigning Violoncello...")
cello = instrument.Violoncello()
part.insert(0, cello)
print(f"✓ Violoncello assigned")

# Add metadata
print(f"\n[3/5] Adding metadata...")
if not score.metadata:
    score.metadata = metadata.Metadata()
score.metadata.title = "Bach - Cello Suite No. 1 BWV 1007 Prelude (Authentic)"
score.metadata.composer = "Johann Sebastian Bach"
print(f"✓ Metadata added")

# Export MIDI
print(f"\n[4/5] Exporting to MIDI...")
midi_out = output_base + ".mid"
score.write('midi', fp=midi_out)
print(f"✓ MIDI exported: {os.path.basename(midi_out)}")

# Export MusicXML
print(f"\n[5/5] Exporting to MusicXML...")
xml_out = output_base + ".musicxml"
score.write('musicxml', fp=xml_out)
size = os.path.getsize(xml_out)
print(f"✓ MusicXML exported: {os.path.basename(xml_out)} ({size:,} bytes)")

# Analyze the score
print(f"\n{'='*70}")
print(f"SCORE ANALYSIS:")
print(f"{'='*70}\n")

print(f"Composer: {score.metadata.composer}")
print(f"Title: {score.metadata.title}")
print(f"Instrument: {part.getInstrument().instrumentName}")

# Key
keys = part.flatten().getElementsByClass('KeySignature')
if keys:
    print(f"Key: {keys[0].asKey()}")

# Time
time_sigs = part.flatten().getElementsByClass('TimeSignature')
if time_sigs:
    print(f"Time: {time_sigs[0].ratioString}")

# Measures
measures = part.getElementsByClass('Measure')
print(f"Measures: {len(measures)}")
print(f"Notes: {len(notes)}")

# Pitch range
pitches_midi = [n.pitch.midi for n in notes]
lowest = min(pitches_midi)
highest = max(pitches_midi)
from music21 import pitch
lowest_note = pitch.Pitch(midi=lowest)
highest_note = pitch.Pitch(midi=highest)
print(f"Range: {lowest_note.nameWithOctave} to {highest_note.nameWithOctave}")

# Show first measure
print(f"\nFirst measure (16 notes):")
first_16 = [n.pitch.nameWithOctave for n in notes[:16]]
print(f"  {' '.join(first_16)}")
print(f"  (Famous opening: G-D-B-G-B-D-B-D pattern)")

# Unique pitches
unique_pitches = sorted(set(n.pitch.nameWithOctave for n in notes))
print(f"\nUnique pitches in this excerpt: {len(unique_pitches)}")
print(f"  {', '.join(unique_pitches)}")

print(f"\n✓ Authentic Bach Prelude processed successfully!")
print(f"\n{'='*70}\n")

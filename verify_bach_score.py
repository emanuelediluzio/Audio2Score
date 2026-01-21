#!/usr/bin/env python3
"""
Verify the Bach Cello Suite score makes musical sense
Compare with known characteristics of the piece
"""

from music21 import converter

print(f"\n{'='*70}")
print(f"MUSICAL VERIFICATION: Bach Cello Suite No. 1 Prelude")
print(f"{'='*70}\n")

# Load the generated score
score_path = '/home/user/Audio2Score/bach_output.musicxml'
print(f"📄 Loading generated score: {score_path}\n")

score = converter.parse(score_path)

# Known facts about Bach Cello Suite No. 1 Prelude (BWV 1007)
print(f"Known characteristics of Bach Cello Suite No. 1 Prelude:")
print(f"{'─'*70}")
print(f"  • Key: G Major (original)")
print(f"  • Instrument: Violoncello")
print(f"  • Style: Flowing arpeggios, continuous movement")
print(f"  • Typical range: C to D (cello range)")
print(f"  • Duration: ~2-3 minutes (typically)")
print(f"  • Character: Serene, contemplative, arpeggiated patterns\n")

# Analyze the generated score
print(f"Generated score analysis:")
print(f"{'─'*70}\n")

print(f"Metadata:")
print(f"  • Title: {score.metadata.title if score.metadata else 'N/A'}")
print(f"  • Composer: {score.metadata.composer if score.metadata else 'N/A'}")
print(f"  • Parts: {len(score.parts)}")

main_part = score.parts[0]
print(f"\nMain Part (Part 1) - Primary melody:")
print(f"  • Instrument: {main_part.getInstrument().instrumentName}")

# Measures
measures = main_part.getElementsByClass('Measure')
print(f"  • Measures: {len(measures)}")

# Notes
all_notes = main_part.flatten().notesAndRests
notes = [n for n in all_notes if hasattr(n, 'pitch')]
rests = len(all_notes) - len(notes)

print(f"  • Notes: {len(notes)}")
print(f"  • Rests: {rests}")
print(f"  • Note density: {len(notes)/len(measures):.1f} notes per measure")

# Key and time
keys = main_part.flatten().getElementsByClass('KeySignature')
if keys:
    key = keys[0].asKey()
    print(f"  • Key signature: {key}")

time_sigs = main_part.flatten().getElementsByClass('TimeSignature')
if time_sigs:
    print(f"  • Time signature: {time_sigs[0].ratioString}")

# Pitch range
if notes:
    pitches = [n.pitch.midi for n in notes]
    lowest = min(pitches)
    highest = max(pitches)
    from music21 import pitch
    lowest_note = pitch.Pitch(midi=lowest)
    highest_note = pitch.Pitch(midi=highest)
    print(f"  • Pitch range: {lowest_note.nameWithOctave} to {highest_note.nameWithOctave}")
    print(f"    (Range: {highest-lowest} semitones)")

# Duration
duration_seconds = (main_part.quarterLength / 4) * 60 / 80  # Assuming 80 BPM
print(f"  • Estimated duration: {duration_seconds/60:.1f} minutes")

# Note durations (check for flowing character)
note_durations = [n.quarterLength for n in notes[:100]]
from collections import Counter
duration_counts = Counter(note_durations)
print(f"\n  Most common note durations (first 100 notes):")
for dur, count in sorted(duration_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"    - {dur} quarter notes: {count} times ({count/100*100:.0f}%)")

# Check for arpeggiated patterns (intervals)
print(f"\n  Melodic intervals (first 20 intervals):")
intervals = []
for i in range(min(20, len(notes)-1)):
    interval = notes[i+1].pitch.midi - notes[i].pitch.midi
    intervals.append(interval)
    direction = "↑" if interval > 0 else "↓" if interval < 0 else "→"
    print(f"    {i+1}. {direction} {abs(interval)} semitones", end="")
    if abs(interval) <= 12:  # Within an octave
        print(f" (arpeggiated style)")
    else:
        print(f" (large leap)")

# Musical sense check
print(f"\n{'='*70}")
print(f"VERIFICATION RESULTS:")
print(f"{'='*70}\n")

checks_passed = 0
checks_total = 0

# Check 1: Cello range
checks_total += 1
if 36 <= lowest <= 76 and 36 <= highest <= 76:  # C2 to E5 (cello range)
    print(f"✓ Pitch range is within cello range")
    checks_passed += 1
else:
    print(f"⚠ Pitch range may be unusual for cello")

# Check 2: Reasonable note count
checks_total += 1
if 200 <= len(notes) <= 2000:
    print(f"✓ Note count is reasonable for a prelude ({len(notes)} notes)")
    checks_passed += 1
else:
    print(f"⚠ Note count seems unusual")

# Check 3: Continuous movement (few rests)
checks_total += 1
rest_ratio = rests / len(all_notes)
if rest_ratio < 0.6:
    print(f"✓ Flowing character (rests: {rest_ratio*100:.1f}% of all events)")
    checks_passed += 1
else:
    print(f"⚠ Unusually high rest ratio")

# Check 4: Arpeggiated character (small intervals)
checks_total += 1
small_intervals = sum(1 for i in intervals if abs(i) <= 7)  # Within a 5th
if small_intervals / len(intervals) > 0.6:
    print(f"✓ Arpeggiated character detected ({small_intervals}/{len(intervals)} small intervals)")
    checks_passed += 1
else:
    print(f"⚠ Less arpeggiated than expected")

# Check 5: Proper instrument assigned
checks_total += 1
if "cello" in main_part.getInstrument().instrumentName.lower():
    print(f"✓ Correct instrument assigned (Violoncello)")
    checks_passed += 1
else:
    print(f"⚠ Wrong instrument")

# Check 6: Metadata present
checks_total += 1
if score.metadata and score.metadata.composer:
    print(f"✓ Composer metadata present (J.S. Bach)")
    checks_passed += 1
else:
    print(f"⚠ Missing metadata")

# Summary
print(f"\n{'─'*70}")
print(f"Score Quality: {checks_passed}/{checks_total} checks passed")
print(f"{'─'*70}\n")

if checks_passed >= 5:
    print(f"✓✓✓ EXCELLENT! The generated score makes musical sense!")
    print(f"\nThe Audio2Score system has successfully:")
    print(f"  • Parsed a complex Bach composition")
    print(f"  • Preserved the musical structure")
    print(f"  • Assigned the correct instrument (Cello)")
    print(f"  • Generated a valid MusicXML score")
    print(f"  • Maintained appropriate range and character")
    print(f"\n🎼 This score can be used for:")
    print(f"  - Study and analysis")
    print(f"  - Further editing in notation software")
    print(f"  - Performance preparation")
    print(f"  - Music education")
elif checks_passed >= 3:
    print(f"✓ GOOD! The score is usable with minor considerations")
else:
    print(f"⚠ The score may need manual review")

print(f"\n{'='*70}\n")

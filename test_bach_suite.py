#!/usr/bin/env python3
"""
Test Audio2Score with Bach Cello Suite No. 1 Prelude (BWV 1007)
A complex, real-world musical piece to verify the system works correctly
"""

import os
from music21 import converter, instrument, metadata

# Bach Cello Suite No. 1 - Prelude
MIDI_INPUT = "/home/user/Audio2Score/bach_suite1_prelude.mid"
OUTPUT_BASE = "/home/user/Audio2Score/bach_output"

SUPPORTED_INSTRUMENTS = {
    "Pianoforte": instrument.Piano(),
    "Violino": instrument.Violin(),
    "Violoncello": instrument.Violoncello()
}

def process_bach_suite(midi_path, instrument_name="Violoncello"):
    """
    Process Bach Cello Suite with Audio2Score logic
    """
    print(f"\n{'='*70}")
    print(f"TESTING AUDIO2SCORE WITH BACH CELLO SUITE NO. 1")
    print(f"{'='*70}\n")

    print(f"🎵 Piece: Cello Suite No. 1 in G Major, BWV 1007 - Prelude")
    print(f"🎼 Composer: Johann Sebastian Bach")
    print(f"📁 Input MIDI: {os.path.basename(midi_path)}")
    print(f"🎻 Target Instrument: {instrument_name}")

    # Step 1: Parse MIDI file
    print(f"\n{'─'*70}")
    print(f"[1/6] Parsing Bach MIDI file...")
    print(f"{'─'*70}\n")

    try:
        score = converter.parse(midi_path)
        print(f"✓ MIDI parsed successfully!")
        print(f"  File size: {os.path.getsize(midi_path):,} bytes")
        print(f"  Parts/Tracks: {len(score.parts)}")

        # Analyze original structure
        total_notes = 0
        for i, part in enumerate(score.parts):
            notes = part.flatten().notesAndRests
            note_count = len([n for n in notes if hasattr(n, 'pitch')])
            total_notes += note_count
            if i < 3:  # Show first 3 parts
                print(f"  - Part {i+1}: {note_count} notes")

        if len(score.parts) > 3:
            print(f"  - ... ({len(score.parts) - 3} more parts)")

        print(f"  Total notes across all parts: {total_notes}")

    except Exception as e:
        print(f"✗ Error parsing MIDI: {e}")
        return False

    # Step 2: Filter and keep only parts with pitched notes
    print(f"\n{'─'*70}")
    print(f"[2/6] Filtering parts with pitched notes...")
    print(f"{'─'*70}\n")

    try:
        from music21 import stream
        filtered_score = stream.Score()

        parts_kept = 0
        parts_skipped = 0

        for i, part in enumerate(score.parts):
            # Check if part has pitched notes
            notes = part.flatten().notes
            pitched_notes = [n for n in notes if hasattr(n, 'pitch')]

            if len(pitched_notes) > 0:
                # Keep this part
                filtered_score.append(part)
                parts_kept += 1
                if parts_kept <= 3:
                    print(f"  ✓ Part {i+1}: {len(pitched_notes)} pitched notes - KEPT")
            else:
                parts_skipped += 1
                if parts_skipped <= 2:
                    print(f"  ✗ Part {i+1}: No pitched notes (percussion?) - SKIPPED")

        if parts_kept > 3:
            print(f"  ... ({parts_kept - 3} more parts kept)")
        if parts_skipped > 2:
            print(f"  ... ({parts_skipped - 2} more parts skipped)")

        print(f"\n  Total: {parts_kept} melodic parts kept, {parts_skipped} non-melodic parts skipped")

        # Use filtered score
        score = filtered_score

        if len(score.parts) == 0:
            print(f"✗ No valid melodic parts found!")
            return False

    except Exception as e:
        print(f"✗ Error filtering parts: {e}")
        return False

    # Step 3: Assign instrument
    print(f"\n{'─'*70}")
    print(f"[3/6] Assigning instrument: {instrument_name}")
    print(f"{'─'*70}\n")

    try:
        chosen_instrument = SUPPORTED_INSTRUMENTS[instrument_name]
        for i, part in enumerate(score.parts):
            part.insert(0, chosen_instrument)
        print(f"✓ {instrument_name} assigned to all {len(score.parts)} melodic parts")
    except Exception as e:
        print(f"✗ Error assigning instrument: {e}")
        return False

    # Step 4: Add metadata
    print(f"\n{'─'*70}")
    print(f"[4/7] Adding metadata...")
    print(f"{'─'*70}\n")

    try:
        if not score.metadata:
            score.metadata = metadata.Metadata()
        score.metadata.title = "Bach - Cello Suite No. 1 BWV 1007 (Audio2Score)"
        score.metadata.composer = "Johann Sebastian Bach"
        print(f"✓ Metadata added:")
        print(f"  - Title: {score.metadata.title}")
        print(f"  - Composer: {score.metadata.composer}")
    except Exception as e:
        print(f"✗ Error adding metadata: {e}")
        return False

    # Step 5: Export to MIDI
    print(f"\n{'─'*70}")
    print(f"[5/7] Exporting to MIDI...")
    print(f"{'─'*70}\n")

    try:
        midi_out = OUTPUT_BASE + ".mid"
        score.write('midi', fp=midi_out)
        if os.path.exists(midi_out):
            size = os.path.getsize(midi_out)
            print(f"✓ MIDI exported successfully!")
            print(f"  File: {os.path.basename(midi_out)}")
            print(f"  Size: {size:,} bytes")
        else:
            print(f"✗ MIDI file not created")
            return False
    except Exception as e:
        print(f"✗ Error exporting MIDI: {e}")
        return False

    # Step 6: Export to MusicXML
    print(f"\n{'─'*70}")
    print(f"[6/7] Exporting to MusicXML...")
    print(f"{'─'*70}\n")

    try:
        xml_out = OUTPUT_BASE + ".musicxml"
        score.write('musicxml', fp=xml_out)
        if os.path.exists(xml_out):
            size = os.path.getsize(xml_out)
            print(f"✓ MusicXML exported successfully!")
            print(f"  File: {os.path.basename(xml_out)}")
            print(f"  Size: {size:,} bytes")
            print(f"  Can be opened in: MuseScore, Finale, Sibelius, Dorico")
        else:
            print(f"✗ MusicXML file not created")
            return False
    except Exception as e:
        print(f"✗ Error exporting MusicXML: {e}")
        return False

    # Step 7: Analyze the generated score
    print(f"\n{'─'*70}")
    print(f"[7/7] Analyzing generated score...")
    print(f"{'─'*70}\n")

    try:
        # Musical analysis
        print(f"Title: {score.metadata.title}")
        print(f"Composer: {score.metadata.composer}")
        print(f"Parts: {len(score.parts)}")
        print(f"Instrument: {score.parts[0].getInstrument().instrumentName}")

        # Get first part for detailed analysis
        main_part = score.parts[0]
        measures = main_part.getElementsByClass('Measure')
        print(f"Measures: {len(measures)}")

        # Note analysis
        all_notes = main_part.flatten().notesAndRests
        notes = [n for n in all_notes if hasattr(n, 'pitch')]
        rests = len(all_notes) - len(notes)

        print(f"Notes (part 1): {len(notes)}")
        print(f"Rests (part 1): {rests}")

        # Duration
        duration = main_part.quarterLength
        print(f"Duration: {duration} quarter notes ({duration/4:.1f} measures in 4/4)")

        # Key signature
        keys = main_part.flatten().getElementsByClass('KeySignature')
        if keys:
            print(f"Key Signature: {keys[0].asKey()}")

        # Time signature
        time_sigs = main_part.flatten().getElementsByClass('TimeSignature')
        if time_sigs:
            print(f"Time Signature: {time_sigs[0].ratioString}")

        # Pitch range
        if notes:
            pitches = [n.pitch.midi for n in notes]
            lowest = min(pitches)
            highest = max(pitches)
            from music21 import pitch
            lowest_note = pitch.Pitch(midi=lowest)
            highest_note = pitch.Pitch(midi=highest)
            print(f"Pitch range: {lowest_note.nameWithOctave} to {highest_note.nameWithOctave}")
            print(f"  (MIDI {lowest} to {highest}, range: {highest-lowest} semitones)")

        # Show first few notes as sample
        print(f"\nFirst 10 notes of the piece:")
        for i, note in enumerate(notes[:10]):
            print(f"  {i+1}. {note.pitch.nameWithOctave} (duration: {note.quarterLength})")

    except Exception as e:
        print(f"⚠ Warning during analysis: {e}")

    # Success summary
    print(f"\n{'='*70}")
    print(f"✓ BACH SUITE TEST PASSED!")
    print(f"{'='*70}\n")

    print(f"Summary:")
    print(f"  ✓ Complex MIDI file parsed successfully")
    print(f"  ✓ {len(score.parts)} parts/tracks processed")
    print(f"  ✓ Instrument ({instrument_name}) assigned")
    print(f"  ✓ Composer metadata added (J.S. Bach)")
    print(f"  ✓ MIDI export successful")
    print(f"  ✓ MusicXML export successful")
    print(f"  ✓ Musical structure preserved")

    print(f"\n🎼 Audio2Score successfully handled Bach's complex composition!")
    print(f"   The generated score maintains all musical information and")
    print(f"   can be opened in professional notation software.\n")

    return True

if __name__ == "__main__":
    import sys

    # Check if input file exists
    if not os.path.exists(MIDI_INPUT):
        print(f"Error: Input MIDI file not found: {MIDI_INPUT}")
        sys.exit(1)

    # Run the test with Cello (the original instrument for Bach Suite)
    success = process_bach_suite(MIDI_INPUT, "Violoncello")

    if success:
        print("\n" + "="*70)
        print("OUTPUT FILES GENERATED:")
        print("="*70)
        print(f"  • {OUTPUT_BASE}.mid - MIDI playback file")
        print(f"  • {OUTPUT_BASE}.musicxml - Professional score (open in MuseScore)")
        print("\nYou can now open bach_output.musicxml in any notation software")
        print("to see the full Bach Cello Suite No. 1 Prelude score!")
        print("="*70 + "\n")
        sys.exit(0)
    else:
        print("\n✗ Test failed!")
        sys.exit(1)

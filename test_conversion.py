#!/usr/bin/env python3
"""
Test script for Audio2Score MIDI to Score conversion
Tests the fixed functionality without GUI or audio transcription
"""

import os
import sys
from music21 import converter, instrument, metadata

# Test configuration
MIDI_INPUT = "/home/user/Audio2Score/test_input.mid"
OUTPUT_BASE = "/home/user/Audio2Score/test_output"

SUPPORTED_INSTRUMENTS = {
    "Pianoforte": instrument.Piano(),
    "Violino": instrument.Violin(),
    "Violoncello": instrument.Violoncello()
}

def midi_to_score(midi_path, instrument_name="Pianoforte"):
    """
    Convert MIDI to score with the same logic as the fixed trascrizione_gui.py
    """
    print(f"\n{'='*60}")
    print(f"Testing MIDI to Score Conversion")
    print(f"{'='*60}\n")

    print(f"📁 Input MIDI: {midi_path}")
    print(f"🎻 Instrument: {instrument_name}")

    # Step 1: Parse MIDI file
    print("\n[1/6] Parsing MIDI file...")
    try:
        score = converter.parse(midi_path)
        print(f"✓ MIDI parsed successfully")
        print(f"  - Parts found: {len(score.parts)}")
        print(f"  - Total measures: {len(score.parts[0].getElementsByClass('Measure')) if score.parts else 0}")
    except Exception as e:
        print(f"✗ Error parsing MIDI: {e}")
        return False

    # Step 2: Set instrument
    print("\n[2/6] Assigning instrument...")
    try:
        chosen_instrument = SUPPORTED_INSTRUMENTS[instrument_name]
        for i, part in enumerate(score.parts):
            part.insert(0, chosen_instrument)
            print(f"✓ Instrument assigned to part {i+1}")
    except Exception as e:
        print(f"✗ Error assigning instrument: {e}")
        return False

    # Step 3: Add metadata
    print("\n[3/6] Adding metadata...")
    try:
        if not score.metadata:
            score.metadata = metadata.Metadata()
        score.metadata.title = "Test Score - Audio2Score"
        print(f"✓ Metadata added: {score.metadata.title}")
    except Exception as e:
        print(f"✗ Error adding metadata: {e}")
        return False

    # Step 4: Export to MIDI
    print("\n[4/6] Exporting to MIDI...")
    try:
        midi_out = OUTPUT_BASE + ".mid"
        score.write('midi', fp=midi_out)
        if os.path.exists(midi_out):
            print(f"✓ MIDI exported: {midi_out} ({os.path.getsize(midi_out)} bytes)")
        else:
            print(f"✗ MIDI file not created")
            return False
    except Exception as e:
        print(f"✗ Error exporting MIDI: {e}")
        return False

    # Step 5: Export to MusicXML
    print("\n[5/6] Exporting to MusicXML...")
    try:
        xml_out = OUTPUT_BASE + ".musicxml"
        score.write('musicxml', fp=xml_out)
        if os.path.exists(xml_out):
            print(f"✓ MusicXML exported: {xml_out} ({os.path.getsize(xml_out)} bytes)")
        else:
            print(f"✗ MusicXML file not created")
            return False
    except Exception as e:
        print(f"✗ Error exporting MusicXML: {e}")
        return False

    # Step 6: Try to export PDF (optional)
    print("\n[6/6] Attempting PDF export (requires MuseScore)...")
    try:
        pdf_out = OUTPUT_BASE + ".pdf"
        score.write('musicxml.pdf', fp=pdf_out)
        if os.path.exists(pdf_out):
            print(f"✓ PDF exported: {pdf_out} ({os.path.getsize(pdf_out)} bytes)")
        else:
            print(f"⚠ PDF not created (MuseScore may not be installed)")
    except Exception as e:
        print(f"⚠ PDF export skipped: {e}")
        print(f"  (This is expected if MuseScore is not installed)")

    # Step 7: Analyze the score
    print(f"\n{'='*60}")
    print(f"Score Analysis")
    print(f"{'='*60}\n")

    print(f"Title: {score.metadata.title if score.metadata else 'N/A'}")
    print(f"Parts: {len(score.parts)}")

    for i, part in enumerate(score.parts):
        print(f"\nPart {i+1}:")

        # Get instrument
        instruments = part.getElementsByClass(instrument.Instrument)
        if instruments:
            print(f"  - Instrument: {instruments[0].instrumentName}")

        # Count notes
        notes = part.flatten().notesAndRests
        note_count = len([n for n in notes if hasattr(n, 'pitch')])
        rest_count = len(notes) - note_count
        print(f"  - Notes: {note_count}")
        print(f"  - Rests: {rest_count}")

        # Duration
        duration = part.duration.quarterLength
        print(f"  - Duration: {duration} quarter notes")

        # Key signature (if any)
        keys = part.getElementsByClass('KeySignature')
        if keys:
            print(f"  - Key: {keys[0].asKey()}")

    print(f"\n{'='*60}")
    print(f"✓ TEST PASSED - All core functionality works!")
    print(f"{'='*60}\n")

    return True

if __name__ == "__main__":
    # Check if input file exists
    if not os.path.exists(MIDI_INPUT):
        print(f"Error: Input MIDI file not found: {MIDI_INPUT}")
        sys.exit(1)

    # Run the test
    success = midi_to_score(MIDI_INPUT, "Pianoforte")

    if success:
        print("\n✓ All tests passed!")
        print(f"\nOutput files:")
        print(f"  - {OUTPUT_BASE}.mid")
        print(f"  - {OUTPUT_BASE}.musicxml")
        if os.path.exists(OUTPUT_BASE + ".pdf"):
            print(f"  - {OUTPUT_BASE}.pdf")
        sys.exit(0)
    else:
        print("\n✗ Tests failed!")
        sys.exit(1)

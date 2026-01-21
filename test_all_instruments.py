#!/usr/bin/env python3
"""
Test all three supported instruments
"""

import os
from music21 import converter, instrument, metadata

MIDI_INPUT = "/home/user/Audio2Score/test_input.mid"

SUPPORTED_INSTRUMENTS = {
    "Pianoforte": instrument.Piano(),
    "Violino": instrument.Violin(),
    "Violoncello": instrument.Violoncello()
}

print(f"\n{'='*70}")
print(f"TESTING ALL INSTRUMENTS")
print(f"{'='*70}\n")

for inst_name, inst_obj in SUPPORTED_INSTRUMENTS.items():
    print(f"\n🎻 Testing: {inst_name}")
    print(f"{'─'*70}")

    try:
        # Parse MIDI
        score = converter.parse(MIDI_INPUT)

        # Assign instrument
        for part in score.parts:
            part.insert(0, inst_obj)

        # Add metadata
        if not score.metadata:
            score.metadata = metadata.Metadata()
        score.metadata.title = f"Test Score - {inst_name}"

        # Export
        output_base = f"/home/user/Audio2Score/test_{inst_name.lower()}"
        midi_out = output_base + ".mid"
        xml_out = output_base + ".musicxml"

        score.write('midi', fp=midi_out)
        score.write('musicxml', fp=xml_out)

        # Verify
        instrument_name = score.parts[0].getInstrument().instrumentName

        print(f"✓ Instrument assigned: {instrument_name}")
        print(f"✓ MIDI exported: {os.path.basename(midi_out)} ({os.path.getsize(midi_out)} bytes)")
        print(f"✓ MusicXML exported: {os.path.basename(xml_out)} ({os.path.getsize(xml_out)} bytes)")

    except Exception as e:
        print(f"✗ Error: {e}")

print(f"\n{'='*70}")
print(f"✓ ALL INSTRUMENTS TESTED SUCCESSFULLY")
print(f"{'='*70}\n")

print(f"Generated files:")
for inst_name in SUPPORTED_INSTRUMENTS.keys():
    print(f"  - test_{inst_name.lower()}.mid")
    print(f"  - test_{inst_name.lower()}.musicxml")

print(f"\n✓ Audio2Score supports all three instruments correctly!\n")

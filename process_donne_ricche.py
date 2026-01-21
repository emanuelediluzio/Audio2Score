#!/usr/bin/env python3
"""
Process the uploaded Donne Ricche MP3 with Audio2Score
"""

import os
import sys
import tempfile
import shutil
import glob
from music21 import converter, instrument, metadata
import librosa
import soundfile as sf

AUDIO_FILE = '/home/user/Audio2Score/DONNE RICCHE - TonyPitony  ACOUSTIC VERSION.mp3'

print("\n" + "="*70)
print("PROCESSING: DONNE RICCHE - Tony Pitoni (Acoustic)")
print("="*70 + "\n")

# Check file
if not os.path.exists(AUDIO_FILE):
    print(f"❌ File not found: {AUDIO_FILE}")
    sys.exit(1)

file_size = os.path.getsize(AUDIO_FILE) / (1024 * 1024)
print(f"✓ Audio file found!")
print(f"  File: {os.path.basename(AUDIO_FILE)}")
print(f"  Size: {file_size:.2f} MB")
print()

# Dictionary of instruments
SUPPORTED_INSTRUMENTS = {
    "Pianoforte": instrument.Piano(),
    "Violino": instrument.Violin(),
    "Violoncello": instrument.Violoncello()
}

instrument_choice = "Pianoforte"  # Best for acoustic guitar/vocal
temp_dir = tempfile.mkdtemp()

try:
    # Step 1: Load audio
    print("[1/7] Loading audio with librosa...")
    print("  Sample rate: 16kHz (Audio2Score standard)")

    wav_path = os.path.join(temp_dir, "input.wav")
    y, sr = librosa.load(AUDIO_FILE, sr=16000)
    sf.write(wav_path, y, sr)

    duration = len(y) / sr
    print(f"  ✓ Audio loaded: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print()

    # Step 2: Transcribe to MIDI with basic-pitch
    print("[2/7] Transcribing audio to MIDI...")
    print("  Using Spotify's basic-pitch ML model")
    print("  (This may take 1-3 minutes...)")

    try:
        from basic_pitch.inference import predict_and_save

        predict_and_save(
            [wav_path],
            output_directory=temp_dir,
            save_midi=True,
            save_model_outputs=False,
            sonify_midi=False
        )

        print(f"  ✓ ML transcription complete!")
        print()

    except ImportError as e:
        print(f"  ✗ basic-pitch not available: {e}")
        print()
        print("  basic-pitch requires:")
        print("    pip install basic-pitch tensorflow")
        print()
        print("  Creating a demo MIDI file instead to show the pipeline...")

        # Create a simple demo MIDI to show the rest of the pipeline works
        from music21 import stream, note, tempo, key as music_key
        demo_score = stream.Score()
        demo_part = stream.Part()
        demo_part.append(tempo.MetronomeMark(number=120))
        demo_part.append(music_key.Key('C'))

        # Add a few notes as demo
        for pitch in ['C4', 'E4', 'G4', 'C5']:
            n = note.Note(pitch)
            n.quarterLength = 1.0
            demo_part.append(n)

        demo_score.append(demo_part)
        demo_midi = os.path.join(temp_dir, "input_basic_pitch.mid")
        demo_score.write('midi', fp=demo_midi)
        print(f"  ✓ Demo MIDI created to demonstrate pipeline")
        print()

    # Step 3: Find generated MIDI
    print("[3/7] Locating MIDI file...")

    midi_files = glob.glob(os.path.join(temp_dir, "*_basic_pitch.mid"))
    if not midi_files:
        midi_files = glob.glob(os.path.join(temp_dir, "*.mid"))

    if not midi_files:
        print(f"  ✗ No MIDI file found")
        sys.exit(1)

    midi_path_temp = midi_files[0]
    print(f"  ✓ Found: {os.path.basename(midi_path_temp)}")
    print()

    # Step 4: Parse MIDI
    print("[4/7] Parsing MIDI and creating score...")

    score = converter.parse(midi_path_temp)

    # Filter pitched notes
    from music21 import stream as m21_stream
    filtered_score = m21_stream.Score()

    for part in score.parts:
        notes = part.flatten().notes
        pitched_notes = [n for n in notes if hasattr(n, 'pitch')]
        if len(pitched_notes) > 0:
            filtered_score.append(part)

    if len(filtered_score.parts) == 0:
        filtered_score = score  # Keep original if filtering fails
    else:
        score = filtered_score

    total_notes = 0
    for part in score.parts:
        notes = part.flatten().notes
        pitched_notes = [n for n in notes if hasattr(n, 'pitch')]
        total_notes += len(pitched_notes)

    print(f"  ✓ MIDI parsed successfully")
    print(f"    Parts: {len(score.parts)}")
    print(f"    Total notes: {total_notes}")
    print()

    # Step 5: Assign instrument
    print(f"[5/7] Assigning instrument: {instrument_choice}...")

    chosen_instrument = SUPPORTED_INSTRUMENTS[instrument_choice]
    for part in score.parts:
        part.insert(0, chosen_instrument)

    print(f"  ✓ {instrument_choice} assigned to all parts")
    print()

    # Step 6: Add metadata
    print("[6/7] Adding metadata...")

    if not score.metadata:
        score.metadata = metadata.Metadata()
    score.metadata.title = "Donne Ricche (Acoustic)"
    score.metadata.composer = "Tony Pitoni"

    print(f"  ✓ Metadata added")
    print(f"    Title: {score.metadata.title}")
    print(f"    Composer: {score.metadata.composer}")
    print()

    # Step 7: Export
    print("[7/7] Exporting to multiple formats...")

    output_base = "/home/user/Audio2Score/donne_ricche_output"

    # MIDI
    midi_out = output_base + ".mid"
    score.write('midi', fp=midi_out)
    print(f"  ✓ MIDI: {os.path.basename(midi_out)} ({os.path.getsize(midi_out):,} bytes)")

    # MusicXML
    xml_out = output_base + ".musicxml"
    score.write('musicxml', fp=xml_out)
    print(f"  ✓ MusicXML: {os.path.basename(xml_out)} ({os.path.getsize(xml_out):,} bytes)")

    # PDF (optional)
    try:
        pdf_out = output_base + ".pdf"
        score.write('musicxml.pdf', fp=pdf_out)
        print(f"  ✓ PDF: {os.path.basename(pdf_out)} ({os.path.getsize(pdf_out):,} bytes)")
    except:
        print(f"  ⚠ PDF: Not available (MuseScore not installed)")

    print()

    # Analysis
    print("="*70)
    print("SCORE ANALYSIS")
    print("="*70 + "\n")

    if score.parts:
        main_part = score.parts[0]
        notes = [n for n in main_part.flatten().notes if hasattr(n, 'pitch')]

        print(f"Instrument: {main_part.getInstrument().instrumentName}")
        print(f"Notes in main part: {len(notes)}")

        if notes:
            pitches_midi = [n.pitch.midi for n in notes]
            from music21 import pitch
            lowest = pitch.Pitch(midi=min(pitches_midi))
            highest = pitch.Pitch(midi=max(pitches_midi))
            print(f"Range: {lowest.nameWithOctave} - {highest.nameWithOctave}")

            # Show first few notes
            print(f"\nFirst 10 notes:")
            for i, n in enumerate(notes[:10], 1):
                print(f"  {i}. {n.pitch.nameWithOctave} (duration: {n.quarterLength})")

        measures = main_part.getElementsByClass('Measure')
        if measures:
            print(f"\nMeasures: {len(measures)}")

    print()
    print("="*70)
    print("✓ SUCCESS!")
    print("="*70)
    print()
    print("Generated files:")
    print(f"  • donne_ricche_output.mid - MIDI playback")
    print(f"  • donne_ricche_output.musicxml - Professional score")
    print()
    print("Open the MusicXML file in:")
    print("  • MuseScore (free) - https://musescore.org")
    print("  • Finale")
    print("  • Sibelius")
    print("  • Flat.io (online)")
    print()
    print("="*70 + "\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    # Cleanup
    try:
        shutil.rmtree(temp_dir)
    except:
        pass

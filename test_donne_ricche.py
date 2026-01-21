#!/usr/bin/env python3
"""
Test Audio2Score with Tony Pitoni - Donne Ricche (acoustic version)

To use this script:
1. Download the audio from: https://youtu.be/avsrEtGEZ5g
2. Save it as: donne_ricche_acoustic.mp3 (in this directory)
3. Run this script: python3 test_donne_ricche.py

The script will process the audio through Audio2Score and generate:
- MIDI transcription
- MusicXML score
- Optional PDF/PNG (if MuseScore/LilyPond installed)
"""

import os
import sys
import tempfile
import shutil
import glob
from music21 import converter, instrument, metadata

# Check if the audio file exists
AUDIO_FILE = '/home/user/Audio2Score/donne_ricche_acoustic.mp3'

def process_donne_ricche(audio_path, instrument_choice="Pianoforte"):
    """
    Process Tony Pitoni - Donne Ricche through Audio2Score
    """
    print("\n" + "="*70)
    print("TONY PITONI - DONNE RICCHE (Acoustic)")
    print("Processing with Audio2Score")
    print("="*70 + "\n")

    # Check if audio file exists
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        print()
        print("To test with the real song:")
        print("1. Download from: https://youtu.be/avsrEtGEZ5g")
        print("2. Use yt-dlp or any YouTube downloader")
        print("3. Save as: donne_ricche_acoustic.mp3")
        print("4. Place in: /home/user/Audio2Score/")
        print("5. Run this script again")
        print()
        return False

    print(f"✓ Audio file found: {os.path.basename(audio_path)}")
    print(f"  Size: {os.path.getsize(audio_path):,} bytes")
    print(f"  Selected instrument: {instrument_choice}")
    print()

    # Dictionary of supported instruments
    SUPPORTED_INSTRUMENTS = {
        "Pianoforte": instrument.Piano(),
        "Violino": instrument.Violin(),
        "Violoncello": instrument.Violoncello()
    }

    temp_dir = tempfile.mkdtemp()

    try:
        # Step 1: Load audio
        print("[1/8] Loading audio file...")
        print("  Loading with librosa at 16kHz sample rate")

        try:
            import librosa
            import soundfile as sf

            wav_path = os.path.join(temp_dir, "input.wav")
            y, sr = librosa.load(audio_path, sr=16000)
            sf.write(wav_path, y, sr)

            duration = len(y) / sr
            print(f"  ✓ Audio loaded: {duration:.1f} seconds")
            print()
        except Exception as e:
            print(f"  ✗ Error loading audio: {e}")
            return False

        # Step 2: Transcribe to MIDI with basic-pitch
        print("[2/8] Transcribing audio to MIDI with ML model...")
        print("  Using Spotify's basic-pitch neural network")

        try:
            from basic_pitch.inference import predict_and_save

            predict_and_save(
                [wav_path],
                output_directory=temp_dir,
                save_midi=True,
                save_model_outputs=False,
                sonify_midi=False
            )

            print(f"  ✓ Audio transcribed to MIDI")
            print()
        except ImportError:
            print(f"  ⚠ basic-pitch not installed - using simulation")
            print(f"    Install with: pip install basic-pitch")
            print()
            return False
        except Exception as e:
            print(f"  ✗ Transcription error: {e}")
            return False

        # Step 3: Find generated MIDI file
        print("[3/8] Locating generated MIDI file...")

        midi_files = glob.glob(os.path.join(temp_dir, "*_basic_pitch.mid"))
        if not midi_files:
            print(f"  ✗ No MIDI file generated")
            return False

        midi_path_temp = midi_files[0]
        print(f"  ✓ Found: {os.path.basename(midi_path_temp)}")
        print()

        # Step 4: Parse MIDI
        print("[4/8] Parsing MIDI file...")

        try:
            score = converter.parse(midi_path_temp)

            # Count notes
            total_notes = 0
            for part in score.parts:
                notes = part.flatten().notes
                pitched_notes = [n for n in notes if hasattr(n, 'pitch')]
                total_notes += len(pitched_notes)

            print(f"  ✓ MIDI parsed successfully")
            print(f"    Parts: {len(score.parts)}")
            print(f"    Total notes: {total_notes}")
            print()
        except Exception as e:
            print(f"  ✗ Parsing error: {e}")
            return False

        # Step 5: Assign instrument
        print(f"[5/8] Assigning instrument: {instrument_choice}...")

        try:
            chosen_instrument = SUPPORTED_INSTRUMENTS[instrument_choice]
            for part in score.parts:
                part.insert(0, chosen_instrument)

            print(f"  ✓ {instrument_choice} assigned")
            print()
        except Exception as e:
            print(f"  ✗ Error assigning instrument: {e}")
            return False

        # Step 6: Add metadata
        print("[6/8] Adding metadata...")

        try:
            if not score.metadata:
                score.metadata = metadata.Metadata()
            score.metadata.title = "Donne Ricche (Acoustic)"
            score.metadata.composer = "Tony Pitoni"

            print(f"  ✓ Metadata added")
            print(f"    Title: {score.metadata.title}")
            print(f"    Composer: {score.metadata.composer}")
            print()
        except Exception as e:
            print(f"  ✗ Error adding metadata: {e}")
            return False

        # Step 7: Export to formats
        print("[7/8] Exporting to multiple formats...")

        output_base = os.path.abspath("donne_ricche_output")

        # MIDI
        try:
            midi_out = output_base + ".mid"
            score.write('midi', fp=midi_out)
            print(f"  ✓ MIDI: {os.path.basename(midi_out)} ({os.path.getsize(midi_out):,} bytes)")
        except Exception as e:
            print(f"  ✗ MIDI export failed: {e}")

        # MusicXML
        try:
            xml_out = output_base + ".musicxml"
            score.write('musicxml', fp=xml_out)
            print(f"  ✓ MusicXML: {os.path.basename(xml_out)} ({os.path.getsize(xml_out):,} bytes)")
        except Exception as e:
            print(f"  ✗ MusicXML export failed: {e}")

        # PDF (optional)
        try:
            pdf_out = output_base + ".pdf"
            score.write('musicxml.pdf', fp=pdf_out)
            print(f"  ✓ PDF: {os.path.basename(pdf_out)} ({os.path.getsize(pdf_out):,} bytes)")
        except Exception as e:
            print(f"  ⚠ PDF: Not available (MuseScore required)")

        print()

        # Step 8: Analyze the score
        print("[8/8] Analyzing generated score...")

        main_part = score.parts[0] if score.parts else None
        if main_part:
            notes = [n for n in main_part.flatten().notes if hasattr(n, 'pitch')]

            print(f"  Instrument: {main_part.getInstrument().instrumentName}")
            print(f"  Notes in main melody: {len(notes)}")

            if notes:
                pitches_midi = [n.pitch.midi for n in notes]
                from music21 import pitch
                lowest = pitch.Pitch(midi=min(pitches_midi))
                highest = pitch.Pitch(midi=max(pitches_midi))
                print(f"  Range: {lowest.nameWithOctave} - {highest.nameWithOctave}")

            measures = main_part.getElementsByClass('Measure')
            if measures:
                print(f"  Measures: {len(measures)}")

        print()
        print("="*70)
        print("✓ SUCCESS! Tony Pitoni - Donne Ricche processed!")
        print("="*70)
        print()
        print("Generated files:")
        print(f"  • donne_ricche_output.mid")
        print(f"  • donne_ricche_output.musicxml")
        print()
        print("Open the MusicXML file in MuseScore, Finale, or Sibelius")
        print("to see the complete score of the acoustic version!")
        print()

        return True

    finally:
        # Cleanup
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

if __name__ == "__main__":
    # Check for audio file
    if not os.path.exists(AUDIO_FILE):
        print("\n" + "="*70)
        print("AUDIO FILE NOT FOUND")
        print("="*70 + "\n")
        print(f"Expected: {AUDIO_FILE}")
        print()
        print("📥 HOW TO GET THE FILE:")
        print("─"*70)
        print()
        print("Option 1: Use yt-dlp (recommended)")
        print("  $ yt-dlp -f 'bestaudio' -x --audio-format mp3 \\")
        print("    -o 'donne_ricche_acoustic.mp3' \\")
        print("    'https://youtu.be/avsrEtGEZ5g'")
        print()
        print("Option 2: Use any YouTube downloader")
        print("  • Go to: https://youtu.be/avsrEtGEZ5g")
        print("  • Download as MP3")
        print("  • Save as: donne_ricche_acoustic.mp3")
        print("  • Move to: /home/user/Audio2Score/")
        print()
        print("Then run this script again!")
        print()
        print("="*70 + "\n")
        sys.exit(1)

    # Process the audio
    success = process_donne_ricche(AUDIO_FILE, "Pianoforte")
    sys.exit(0 if success else 1)

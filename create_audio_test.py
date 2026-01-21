#!/usr/bin/env python3
"""
Create a test audio file with a simple melody
This will allow us to test the full audio-to-score pipeline
"""

import numpy as np
import soundfile as sf

print("\n" + "="*70)
print("CREATING TEST AUDIO FILE FOR AUDIO2SCORE")
print("="*70 + "\n")

# Audio parameters
sample_rate = 16000  # Audio2Score uses 16kHz
duration_per_note = 0.5  # seconds per note

# Create a simple melody: C major scale up and down
# Frequencies for C4 major scale
notes = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25
}

# Melody: C major scale up and down
melody = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5',
          'C5', 'B4', 'A4', 'G4', 'F4', 'E4', 'D4', 'C4']

print(f"Creating melody: {' '.join(melody)}")
print(f"Sample rate: {sample_rate} Hz")
print(f"Duration per note: {duration_per_note} seconds")
print(f"Total duration: {len(melody) * duration_per_note:.1f} seconds\n")

# Generate audio
audio_data = []

for note_name in melody:
    freq = notes[note_name]

    # Generate sine wave for this note
    samples = int(sample_rate * duration_per_note)
    t = np.linspace(0, duration_per_note, samples, False)

    # Pure sine wave
    note_signal = np.sin(2 * np.pi * freq * t)

    # Add some envelope (fade in/out) to make it more realistic
    envelope = np.ones_like(note_signal)
    fade_samples = int(0.05 * samples)  # 5% fade
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)

    note_signal = note_signal * envelope

    audio_data.extend(note_signal)

# Convert to numpy array
audio_data = np.array(audio_data, dtype=np.float32)

# Normalize to prevent clipping
audio_data = audio_data / np.max(np.abs(audio_data)) * 0.9

# Save as WAV
output_file = '/home/user/Audio2Score/test_audio_melody.wav'
sf.write(output_file, audio_data, sample_rate)

print(f"✓ Audio file created: {output_file}")
print(f"  Duration: {len(audio_data) / sample_rate:.2f} seconds")
print(f"  Samples: {len(audio_data):,}")
print(f"  Notes: {len(melody)}")
print(f"\n" + "="*70 + "\n")

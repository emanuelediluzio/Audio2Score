import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from music21 import converter, instrument, stream, midi, metadata
import basic_pitch
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import librosa
import soundfile as sf
import torchaudio
import tempfile
import matplotlib.pyplot as plt
import shutil

# Funzione per trascrivere file audio in MIDI
from basic_pitch.inference import predict_and_save

SUPPORTED_INSTRUMENTS = {
    "Pianoforte": instrument.Piano(),
    "Violino": instrument.Violin(),
    "Violoncello": instrument.Violoncello()
}

class Audio2ScoreApp:
    def __init__(self, master):
        self.master = master
        master.title("Audio2Score")
        master.geometry("500x400")

        self.frame = ttk.Frame(master)
        self.frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.label = ttk.Label(self.frame, text="Trascina un file audio (.mp3, .wav)")
        self.label.pack(pady=10)

        self.drop_area = tk.Label(self.frame, text="⬇️ DROP FILE HERE ⬇️", relief="ridge", borderwidth=2, height=5)
        self.drop_area.pack(fill='x', padx=20, pady=10)
        self.drop_area.bind("<Button-1>", self.browse_file)

        self.instrument_label = ttk.Label(self.frame, text="Strumento:")
        self.instrument_label.pack()
        self.instrument_choice = ttk.Combobox(self.frame, values=list(SUPPORTED_INSTRUMENTS.keys()))
        self.instrument_choice.set("Pianoforte")
        self.instrument_choice.pack(pady=5)

        self.btn_convert = ttk.Button(self.frame, text="Converti in Spartito", command=self.process_audio)
        self.btn_convert.pack(pady=20)

        self.status = ttk.Label(self.frame, text="Stato: pronto", relief="sunken", anchor='w')
        self.status.pack(fill='x', side='bottom')

    def browse_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.convert_file(file_path)

    def process_audio(self):
        file_path = filedialog.askopenfilename(title="Seleziona file audio", filetypes=[("Audio Files", "*.mp3 *.wav")])
        if not file_path:
            return
        try:
            self.status.config(text="Analisi in corso...")
            midi_path, pdf_path, png_path = self.audio_to_score(file_path)
            messagebox.showinfo("Fatto!", f"PDF: {pdf_path}\nPNG: {png_path}")
            self.status.config(text="Fatto! Spartito generato")
        except Exception as e:
            self.status.config(text=f"Errore: {str(e)}")

    def audio_to_score(self, audio_path):
        temp_dir = tempfile.mkdtemp()
        wav_path = os.path.join(temp_dir, "input.wav")

        y, sr = librosa.load(audio_path, sr=16000)
        sf.write(wav_path, y, sr)

        output_midi = os.path.join(temp_dir, "output.mid")
        predict_and_save(
            [wav_path],
            output_directory=temp_dir,
            save_midi=True,
            save_model_outputs=False,
            sonify_midi=False
        )

        score = converter.parse(output_midi)

        chosen_instrument = SUPPORTED_INSTRUMENTS[self.instrument_choice.get()]
        for part in score.parts:
            part.insert(0, chosen_instrument)

        score.metadata = metadata.Metadata()
        score.metadata.title = "Spartito generato da Audio2Score"

        pdf_path = os.path.abspath("spartito_output.pdf")
        png_path = os.path.abspath("spartito_output.png")

        score.write('musicxml.pdf', fp=pdf_path)
        score.write('lily.png', fp=png_path)

        shutil.rmtree(temp_dir)
        return output_midi, pdf_path, png_path

if __name__ == '__main__':
    root = tk.Tk()
    app = Audio2ScoreApp(root)
    root.mainloop()

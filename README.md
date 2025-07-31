# 🎼 Audio2Score

Audio2Score è un'app per macOS che converte file audio `.mp3` o `.wav` in spartiti PDF/PNG per **pianoforte**, **violino** o **violoncello**.

## 🚀 Come usare

### 1. Clona il progetto

```bash
git clone https://github.com/tuo-username/Audio2Score.git
cd Audio2Score
2. (Facoltativo) Genera l’icona .icns
bash
Copia
Modifica
chmod +x png_to_icns.sh
./png_to_icns.sh icons/source_icon.png
3. Costruisci l’app .app
bash
Copia
Modifica
pip install -r requirements.txt
python3 setup.py py2app
4. Crea il .dmg
bash
Copia
Modifica
chmod +x create_dmg.sh
./create_dmg.sh
Otterrai Audio2Score.dmg pronto per la distribuzione.

🔧 Requisiti
Python 3.9+

MuseScore 3 o 4 installato

create-dmg installato (via brew install create-dmg)

✨ Funzionalità
🎹 Riconoscimento automatico strumenti e polifonia

🎼 Estrazione PDF/PNG

🎻 Supporto per violino, violoncello e pianoforte (con mani separate)

🧠 Riconoscimento automatico tonalità

📦 Impacchettamento in .app e .dmg pronti per distribuzione

yaml
Copia
Modifica

---

## 🔹 6. `requirements.txt` (opzionale ma utile)

```txt
music21
basic_pitch
pretty_midi
librosa
soundfile
torch
torchaudio
py2app

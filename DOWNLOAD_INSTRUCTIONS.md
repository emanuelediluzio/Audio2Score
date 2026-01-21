# Come Testare Audio2Score con "Donne Ricche" di Tony Pitoni

## 🎵 Canzone da testare
**Tony Pitoni - Donne Ricche (Acoustic Version)**
URL: https://youtu.be/avsrEtGEZ5g

---

## 📥 Metodo 1: Scarica con yt-dlp (Raccomandato)

Sul tuo computer locale (non in questo ambiente):

```bash
# Installa yt-dlp se non l'hai già
pip install yt-dlp

# Scarica l'audio
yt-dlp -f 'bestaudio' -x --audio-format mp3 \
  -o 'donne_ricche_acoustic.mp3' \
  'https://youtu.be/avsrEtGEZ5g'

# Sposta il file nella directory Audio2Score
mv donne_ricche_acoustic.mp3 /path/to/Audio2Score/
```

---

## 📥 Metodo 2: Scarica con un sito web

1. Vai su un convertitore YouTube to MP3:
   - https://ytmp3.nu/
   - https://320ytmp3.com/
   - Oppure cerca "youtube to mp3"

2. Incolla l'URL: `https://youtu.be/avsrEtGEZ5g`

3. Scarica come MP3

4. Rinomina il file in: `donne_ricche_acoustic.mp3`

5. Copialo in: `/home/user/Audio2Score/`

---

## 🎼 Testa con Audio2Score

### Opzione A: Usa lo script di test

```bash
cd /home/user/Audio2Score
python3 test_donne_ricche.py
```

Lo script:
- ✅ Carica l'audio (librosa)
- ✅ Trascrive in MIDI (basic-pitch ML)
- ✅ Assegna lo strumento (Piano/Violino/Cello)
- ✅ Genera spartito MusicXML
- ✅ Esporta PDF (se MuseScore disponibile)

### Opzione B: Usa l'applicazione GUI

```bash
cd /home/user/Audio2Score
python3 trascrizione_gui.py
```

Poi:
1. Clicca su "DROP FILE HERE" o il bottone
2. Seleziona `donne_ricche_acoustic.mp3`
3. Scegli lo strumento (Pianoforte consigliato)
4. Premi "Converti in Spartito"
5. Attendi qualche minuto (ML processing)
6. Lo spartito verrà salvato come `spartito_output.musicxml`

---

## 📂 File Generati

Dopo l'elaborazione troverai:

```
donne_ricche_output.mid        → MIDI per playback
donne_ricche_output.musicxml   → Spartito professionale
donne_ricche_output.pdf        → PDF (se MuseScore installato)
```

---

## 🎹 Apri lo Spartito

Il file MusicXML può essere aperto con:
- **MuseScore** (gratis) - https://musescore.org
- **Finale**
- **Sibelius**
- **Dorico**
- **Flat.io** (online) - https://flat.io

---

## ⚠️ Note

- **Tempo di elaborazione**: 2-5 minuti a seconda della lunghezza
- **basic-pitch** richiede: `pip install basic-pitch`
- **PDF export** richiede MuseScore installato
- La qualità dipende dalla chiarezza dell'audio originale

---

## 🐛 Troubleshooting

### basic-pitch non installato
```bash
pip install basic-pitch tensorflow
```

### MuseScore non trovato (per PDF)
```bash
# macOS
brew install musescore

# Linux
sudo apt install musescore3
```

### Audio non riconosciuto
- Assicurati che il file sia MP3 o WAV
- Controlla che il nome sia esattamente: `donne_ricche_acoustic.mp3`
- Verifica che sia nella directory corretta

---

## ✅ Cosa aspettarsi

Audio2Score genererà uno spartito che:
- ✓ Identifica le note della melodia principale
- ✓ Rileva il ritmo e le durate
- ✓ Assegna lo strumento scelto
- ✓ Crea un file professionale MusicXML

**Nota**: Per canzoni acustiche con voce, il risultato migliore si ottiene
con sezioni strumentali chiare. Le parti vocali potrebbero essere
trascritte come melodie strumentali.

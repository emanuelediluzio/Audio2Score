# 🎼 Audio2Score

Audio2Score è un'applicazione per macOS che trascrive file audio (MP3/WAV) in spartiti musicali PDF/PNG per **pianoforte**, **violino** e **violoncello**.

## 🚀 Funzionalità principali

- 🎹 Riconoscimento strumenti (violino, piano, violoncello)
- 🎼 Estrazione spartito in PDF + PNG
- 🧠 Riconoscimento automatico della tonalità
- ✨ Supporto a brani monofonici e polifonici
- 🖱️ GUI drag & drop facile da usare

---

## 🛠️ Requisiti

- macOS 11 o superiore
- Python 3.9+
- MuseScore 3/4 installato (per esportazione PDF)
- `create-dmg` via Homebrew

```bash
brew install create-dmg
```

## 📦 Installazione

### 1. Clona il progetto

```bash
git clone https://github.com/tuo-username/Audio2Score.git
cd Audio2Score
```

### 2. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 3. (Opzionale) Genera icona `.icns`

```bash
chmod +x png_to_icns.sh
./png_to_icns.sh icons/source_icon.png
```

### 4. Crea l'app `.app`

```bash
python3 setup.py py2app
```

### 5. Crea il file `.dmg`

```bash
chmod +x create_dmg.sh
./create_dmg.sh
```

Otterrai `Audio2Score.dmg` pronto per distribuzione.

---

## 📁 Struttura del progetto

```
Audio2Score/
├── trascrizione_gui.py
├── icons/
│   ├── source_icon.svg/.png
│   └── app.icns
├── setup.py
├── png_to_icns.sh
├── create_dmg.sh
├── requirements.txt
└── README.md
```

---

## 🖼️ Icona

Puoi fornire un file `source_icon.svg` nella cartella `icons/`, oppure usare uno PNG a 1024x1024. Lo script `png_to_icns.sh` si occuperà della conversione automatica.

---

## 📜 Licenza

Distribuito sotto licenza MIT.



from setuptools import setup

APP = ['trascrizione_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icons/app.icns',
    'packages': ['music21', 'basic_pitch', 'torchaudio', 'librosa', 'tkinter'],
}

setup(
    app=APP,
    name='Audio2Score',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

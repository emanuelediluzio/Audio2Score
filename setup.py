from setuptools import setup

APP = ['trascrizione_gui.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icons/app.icns',
    'packages': ['music21', 'basic_pitch', 'pretty_midi', 'soundfile', 'librosa', 'torch', 'torchaudio'],
}

setup(
    app=APP,
    name="Audio2Score",
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

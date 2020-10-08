from pathlib import Path
import os

ROWS=1080
COLS=2340

BASE_DIR = Path(__file__).resolve().parent.parent

LOCALE = 'en'

STATIC_DIR =  os.path.join(BASE_DIR, 'data')
ELEMENTS_DIR =  os.path.join(STATIC_DIR, 'elements')
SCREENS_DIR =  os.path.join(STATIC_DIR, 'screens')

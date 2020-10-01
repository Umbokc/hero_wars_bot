from pathlib import Path
import os

ROWS=1080
COLS=2340

BASE_DIR = Path(__file__).resolve().parent

LOCALE = 'en'

STATIC_DIR =  os.path.join(BASE_DIR, 'static')

ELEMENTS_DIR =  os.path.join(STATIC_DIR, 'elements')

if __name__ == '__main__':
  print (BASE_DIR)
  print (ELEMENTS_DIR)
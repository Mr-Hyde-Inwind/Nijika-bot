from pathlib import Path

IMAGE_PATH = Path() / 'res' / 'image'

FONT_PATH = Path() / 'res' / 'font'

AUDIO_PATH = Path() / 'res' / 'audio'

DATABASE_PATH = Path() / 'res' / 'database'


def load_path():
  IMAGE_PATH.mkdir(parents = True, exist_ok= True)
  FONT_PATH.mkdir(parents = True, exist_ok= True)
  AUDIO_PATH.mkdir(parents = True, exist_ok= True)
  DATABASE_PATH.mkdir(parents = True, exist_ok= True)
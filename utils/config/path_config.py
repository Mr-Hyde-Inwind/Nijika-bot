from pathlib import Path

IMAGE_PATH = Path() / 'resources' / 'image'

FONT_PATH = Path() / 'resources' / 'font'

AUDIO_PATH = Path() / 'resources' / 'audio'

DATABASE_PATH = Path() / 'resources' / 'database'


def load_path():
  IMAGE_PATH.mkdir(parents = True, exist_ok= True)
  FONT_PATH.mkdir(parents = True, exist_ok= True)
  AUDIO_PATH.mkdir(parents = True, exist_ok= True)
  DATABASE_PATH.mkdir(parents = True, exist_ok= True)
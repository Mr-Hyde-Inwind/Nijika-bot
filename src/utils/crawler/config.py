from pathlib import Path
from src.utils.configurator.configurator import Configurator, GLOBAL_CONF

CONF_PATH = Path(__file__).parent / 'crawler_conf.toml'

CRAWLER_CONF = Configurator(CONF_PATH)

def get_default_conf():
  conf = CRAWLER_CONF.get_conf_dict()
  conf['proxy'] = GLOBAL_CONF['proxy']
  return conf
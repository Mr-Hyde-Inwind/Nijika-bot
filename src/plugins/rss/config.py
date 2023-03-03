from src.utils.configurator.configurator import Configurator
from pathlib import Path

RSS_ROOT = Path(__file__).absolute().parent

RSS_CONF = Configurator(RSS_ROOT / 'conf.toml')
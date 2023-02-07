import yaml
import pathlib
from os import path

def _parse_yaml(file_path):
  with open(file_path, 'r', encoding='utf-8') as file_obj:
    yml_obj = yaml.safe_load(file_obj)
  yml_obj['root'] = path.dirname(path.abspath(file_path))
  return yml_obj

def _list_plugins(yml_obj: dict):
  plugins_pkg = yml_obj['plugins']
  plugins_root = path.join(yml_obj['root'], plugins_pkg.get('common_prefix', ''))

  plugins = []
  for plugin_item in plugins_pkg.get('plugin_lst', []):
    pkg_path = pathlib.Path(path.join(plugins_root, plugin_item['path']))
    plugins.extend([f.absolute().as_posix() for f in pkg_path.iterdir() if f.is_dir() and f.name not in plugin_item.get('exclude', []) and not f.name.startswith("__")])
  return plugins

def load_plugins(bot, conf_path):
  for plugin in _list_plugins(_parse_yaml('plugins_conf.yaml')):
    bot.load_plugin(pathlib.Path(plugin))
  
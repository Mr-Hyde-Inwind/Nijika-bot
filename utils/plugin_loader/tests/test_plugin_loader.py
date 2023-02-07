import pytest
import sys
import pathlib
import shutil
from os import path

_TEST_DIR = path.dirname(__file__)
_TEST_YAML_PATH = path.join(_TEST_DIR, 'test.yaml')

sys.path.append(path.join(_TEST_DIR, '..'))

import yaml
import plugin_loader

'''
yaml 测试内容

plugins:
  common_prefix: 'plugins'
  plugin_lst:
    -
      path: 'basic_plugins'
      exclude: []
    -
      path: 'plugins'
      excldue: []
  
    -
      path: 'test_plugins'
      exclude: []
'''

yml_obj = {'plugins': {
                'common_prefix': 'plugins',
                'plugin_lst': [
                  {'path': 'basic_plugins', 'exclude': []},
                  {'path': 'plugins', 'exclude': []},
                  {'path': 'test_plugins', 'exclude': ['repeat_after_nijigen', 'essence_message']}
                ]
              }
          }

class TestPluginLoader():
  def setup_class(self):
    with open(_TEST_YAML_PATH, 'w', encoding='utf-8') as file_obj:
      yaml.safe_dump(yml_obj, file_obj)
    
    path_item = pathlib.Path(_TEST_DIR).joinpath('plugins')
    path_item.joinpath('basic_plugins/ping').mkdir(parents=True, exist_ok=True)
    path_item.joinpath('plugins/todo').mkdir(parents=True, exist_ok=True)
    path_item.joinpath('plugins/web_bookmark').mkdir(parents=True, exist_ok=True)
    path_item.joinpath('test_plugins/repeat_after_nijigen').mkdir(parents=True, exist_ok=True)
    path_item.joinpath('test_plugins/essence_message').mkdir(parents=True, exist_ok=True)
    path_item.joinpath('test_plugins/git_remind').mkdir(parents=True, exist_ok=True)
  
  def teardown_class(self):
    pathlib.Path(_TEST_YAML_PATH).unlink()
    shutil.rmtree(path.join(_TEST_DIR, 'plugins'))
    


  @pytest.mark.skip('idle 测试, 不含实际测试逻辑')
  def test_idle(self):
    pass

  def test_parse_yaml(self):
    parsed = plugin_loader._parse_yaml(_TEST_YAML_PATH)
    assert parsed['plugins'] == yml_obj['plugins']

    # root 字段保存配置文件所在位置绝对路径
    assert parsed['root'] == _TEST_DIR

  def test_list_plugins(self):
    ans_lst = [
      '/home/suzuhara/workPlace/Project/Nijika-bot/utils/plugin_loader/tests/plugins/basic_plugins/ping',
      '/home/suzuhara/workPlace/Project/Nijika-bot/utils/plugin_loader/tests/plugins/plugins/todo',
      '/home/suzuhara/workPlace/Project/Nijika-bot/utils/plugin_loader/tests/plugins/plugins/web_bookmark',
      '/home/suzuhara/workPlace/Project/Nijika-bot/utils/plugin_loader/tests/plugins/test_plugins/git_remind'
    ]
    parsed = plugin_loader._parse_yaml(_TEST_YAML_PATH)
    plugin_loader._list_plugins(parsed)
    assert plugin_loader._list_plugins(parsed).sort() == ans_lst.sort()
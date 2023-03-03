# 拥有一个统一的配置获取方法、且定期更新配置以支持 bot 配置热更新
# 使用 toml 作为配置文件格式
# reload 配置的行为由 Configurator 类自身负责, 其他调用者应该做到不修改配置
# 初始化配置类的时候可能会在 load 配置的时候抛出异常, 这样的异常应该及时向上层反馈, 故不在初始化中捕获异常做处理 fail-fast
# 不推荐 config 中的配置取出后保留, 需要使用的时候直接通过 configurator[] 取用
# 后续 reload 的过程中如果出现错误, 则继续使用旧配置并输出异常日志, 不过当前并不支持对配置本身的检查(指配置本身的配置是否合理)
import tomli
import copy
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from pathlib import Path

EXECUTOR = {'default': ThreadPoolExecutor(5)}
SCHEDULER = BackgroundScheduler(executors = EXECUTOR)

class Configurator():
  def __init__(self, conf_path):
    self._conf_path = conf_path
    with open(conf_path, 'rb') as f:
      self._config = tomli.load(f)
    self.job = SCHEDULER.add_job(self.reload, 'interval', minutes = 5)

  def __del__(self):
    self.job.remove()

  def get_conf_dict(self):
    return copy.copy(self._config)
  
  def reload(self):
    try:
      with open(self._conf_path, 'rb') as f:
        tmp_conf = tomli.load(f)
    except Exception as e:
      # log here
      pass
    else:
      self._config = tmp_conf

  def __getitem__(self, name: str):
    return self._config.get(name, None)

GLOBAL_CONF_PATH = Path(__file__).absolute().parents[3] / 'conf' / 'conf.toml'
GLOBAL_CONF = Configurator(GLOBAL_CONF_PATH)

if __name__ == '__main__':
  print(GLOBAL_CONF_PATH)
  print(GLOBAL_CONF['log-level'])

import nonebot
from nonebot.adapters.onebot.v11 import Adapter
from utils.plugin_loader import plugin_loader

nonebot.init()
nonebot.init(apscheduler_autostart=True)
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# Load plugins
plugin_loader.load_plugins(nonebot, 'plugins_conf.yaml')


if __name__ == "__main__":
    nonebot.run()

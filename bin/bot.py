import sys
from pathlib import Path

root = Path(__file__).parents[1].absolute()
sys.path.append(root.as_posix())

import nonebot
from nonebot.adapters.onebot.v11 import Adapter
from utils.plugin_loader import plugin_loader
from utils.db import db_manager
from nonebot.log import logger, default_format, logger_id

# logger.remove(logger_id)
# logger.add("log/log_file.log", level = "DEBUG", format = default_format, rotation = "1 day", retention = '10 days')
nonebot.init()

# 加载定时组件
nonebot.init(apscheduler_autostart=True)

driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# Load plugins
plugin_loader.load_plugins(nonebot, 'plugins_conf.yaml')


# ----------- 从 src/plugins 加载插件, 这将是之后的标准
plugins_path = root / 'src' / 'plugins'
nonebot.load_plugins(plugins_path.absolute().as_posix())


@driver.on_shutdown
async def _():
    db_manager.close() 


if __name__ == "__main__":
    nonebot.run()

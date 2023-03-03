import nonebot
from pathlib import Path

root = Path(__file__).parent
nonebot.load_plugin(root / 'sub_manager.py')
nonebot.load_plugin(root / 'panel.py')

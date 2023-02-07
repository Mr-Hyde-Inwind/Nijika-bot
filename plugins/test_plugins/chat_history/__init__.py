import nonebot
from pathlib import Path
from utils.db import db_manager

sql = '''
CREATE TABLE CHAT_HISTORY(
  ID        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  USR_ID    INTEGER                           NOT NULL,
  GROUP_ID  INTEGER,
  MSG       TEXT                              NOT NULL,
  PLAIN     TEXT,
  TIMESTAMP INTEGER                           NOT NULL
);
'''

try:
  db_manager.get_default_connection().execute(sql)
except Exception as e:
  print(e)
  print("消息备份或许不可用")

nonebot.load_plugins(str(Path(__file__).parent.resolve()))
import sqlite3
import pathlib

_connections = {}

DB_ROOT = pathlib.Path(__file__).parent.joinpath('source').absolute().as_posix()
DEFAULT_DB = pathlib.Path(DB_ROOT).joinpath('ryou.db').absolute().as_posix()
pathlib.Path(DB_ROOT).mkdir(parents=True, exist_ok=True)

class DbConnection():
  def __init__(self, db_url: str):
    self._db_url = db_url
    self._conn = sqlite3.connect(db_url)
  
  def __repr__(self):
    return "DB connection to {url}".format(url = self._db_url)

  def execute(self, sql, params = ()):
    if sql.strip().lower().startswith('select'):
      errmsg = '{parameter}...: SELECT is not allowed in execute'.format(parameter = sql[:21])
      raise ValueError(errmsg)
    self._conn.cursor().execute(sql, params)
    self._conn.commit()
  
  def query(self, sql) -> list:
    if not sql.strip().lower().startswith('select'):
      errmsg = '{parameter}...: Only allowed SELECT SQL when querying DB'.format(parameter = sql[:21])
      raise ValueError(errmsg)

    cursor = self._conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_connection(db_path: str) -> DbConnection:
  return _connections.setdefault(db_path, DbConnection(db_path))

def get_default_connection() -> DbConnection:
  return get_connection(DEFAULT_DB)

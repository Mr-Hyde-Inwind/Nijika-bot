import os
from os import path
import sys
import pathlib
import pytest
import sqlite3
import shutil

_test_root = path.split(__file__)[0]
_db_source = path.join(_test_root, 'source')
_test_db_pathA = path.join(_db_source, 'testA.db')
_test_db_pathB = path.join(_db_source, 'testB.db')

sys.path.append(path.join(_test_root, "../"))

import db_manager

# 测试用例前创建表
@pytest.fixture(scope = 'function')
def create_test_table():
  conn = db_manager.get_connection(_test_db_pathA)
  conn.execute("CREATE TABLE movie(title, year, score)")

# 完成测试用例后删除表
@pytest.fixture(scope = 'function')
def drop_test_table():
  yield
  conn = db_manager.get_connection(_test_db_pathA)
  conn.execute("DROP TABLE movie")

class TestDb():
  def setup_class(self):
    pathlib.Path(_db_source).mkdir(parents=True, exist_ok=True)
    
  def teardown_class(self):
    shutil.rmtree(_db_source)

  def test_create_db(self):
    db_manager.get_connection(_test_db_pathA)
    db_manager.get_connection(_test_db_pathB)
    assert path.exists(_test_db_pathA)
    assert path.exists(_test_db_pathB)

  def test_get_same_connection(self):
    connA = db_manager.get_connection(_test_db_pathA)
    same_conn = db_manager.get_connection(_test_db_pathA)
    assert connA is same_conn

  def test_get_diff_connection(self):
    connA = db_manager.get_connection(_test_db_pathA)
    connB = db_manager.get_connection(_test_db_pathB)
    assert not connA is connB

  def test_connection_repr(self):
    connA = db_manager.get_connection(_test_db_pathA)
    assert repr(connA) == 'DB connection to {db_url}'.format(db_url = _test_db_pathA)

  def test_create_table(self, drop_test_table):
    conn = db_manager.get_connection(_test_db_pathA)
    conn.execute("CREATE TABLE movie(title, year, score)") 
    response_lst = conn.query("SELECT name from sqlite_master")
    assert response_lst[0][0] == 'movie'

  def test_insert_data(self, create_test_table, drop_test_table):
    sql = '''
       INSERT INTO movie VALUES ('Hello', '1997', '9.5')
    '''
    conn = db_manager.get_connection(_test_db_pathA)
    conn.execute(sql)
    response_lst = conn.query("SELECT * from movie")
    assert response_lst[0] == ('Hello', '1997', '9.5')

  def test_get_data_error(self, create_test_table, drop_test_table):
    conn = db_manager.get_connection(_test_db_pathA)

    # query 方法不接受 SELECT 以外的其他 SQL 语句
    with pytest.raises(ValueError):
      conn.query('INSERT INTO movie VALUES ("Hello", "1997", "9.5")')
    with pytest.raises(ValueError):
      conn.query('CREATE TABLE movie2(title, year, score)')

    # 其他执行错误交由 sqlite3 抛出异常
    with pytest.raises(sqlite3.OperationalError):
      conn.query("SELECT * fom movie")

  def test_execute_error(self, create_test_table, drop_test_table):
    conn = db_manager.get_connection(_test_db_pathA)
    with pytest.raises(ValueError):
      conn.execute('SELECT * from movie')
      
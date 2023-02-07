import sqlite3

SQL = '''
SELECT
  PLAIN
FROM
  CHAT_HISTORY
WHERE
  PLAIN NOT NULL
  AND PLAIN != ''
ORDER BY TIMESTAMP DESC
LIMIT 10
'''

conn = sqlite3.connect('ryou.db')
res = conn.execute(SQL)
print(res.fetchall())


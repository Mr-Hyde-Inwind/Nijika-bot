# 时间单位用 ms 考虑
import functools
import asyncio
from threading import Lock
from datetime import datetime
from time import time

class TokenBucket():
  class RateLimitException(Exception):
    def __str__(self) -> str:
      return 'Token in bucket is not enought'


  # 限速为 QPS 形式
  # 内部计时使用 milliseconds
  def __init__(self, capacity, refill_rate = 1):
    self._capacity = capacity * 1000
    self._refill_rate = refill_rate
    self._tokens = capacity * 1000
    self._last_fill_time = int(time() * 1000)
    self._lock = Lock()


  def refill(self):
    current = int(time() * 1000)
    new_tokens = self._tokens + (current - self._last_fill_time) * self._refill_rate
    self._tokens = min(new_tokens, self._capacity)
    self._last_fill_time = current


  def consume(self, token):
    self._lock.acquire() 
    self.refill()
    if self._tokens < (token * 1000):
      res = False
    else:
      self._tokens = self._tokens - token * 1000
      res = True
    self._lock.release()
    return res


  def try_acquire(self):
    if self.consume(1):
      return
    else:
      raise TokenBucket.RateLimitException()

  async def asyncsleep_and_try(self, max_retry = -1):
    retry_count = 0
    while True:
      if self.consume(1):
        break
      elif max_retry > 0 and retry_count >= max_retry:
        raise TokenBucket.RateLimitException()
      else:
        await asyncio.sleep(1 / self._refill_rate)

BUCKET_DICT = {
  'default': TokenBucket(capacity = 5, refill_rate = 1)
}


def async_with_rate_limit(id = 'default', capacity = 3, rate = 5, retry = False, max_retry = -1):
  bucket = BUCKET_DICT.setdefault(id, TokenBucket(capacity, rate))
  def decorate(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
      if retry:
        await bucket.asyncsleep_and_try(max_retry = max_retry)
      else:
        bucket.try_acquire()
      return await func(*args, **kwargs)
    return wrapper
  return decorate

if __name__ == '__main__':
  @async_with_rate_limit(id = 'test', capacity = 3, rate = 1, retry = True)
  async def test(id):
    print('work start id: ', id)
    await asyncio.sleep(3)
    print('success {} on {}'.format(id, datetime.now()))
    return id

  async def wrap():
    for future in asyncio.as_completed(map(test, range(10))):
      result = await future

  tasks = []

  loop = asyncio.get_event_loop()
  task = asyncio.ensure_future(wrap())

  loop.run_until_complete(task)
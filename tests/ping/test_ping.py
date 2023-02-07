import sys, os
import pytest
from nonebug import App

sys.path.append(os.getcwd())

@pytest.mark.asyncio
async def test_ping(app: App):
  from plugins.basic_plugins.ping import ping
  from tests.utils import make_fake_event, make_fake_message

  Message = make_fake_message()

  async with app.test_matcher(ping) as ctx:
    bot = ctx.create_bot()
    msg = Message("ping")
    event = make_fake_event(_message = msg, _to_me = True)()

    ctx.receive_event(bot, event)
    ctx.should_call_send(event, "はいはい、ここにいるよ～", True)
    ctx.should_finished()

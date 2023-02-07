from nonebug import App
import pytest


@pytest.mark.asyncio
async def test_backup(app: App):
  from plugins.test_plugins.chat_history.backup import message_backup
  from tests.utils import make_fake_event, make_fake_message
  Message = make_fake_message()

  async with app.test_matcher(message_backup) as ctx:
    pass
import sys, os
import pytest

from nonebug import App
sys.path.append(os.getcwd())


HELP_MSG = '''
todo [ACTTION] [TODO/EVENT ID]
Avaliable action:
  list:   list all todo events associated with your ID.
  add:    Add a new event to your list.
  finish: Mark a event finished in your list and delete it.
'''

EMPTY_LIST = "清单空空如也, 开摆!"

@pytest.mark.asyncio
async def test_todo(app: App):
  from plugins.test_plugins.todo import todo
  from tests.utils import make_fake_event, make_fake_message

  Message = make_fake_message()

  async with app.test_matcher(todo) as ctx:
    bot = ctx.create_bot()
    msg = Message("todo")
    event = make_fake_event(_message = msg, _to_me = True)()

    ctx.receive_event(bot, event)
    ctx.should_call_send(event, "请指定功能和必要参数捏, 或者试试 todo help 来获取帮助吧", True)
    ctx.should_finished()
  
  async with app.test_matcher(todo) as ctx:
    bot = ctx.create_bot()
    msg = Message("todo list")
    event = make_fake_event(_message = msg, to_me = True)()

    ctx.receive_event(bot, event)
    ctx.should_call_send(event, EMPTY_LIST, True)
    ctx.should_finished()
  
  async with app.test_matcher(todo) as ctx:
    bot = ctx.create_bot()
    msg = Message("todo help")
    event = make_fake_event(_message = msg, to_me = True)()

    ctx.receive_event(bot, event)
    ctx.should_call_send(event, HELP_MSG, True)
    ctx.should_finished()

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import ArgPlainText, CommandArg
from nonebot.adapters import Message
import random


roll = on_command("roll", rule = to_me(), priority = 5, block = True)

HELP_MSG = 'roll command should be like "roll [NUMBER OF DICE]d[NUMBER OF SURFACE], ' \
            'eg: 1d6 ([NUMBER OF DICE] <= 10) ' \
            'both of [NUMBER OF DICE] and [NUMBER OF SURFACE] should be positive"'

def check_params(params: list) -> bool:
  if len(params) != 2:
    return False
  if type(params[0]) is not int or type(params[0]) is not int:
    return False
  if params[0] < 0 or params[1] <= 0:
    return False
  return True
  

@roll.handle()
async def _(args: Message = CommandArg()):
  plain = args.extract_plain_text().strip().split()
  if len(plain) != 1:
    await roll.finish(HELP_MSG)
    return 
  params = plain[0].strip().split('d')

  try:
    params = [int(i) for i in params]
  except Exception as e:
    print(e)
    await roll.finish(HELP_MSG)
    return
  
  if not check_params(params):
    await roll.finish(HELP_MSG)
    return

  dices = [random.randint(1, params[1]) for i in range(params[0])]
  result = "\n".join(["%s. %s" % tup for tup in zip(range(1, params[0] + 1), dices)])
  result = plain[0] + "\n" + result

  await roll.finish(result)
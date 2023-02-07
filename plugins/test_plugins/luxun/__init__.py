import base64
import random
from io import BytesIO
from utils.config.path_config import IMAGE_PATH, FONT_PATH

from PIL import (
  Image,
  ImageDraw,
  ImageFont
)
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment, Message

LUXUN_PATH = IMAGE_PATH / "luxun" / "luxun.jpg"
HIMMLER_PATH = IMAGE_PATH / "luxun" / "himmler.jpg"
LUXUN_ANCHOR = "--鲁迅"

ANCHOR = {'luxun': '--鲁迅', 'himmler': '--Himmler'}
BACKGROUND_PATH = {'luxun': LUXUN_PATH, 'himmler': HIMMLER_PATH}

ANCHOR_FONT = ImageFont.truetype(font = (FONT_PATH / "msyh.ttf").absolute().as_posix(), size = 30)
TEXT_FONT = ImageFont.truetype(font = (FONT_PATH / "msyh.ttf").absolute().as_posix(), size = 34)

def draw_phrase(content: str, who: str) -> Image:
  im = Image.open(BACKGROUND_PATH[who].absolute().as_posix(), mode = 'r')
  draw = ImageDraw.Draw(im)
  add_text(im, draw, divide_text(im, content))
  add_anchor(im, draw, who)
  return im


def add_anchor(im: Image, draw: ImageDraw, who: str) -> Image:
  x = im.width - ANCHOR_FONT.getbbox(ANCHOR[who])[2] - 30
  y = im.height * 0.80 
  draw.text(xy = (x, y), text = ANCHOR[who], fill = (255, 255, 255), font = ANCHOR_FONT)
  return im

def add_text(im: Image, draw: ImageDraw, txt: str) -> Image:
  x = (im.width - TEXT_FONT.getbbox(txt)[2]) / 2
  y = im.height * 0.625
  draw.text(xy = (x, y), text = txt, fill = (255, 255, 255), font = TEXT_FONT)
  return im

def divide_text(background: Image, txt: str) -> str:
  divided = txt
  return divided

luxun = on_command("鲁迅说", aliases = {"鲁迅说过"}, priority = 5, block = True)

@luxun.handle()
async def _(arg: Message = CommandArg()):
  args = arg.extract_plain_text().strip()
  content = '我说什么了？'
  if args.startswith(",") or args.startswith("，"):
    args = args[1:].strip()
  if args:
    content = args
  if len(content) > 13:
    content = random.choice(['我没说过这话', '兄弟, 说这么多上不来气', '你来当大文豪 ^^;'])

  im = draw_phrase(content, 'luxun')
  buf = BytesIO()
  im.save(buf, format = 'PNG')
  b64_str = base64.b64encode(buf.getvalue()).decode()

  await luxun.send(MessageSegment.image("base64://" + b64_str))


himmler = on_command("希姆莱说", aliases = {"海因里希部长托我给您带个话", "希姆莱说过"}, priority = 5, block = True)
@himmler.handle()
async def _(arg: Message = CommandArg()):
  args = arg.extract_plain_text().strip()
  content = '我说什么了？'
  if args.startswith(",") or args.startswith("，"):
    args = args[1:].strip()
  if args:
    content = args
  if len(content) > 13:
    content = random.choice(['我没说过这话', '你有点太极端了 ^^;', '你来统帅盖世太保 ^^;'])

  im = draw_phrase(content, 'himmler')
  buf = BytesIO()
  im.save(buf, format = 'PNG')
  b64_str = base64.b64encode(buf.getvalue()).decode()

  await luxun.send(MessageSegment.image("base64://" + b64_str))

from bilireq.user import get_videos
from bilireq.video import get_video_share
import asyncio

res = asyncio.run(get_video_share('BV1dv4y1x79D'))
print(res)

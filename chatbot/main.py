import os
import re

from vkbottle.polling import BotPolling
from vkbottle.api import API
from vkbottle.bot import Bot
from vkbottle_types.events import GroupEventType

from model import Event

TOKEN = os.environ.get("API_TOKEN")
HASHTAGS = os.environ.get("HASHTAGS")
RECIPIENTS = os.environ.get("RECIPIENTS")

hashtags_pattern = re.compile(HASHTAGS.replace(',', '|'))

api = API(token=TOKEN)
polling = BotPolling(api, wait=2)
bot = Bot(api=api, polling=polling)


@bot.on.raw_event(event=[GroupEventType.WALL_REPLY_NEW, GroupEventType.WALL_POST_NEW], dataclass=Event)
async def wall_updates(event: Event):
    post = f"wall{event.object.owner_id}_{event.object.id}"
    if hashtags_pattern.findall(event.object.text.lower()):
        await api.messages.send(attachment=post, user_id=RECIPIENTS, random_id=0)


if __name__ == '__main__':
    bot.run_forever()

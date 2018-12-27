#from app import app
#app.run()
import json
import os
import requests
from pprint import pprint as pp

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_WEBHOOK_INC = os.environ.get('SLACK_WEBHOOK_INC')

def slack_post_msg(text, channel, **kwargs):
    data = {
        "token": SLACK_BOT_TOKEN,
        "channel": channel,
        "text": text
    }

    data.update(kwargs)

    response = requests.post(
        url="https://slack.com/api/chat.postMessage",
        data=data
    )

    pp("response from 'slack_post_msg' [%d]: %s" % (
            response.status_code,
            json.dumps(json.loads(response.text), indent=4)
    ))

slack_post_msg(
    text='Hello from epic bot!',
    channel='testch',
    #channel='#random',
    icon_emoji=':sunglasses:'
    )
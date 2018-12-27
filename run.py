#from app import app
#app.run()
import json
import os

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_WEBHOOK_INC = os.environ.get('SLACK_WEBHOOK_INC')

def slack_send_webhook(text, channel, **kwargs):

    data = {
        "channel": channel,
        "text": text
    }

    data.update(kwargs)

    response = requests.post(
        url=SLACK_WEBHOOK_INC,
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    pp("response from 'send_webhook' [%d]: %s" % (
        response.status_code,
        response.text
    ))

slack_send_webhook(
text='Hello from epic bot!',
#channel='#general',
channel='#testch', #"#random"
icon_emoji=':sunglasses:'
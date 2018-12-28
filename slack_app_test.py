import json
import os
import requests
from flask import Flask, make_response
from pprint import pprint as pp

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_WEBHOOK_INC = os.environ.get('SLACK_WEBHOOK_INC')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def on_root():
    return make_response('<h1>Hello world!</h1>', 200)

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

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, threaded=True)
# slack_post_msg(
#     text='Hello from epic bot!',
#     channel='testch',
#     #channel='#random',
#     icon_emoji=':sunglasses:'
#     )
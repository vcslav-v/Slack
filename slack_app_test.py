import json
import resources
import flask
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

@app.route('/api/income', methods=['POST'])
def income_get():
    data = {
        "token": SLACK_BOT_TOKEN,
        'trigger_id': flask.request.values["trigger_id"],
        "dialog": json.dumps(resources.dialog_income)
    }

    response = requests.post(
        url="https://slack.com/api/dialog.open",
        data=data
    )

    pp(response)

    return make_response("Processing started...", 200)


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
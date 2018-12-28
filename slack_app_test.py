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

@app.route('/api/interactive_action', methods=['POST'])
def on_interactive_action():

    response_text = ''
    interactive_action = json.loads(flask.request.values["payload"])

    try:

        if interactive_action["type"] == "interactive_message":
            pass

        elif interactive_action["type"] == "dialog_submission":
            write_gdoc(interactive_action)

    except Exception as ex:
        response_text = ":x: Error: `%s`" % ex

    return make_response(response_text, 200)

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

def write_gdoc(message):

    pp('Task started...')

    response_text = 'Good'

    slack_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:',
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
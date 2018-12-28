import json
import resources
import flask
import os
import requests
from flask import Flask, make_response
from pprint import pprint as pp
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_WEBHOOK_INC = os.environ.get('SLACK_WEBHOOK_INC')
PLUS_ROW = '3'

app = Flask(__name__)

# штука чисто для теста - отдает hello world если зайти на url бота
@app.route('/', methods=['GET'])
def on_root():
    return make_response('<h1>Hello world!</h1>', 200)

# поднимается на слэш команду /income добавляем новый доход
@app.route('/api/income', methods=['POST'])
def income_get():
    data = {
        'token': SLACK_BOT_TOKEN,
        'trigger_id': flask.request.values['trigger_id'],
        'dialog': json.dumps(resources.dialog_income)
    }

    response = requests.post(
        url='https://slack.com/api/dialog.open',
        data=data
    )

    pp(response)

    return make_response('Processing started...', 200)

# Обрабатываем форму
@app.route('/api/interactive_action', methods=['POST'])
def on_interactive_action():
    pp('foo!')
    

    response_text = 'bad'
    interactive_action = json.loads(flask.request.values['payload'])
    pp(interactive_action)

    try:
        if interactive_action['callback_id'] == 'income_form':
            pass

        elif interactive_action['type'] == 'dialog_submission':
            if interactive_action['title'] == 'Доход':
                pp('HI!')
                write_income_gdoc(interactive_action)

    except Exception as ex:
        response_text = ':x: Error: `%s`' % ex

    return make_response(response_text, 200)

def slack_post_msg(text, channel, **kwargs):
    data = {
        'token': SLACK_BOT_TOKEN,
        'channel': channel,
        'text': text
    }

    data.update(kwargs)

    response = requests.post(
        url='https://slack.com/api/chat.postMessage',
        data=data
    )

    pp("response from 'slack_post_msg' [%d]: %s" % (
            response.status_code,
            json.dumps(json.loads(response.text), indent=4)
    ))

def slack_send_webhook(text, channel, **kwargs):

    data = {
        'channel': channel,
        'text': text
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

# Пишем в google sheet
def write_income_gdoc(message):

    
    pp('Task started...')
    submission = message['submission']

    response_text = 'Good'
    tm = datetime.strftime(datetime.now(), '%m')

    if submission['income_from'] == 'plus':
        income_plus_writer(table_currency_changer(submission['income_currency']), submission['income_value'], tm)
    elif submission['income_from'] == 'banners':
        response_text = 'Banners'
    elif submission['income_from'] == 'email':
        response_text = 'Email'
    elif submission['income_from'] == 'products':
        response_text = 'Products'


    slack_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:',
    )

def table_currency_changer(cur):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(resources.client_secret, scope)
    client = gspread.authorize(creds)

    if cur == 'usd':
        sheet = client.open('PB2019USD').sheet1
    elif cur == 'rur':
        sheet = client.open('PB2019RUR').sheet1
    elif cur == 'eur':
        sheet = client.open('PB2019EUR').sheet1
    return sheet

def income_plus_writer(table, income, tm):
    letter = resources.mouth_dic[tm]
    place = letter + PLUS_ROW
    data = table.acell(place, 'FORMULA')

    if data[:1] == '=':
        data = data + '+' + income
    else:
        data = '=' + income

    table.update_acell(place, data)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
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
from flask_sqlalchemy import SQLAlchemy

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_WEBHOOK_INC = os.environ.get('SLACK_WEBHOOK_INC')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

import models

# штука чисто для теста - отдает hello world если зайти на url бота
@app.route('/', methods=['GET'])
def on_root():
    return make_response('sec', 200)

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

@app.route('/api/expense', methods=['POST'])
def expense_get():
    data = {
        'token': SLACK_BOT_TOKEN,
        'trigger_id': flask.request.values['trigger_id'],
        'dialog': json.dumps(resources.dialog_expense)
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
    response_text = ''
    interactive_action = json.loads(flask.request.values['payload'])
    pp(interactive_action)

    try:
        if interactive_action['type'] == 'interactive_message':
            pass

        elif interactive_action['type'] == 'dialog_submission':
            if interactive_action['callback_id'] == 'income_form':
                write_income_gdoc(interactive_action)
            elif interactive_action['callback_id'] == 'expense_form':
                write_expense_gdoc(interactive_action)
            elif interactive_action['callback_id'] == 'dialog_income_email':
                write_email_income(interactive_action)

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

    submission = message['submission']

    response_text = 'Smth bad'
    tm = datetime.strftime(datetime.now(), '%m')

    if submission['income_from'] == 'plus':
        if submission['comment'] == '':
            response_text = (resources.plus_income+submission['income_value'] + submission['income_currency'] + ' / '
                            + submission['income_to'])
        else:
            response_text = (resources.plus_income + submission['income_value'] + submission['income_currency'] + ' / '
                            + submission['income_to'] + ' / ' + submission['comment'])
        gdoc_writer(table_currency_changer(submission['income_currency']), submission['income_value'], tm, resources.PLUS_ROW)
    
    elif submission['income_from'] == 'banners':
        if submission['comment'] == '':
            response_text = (resources.banner_income+submission['income_value'] + submission['income_currency'] + ' / '
                            + submission['income_to'])
        else:
            response_text = (resources.banner_income+submission['income_value'] + submission['income_currency'] + ' / '
                            + submission['income_to'] + ' / ' + submission['comment'])
        gdoc_writer(table_currency_changer(submission['income_currency']), submission['income_value'], 
                            tm, resources.BANNERS_ROW)
    
    elif submission['income_from'] == 'email':
        try:
            del_row = models.finam_income.query.filter_by(user_id = message['user']['id']).first()
            if del_row:
                db.session.delete(del_row)
            new_row = models.finam_income(chanel_id = message['channel']['id'], income_value = submission['income_value'], 
            income_currency = submission['income_currency'], income_to = submission['income_to'], 
            comment = submission['comment'], income_from = submission['income_from'], user_id = message['user']['id'])
            db.session.add(new_row)
            db.session.commit()

            pp(message)

            make_response('', 200)

            data = {
            'token': SLACK_BOT_TOKEN,
            'channel': message['channel']['id'],
            'dialog': json.dumps(resources.dialog_income_email)
            }

            # response = requests.post(
            # url='https://slack.com/api/dialog.open',
            # data=data
            # )

            slack_send_webhook(
            text=response_text,
            channel=message['channel']['id'],
            icon=':chart_with_upwards_trend:',
            dialog=json.dumps(resources.dialog_income_email)
            )
            
        except Exception as ex:
            response_text = ':x: Error: `%s`' % ex

    elif submission['income_from'] == 'products':
        response_text = 'Products'


    slack_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:'
    )

def write_email_income(message):

    submission = message['submission']

    response_text = 'Smth bad'
    tm = int(datetime.strftime(datetime.now(), '%m'))
    data = models.finam_income.query.filter_by(user_id = message['user']['id']).first()
    response_text = data['comment']


    # if data['comment'] == '':
    #         response_text = (resources.plus_income+submission['income_value'] + submission['income_currency'] + ' / '
    #                         + submission['income_to'])
    #     else:
    #         response_text = (resources.plus_income+submission['income_value'] + submission['income_currency'] + ' / '
    #                         + submission['income_to'] + ' / ' + submission['comment'])
    #     gdoc_writer(table_currency_changer(submission['income_currency']), submission['income_value'], tm, resources.PLUS_ROW)

    slack_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:'
    )

def write_expense_gdoc(message):

    submission = message['submission']

    response_text = 'Smth bad'
    tm = datetime.strftime(datetime.now(), '%m')

    if submission['expense_to'] == 'Products':
        pass

    elif submission['expense_to'] == 'Tech':
        if submission['comment'] == '':
            response_text = (resources.tech_expense + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
        else:
            response_text = (resources.tech_expense + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
        gdoc_writer(table_currency_changer(submission['expense_currency']), submission['expense_value'], tm, 
                    resources.TECH_ROW)

    elif submission['expense_to'] == 'Аренда':
        if submission['comment'] == '':
            response_text = (resources.rent + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
        else:
            response_text = (resources.rent + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
        gdoc_writer(table_currency_changer(submission['expense_currency']), submission['expense_value'], tm, 
                    resources.RENT_ROW)

    elif submission['expense_to'] == 'Инвестиции':
        if submission['comment'] == '':
            response_text = (resources.invest + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
        else:
            response_text = (resources.invest + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
        gdoc_writer(table_currency_changer(submission['expense_currency']), submission['expense_value'], tm, 
                    resources.INVEST_ROW)

    elif submission['expense_to'] == 'Иное':
        if submission['comment'] == '':
            response_text = (resources.other_expense + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
        else:
            response_text = (resources.other_expense + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
        gdoc_writer(table_currency_changer(submission['expense_currency']), submission['expense_value'], tm, 
                    resources.OTHER_EXP_ROW)

    slack_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:'
    )

def table_currency_changer(cur):
    pp('table_currency_changer')
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(resources.client_secret, scope)
    client = gspread.authorize(creds)

    if cur == 'USD':
        sheet = client.open('PB2019USD').sheet1
    elif cur == 'RUR':
        sheet = client.open('PB2019RUR').sheet1
    elif cur == 'EUR':
        sheet = client.open('PB2019EUR').sheet1
    return sheet

def gdoc_writer(table, income, tm, row):
    pp('gdoc_writer')
    letter = resources.month_dic[str(tm)]
    place = letter + row
    data = table.acell(place, 'FORMULA')

    if data.value[:1] == '=':
        data = data.value + '+' + income
    else:
        data = '=' + income

    table.update_acell(place, data)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
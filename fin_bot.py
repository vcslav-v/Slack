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
from concurrent.futures import ThreadPoolExecutor

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_WEBHOOK_INC = os.environ.get('SLACK_WEBHOOK_INC')

app = Flask(__name__)
executor = ThreadPoolExecutor(1)

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

    requests.post(
        url='https://slack.com/api/dialog.open',
        data=data
    )

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
                executor.submit(
                write_income_gdoc,
                interactive_action)
            elif interactive_action['callback_id'] == 'expense_form':
                executor.submit(
                write_expense_gdoc,
                interactive_action)

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
    
    elif submission['income_from'][:5] == 'Email':
        if submission['comment'] == '':
            response_text = (resources.income + submission['income_from'] + '* / ' + submission['income_value'] 
                            + submission['income_currency'] + ' / ' + submission['income_to'])
        else:
            response_text = (resources.income + submission['income_from'] + '* / ' +submission['income_value'] 
                            + submission['income_currency'] + ' / ' + submission['income_to'] + ' / ' 
                            + submission['comment'])

        gdoc_writer(table_currency_changer(submission['income_currency']), submission['income_value'], 
                            tm, resources.EMAIL_COLUMNS[submission['income_from']], False, 'Доход-Email')

    elif submission['income_from'][:7] == 'Markets' or submission['income_from'][:5] == 'Deals':
        if submission['comment'] == '':
            response_text = (resources.income + submission['income_from'] + '* / ' + submission['income_value'] 
                            + submission['income_currency'] + ' / ' + submission['income_to'])
        else:
            response_text = (resources.income + submission['income_from'] + '* / ' +submission['income_value'] 
                            + submission['income_currency'] + ' / ' + submission['income_to'] + ' / ' 
                            + submission['comment'])

        gdoc_writer(table_currency_changer(submission['income_currency']), submission['income_value'], 
                            tm, resources.PRODUCTS_COLUMNS[submission['income_from']], False, 'Доход-Products')


    slack_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:'
    )

def write_expense_gdoc(message):

    submission = message['submission']

    response_text = 'Smth bad'
    tm = datetime.strftime(datetime.now(), '%m')

    if submission['expense_to'][:8] == 'Products':
        if submission['comment'] == '':
            response_text = (resources.expense + submission['expense_to'] + '* / ' + submission['expense_value'] 
                            + submission['expense_currency'] + ' / ' + submission['expense_from'])
        else:
            response_text = (resources.expense + submission['expense_to'] + '* / ' + submission['expense_value'] 
                            + submission['expense_currency'] + ' / ' + submission['expense_from'] + ' / ' 
                            + submission['comment'])

        gdoc_writer(table_currency_changer(submission['expense_currency']), submission['expense_value'], 
                            tm, resources.PRODUCTS_EXPENSE_COLUMNS[submission['expense_to']], False, 'Расх-Products')

    elif submission['expense_to'] == 'Tech':
        if submission['comment'] == '':
            response_text = (resources.tech_expense + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
        else:
            response_text = (resources.tech_expense + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
        table = table_currency_changer(submission['expense_currency'])

        gdoc_writer(table, submission['expense_value'], tm, resources.TECH_ROW)
        # gdoc_account_writer(table, str(int(submission['expense_value']) * (-1)), submission['expense_from'])

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

def gdoc_writer(table, income, tm, category, flat=True, sheet = ''):

    if flat:
        letter = resources.month_dic[str(tm)]
        place = letter + category
    else:
        row = str(int(tm)+1)
        place = category + row
    
    if sheet:
        table = table.spreadsheet.worksheet(sheet)

    data = table.acell(place, 'FORMULA')

    if data.value[:1] == '=':
        data = data.value + '+' + income
    else:
        data = '=' + income

    table.update_acell(place, data)

def gdoc_account_writer(table, value, acc):
    table = table.spreadsheet.worksheet('Счета')
    letter = resources.ACC_COLUMNS[acc]
    rows = table.col_values(resources.NUM_to_COLUMNS(letter))
    new_row = rows.count() + 1
    place = letter + str(new_row)

    table.update_acell(place, value)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
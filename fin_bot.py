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

MATTERMOST_WEBHOOK_INC = os.environ.get('mattermostWebhook')

app = Flask(__name__)
executor = ThreadPoolExecutor(1)

# штука чисто для теста - отдает hello world если зайти на url бота
@app.route('/', methods=['GET'])
def on_root():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(resources.client_secret, scope)
    client = gspread.authorize(creds)
    sheet = client.open('PB2020USD').sheet1
    cop = client.copy('1MER7Evxjaszv1aAjPONZqvogpYCQ5EmWV49zI3q7MeY', 'PB2020USD-copy', True) 

    return make_response(str(cop), 200)

# поднимается на слэш команду /income добавляем новый доход
@app.route('/api/income', methods=['POST'])
def income_get():
    data = {
        'trigger_id': flask.request.values['trigger_id'],
        'url':'https://{}/api/interactive_action'.format(os.environ.get('SelfUrl')),
        'dialog': resources.dialog_income
    }

    requests.post(
        url='https://{}/api/v4/actions/dialogs/open'.format(os.environ.get('MattermostUrl')),
        json=data
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

@app.route('/api/trans', methods=['POST'])
def trans():
    data = {
        'token': SLACK_BOT_TOKEN,
        'trigger_id': flask.request.values['trigger_id'],
        'dialog': json.dumps(resources.dialog_trans)
    }

    requests.post(
        url='https://slack.com/api/dialog.open',
        data=data
    )

    return make_response('Processing started...', 200)

@app.route('/api/tocash', methods=['POST'])
def tocash():
    data = {
        'token': SLACK_BOT_TOKEN,
        'trigger_id': flask.request.values['trigger_id'],
        'dialog': json.dumps(resources.dialog_tocash)
    }

    requests.post(
        url='https://slack.com/api/dialog.open',
        data=data
    )

    return make_response('Processing started...', 200)


# Обрабатываем форму
@app.route('/api/interactive_action', methods=['POST'])
def on_interactive_action():
    interactive_action = flask.request.json
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
            """
            Тк эти опции работали не верно - закоменчено до лучших времён
            elif interactive_action['callback_id'] == 'trans_form':
                executor.submit(
                write_trans_gdoc,
                interactive_action)
            
            elif interactive_action['callback_id'] == 'tocash_form':
                executor.submit(
                write_tocash_gdoc,
                interactive_action)
                pass
            """
    except Exception as ex:
        response_text = ':x: Error: `%s`' % ex

    return make_response('response_text', 200)


def mattermost_send_webhook(text, **kwargs):

    data = {
        'text': text
    }

    data.update(kwargs)

    response = requests.post(
        url=MATTERMOST_WEBHOOK_INC,
        json=data,
        headers={'content-type': 'application/json'}
    )

    pp("response from 'send_webhook' [%d]: %s" % (
        response.status_code,
        response.text
    ))

# Пишем в google sheet
def write_income_gdoc(message):
    pp('write_income_gdoc')

    submission = message['submission']
    pp(submission)
    response_text = 'Smth bad'
    tm = datetime.strftime(datetime.now(), '%m')
    pp(submission['income_from'] == 'inthedesignest')

    if submission['income_from'] == 'plus':
        if submission['comment'] == '':
            response_text = (resources.plus_income+submission['income_value'] + ' ' +submission['income_currency'] + ' / '
                            + submission['income_to'])
            comment = submission['income_from']
        else:
            response_text = (resources.plus_income + submission['income_value'] + ' ' + submission['income_currency'] + ' / '
                            + submission['income_to'] + ' / ' + submission['comment'])
            comment = submission['income_from'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['income_currency'])

        gdoc_writer(table, submission['income_value'], tm, resources.PLUS_ROW)
        gdoc_account_writer(table, submission['income_value'], submission['income_to'], comment)
    
    elif submission['income_from'] == 'banners':
        if submission['comment'] == '':
            response_text = (resources.banner_income+submission['income_value'] + ' ' + submission['income_currency'] + ' / '
                            + submission['income_to'])
            comment = submission['income_from']
        else:
            response_text = (resources.banner_income+submission['income_value'] + ' ' + submission['income_currency'] + ' / '
                            + submission['income_to'] + ' / ' + submission['comment'])
            comment = submission['income_from'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['income_currency'])
        gdoc_writer(table, submission['income_value'], tm, resources.BANNERS_ROW)
        gdoc_account_writer(table, submission['income_value'], submission['income_to'], comment)

    elif submission['income_from'] == 'inthedesignest':
        if submission['comment'] == '':
            response_text = (resources.designest_income+submission['income_value'] + ' ' + submission['income_currency'] + ' / '
                            + submission['income_to'])
            comment = submission['income_from']
        else:
            response_text = (resources.designest_income+submission['income_value'] + ' ' + submission['income_currency'] + ' / '
                            + submission['income_to'] + ' / ' + submission['comment'])
            comment = submission['income_from'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['income_currency'])
        gdoc_writer(table, submission['income_value'], tm, resources.DESIGNEST_INCOME_ROW)
        gdoc_account_writer(table, submission['income_value'], submission['income_to'], comment)
    
    elif submission['income_from'][:5] == 'Email':
        if submission['comment'] == '':
            response_text = (resources.income + submission['income_from'] + '* / ' + submission['income_value'] 
                            + ' ' + submission['income_currency'] + ' / ' + submission['income_to'])
            comment = submission['income_from']
        else:
            response_text = (resources.income + submission['income_from'] + '* / ' +submission['income_value'] 
                            + ' ' + submission['income_currency'] + ' / ' + submission['income_to'] + ' / ' 
                            + submission['comment'])
            comment = submission['income_from'] + ' / ' + submission['comment']

        table = table_currency_changer(submission['income_currency'])
        gdoc_writer(table, submission['income_value'], tm, resources.EMAIL_COLUMNS[submission['income_from']],
                    False, 'Доход-Email')
        gdoc_account_writer(table, submission['income_value'], submission['income_to'], comment)

    elif submission['income_from'][:12] == 'Marketplaces' or submission['income_from'][:5] == 'Deals':
        if submission['comment'] == '':
            response_text = (resources.income + submission['income_from'] + '* / ' + submission['income_value'] 
                            + ' ' + submission['income_currency'] + ' / ' + submission['income_to'])
            comment = submission['income_from']
        else:
            response_text = (resources.income + submission['income_from'] + '* / ' +submission['income_value'] 
                            + ' ' + submission['income_currency'] + ' / ' + submission['income_to'] + ' / ' 
                            + submission['comment'])
            comment = submission['income_from'] + ' / ' + submission['comment']

        table = table_currency_changer(submission['income_currency'])
        gdoc_writer(table, submission['income_value'], tm, resources.PRODUCTS_COLUMNS[submission['income_from']], 
                    False, 'Доход-Products')
        gdoc_account_writer(table, submission['income_value'], submission['income_to'], comment)

    elif submission['income_from'][:5] == 'Stock':
        if submission['comment'] == '':
            response_text = (resources.income + submission['income_from'] + '* / ' + submission['income_value'] 
                            + ' ' + submission['income_currency'] + ' / ' + submission['income_to'])
            comment = submission['income_from']
        else:
            response_text = (resources.income + submission['income_from'] + '* / ' +submission['income_value'] 
                            + ' ' + submission['income_currency'] + ' / ' + submission['income_to'] + ' / ' 
                            + submission['comment'])
            comment = submission['income_from'] + ' / ' + submission['comment']

        table = table_currency_changer(submission['income_currency'])
        gdoc_writer(table, submission['income_value'], tm, resources.STOCKS_COLUMNS[submission['income_from']], 
                    False, 'Доход-Stocks')
        gdoc_account_writer(table, submission['income_value'], submission['income_to'], comment)

    pp(response_text)
    mattermost_send_webhook(
        text=response_text,
        icon=':chart_with_upwards_trend:'
    )
"""
def write_trans_gdoc(message):
    submission = message['submission']
    try:
        table = table_currency_changer(submission['trans_currency'])
        table = table.spreadsheet.worksheet('Счета')
        from_letter = resources.ACC_COLUMNS[submission['trans_from']]
        rows = table.col_values(resources.COLUMNS_TO_NUM[from_letter])
        new_row = len(rows) + 1
        place = from_letter + str(new_row)
        table.update_acell(place, '-' + submission['trans_value'])
        c_from_letter = resources.NUM_to_COLUMNS[resources.COLUMNS_TO_NUM[from_letter]+1]
        comment_place = c_from_letter + str(new_row)
        table.update_acell(comment_place, 'Перевод в ' + submission['trans_to'])

        to_letter = resources.ACC_COLUMNS[submission['trans_to']]
        rows = table.col_values(resources.COLUMNS_TO_NUM[to_letter])
        new_row = len(rows) + 1
        place = to_letter + str(new_row)
        table.update_acell(place, submission['trans_value'])
        c_to_letter = resources.NUM_to_COLUMNS[resources.COLUMNS_TO_NUM[to_letter]+1]
        comment_place = c_to_letter + str(new_row)
        table.update_acell(comment_place, 'Перевод  из ' + submission['trans_from'])

    except Exception as ex:
            pp(ex)

    response_text = ('*Перевод* из ' + submission['trans_from'] + ' в ' + submission['trans_to'] + ' ' +
                    submission['trans_value'] + ' ' + submission['trans_currency'])

    mattermost_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:'
    )
    
def write_tocash_gdoc(message):
    submission = message['submission']
    try:
        table = table_currency_changer(submission['currency'])
        table = table.spreadsheet.worksheet('Счета')
        letter = resources.ACC_COLUMNS[submission['to_cash_acc']]
        rows = table.col_values(resources.COLUMNS_TO_NUM[letter])
        new_row = len(rows) + 1
        place = letter + str(new_row)
        table.update_acell(place, '-' + submission['value'])
        c_letter = resources.NUM_to_COLUMNS[resources.COLUMNS_TO_NUM[letter]+1]
        comment_place = c_letter + str(new_row)
        table.update_acell(comment_place, 'Вывод')

    except Exception as ex:
            pp(ex)

    response_text = ('*Вывод* из ' + submission['to_cash_acc'] + ' / ' + submission['value'] + ' ' + submission['currency'])

    mattermost_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:'
    )       
"""
def write_expense_gdoc(message):

    submission = message['submission']

    response_text = 'Smth bad'
    tm = datetime.strftime(datetime.now(), '%m')

    if submission['expense_to'][:8] == 'Products':
        if submission['comment'] == '':
            response_text = (resources.expense + submission['expense_to'] + '* / ' + submission['expense_value'] 
                            + ' ' + submission['expense_currency'] + ' / ' + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.expense + submission['expense_to'] + '* / ' + submission['expense_value'] 
                            + ' ' + submission['expense_currency'] + ' / ' + submission['expense_from'] + ' / ' 
                            + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']

        table = table_currency_changer(submission['expense_currency'])
        gdoc_writer(table, submission['expense_value'], tm, resources.PRODUCTS_EXPENSE_COLUMNS[submission['expense_to']],
                    False, 'Расх-Products')
        
        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    elif submission['expense_to'] == 'Content - TheDesignest':
        if submission['comment'] == '':
            response_text = (resources.designest_content + submission['expense_value'] + ' ' + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.designest_content + submission['expense_value'] + ' ' + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['expense_currency'])

        gdoc_writer(table, submission['expense_value'], tm, resources.DESIGNEST_ROW)

        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    elif submission['expense_to'] == 'Tech':
        if submission['comment'] == '':
            response_text = (resources.tech_expense + submission['expense_value'] + ' ' + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.tech_expense + submission['expense_value'] + ' ' + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['expense_currency'])

        gdoc_writer(table, submission['expense_value'], tm, resources.TECH_ROW)
            
        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    elif submission['expense_to'] == 'Аренда':
        if submission['comment'] == '':
            response_text = (resources.rent + submission['expense_value'] + ' ' + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.rent + submission['expense_value'] + ' ' + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['expense_currency'])
        gdoc_writer(table, submission['expense_value'], tm, resources.RENT_ROW)
        
        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    elif submission['expense_to'] == 'Инвестиции':
        if submission['comment'] == '':
            response_text = (resources.invest + submission['expense_value'] + ' ' + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.invest + submission['expense_value'] + ' ' + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['expense_currency'])
        gdoc_writer(table, submission['expense_value'], tm, resources.INVEST_ROW)
        
        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    elif submission['expense_to'] == 'Иное':
        if submission['comment'] == '':
            response_text = (resources.other_expense + submission['expense_value'] + ' ' + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.other_expense + submission['expense_value'] + ' ' + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['expense_currency'])
        gdoc_writer(table, submission['expense_value'], tm, resources.OTHER_EXP_ROW)

        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    mattermost_send_webhook(
        text=response_text,
        icon=':chart_with_upwards_trend:'
    )

def table_currency_changer(cur):

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(resources.client_secret, scope)
    client = gspread.authorize(creds)

    if cur == 'USD':
        sheet = client.open('PB2020USD').sheet1
    elif cur == 'RUR':
        sheet = client.open('PB2020RUR').sheet1
    elif cur == 'EUR':
        sheet = client.open('PB2020EUR').sheet1
    return sheet

def gdoc_writer(table, income, tm, category, flat=True, sheet = ''):
    pp('gdoc_writer')

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

def gdoc_account_writer(table, value, acc, comment):
    
    if float(value)<0 and acc=='Nick Cash' or acc=='Mello Cash' or acc== 'Mello Bank':
        b_letter = 'c'
        try:
            balance = table.spreadsheet.worksheet('Баланс Ник/Мелло')
            if acc=='Nick Cash': 
                b_letter = 'a'
            rows = balance.col_values(resources.COLUMNS_TO_NUM[b_letter])
            new_row = len(rows) + 1
            place = b_letter + str(new_row)
            balance.update_acell(place, value)

            c_letter = resources.NUM_to_COLUMNS[resources.COLUMNS_TO_NUM[b_letter]+1]
            comment_place = c_letter + str(new_row)
            balance.update_acell(comment_place, comment)

        except Exception as ex:
            pp(ex)
            comment = comment + ' / ' + 'НЕ В БАЛАНСЕ!'

    table = table.spreadsheet.worksheet('Счета')
    letter = resources.ACC_COLUMNS[acc]

    rows = table.col_values(resources.COLUMNS_TO_NUM[letter])
    new_row = len(rows) + 1
    place = letter + str(new_row)

    table.update_acell(place, value)


    c_letter = resources.NUM_to_COLUMNS[resources.COLUMNS_TO_NUM[letter]+1]
    comment_place = c_letter + str(new_row)

    table.update_acell(comment_place, comment)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
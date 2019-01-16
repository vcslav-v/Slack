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
                try:
                    float(interactive_action['submission']['income_value'])
                except Exception as ex:
                    slack_send_webhook(text=ex, channel=interactive_action['channel']['id'])
                    return make_response(response_text, 200)
                executor.submit(
                write_income_gdoc,
                interactive_action)
                    
            elif interactive_action['callback_id'] == 'expense_form':
                try:
                    float(interactive_action['submission']['expense_value'])
                except Exception as ex:
                    slack_send_webhook(text=ex, channel=interactive_action['channel']['id'])
                    return make_response(response_text, 200)

                executor.submit(
                write_expense_gdoc,
                interactive_action)

            elif interactive_action['callback_id'] == 'trans_form':
                try:
                    float(interactive_action['submission']['trans_value_from'])
                    float(interactive_action['submission']['trans_value_to'])
                except Exception as ex:
                    slack_send_webhook(text=ex, channel=interactive_action['channel']['id'])
                    return make_response(response_text, 200)

                executor.submit(
                write_trans_gdoc,
                interactive_action)
                pass

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
    pp('write_income_gdoc')

    submission = message['submission']

    response_text = 'Smth bad'
    tm = datetime.strftime(datetime.now(), '%m')

    if submission['income_from'] == 'plus':
        if submission['comment'] == '':
            response_text = (resources.plus_income+submission['income_value'] + submission['income_currency'] + ' / '
                            + submission['income_to'])
            comment = submission['income_from']
        else:
            response_text = (resources.plus_income + submission['income_value'] + submission['income_currency'] + ' / '
                            + submission['income_to'] + ' / ' + submission['comment'])
            comment = submission['income_from'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['income_currency'])

        gdoc_writer(table, submission['income_value'], tm, resources.PLUS_ROW)
        gdoc_account_writer(table, submission['income_value'], submission['income_to'], comment)
    
    elif submission['income_from'] == 'banners':
        if submission['comment'] == '':
            response_text = (resources.banner_income+submission['income_value'] + submission['income_currency'] + ' / '
                            + submission['income_to'])
            comment = submission['income_from']
        else:
            response_text = (resources.banner_income+submission['income_value'] + submission['income_currency'] + ' / '
                            + submission['income_to'] + ' / ' + submission['comment'])
            comment = submission['income_from'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['income_currency'])
        gdoc_writer(table, submission['income_value'], tm, resources.BANNERS_ROW)
        gdoc_account_writer(table, submission['income_value'], submission['income_to'], comment)
    
    elif submission['income_from'][:5] == 'Email':
        if submission['comment'] == '':
            response_text = (resources.income + submission['income_from'] + '* / ' + submission['income_value'] 
                            + submission['income_currency'] + ' / ' + submission['income_to'])
            comment = submission['income_from']
        else:
            response_text = (resources.income + submission['income_from'] + '* / ' +submission['income_value'] 
                            + submission['income_currency'] + ' / ' + submission['income_to'] + ' / ' 
                            + submission['comment'])
            comment = submission['income_from'] + ' / ' + submission['comment']

        table = table_currency_changer(submission['income_currency'])
        gdoc_writer(table, submission['income_value'], tm, resources.EMAIL_COLUMNS[submission['income_from']],
                    False, 'Доход-Email')
        gdoc_account_writer(table, submission['income_value'], submission['income_to'], comment)

    elif submission['income_from'][:12] == 'Marketplaces' or submission['income_from'][:5] == 'Deals':
        if submission['comment'] == '':
            response_text = (resources.income + submission['income_from'] + '* / ' + submission['income_value'] 
                            + submission['income_currency'] + ' / ' + submission['income_to'])
            comment = submission['income_from']
        else:
            response_text = (resources.income + submission['income_from'] + '* / ' +submission['income_value'] 
                            + submission['income_currency'] + ' / ' + submission['income_to'] + ' / ' 
                            + submission['comment'])
            comment = submission['income_from'] + ' / ' + submission['comment']

        table = table_currency_changer(submission['income_currency'])
        gdoc_writer(table, submission['income_value'], tm, resources.PRODUCTS_COLUMNS[submission['income_from']], 
                    False, 'Доход-Products')
        gdoc_account_writer(table, submission['income_value'], submission['income_to'], comment)


    slack_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:'
    )

def write_trans_gdoc(message):
    submission = message['submission']
    try:
        fee_table = table_currency_changer('FEE')
        fee = float(submission['trans_value_from']) - float(submission['trans_value_to'])
        if fee != 0:
            com_letter = 'a'
            rows = fee_table.col_values(resources.COLUMNS_TO_NUM[com_letter])
            new_row = len(rows) + 1
            place = com_letter + str(new_row)
            fee_table.update_acell(place, str(fee))
            com_letter = 'b'
            place = com_letter + str(new_row)
            fee_table.update_acell(place, submission['trans_currency'])
            com_letter = 'c'
            place = com_letter + str(new_row)
            fee_table.update_acell(place, submission['trans_from'])
            com_letter = 'd'
            place = com_letter + str(new_row)
            fee_table.update_acell(place, submission['trans_to'])
    except expression as ex:
        pp(ex)

    if submission['trans_currency'][:3]==submission['trans_currency'][-3:]:
        table = table_currency_changer(submission['trans_currency'][:3])
        table = table.spreadsheet.worksheet('Счета')
        from_letter = resources.ACC_COLUMNS[submission['trans_from']]
        rows = table.col_values(resources.COLUMNS_TO_NUM[from_letter])
        new_row = len(rows) + 1
        place = from_letter + str(new_row)
        table.update_acell(place, '-' + submission['trans_value_from'])
        c_from_letter = resources.NUM_to_COLUMNS[resources.COLUMNS_TO_NUM[from_letter]+1]
        comment_place = c_from_letter + str(new_row)
        table.update_acell(comment_place, 'Перевод в ' + submission['trans_to'])

        to_letter = resources.ACC_COLUMNS[submission['trans_to']]
        rows = table.col_values(resources.COLUMNS_TO_NUM[to_letter])
        new_row = len(rows) + 1
        place = to_letter + str(new_row)
        table.update_acell(place, submission['trans_value_to'])
        c_to_letter = resources.NUM_to_COLUMNS[resources.COLUMNS_TO_NUM[to_letter]+1]
        comment_place = c_to_letter + str(new_row)
        table.update_acell(comment_place, 'Перевод  из ' + submission['trans_to'])

    else:
        table_from = table_currency_changer(submission['trans_currency'][:3])
        table_to = table_currency_changer(submission['trans_currency'][-3:])
        table_from = table_from.spreadsheet.worksheet('Счета')
        table_to = table_to.spreadsheet.worksheet('Счета')

        from_letter = resources.ACC_COLUMNS[submission['trans_from']]
        rows = table_from.col_values(resources.COLUMNS_TO_NUM[from_letter])
        new_row = len(rows) + 1
        place = from_letter + str(new_row)
        table_from.update_acell(place, '-' + submission['trans_value_from'])
        c_from_letter = resources.NUM_to_COLUMNS[resources.COLUMNS_TO_NUM[from_letter]+1]
        comment_place = c_from_letter + str(new_row)
        table_from.update_acell(comment_place, 'Перевод в ' + submission['trans_to'])

        to_letter = resources.ACC_COLUMNS[submission['trans_to']]
        rows = table_to.col_values(resources.COLUMNS_TO_NUM[to_letter])
        new_row = len(rows) + 1
        place = to_letter + str(new_row)
        table_to.update_acell(place, submission['trans_value_to'])
        c_to_letter = resources.NUM_to_COLUMNS[resources.COLUMNS_TO_NUM[to_letter]+1]
        comment_place = c_to_letter + str(new_row)
        table_to.update_acell(comment_place, 'Перевод  из ' + submission['trans_to'])
        

def write_expense_gdoc(message):

    submission = message['submission']

    response_text = 'Smth bad'
    tm = datetime.strftime(datetime.now(), '%m')

    if submission['expense_to'][:8] == 'Products':
        if submission['comment'] == '':
            response_text = (resources.expense + submission['expense_to'] + '* / ' + submission['expense_value'] 
                            + submission['expense_currency'] + ' / ' + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.expense + submission['expense_to'] + '* / ' + submission['expense_value'] 
                            + submission['expense_currency'] + ' / ' + submission['expense_from'] + ' / ' 
                            + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']

        table = table_currency_changer(submission['expense_currency'])
        gdoc_writer(table, submission['expense_value'], tm, resources.PRODUCTS_EXPENSE_COLUMNS[submission['expense_to']],
                    False, 'Расх-Products')
        
        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    elif submission['expense_to'] == 'Content - TheDesignest':
        if submission['comment'] == '':
            response_text = (resources.designest_content + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.designest_content + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['expense_currency'])

        gdoc_writer(table, submission['expense_value'], tm, resources.DESIGNEST_ROW)

        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    elif submission['expense_to'] == 'Tech':
        if submission['comment'] == '':
            response_text = (resources.tech_expense + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.tech_expense + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['expense_currency'])

        gdoc_writer(table, submission['expense_value'], tm, resources.TECH_ROW)
            
        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    elif submission['expense_to'] == 'Аренда':
        if submission['comment'] == '':
            response_text = (resources.rent + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.rent + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['expense_currency'])
        gdoc_writer(table, submission['expense_value'], tm, resources.RENT_ROW)
        
        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    elif submission['expense_to'] == 'Инвестиции':
        if submission['comment'] == '':
            response_text = (resources.invest + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.invest + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['expense_currency'])
        gdoc_writer(table, submission['expense_value'], tm, resources.INVEST_ROW)
        
        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    elif submission['expense_to'] == 'Иное':
        if submission['comment'] == '':
            response_text = (resources.other_expense + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'])
            comment = submission['expense_to']
        else:
            response_text = (resources.other_expense + submission['expense_value'] + submission['expense_currency'] + ' / '
                            + submission['expense_from'] + ' / ' + submission['comment'])
            comment = submission['expense_to'] + ' / ' + submission['comment']
        table = table_currency_changer(submission['expense_currency'])
        gdoc_writer(table, submission['expense_value'], tm, resources.OTHER_EXP_ROW)

        gdoc_account_writer(table, str(float(submission['expense_value']) * (-1)), submission['expense_from'],
                            comment)

    slack_send_webhook(
        text=response_text,
        channel=message['channel']['id'],
        icon=':chart_with_upwards_trend:'
    )

def table_currency_changer(cur):

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(resources.client_secret, scope)
    client = gspread.authorize(creds)

    if cur == 'USD':
        sheet = client.open('PB2019USD').sheet1
    elif cur == 'RUR':
        sheet = client.open('PB2019RUR').sheet1
    elif cur == 'EUR':
        sheet = client.open('PB2019EUR').sheet1
    elif cur == 'FEE':
        sheet = client.open('FEE').sheet1
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
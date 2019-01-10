dialog_income = {
    'title': 'Доход',
    'submit_label': 'Submit',
    'callback_id': 'income_form',
    'elements': [
        {
            'label': 'Категория',
            'type': 'select',
            'name': 'income_from',
            'placeholder': 'Выберите категорию',
            'value': 'Markets - Design cuts',
            'options': [
                {
                    'label': 'Markets - Design cuts',
                    'value': 'Markets - Design cuts'
                },
                {
                    'label': 'Markets - Creative Market',
                    'value': 'Markets - Creative Market'
                },
                {
                    'label': 'Markets - Yello images',
                    'value': 'Markets - Yello images'
                },
                {
                    'label': 'Markets - Your work for them',
                    'value': 'Markets - Your work for them'
                },
                {
                    'label': 'Markets - Envano',
                    'value': 'Markets - Envano'
                },
                {
                    'label': 'Markets - Envato Elements',
                    'value': 'Markets - Envato Elements'
                },
                {
                    'label': 'Markets - Other',
                    'value': 'Markets - Other'
                },
                {
                    'label': 'Email - Direct',
                    'value': 'Email - Direct'
                },
                {
                    'label': 'Email - BSA/Syndicate',
                    'value': 'Email - BSA/Syndicate'
                },
                {
                    'label': 'Email - Baw Media',
                    'value': 'Email - Baw Media'
                },    
                {
                    'label': 'Email - Hacking UI',
                    'value': 'Email - Hacking UI'
                },
                {
                    'label': 'Email - Design Cuts',
                    'value': 'Email - Design Cuts'
                },
                {
                    'label': 'Email - Paved',
                    'value': 'Email - Paved'
                },
                {
                    'label': 'Deals - Design cuts',
                    'value': 'Deals - Design cuts'
                },
                 {
                    'label': 'Deals - Deal Jambo',
                    'value': 'Deals - Deal Jambo'
                },
                {
                    'label': 'Deals - Mighty deals',
                    'value': 'Deals - Mighty deals'
                },
                {
                    'label': 'Deals - Other',
                    'value': 'Deals - Other'
                },
                {
                    'label': 'Plus',
                    'value': 'plus'
                },
                {
                    'label': 'Banners',
                    'value': 'banners'
                }
            ]
        },

        {
            'type': 'text',
            'label': 'Сумма',
            'name': 'income_value'
        },

        {
            'label': 'Валюта',
            'type': 'select',
            'name': 'income_currency',
            'placeholder': 'Выберите валюту',
            'value': 'USD',
            'options': [
                {
                    'label': 'USD',
                    'value': 'USD'
                },
                {
                    'label': 'RUR',
                    'value': 'RUR'
                },
                {
                    'label': 'EUR',
                    'value': 'EUR'
                }
            ]
        },
        {
            'label': 'Счёт',
            'type': 'select',
            'name': 'income_to',
            'placeholder': 'Укажите куда пришли деньги',
            'value': 'Ksenia PayPal',
            'options': [
                {
                    'label': 'Ksenia PayPal',
                    'value': 'Ksenia PayPal'
                },
                {
                    'label': 'Milka PayPal',
                    'value': 'Milka PayPal'
                },
                {
                    'label': 'Payoner',
                    'value': 'Payoner'
                },
                {
                    'label': 'Astakhov PayPal',
                    'value': 'Astakhov PayPal'
                },
                {
                    'label': 'Plus PayPal',
                    'value': 'Plus PayPal'
                },
                {
                    'label': 'Mello Bank',
                    'value': 'Mello Bank'
                },
                {
                    'label': 'Mello Cash',
                    'value': 'Mello Cash'
                },
                {
                    'label': 'Nick Cash',
                    'value': 'Nick Cash'
                }
            ]
        },
        {
            'type': 'text',
            'label': 'Комментарий',
            'name': 'comment'
        }
    ]
}
dialog_expense = {
    'title': 'Расход',
    'submit_label': 'Submit',
    'callback_id': 'expense_form',
    'elements': [
        {
            'label': 'Категория',
            'type': 'select',
            'name': 'expense_to',
            'placeholder': 'Выберите категорию',
            'value': 'Products - Freebie',
            'options': [
                {
                    'label': 'Products - Freebie',
                    'value': 'Products - Freebie'
                },
                {
                    'label': 'Products - Plus',
                    'value': 'Products - Plus'
                },
                {
                    'label': 'Tech',
                    'value': 'Tech'
                },
                {
                    'label': 'Аренда',
                    'value': 'Аренда'
                },
                {
                    'label': 'Инвестиции',
                    'value': 'Инвестиции'
                },
                {
                    'label': 'Иное',
                    'value': 'Иное'
                }
            ]
        },

        {
            'type': 'text',
            'label': 'Сумма',
            'name': 'expense_value'
        },

        {
            'label': 'Валюта',
            'type': 'select',
            'name': 'expense_currency',
            'placeholder': 'Выберите валюту',
            'value': 'USD',
            'options': [
                {
                    'label': 'USD',
                    'value': 'USD'
                },
                {
                    'label': 'RUR',
                    'value': 'RUR'
                },
                {
                    'label': 'EUR',
                    'value': 'EUR'
                }
            ]
        },

        {
            'label': 'Счёт',
            'type': 'select',
            'name': 'expense_from',
            'placeholder': 'Укажите c какого счёта была оплата',
            'value': 'Ksenia PayPal',
            'options': [
                {
                    'label': 'Ksenia PayPal',
                    'value': 'Ksenia PayPal'
                },
                {
                    'label': 'Milka PayPal',
                    'value': 'Milka PayPal'
                },
                {
                    'label': 'Payoner',
                    'value': 'Payoner'
                },
                {
                    'label': 'Astakhov PayPal',
                    'value': 'Astakhov PayPal'
                },
                {
                    'label': 'Plus PayPal',
                    'value': 'Plus PayPal'
                },
                {
                    'label': 'Mello Bank',
                    'value': 'Mello Bank'
                },
                {
                    'label': 'Mello Cash',
                    'value': 'Mello Cash'
                },
                {
                    'label': 'Nick Cash',
                    'value': 'Nick Cash'
                }
            ]
        },

        {
            'type': 'text',
            'label': 'Комментарий',
            'name': 'comment'
        }
    ]
}
month_dic = {
    '01':'b',
    '02':'c',
    '03':'d',
    '04':'e',
    '05':'f',
    '06':'g',
    '07':'h',
    '08':'i',
    '09':'j',
    '10':'k',
    '11':'l',
    '12':'m'
}
import os
i=0
secret = ''
while i<=25:
    secret = secret + os.environ.get('sec'+str(i)) + '\n'
    i=i+1
client_secret = {
    'type': os.environ.get('g_type'),
    'project_id': os.environ.get('g_project_id'),
    'private_key_id': os.environ.get('g_private_key_id'),
    'private_key': '-----BEGIN PRIVATE KEY-----\n'+secret+'-----END PRIVATE KEY-----\n',
    'client_email': os.environ.get('g_client_email'),
    'client_id': os.environ.get('g_client_id'),
    'auth_uri': os.environ.get('g_auth_uri'),
    'token_uri': os.environ.get('g_token_uri'),
    'auth_provider_x509_cert_url': os.environ.get('g_auth_provider_x509_cert_url'),
    'client_x509_cert_url': os.environ.get('g_client_x509_cert_url')
}

PLUS_ROW = '3'
BANNERS_ROW = '6'
TECH_ROW = '13'
RENT_ROW = '14'
INVEST_ROW = '15'
OTHER_EXP_ROW = '16'
EMAIL_COLUMNS = {
    'Email - Direct':'b',
    'Email - BSA/Syndicate':'c',
    'Email - Baw Media':'d',
    'Email - Hacking UI':'e',
    'Email - Design Cuts':'f',
    'Email - Paved':'g'
}

PRODUCTS_COLUMNS = {
    'Deals - Design cuts':'b',
    'Deals - Deal Jambo':'c',
    'Deals - Mighty deals':'d',
    'Deals - Other':'e',
    'Markets - Design cuts':'f',
    'Markets - Creative Market':'g',
    'Markets - Yello images':'h',
    'Markets - Your work for them':'i',
    'Markets - Envano':'j',
    'Markets - Envato Elements':'k',
    'Markets - Other':'l'
}

PRODUCTS_EXPENSE_COLUMNS = {
    'Products - Freebie':'b',
    'Products - Plus':'c'
}

ACC_COLUMNS = {
    'Ksenia PayPal':'a',
    'Milka PayPal':'c',
    'Payoner':'e',
    'Astakhov PayPal':'g',
    'Plus PayPal':'i',
    'Mello Bank':'k',
    'Mello Cash':'m',
    'Nick Cash':'o'
}
COLUMNS_TO_NUM = {
    'a':1,
    'b':2,
    'c':3,
    'd':4,
    'e':5,
    'f':6,
    'g':7,
    'h':8,
    'i':9,
    'j':10,
    'k':11,
    'l':12,
    'm':13,
    'n':14,
    'o':15,
    'p':16,
    'q':17,
    'r':18,
    's':19,
    't':20,
    'u':21,
    'v':22,
    'w':23,
    'x':24,
    'y':25,
    'z':25
}

NUM_to_COLUMNS = {
    1:'a',
    2:'b',
    3:'c',
    4:'d',
    5:'e',
    6:'f',
    7:'g',
    8:'h',
    9:'i',
    10:'j',
    11:'k',
    12:'l',
    13:'m',
    14:'n',
    15:'o',
    16:'p',
    17:'q',
    18:'r',
    19:'s',
    20:'t',
    21:'u',
    22:'v',
    23:'w',
    24:'x',
    25:'y',
    26:'z'
}

plus_income = '*Доход Plus* / '
banner_income = '*Доход Banners* / '
income = '*Доход '
tech_expense = '*Расход Tech* / '
rent = '*Расход Аренда* / '
invest = '*Расход Инвестиции* / '
other_expense = '*Расход Иное* / '
expense = '*Расход '
dialog_income = {
    'title': 'Доход',
    'submit_label': 'Submit',
    'callback_id': 'income_form',
    'elements': [
        {
            'type': 'text',
            'display_name': 'Комментарий',
            'name': 'comment',
            'subtype': 'text'
        },
        {
            'type': 'text',
            'display_name': 'Сумма',
            'name': 'income_value',
            'subtype': 'text'
        },

        {
            'display_name': 'Валюта',
            'type': 'select',
            'name': 'income_currency',
            'placeholder': 'Выберите валюту',
            'default': 'USD',
            'options': [
                {
                    'text': 'USD',
                    'value': 'USD'
                },
                {
                    'text': 'RUR',
                    'value': 'RUR'
                },
                {
                    'text': 'EUR',
                    'value': 'EUR'
                }
            ]
        },
        {
            'display_name': 'Счёт',
            'type': 'select',
            'name': 'income_to',
            'placeholder': 'Укажите куда пришли деньги',
            'default': 'Ksenia PayPal',
            'options': [
                {
                    'text': 'Ksenia PayPal',
                    'value': 'Ksenia PayPal'
                },
                {
                    'text': 'Milka PayPal',
                    'value': 'Milka PayPal'
                },
                {
                    'text': 'Antonina PayPal',
                    'value': 'Antonina PayPal'
                },
                {
                    'text': 'Payoneer',
                    'value': 'Payoneer'
                },
                {
                    'text': 'Astakhov PayPal',
                    'value': 'Astakhov PayPal'
                },
                {
                    'text': 'Plus PayPal',
                    'value': 'Plus PayPal'
                },
                {
                    'text': 'Mello Bank',
                    'value': 'Mello Bank'
                },
                {
                    'text': 'Mello Cash',
                    'value': 'Mello Cash'
                },
                {
                    'text': 'Nick Cash',
                    'value': 'Nick Cash'
                }
            ]
        },
        {
            'display_name': 'Категория',
            'type': 'select',
            'name': 'income_from',
            'placeholder': 'Выберите категорию',
            'default': 'Marketplaces - Design cuts',
            'options': [
                {
                    'text': 'Marketplaces - Design cuts',
                    'value': 'Marketplaces - Design cuts'
                },
                {
                    'text': 'Marketplaces - Creative Market',
                    'value': 'Marketplaces - Creative Market'
                },
                {
                    'text': 'Marketplaces - Yellow Images',
                    'value': 'Marketplaces - Yellow Images'
                },
                {
                    'text': 'Marketplaces - YouWorkForThem',
                    'value': 'Marketplaces - YouWorkForThem'
                },
                {
                    'text': 'Marketplaces - Envato',
                    'value': 'Marketplaces - Envato'
                },
                {
                    'text': 'Marketplaces - Envato Elements',
                    'value': 'Marketplaces - Envato Elements'
                },
                {
                    'text': 'Marketplaces - Other',
                    'value': 'Marketplaces - Other'
                },
                {
                    'text': 'Marketplaces - Self',
                    'value': 'Marketplaces - Self'
                },
                {
                    'text': 'Email - Direct',
                    'value': 'Email - Direct'
                },
                {
                    'text': 'Email - BSA/Syndicate',
                    'value': 'Email - BSA/Syndicate'
                },
                {
                    'text': 'Email - Baw Media',
                    'value': 'Email - Baw Media'
                },    
                {
                    'text': 'Email - Hacking UI',
                    'value': 'Email - Hacking UI'
                },
                {
                    'text': 'Email - Design Cuts',
                    'value': 'Email - Design Cuts'
                },
                {
                    'text': 'Email - Paved',
                    'value': 'Email - Paved'
                },
                {
                    'text': 'Deals - Design cuts',
                    'value': 'Deals - Design cuts'
                },
                 {
                    'text': 'Deals - Deal Jambo',
                    'value': 'Deals - Deal Jambo'
                },
                {
                    'text': 'Deals - Mighty deals',
                    'value': 'Deals - Mighty deals'
                },
                {
                    'text': 'Deals - Other',
                    'value': 'Deals - Other'
                },
                {
                    'text': 'Plus',
                    'value': 'plus'
                },
                {
                    'text': 'Banners',
                    'value': 'banners'
                },
                {
                    'text': 'The Designest',
                    'value': 'inthedesignest'
                },
                {
                    'text': 'Stock - Freepik',
                    'value': 'Stock - Freepik'
                },
                {
                    'text': 'Stock - Adobe Stock',
                    'value': 'Stock - Adobe Stock'
                },
                {
                    'text': 'Stock - Shutter',
                    'value': 'Stock - Shutter'
                },
                {
                    'text': 'Stock - iStock Photo',
                    'value': 'Stock - iStock Photo'
                }
            ]
        }
    ]
}

dialog_trans = {
    'title': 'Перевод',
    'submit_label': 'Submit',
    'callback_id': 'trans_form',
    'elements': [
        {
            'label': 'От',
            'type': 'select',
            'name': 'trans_from',
            'placeholder': 'Укажите откуда ушли деньги',
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
                    'label': 'Payoneer',
                    'value': 'Payoneer'
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
            'label': 'Куда',
            'type': 'select',
            'name': 'trans_to',
            'placeholder': 'Укажите куда пришли деньги',
            'value': 'Milka PayPal',
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
                    'label': 'Antonina PayPal',
                    'value': 'Antonina PayPal'
                },
                {
                    'label': 'Payoneer',
                    'value': 'Payoneer'
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
            'label': 'Сумма',
            'name': 'trans_value'
        },
        {
            'label': 'Валюта',
            'type': 'select',
            'name': 'trans_currency',
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
        }
    ]
}

dialog_tocash = {
    'title': 'Вывод',
    'submit_label': 'Submit',
    'callback_id': 'tocash_form',
    'elements': [
        {
            'label': 'Счет',
            'type': 'select',
            'name': 'to_cash_acc',
            'placeholder': 'Счет',
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
                    'label': 'Antonina PayPal',
                    'value': 'Antonina PayPal'
                },
                {
                    'label': 'Payoneer',
                    'value': 'Payoneer'
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
            'label': 'Сумма',
            'name': 'value'
        },
        {
            'label': 'Валюта',
            'type': 'select',
            'name': 'currency',
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
        }
    ]
}
dialog_expense = {
    'title': 'Расход',
    'submit_label': 'Submit',
    'callback_id': 'expense_form',
    'elements': [
        {
            'type': 'text',
            'display_name': 'Комментарий',
            'name': 'comment',
            'subtype': 'text'
        },

        {
            'type': 'text',
            'display_name': 'Сумма',
            'name': 'expense_value',
            'subtype': 'text'
        },

        {
            'display_name': 'Валюта',
            'type': 'select',
            'name': 'expense_currency',
            'placeholder': 'Выберите валюту',
            'default': 'USD',
            'options': [
                {
                    'text': 'USD',
                    'value': 'USD'
                },
                {
                    'text': 'RUR',
                    'value': 'RUR'
                },
                {
                    'text': 'EUR',
                    'value': 'EUR'
                }
            ]
        },

        {
            'display_name': 'Счёт',
            'type': 'select',
            'name': 'expense_from',
            'placeholder': 'Укажите c какого счёта была оплата',
            'default': 'Ksenia PayPal',
            'options': [
                {
                    'text': 'Ksenia PayPal',
                    'value': 'Ksenia PayPal'
                },
                {
                    'text': 'Milka PayPal',
                    'value': 'Milka PayPal'
                },
                {
                    'text': 'Antonina PayPal',
                    'value': 'Antonina PayPal'
                },
                {
                    'text': 'Payoneer',
                    'value': 'Payoneer'
                },
                {
                    'text': 'Astakhov PayPal',
                    'value': 'Astakhov PayPal'
                },
                {
                    'text': 'Plus PayPal',
                    'value': 'Plus PayPal'
                },
                {
                    'text': 'Mello Bank',
                    'value': 'Mello Bank'
                },
                {
                    'text': 'Mello Cash',
                    'value': 'Mello Cash'
                },
                {
                    'text': 'Nick Cash',
                    'value': 'Nick Cash'
                }
            ]
        },

        {
            'display_name': 'Категория',
            'type': 'select',
            'name': 'expense_to',
            'placeholder': 'Выберите категорию',
            'default': 'Products - Freebie',
            'options': [
                {
                    'text': 'Products - Freebie',
                    'value': 'Products - Freebie'
                },
                {
                    'text': 'Products - Plus',
                    'value': 'Products - Plus'
                },
                {
                    'text': 'Content - TheDesignest',
                    'value': 'Content - TheDesignest'
                },
                {
                    'text': 'Tech',
                    'value': 'Tech'
                },
                {
                    'text': 'Аренда',
                    'value': 'Аренда'
                },
                {
                    'text': 'Инвестиции',
                    'value': 'Инвестиции'
                },
                {
                    'text': 'Иное',
                    'value': 'Иное'
                }
            ]
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
DESIGNEST_INCOME_ROW = '7'
DESIGNEST_ROW = '13'
TECH_ROW = '14'
RENT_ROW = '15'
INVEST_ROW = '16'
OTHER_EXP_ROW = '17'
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
    'Marketplaces - Design cuts':'f',
    'Marketplaces - Creative Market':'g',
    'Marketplaces - Yellow Images':'h',
    'Marketplaces - YouWorkForThem':'i',
    'Marketplaces - Envato':'j',
    'Marketplaces - Envato Elements':'k',
    'Marketplaces - Other':'l',
    'Marketplaces - Self':'m'
}

STOCKS_COLUMNS = {
    'Stock - Freepik':'b',
    'Stock - Adobe Stock':'c',
    'Stock - Shutter':'d',
    'Stock - iStock Photo':'e'
}

PRODUCTS_EXPENSE_COLUMNS = {
    'Products - Freebie':'b',
    'Products - Plus':'c'
}

ACC_COLUMNS = {
    'Ksenia PayPal':'a',
    'Milka PayPal':'c',
    'Payoneer':'e',
    'Astakhov PayPal':'g',
    'Plus PayPal':'i',
    'Mello Bank':'k',
    'Mello Cash':'m',
    'Nick Cash':'o',
    'Antonina PayPal':'q'
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
plus_income = '**Доход Plus** / '
freepik_income = '**Доход freepik** '
shutter_income = '**Доход shutter** '
adobe_income = '**Доход adobe Stock**'
istock_income = '**Доход istock photo**'
banner_income = '**Доход Banners** / '
designest_income = '**Доход The Designest** / '
income = '**Доход '
tech_expense = '**Расход Tech** / '
designest_content = '**Расход на контент TheDesignest** / '
rent = '**Расход Аренда** / '
invest = '**Расход Инвестиции** / '
other_expense = '**Расход Иное** / '
expense = '**Расход '
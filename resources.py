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
            'value': 'products',
            'options': [
                {
                    'label': 'Products',
                    'value': 'products'
                },
                {
                    'label': 'Email',
                    'value': 'email'
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
                    'label': 'Mello PayPal',
                    'value': 'Mello PayPal'
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
                    'label': 'Никита',
                    'value': 'Никита'
                }
            ]
        },
        {
            'label': 'Подкатегория для email',
            'type': 'select',
            'name': 'income_form_email',
            'placeholder': 'Уточнените категорию email',
            'value': 'Direct',
            'options': [
                {
                    'label': 'Direct',
                    'value': 'Direct'
                },
                {
                    'label': 'BSA/Syndicate',
                    'value': 'BSA/Syndicate'
                },
                {
                    'label': 'Baw Media',
                    'value': 'Baw Media'
                },
                {
                    'label': 'Hacking UI',
                    'value': 'Hacking UI'
                },
                {
                    'label': 'Design Cuts',
                    'value': 'Design Cuts'
                },
                {
                    'label': 'Paved',
                    'value': 'Paved'
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

dialog_income_email = {
    'title': 'Email-доход',
    'submit_label': 'Submit',
    'callback_id': 'income_form_email',
    'elements': [
        
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
            'value': 'products',
            'options': [
                {
                    'label': 'Products',
                    'value': 'Products'
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
            'value': 'usd',
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
            'value': 'ks',
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
                    'label': 'Mello PayPal',
                    'value': 'Mello PayPal'
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
                    'label': 'Никита',
                    'value': 'Никита'
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

plus_income = '*Доход Plus* / '
banner_income = '*Доход Banners* / '
tech_expense = '*Расход Tech* / '
rent = '*Расход Аренда* / '
invest = '*Расход Инвестиции* / '
other_expense = '*Расход Иное* / '
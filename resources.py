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
            'label': 'Валюта',
            'type': 'select',
            'name': 'income_currency',
            'placeholder': 'Выберите валюту',
            'value': 'usd',
            'options': [
                {
                    'label': 'USD',
                    'value': 'usd'
                },
                {
                    'label': 'RUR',
                    'value': 'rur'
                },
                {
                    'label': 'EUR',
                    'value': 'eur'
                }
            ]
        },

        {
            'type': 'text',
            'label': 'Сколько?',
            'name': 'income_value'
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
client_secret = {
    'type': os.environ.get('g_type'),
    'project_id': os.environ.get('g_project_id'),
    'private_key_id': os.environ.get('g_private_key_id'),
    'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC6PhEykJ7pvq81\nSHhNKRPayGa9WLCKmTcRgA9HEnbfY7tPAw1EQtheMEF57KIHXgr4lWIferCTlW1u\n2WSEL6S4XZmw00Di5cwElzHxLMKL1qX6rjE27B5KdFrRRMkvp3UBunBiOZApSAXE\n6snCjG8GiU7lHSq8EHnnTAVfvscowCaTbTPHC9Qb6v41cUiiHlNlhiysosmTiUAN\nE1ifHDrA8g9CmU0zsD0uG7BuiQjIZJ0xlC999yDOuzPBZrx+I8nHSw/lRhEc/BU1\n49nnWnMgfUf/cYcHpbJtdGwMApN295kuwkrE0wMMNZAIPOQiN02SqAohK0nCHT9L\neE0xBAStAgMBAAECggEAClm7NnJzpn12utEbgHxNMm5LSXAlpZpExXf2wWYtDZa7\nGPXMNbQ6Vqe7Z9WHHr4zAWQ59xJoQFeAZLX3wGHud2GaUkm3VDTdvQ6TE7p/WGq2\nQEOQkCMYvt4PEwzN2pRlrBIqv0bANI8gZPSAgIux+uzEIfcYQinvQHPI46yUYHcP\nE2b1B0T95kbSeSNscl1J5Wl2YAYP9Tkpl8TVTvaf6iLdMM24Z4cFOrF9eg2DTJzl\nRu9xtjuoMeUUZ+vvs0vK1yZlYTyCbcMwaZf3YJdLJQh9DOJRT8gyP4mVCLhGBoBn\n+b14RrJuXAhmkBPxNdjFvOxETSKEEJfGQittaue/WQKBgQDjZ1d8rTz6qyfuz/RA\nn1HS33jiC943lzmAZuvHKjyAtLOsHe/iHGHdaTj+yPwORZAJWEHJGJCLl1JQ+Uaf\ns56K/elb96b8Ut1aRVJ2aHGHIql/uh3STaSlVY0H/4PTmeS4cAs4LDqRYyfJBbEt\nPefz20FeB2PfW2QfAYy58rNilQKBgQDRqaYbCCosqHc9J9HKXgOJER+HNzhMPdhP\nY6JD0nb5RP9wyNbPAMjh7JTyBp3gDpkxg0am3wpNWFrKN3PMFg+llZTnfc3GWTtp\ni8S3m1QgfWwsrwL37kdn0QO6jMfvchFZzX8kJ+l/YuPPTiNjsBIpDAr8Vt7cEGNI\nLhvkDJfruQKBgQDgpu8fFGXxnbTNkFNUpBBJqsvZRLA7awI7f3HeSDONUvdNSiX5\n0uA7w/+ydQvNbZtmH/Kdn87smImRxTGoA+LUnRM07+vfyl0zGNjmcTf2sJ+St2NO\np7XIQEQbaqnpGVeDfe0XiVoy1youxZjLgSTtG+Xv5o0b00WN/BHygXoGIQKBgGIJ\ntx9KyRXKzL7vAL1lCrgsJpb+rjeQb7Znu3eFUZarudpOP4vaLRTfoKIvj+E2UlIB\ntabQAqw6FXIbTe1vn29pK5C3leIa1Zo7/gdw/XyXyV53k6bFZ+RWqyyvKcqAhzZ7\nzejlNN0ZK7dDLW8u5L8G35gxMtKqYxJcZTRU4zEZAoGAWIANAKA07I5xTQRgjtV+\ndGNHecjbRMs8SFlUZ9pA8tzsc2RhpVOIZlaeu0MHYdqg0XUKSZiherSPs6Wx3RjZ\n6Sfed+VE60g2P1oGKrp2BfSuDh/FZEWr1hlfeUofwRqpEA52+Hh1J80zbVsilT/1\nZh8WbqFrstl77xRSj5fejQc=\n-----END PRIVATE KEY-----\n',
    'client_email': os.environ.get('g_client_email'),
    'client_id': os.environ.get('g_client_id'),
    'auth_uri': os.environ.get('g_auth_uri'),
    'token_uri': os.environ.get('g_token_uri'),
    'auth_provider_x509_cert_url': os.environ.get('g_auth_provider_x509_cert_url'),
    'client_x509_cert_url': os.environ.get('g_client_x509_cert_url')
}
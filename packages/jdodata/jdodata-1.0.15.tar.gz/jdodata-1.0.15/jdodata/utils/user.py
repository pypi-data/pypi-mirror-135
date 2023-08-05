import json
import requests
from .CONST import HOST


def login(username, password):

    url = "https://opendata.gubaike.com/api/user_manager/login"

    payload = {
        "login_type": "nor_pass",
        "username": username,
        "password": password,
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))

    data = response.json()

    if data['status'] == 'SUCCESS':
        jwt = response.json()['jwt']
    else:
        jwt = ''

    return jwt


def logout(jwt):
    pass

import json
import requests
from decouple import config

base_url = 'https://sunbirdainoise.mooo.com/v1'

def authenticate():
    email = config('ODK_EMAIL')
    password = config('ODK_PASSWORD')

    headers = {'Content-Type': 'application/json'}

    response = requests.post(
        url=base_url + '/sessions',
        json={'email': email, 'password': password},
        headers=headers
    )

    if response.status_code == 200:
        return response.json()['token']

def list_forms():
    token = authenticate()
    headers = {'Authorization': 'Bearer' + token}

    response = requests.get(
        url=base_url + '/projects/2/forms',
        headers=headers
    )

    print(response.text)

def list_form_submissions():
    token = authenticate()
    headers = {'Authorization': 'Bearer' + token}

    response = requests.get(
        url=base_url + '/projects/2/forms/build_Noise-Capture-Form_1614927723/submissions',
        headers=headers
    )

    print(response.text)

def form_details():
    token = authenticate()
    headers = {'Authorization': 'Bearer' + token}

    response = requests.get(
        url=base_url + '/projects/2/forms/build_Noise-Capture-Form_1614927723',
        headers=headers
    )

    print(response.text)


if __name__=='__main__':
    # list_forms()
    # list_form_submissions()
    form_details()
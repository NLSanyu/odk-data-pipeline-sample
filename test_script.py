import json
import requests
from decouple import config


base_url = 'https://sunbirdainoise.mooo.com/v1'
project_id = '2'
form_id = 'build_Noise-Capture-Form_1614927723'
example_submission_uuid = 'uuid:96454e03-14af-4f13-93ca-67b73feb3dc3'
example_submission_filename = '1618068976573.wav'

def authenticate():
    email = config('ODK_EMAIL')
    password = config('ODK_PASSWORD')

    headers = {'Content-Type': 'application/json'}
    url = f'{base_url}/sessions'

    response = requests.post(
        url=url,
        json={'email': email, 'password': password},
        headers=headers
    )

    if response.status_code == 200:
        return response.json()['token']

def list_forms():
    url = f'{base_url}/projects/{project_id}/forms'
    get_request(url)

def list_form_submissions():
    url = f'{base_url}/projects/{project_id}/forms/{form_id}/submissions'
    get_request(url)

def form_details():
    url = f'{base_url}/projects/{project_id}/forms/{form_id}'
    get_request(url)

def download_attachment():
    url = f'''{base_url}/projects/{project_id}/forms/{form_id}/submissions/{example_submission_uuid}/attachments/{example_submission_filename}'''
    get_request(url)


def get_request(url):
    token = authenticate()
    headers = {'Authorization': 'Bearer' + token}
    response = requests.get(
        url=url,
        headers=headers
    )

    print(response.text)


if __name__=='__main__':
    # authenticate()
    # list_forms()
    # list_form_submissions()
    # form_details()
    download_attachment()
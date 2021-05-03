import json
import requests
import logging
from decouple import config
from pathlib import Path

logging.basicConfig(filename='app.log', 
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

base_url = config('ODK_PROJECT_URL')
headers = {}

def authenticate():
    email = config('ODK_EMAIL')
    password = config('ODK_PASSWORD')
    login_url = f'{base_url}v1/sessions'

    response = requests.post(
        login_url,
        json={'email': email, 'password': password}
    )

    if response.status_code == 200:
        return response.json()['token']
    else:
        return response.text

def get_submissions():
    token = authenticate()
    headers = {'Authorization': f'Bearer {token}'}
    service_params = {
        'projectId': config('ODK_PROJECT_ID'),
        'xmlFormId': config('ODK_FORM_ID')
    }
    service_doc_url = f'{base_url}v1/projects/{service_params["projectId"]}/forms/{service_params["xmlFormId"]}.svc'

    try:
        service_doc_response = requests.get(service_doc_url, headers=headers)
    except requests.exceptions.RequestException as err:
        logging.error(f'Service document error: {err}')

    if service_doc_response.status_code != 200:
        logging.error(f'Service document error: {service_doc_response.text}')

    retrieve_url = f'{service_doc_url}/{service_doc_response.json()["value"][0]["name"]}'
    params = {
        '$filter': 'day(__system/submissionDate) eq day(now())'
    }

    try:
        r_retrieve = requests.get(retrieve_url, headers=headers, params=params)
    except requests.exceptions.RequestException as err:
        logging.error(f'Error retrieving submissions: {err}')

    Path('audio').mkdir(parents=True, exist_ok=True)
    
    for item in r_retrieve.json()['value']:
        audio_id = requests.utils.quote(item['__id'])
        audio_name = item['Noise']['audio']
        audio_url = f'{base_url}v1/projects/{service_params["projectId"]}/forms/{service_params["xmlFormId"]}/submissions/{audio_id}/attachments/{audio_name}'
        response = requests.get(audio_url, headers=headers)

        target_file = f'audio/{audio_name}'
        with open(target_file, 'wb') as f:
            f.write(response.content)

if __name__=='__main__':
    get_submissions()
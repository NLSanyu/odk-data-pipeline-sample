import json
import requests
from decouple import config


base_url = 'https://sunbirdainoise.mooo.com/'
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
        'projectId': '2',
        'xmlFormId': 'build_Noise-Capture-Form_1614927723'
    }
    service_doc_url = f'{base_url}v1/projects/{service_params["projectId"]}/forms/{service_params["xmlFormId"]}.svc'
    service_doc_response = requests.get(service_doc_url, headers=headers)

    if service_doc_response.status_code != 200:
        return service_doc_response.text

    retrieve_url = f'{service_doc_url}/{service_doc_response.json()["value"][0]["name"]}'
    params = {
        '$top': '3', # Specify number of records to fetch
        '$count': 'true', # Returns total count of items in table
        #'$filter': day(__system/submissionDate) eq day(now())

    }

    r_retrieve = requests.get(retrieve_url, headers=headers, params=params)
    print(r_retrieve.status_code)

    
    for item in r_retrieve.json()["value"]:
        audio_id = requests.utils.quote(item['__id'])
        audio_name = item['Noise']['audio']
        audio_url = f'{base_url}v1/projects/{service_params["projectId"]}/forms/{service_params["xmlFormId"]}/submissions/{audio_id}/attachments/{audio_name}'

        response = requests.get(audio_url, headers=headers)
        print(response.status_code)

        file = open(audio_name, "wb")
        file.write(response.content)
        file.close()

if __name__=='__main__':
    get_submissions()
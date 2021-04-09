import json
import requests
from decouple import config

email = config('ODK_EMAIL')
password = config('ODK_PASSWORD')

url = 'https://sunbirdainoise.mooo.com/v1/sessions'
credentials = {'email': email, 'password': password}
headers = {'Content-Type': 'application/json'}

def authenticate():
    response = requests.post(
        url=url,
        json=credentials,
        headers=headers
    )

    token_response = response.text

if __name__=='__main__':
    authenticate()
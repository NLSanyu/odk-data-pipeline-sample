import requests
from decouple import config

url = 'https://sunbirdainoise.mooo.com/v1/sessions'
credentials = {
    'email': config('ODK_EMAIL'),
    'password': config('ODK_PASSWORD')
}
response = requests.get(url, auth=requests.auth.HTTPBasicAuth(credentials['email'], credentials['password']))
print(response)
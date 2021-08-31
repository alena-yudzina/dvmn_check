import requests
import os
from dotenv import load_dotenv

load_dotenv()
headers = {
    'Authorization': os.environ['DVMN_TOKEN']
}
timestamp = ''
url = 'https://dvmn.org/api/long_polling/'
while True:
    payload = {
    'timestamp': timestamp
    }
    try:
        print(timestamp)
        response = requests.get(url, headers=headers, timeout=5, params=payload)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
        continue
    print(response.text)
    timestamp =  response.json()['new_attempts'][0]['timestamp']

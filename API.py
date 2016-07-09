from secrets import API_KEY
import requests

BASE_URL = 'https://realtime.mbta.com/developer/api/v2/{command}?api_key={api_key}&format={format}'


def get(command, params, api_key=API_KEY):

    response = requests.get(BASE_URL.format(command=command, api_key=api_key, format='json'), params=params)
    return response.json()

from secrets import API_KEY
import requests

BASE_URL = 'https://realtime.mbta.com/developer/api/v2/{command}?api_key={api_key}&format={format}'
BASE_URL_V3 = 'https://api-v3.mbta.com/{command}?filter[{name}]={value}'


def get(command, params, api_key=API_KEY):

    response = requests.get(BASE_URL.format(command=command, api_key=api_key, format='json'), params=params)
    return response.json()


def getV3(command, filter_name, filter_value, api_key=API_KEY):
    headers = {'x-api-key': api_key}
    response = requests.get(BASE_URL_V3.format(command=command, name=filter_name, value=filter_value), headers=headers)
    return response.json()
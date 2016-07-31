import os

if 'API_KEY' in os.environ:
    API_KEY = os.environ['API_KEY']
else:
    API_KEY = ''

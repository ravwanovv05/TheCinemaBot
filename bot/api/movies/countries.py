import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Country:
    def __init__(self, name: str = None):
        self.name = name

    def list(self):
        url = os.getenv('COUNTRIES_LIST_URL')
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    def details(self, pk):
        url = os.getenv('COUNTRY_DETAILS_URL') + '/' +str(pk)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

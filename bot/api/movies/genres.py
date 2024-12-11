import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Genre:
    def __init__(self, name: str = None):
        self.name = name

    def genres_list(self):
        url = os.getenv('GENRE_LIST_URL')
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    def details(self, pk):
        url = os.getenv('GENRE_DETAILS_URL') + '/' + str(pk)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()



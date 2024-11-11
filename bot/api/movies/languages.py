import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Language:
    def __init__(self, name: str = None):
        self.name = name

    def list(self):
        url = os.getenv('LANGUAGES_LIST_URL')
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Category:
    def __init__(self, title: str = None, paren_id: int = None):
        self.title = title
        self.paren_id = paren_id

    def list(self):
        url = os.getenv('CATEGORIES_LIST_URL')
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    def details(self, pk: int):
        url = f"{os.getenv('CATEGORY_DETAILS_URL')}/{pk}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    def categories(self):
        url = os.getenv('CATEGORIES_URL')
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

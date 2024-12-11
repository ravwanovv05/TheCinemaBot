import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()


def current_year():
    timezone = pytz.timezone('Asia/Tashkent')
    return datetime.now(timezone).year


class Movie:
    def __init__(
            self, title: str = None, year: int = None, part: int = None,
            country_id: int = None, language_id: int = None, code: int = None, genre_id: int = None,
            category_id: int = None
            ):
        
        self.title = title
        self.year = year
        self.part = part
        self.code = code
        self.genre_id = genre_id
        self.country_id = country_id
        self.language_id = language_id
        self.category_id = category_id

    def save(self):
        url = os.getenv('CREATE_MOVIE_URL')
        response = requests.post(
            url, data={
                'title': self.title,
                'year': self.year,
                'part': self.part,
                'code': self.code,
                'genre_id': self.genre_id,
                'country_id': self.country_id,
                'language_id': self.language_id,
                'category_id': self.category_id
            }
        )
        if response.status_code == 201:
            return response.json()
        else:
            print(response.json())

    def movie_by_code(self,  code: int): # noqa
        url = f"{os.getenv('MOVIE_BY_CODE_URL')}/{code}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    def search_movies(self, title: str): # noqa
        url = os.getenv('SEARCH_MOVIES')
        response = requests.get(url, params={'search': title})
        if response.status_code == 200:
            return response.json()
    
    def all_movies(self): # noqa
        url = os.getenv('MOVIES_LIST')
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    def movie_filter (# noqa
            self, genre_id: int = None, country_id: int = None, from_year: int = None, to_year: int = None,
            category_id: int = None,
    ):

        url = os.getenv('MOVIE_FILTER_URL')
        response = requests.get(
            url, data={
                'from_year': from_year,
                'to_year': to_year,
                'genre_id': genre_id,
                'country_id': country_id,
                'category_id': category_id
            }
        )
        if response.status_code == 200:
            return response.json()

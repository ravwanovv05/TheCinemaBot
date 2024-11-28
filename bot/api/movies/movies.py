import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Movie:
    def __init__(
            self, title: str = None, description: str = None, year: int = None, series: int = None, 
            country_id: int = None, language_id: int = None, code: int = None, file_id: str = None, 
            category_id: int = None
            ):
        
        self.title = title
        self.description = description
        self.year = year
        self.series = series
        self.code = code
        self.file_id = file_id
        self.country_id = country_id
        self.language_id = language_id
        self.category_id = category_id

    def save(self):
        url = os.getenv('CREATE_MOVIE_URL')
        response = requests.post(
            url, data={
                'title': self.title,
                'description': self.description,
                'year': self.year,
                'series': self.series,
                'code': self.code,
                'file_id': self.file_id,
                'country_id': self.country_id,
                'language_id': self.language_id,
                'category_id': self.category_id
            }
        )
        if response.status_code == 201:
            return response.json()
        else:
            print(response.json())

    def movie_by_code(self,  code: int):
        url = f"{os.getenv('MOVIE_BY_CODE_URL')}/{code}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    def search_movies(self, title: str):
        url = os.getenv('SEARCH_MOVIES')
        response = requests.get(url, params={'search': title})
        if response.status_code == 200:
            return response.json()
    
    def all_movies(self):
        url = os.getenv('MOVIES_LIST')
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        
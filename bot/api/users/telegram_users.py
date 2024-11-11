import os
import requests
from dotenv import load_dotenv

load_dotenv()


class TelegramUser:
    def __init__(self, first_name: str = None, last_name: str = None, username: str = None, role='user', premium=False, active=True, telegram_id: int = None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.role = role
        self.premium = premium
        self.active = active
        self.telegram_id = telegram_id

    def create_telegram_user(self):
        url = os.getenv('CREATE_TG_USER_URL')
        response = requests.post(
            url=url, data={
                'first_name': self.first_name,
                'last_name': self.last_name,
                'username': self.username,
                'role': self.role,
                'premium': self.premium,
                'active': self.active,
                'telegram_id': self.telegram_id
            }
        )
        if response.status_code == 201:
            return response.json()

    def tg_user_details(self, telegram_id: int):
        url = f"{os.getenv('TG_USER_DETAIL_URL')}/{telegram_id}"
        response = requests.get(url=url)
        if response.status_code == 200:
            return response.json()

    def list(self):
        url = os.getenv('TG_USERS_LIST_URL')
        response = requests.get(url=url)
        if response.status_code == 200:
            return response.json()

    def update(self, user_id: int, data):
        url = f"{os.getenv('UPDATE_TG_USER_URL')}/{user_id}"
        response = requests.patch(url=url, data=data)
        if response.status_code == 200:
            return response.json()


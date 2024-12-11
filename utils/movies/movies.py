from bot.api.movies.categories import Category
from bot.api.movies.countries import Country
from bot.api.movies.genres import Genre


def write_details_of_movie(category_id, year, country_id, genre_id):
    category_name = Category().details(category_id)['name']
    country_name = Country().details(country_id)['name']
    genre_name = Genre().details(genre_id)['name']
    return f"{category_name} | {year}\n{country_name} | {genre_name}"


def write_details_of_filter(from_year, to_year, type_, genre, country):
    pass

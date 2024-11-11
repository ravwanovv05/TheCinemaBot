

def write_details_of_movie(data: dict):
    return f"🎥 NOMI: {data['title']} \n🎬 QISM: {data['series']} \n🌍 TIL: {data['language_id'].split('_')[0]} \n📆 YIL: {data['year']}\n📍 DAVLAT: {data['country_id'].split('_')[0]}"

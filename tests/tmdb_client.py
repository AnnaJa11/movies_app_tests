import requests
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYzhiZGQ2MDRkODVjNTRkYjQ1ZDVkMzY5NmE4NWZiNCIsInN1YiI6IjY1YjgzM2ViMzNhMzc2MDE3Yjg1MTRmZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.y4BhCdT6Zhm8g1_sVyIBMaievYWrq8mtMyWZc_HaYww"

def call_tmdb_api(endpoint):
   full_url = f"https://api.themoviedb.org/3/{endpoint}"
   headers = {
       "Authorization": f"Bearer {API_TOKEN}"
   }
   response = requests.get(full_url, headers=headers)
   response.raise_for_status()
   return response.json()

def get_movies_list(list_type):
   return call_tmdb_api(f"movie/{list_type}")

def get_movies(list_type, how_many):
    data = get_movies_list(list_type)
    return data["results"][:how_many]


def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_single_movie(movie_id):
    return call_tmdb_api(f"movie/{movie_id}")
    

def get_single_movie_cast(movie_id, how_many):
    cast_data = call_tmdb_api(f"movie/{movie_id}/credits")
    return cast_data['cast'][:how_many]
    

def get_movie_images(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/images")
    



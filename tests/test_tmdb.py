import pytest
import sys
sys.path.append('utils')
sys.path.insert(1, r'movies_proj/movies_app')
from tmdb_client import get_poster_url, get_movies_list, get_single_movie, get_single_movie_cast, get_movie_images, get_movies
from unittest.mock import Mock
import requests


def test_get_poster_url_uses_default_size():
   # Przygotowanie danych
   poster_api_path = "https://image.tmdb.org/t/p/w342//qhb1qOilapbapxWQn9jtRCMwXJF.jpg"
   expected_default_size = 'w342'
   # Wywołanie kodu, który testujemy
   poster_url = get_poster_url(poster_api_path=poster_api_path)
   # Porównanie wyników
   assert expected_default_size in poster_url

def test_get_movies_list(monkeypatch):
   # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
   mock_movies_list = ['Movie 1', 'Movie 2']
   mock_movie_id = '787699'

   requests_mock = Mock()
   # Wynik wywołania zapytania do API
   response = requests_mock.return_value
   # Przysłaniamy wynik wywołania metody .json()
   response.json.return_value = mock_movies_list
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   movies_list = get_movies_list(list_type="popular")
   assert movies_list == mock_movies_list


def test_get_movies(monkeypatch):
    # Dane testowe
    mock_movies_list = {
        "results": [
            {"title": "Movie 1"},
            {"title": "Movie 2"},
            {"title": "Movie 3"}
        ]
    }
    list_type = "popular"
    how_many = 2

    # Tworzenie obiektu mocka dla funkcji get_movies_list
    movies_list_mock = Mock(return_value=mock_movies_list)
    monkeypatch.setattr("tmdb_client.get_movies_list", movies_list_mock)

    # Wywołanie funkcji, którą testujemy
    movies = get_movies(list_type, how_many)

    # Sprawdzenie, czy funkcja get_movies_list została wywołana z prawidłowymi argumentami
    movies_list_mock.assert_called_once_with(list_type)

    # Sprawdzenie, czy wynik funkcji get_movies jest zgodny z oczekiwaniami
    assert len(movies) == how_many
    assert movies[0]["title"] == "Movie 1"
    assert movies[1]["title"] == "Movie 2"

def test_get_single_movie(monkeypatch):
    # Dane testowe
    movie_id = "123456"
    expected_api_call = "movie/123456"
    mock_movie_data = {"title": "Example Movie", "overview": "This is an example movie."}

    # Tworzenie obiektu mocka dla funkcji call_tmdb_api
    call_tmdb_api_mock = Mock(return_value=mock_movie_data)
    monkeypatch.setattr("tmdb_client.call_tmdb_api", call_tmdb_api_mock)

    # Wywołanie funkcji, którą testujemy
    result = get_single_movie(movie_id)

    # Sprawdzenie, czy funkcja call_tmdb_api została wywołana z odpowiednim argumentem
    call_tmdb_api_mock.assert_called_once_with(expected_api_call)

    # Sprawdzenie, czy wynik funkcji jest zgodny z oczekiwanymi danymi
    assert result == mock_movie_data

def test_get_single_movie_cast(monkeypatch):
    # Dane testowe
    movie_id = "123456"
    expected_api_call = f"movie/{movie_id}/credits"
    how_many = 3
    mock_cast_data = {
        "cast": [
            {"name": "Actor 1"},
            {"name": "Actor 2"},
            {"name": "Actor 3"},
            {"name": "Actor 4"}
        ]
    }

    # Tworzenie obiektu mocka dla funkcji call_tmdb_api
    call_tmdb_api_mock = Mock(return_value=mock_cast_data)
    monkeypatch.setattr("tmdb_client.call_tmdb_api", call_tmdb_api_mock)

    # Wywołanie funkcji, którą testujemy
    result = get_single_movie_cast(movie_id, how_many)

    # Sprawdzenie, czy funkcja call_tmdb_api została wywołana z odpowiednim argumentem
    call_tmdb_api_mock.assert_called_once_with(expected_api_call)

    # Sprawdzenie, czy wynik funkcji zawiera oczekiwaną liczbę elementów
    assert len(result) == how_many



def test_get_movie_images(monkeypatch):
    # Dane testowe
    movie_id = "123456"
    expected_api_call = f"movie/{movie_id}/images"
    mock_image_data = {"backdrops": [{"file_path": "/backdrop1.jpg"}, {"file_path": "/backdrop2.jpg"}]}

    # Tworzenie obiektu mocka dla funkcji call_tmdb_api
    call_tmdb_api_mock = Mock(return_value=mock_image_data)
    monkeypatch.setattr("tmdb_client.call_tmdb_api", call_tmdb_api_mock)

    # Wywołanie funkcji, którą testujemy
    result = get_movie_images(movie_id)

    # Sprawdzenie, czy funkcja call_tmdb_api została wywołana z odpowiednim argumentem
    call_tmdb_api_mock.assert_called_once_with(expected_api_call)

    # Sprawdzenie, czy wynik funkcji jest zgodny z oczekiwanymi danymi
    assert result == mock_image_data


def test_get_poster_url_default_size():
    # Dane testowe
    poster_api_path = "abc123xyz"
    expected_url = "https://image.tmdb.org/t/p/w342/abc123xyz"

    # Wywołanie funkcji, którą testujemy
    result = get_poster_url(poster_api_path)

    # Sprawdzenie, czy wynik funkcji jest zgodny z oczekiwanym adresem URL
    assert result == expected_url




if __name__ == '__main__':
   pytest.main()
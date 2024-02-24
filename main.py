from flask import Flask, render_template, request
import tmdb_client
import random


app = Flask(__name__)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route('/')
def homepage():
    default_list_type = 'popular'
    list_types = {
        'top_rated': 'Top rated',
        'upcoming': 'Upcoming',
        'popular': 'Popular',
        'now_playing': 'Now Playing'
    }
    movies = tmdb_client.get_movies(how_many=8, list_type=default_list_type)
    return render_template("homepage.html", movies=movies, list_types=list_types)


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id, how_many=4)
    movie_images = tmdb_client.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images['backdrops'])
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop)




if __name__ == "__main__":
    app.run(debug=True) 
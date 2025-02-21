 a website just like that using Flask/WTForms/SQLite/SQLAlchemy and more. It will allow us to create a beautiful website that lists our top 10 films of all time. As we watch more movies, we can always update our list and keep track of which movies to recommend people.
 
On Windows type:

python -m pip install -r requirements.txt
On MacOS type:

pip3 install -r requirements.txt


When the user types a movie title and clicks "Add Movie", your Flask server should receive the movie title. Next, you should use the requests library to make a request and search The Movie Database API for all the movies that match that title.

You will need to sign up for a free account on The Movie Database.

Then you will need to go to Settings -> API and get an API Key. Fill out their form, get the API key, and then copy that API key into your project.




You will need to read the documentation on The Movie Database to figure out how to request for movie data by making a search query.

https://developers.themoviedb.org/3/search/search-movies
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# load data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movie_list = movies['title'].values


# recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []

    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# home page
@app.route("/")
def home():
    return render_template("index.html", movie_list=movie_list)


# recommendation route
@app.route("/recommend", methods=["POST"])
def get_recommendation():
    movie = request.form.get("movie")
    results = recommend(movie)

    return render_template(
        "index.html",
        movie_list=movie_list,
        recommendations=results
    )


if __name__ == "__main__":
    app.run(debug=True)

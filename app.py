from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# -----------------------
# LOAD DATA
# -----------------------
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity_small.pkl", "rb"))

movie_list = movies['title'].values


# -----------------------
# RECOMMEND FUNCTION
# -----------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    indices = similarity[index]

    recommended_movies = []

    for i in indices:
        recommended_movies.append(movies.iloc[i].title)

    return recommended_movies


# -----------------------
# HOME PAGE
# -----------------------
@app.route("/")
def home():
    return render_template("index.html", movie_list=movie_list)


# -----------------------
# RECOMMEND ROUTE
# -----------------------
@app.route("/recommend", methods=["POST"])
def get_recommendation():
    movie = request.form.get("movie")
    results = recommend(movie)

    return render_template(
        "index.html",
        movie_list=movie_list,
        recommendations=results
    )


# -----------------------
# RUN APP
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

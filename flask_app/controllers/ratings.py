from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.rating import Rating

@app.route("/ratings/<int:recipe_id>")
def ratings(recipe_id):
    ratings = Rating.get_ratings_by_recipe(recipe_id)
    return render_template("ratings.html", ratings=ratings)

@app.route("/ratings/add", methods=["POST"])
def add_rating():
    if not Rating.validate_rating(request.form):
        return redirect('/ratings')
    data = {
        "user_id": session['user_id'],
        "recipe_id": request.form['recipe_id'],
        "rating": request.form['rating']
    }
    Rating.save(data)
    return redirect(f"/ratings/{request.form['recipe_id']}")

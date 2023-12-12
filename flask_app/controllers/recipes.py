from flask import render_template, request, redirect, session, flash, Blueprint
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.comment import Comment

@app.route("/my_recipes/<int:user_id>")
def recipes_by_user_id(user_id):
    recipes = Recipe.get_by_user_id(user_id)
    name=session['name']
    return render_template("my_recipes.html", recipes=recipes, user_id=user_id,name=name)

@app.route("/recipes/update/<int:recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    user_id = session['user_id']
    data = { "user_id": user_id }
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/my_recipes/{user_id}")
    data = {
        "recipe_id": recipe_id,
        "title": request.form['title'],
        "instructions": request.form['instructions'],
        "duration": request.form['duration'],
        "category": request.form['category'],
        "description": request.form['description'],
        "ingredients": request.form['ingredients']
    }
    Recipe.update(data)
    return redirect(f"/my_recipes/{user_id}")

@app.route("/recipes/view/<int:recipe_id>")
def view_recipe(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    user_id = session['user_id']
    name=session['name']
    data = { "user_id": user_id }
    comments = Comment.get_comments_by_recipe(recipe_id)
    if recipe:
        return render_template("view_recipe.html", recipe=recipe, user_id=user_id,name=name,comments=comments)
    else:
        flash("Recipe not found", "error")
        return redirect(f"/dashboard")

@app.route("/recipes/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    user_id = session['user_id']
    data = { "user_id": user_id }
    if recipe:
        return render_template("edit_recipe.html", recipe=recipe, recipe_id=recipe_id, user_id=session['user_id'], name=session['name'])
    else:
        flash("Recipe not found", "error")
        return redirect(f"/my_recipes/{user_id}")

@app.route("/recipes/delete/<int:id>")
def delete_recipe(id):
    recipes = Recipe.delete(id)
    user_id = session['user_id']
    data = { "user_id": user_id }
    return redirect(f"/my_recipes/{user_id}")

@app.route("/recipes")
def all_recipes():
    recipes = Recipe.get_all()
    return render_template("recipes.html", recipes=recipes)

@app.route("/recipes/add")
def add_recipes_form():
    return render_template("add_recipe.html")

@app.route("/recipes/save", methods=["POST"])
def add_recipe():
    user_id = session['user_id']
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes')
    data = {
        "title": request.form['title'],
        "instructions": request.form['instructions'],
        "duration": request.form['duration'],
        "category": request.form['category'],
        "description": request.form['description'],
        "ingredients": request.form['ingredients'],
        "user_id": user_id
    }
    Recipe.save(data)
    
    data["user_id"] = user_id
    return redirect(f"/my_recipes/{user_id}")

@app.route("/recipes/add_comment/<int:recipe_id>", methods=["POST"])
def add_comment(recipe_id):
    user_id = session['user_id']
    data = {
        "comment": request.form['comment'],
        "user_id": user_id,
        "recipe_id": recipe_id,
        "name": request.form['name']
    }
    Comment.save(data)
    
    data["recipe_id"] = recipe_id
    return redirect(f"/recipes/view/{recipe_id}")
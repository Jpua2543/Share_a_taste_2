from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.comment import Comment

@app.route("/comments/<int:recipe_id>")
def comments(recipe_id):
    comments = Comment.get_comments_by_recipe(recipe_id)
    return render_template("comments.html", comments=comments)

@app.route("/comments/add", methods=["POST"])
def add_comment():
    if not Comment.validate_comment(request.form):
        return redirect('/comments')
    data = {
        "user_id": session['user_id'],
        "recipe_id": request.form['recipe_id'],
        "content": request.form['content']
    }
    Comment.save(data)
    return redirect(f"/comments/{request.form['recipe_id']}")

# Add more routes as needed, such as editing and deleting comments
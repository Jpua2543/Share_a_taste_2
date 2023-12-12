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

@app.route("/recipes/add_comment/<int:recipe_id>", methods=["POST"])
def add_comment(recipe_id):
    if 'user_id' not in session:
        flash('You must be logged in to comment')
        return redirect('/login')

    data = {
        "user_id": session['user_id'],
        "recipe_id": recipe_id,
        "comment": request.form['comment'],
        "name": request.form['name']
    }

    Comment.save(data)
    return redirect(f"/recipes/view/{recipe_id}")

@app.route("/comments/edit/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    if 'user_id' not in session:
        flash("Please log in to edit comments.", "error")
        return redirect('/login')
    comment = Comment.get_by_id(comment_id)
    if comment and session['user_id'] == comment.user_id:
        if request.method == "POST":
            if Comment.validate_comment(request.form):
                updated_comment = {
                    "comment_id": comment_id,
                    "comment": request.form['comment']
                }
                Comment.update(updated_comment)
                flash("Comment updated successfully.", "success")
                return redirect(f"/recipes/view/{comment.recipe_id}")
            else:
                return redirect(request.url)
        else:
            return render_template("edit_comment.html", comment=comment)
    else:
        flash("Comment not found or you do not have permission to edit this comment.", "error")
        return redirect('/dashboard')

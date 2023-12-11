from flask import render_template, request,redirect,session
from flask_app import app
from flask import flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def register_login():
    return render_template("registration_login.html")


@app.route("/register", methods= ["POST"] )
def add():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    one_user = User.save(data)
    if one_user:
        session['user_id']=one_user
        session['name'] = request.form['first_name']+ " " +request.form['last_name']
        return redirect("/dashboard")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password","log")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password","log")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['name'] = user_in_db.first_name+ " "+ user_in_db.last_name
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if 'user_id' in session:
        name = session['name']
        user_id = session['user_id']
        recipes = Recipe.get_all_ordered_by_id_desc()
        return render_template("dashboard.html",name=name,user_id=user_id,recipes=recipes)
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
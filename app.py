import os

from flask import Flask, render_template, redirect, request, session, flash
from cs50 import SQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from helpers import login_required, apology

app = Flask(__name__)

app.secret_key = "secret key buddy"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


db = SQL("sqlite:///liftup.db")

@app.after_request
def after_request(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("home.html")

@app.route("/register",  methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm_password")
        
        
        if not username:
            return apology("must provide username", 400)
        
        elif not password:
            return apology("must provide password", 400)
    
        elif not confirmation:
            return apology("must provide confirmation-password", 400)

        elif not password == confirmation:
            return apology("password not matches", 400)

        user_exists = db.execute("SELECT * FROM users WHERE user_name = ?", username)

        if user_exists:
            return apology("user already exists", 400)
        
        hashed_password = generate_password_hash(password)

        id = db.execute("INSERT INTO users (user_name, hash) VALUES (?, ?)", username, hashed_password)
        db.execute("INSERT INTO user_status(user_id) VALUES(?)", id)
        session["user_id"] = id
        session["user_name"] = username

        flash("🎉 Congratulations You started your progress for lifting-up in life 🎉")
        
        return redirect("/")
    
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")        
        
        if not username:
            return apology("must provide username", 400)
        
        elif not password:
            return apology("must provide password", 400)

        user_exists = db.execute("SELECT * FROM users WHERE user_name = ?", username)

        if not user_exists :
            return apology("Invalid username or Password", 400)
        
        elif not check_password_hash(user_exists[0]["hash"], password):
            return apology("Invalid password", 400)
        
        session["user_id"] = user_exists[0]["id"]
        session["user_name"] = username

        flash("!! Logged in successfully !!")

        return redirect("/")
    
    return render_template("login.html")  

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")


@app.route("/eat", methods=["GET", "POST"])
@login_required
def eat():
    if request.method == "POST":
        
        dish = request.form.get("dish")
        description = request.form.get("description")

        if not dish:
            return apology("please provide Dish Name")
        elif not description:
            return apology("please provide description")
        
        dish_id = db.execute("INSERT INTO dishes (dish, description) VALUES(?, ?)", dish, description)
        db.execute("INSERT INTO user_dishes (user_id, dish_id) VALUES(?, ?)", session["user_id"], dish_id)
        
        return redirect("/eat")
    
    if request.method == "GET":

        dishes = db.execute("SELECT * FROM dishes WHERE id IN (SELECT dish_id FROM user_dishes WHERE user_id == ?)", session["user_id"])
        return render_template("eat.html", dishes=dishes)
    
@app.route("/eat/remove", methods=["POST"])
@login_required
def remove_dish():
    dish_name = request.form.get("remove_dish")
    dish_id = db.execute("SELECT id FROM dishes WHERE dish = ?", dish_name)
    db.execute("DELETE FROM user_dishes WHERE dish_id = ?", dish_id[0]["id"])
    db.execute("INSERT INTO finished_dishes (user_id, dish_id) VALUES(?, ?)", session["user_id"],dish_id[0]["id"] )
    return redirect("/eat")

@app.route("/slice")
@login_required
def slice():
    return render_template("slice.html")


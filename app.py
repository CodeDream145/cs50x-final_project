from flask import Flask, render_template, redirect, request, session, flash
from cs50 import SQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta

from helpers import login_required, apology

app = Flask(__name__)

app.secret_key = "secret key buddy"

app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=17)
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


        if not username and not password and not confirmation:
            return render_template("register.html", name_error= "must provide user-name", pass_error="must provide password", user_name=username)        
        
        if not username and not password:
            return render_template("register.html", name_error= "must provide user-name", pass_error="must provide password", user_name=username)
        
        if not username:
            return render_template("register.html", name_error="must provide username")
        
        if not password and username:
            return render_template("register.html", pass_error="must provide password", user_name=username)
    
        if not confirmation and username:
            return render_template("register.html", con_pass_error="must provide confirmation-password", user_name=username)
        
        elif  len(password) < 8 or len(password) > 20:
            return render_template("register.html", pass_error="Password must be between 8 to 20 characters", con_pass_error="Password must be between 8 to 20 characters", user_name=username)

        elif not password == confirmation:
            return render_template("register.html", con_pass_error="password not match", pass_error="password not match", user_name=username)

        user_exists = db.execute("SELECT * FROM users WHERE user_name = ?", username)

        if user_exists:
            return render_template("register.html", name_error="User Already Exists", user_name=username)
        
        hashed_password = generate_password_hash(password)

        id = db.execute("INSERT INTO users (user_name, hash) VALUES (?, ?)", username, hashed_password)
        db.execute("INSERT INTO user_status(user_id) VALUES(?)", id)
        session["user_id"] = id
        session["user_name"] = username

        flash("🎉 Congratulations! You took a major step towards improving your lot in life. 🎉")
        
        return redirect("/")
    
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")        
        
        if not username and not password:
            return render_template("login.html", name_error="must provide username", pass_error="must provide password")
        
        if not username:
            return render_template("login.html", name_error="must provide username")
        
        elif not password and username:
            return render_template("login.html", pass_error="must provide password", user_name=username)

        user_exists = db.execute("SELECT * FROM users WHERE user_name = ?", username)

        if not user_exists :
            return render_template("login.html", name_error="Invaild User Name", user_name=username)
        
        elif not check_password_hash(user_exists[0]["hash"], password):
            return render_template("login.html", pass_error="Invalid Pasword", user_name=username)
        
        session["user_id"] = user_exists[0]["id"]
        session["user_name"] = username

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

        dishes = db.execute("SELECT * FROM dishes WHERE id IN (SELECT dish_id FROM user_dishes WHERE user_id = ?)", session["user_id"])

        if not dish and not description:
            return render_template("eat.html", name_error="Please Provide Dish Name", des_error="Please Provide Description", dishes=dishes)
        elif description and not dish:
            return render_template("eat.html", name_error="Please Provide Dish Name", dishes=dishes, description=description)
        elif len(description) > 3000:
            return render_template("eat.html", des_error="Description should not exceed 3000 chatracters ", dishes=dishes, name=dish, description=description)
        elif len(dish) > 35:
            return render_template("eat.html", name_error="Dish name should not exceed 35 chatracters ", dishes=dishes, name=dish, description=description)

        elif dish and not description:
            return render_template("eat.html", des_error="Please Provide Description", dishes=dishes, name=dish)
        
                
        dish_id = db.execute("INSERT INTO dishes (dish, description, date) VALUES(?, ?, ?)", dish, description, date.today())
        db.execute("INSERT INTO user_dishes (user_id, dish_id) VALUES(?, ?)", session["user_id"], dish_id)        
        
        return redirect("/eat")
    
    if request.method == "GET":

        dishes = db.execute("SELECT * FROM dishes WHERE id IN (SELECT dish_id FROM user_dishes WHERE user_id = ?)", session["user_id"])
        return render_template("eat.html", dishes=dishes)


@app.route("/eat/remove", methods=["POST"])
@login_required
def remove_dish():
    dish_name = request.form.get("remove_dish")
    if not dish_name:
        return apology("Trying Something ha...", 400)
    dish_id = db.execute("SELECT id FROM dishes WHERE dish = ?", dish_name)
    db.execute("DELETE FROM user_dishes WHERE dish_id = ?", dish_id[0]["id"])
    db.execute("INSERT INTO finished_dishes (user_id, dish_id, date) VALUES(?, ?, ?)", session["user_id"],dish_id[0]["id"], date.today() )
    
    goals_completed  = db.execute("SELECT goals_completed FROM user_status WHERE user_id = ?", session["user_id"])
    db.execute("UPDATE user_status SET goals_completed = ? WHERE user_id = ?", int(goals_completed[0]["goals_completed"]) + 1, session["user_id"])
    return redirect("/eat")

@app.route("/slice", methods=["GET", "POST"])
@login_required
def slice():
    days = ["0", "1", "2", "3", "4", "5", "\\0"]
    status = db.execute("SELECT * FROM user_status WHERE user_id = ?", session["user_id"])
    
    
    if request.method =="POST":
        
        finished_day = request.form.get("finished_day")
        current_week = int(status[0]["current_week"])
        days_passed = int(status[0]["days_passed"])

        if not finished_day  == "\\0":
            current_day = days[days.index(finished_day) + 1]
        else:
            current_day = days[0]
            current_week = current_week + 1
        
        days_passed = days_passed + 1
        
        db.execute("UPDATE user_status SET current_day = ?, current_week = ?, days_passed = ?  WHERE user_id = ?", current_day, current_week, days_passed, session["user_id"])

        return redirect("/slice")
    

    return render_template("slice.html", current_day = status[0]["current_day"], current_week = status[0]["current_week"], days = days)

@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    if request.method == "POST":
        year = str(request.form.get("year"))
        month = str(request.form.get("month"))
        day = str(request.form.get("day"))
        finished_date = f"{year}-{month}-{day}"

        goal_history = db.execute("SELECT * FROM dishes Where id IN (SELECT dish_id FROM finished_dishes WHERE user_id = ? AND date = ?)", session["user_id"], finished_date)
        status = db.execute("SELECT * FROM user_status WHERE user_id = ?", session["user_id"])

        months =[]
        days =[]
        for x in range(1,10):
            months.append(f"0{x}")
            days.append(f"0{x}")
        for y in range(10, 32):
            days.append(f"{y}")
        for z in range(10, 13):
            months.append(f"{z}")

        if (month not in months) or (day not in days) :
            return render_template("dashboard.html", status=status, invalid_date= "Invalid Date")
        
        if not goal_history:
            return render_template("dashboard.html", status=status, not_found= f"No Goal was eaten on {year}-{month}-{day}.")

        return render_template("dashboard.html", status=status, goal_history=goal_history)
    
    status = db.execute("SELECT * FROM user_status WHERE user_id = ?", session["user_id"])

    return render_template("dashboard.html", status=status)

@app.route("/hear")
@login_required
def hear():
    return render_template("hear.html")

'''@app.route("/dashboard/history", methods=["POST"])
@login_required
def history(): 
    year = str(request.form.get("year"))
    month = str(request.form.get("month"))
    day = str(request.form.get("day"))
    finished_date = f"{year}-{month}-{day}"

    goal_history = db.execute("SELECT * FROM dishes Where id IN (SELECT dish_id FROM finished_dishes WHERE user_id = ? AND date = ?)", session["user_id"], finished_date)
    status = db.execute("SELECT * FROM user_status WHERE user_id = ?", session["user_id"])

    return render_template("dashboard.html", status=status, goal_history=goal_history)'''
from flask import Flask, render_template, request, session, redirect, url_for, g
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash 
from forms import RegistrationForm, LoginForm, ReviewForm, SuggestionForm, QuizForm, VoteForm, GameForm
from functools import wraps

"""
There are two types of users, regular users and admins. To register as a regular user you can find the link in various places including the nav.
To see the admin features, you can log in with the username Admin and the password admin.
The admin can reset the vote count and also see a full list of the products in the shop and can remove them.
The admin page will redirect to the home page if the user isnt an admin for security reasons.

Vote links with game as the votes casted are entered into the database 
This changes the outcome of the game as the amount of votes cast for the leading chocolate can be seen
It also says if there are no votes yet
test
"""



app = Flask(__name__)
app.config["SECRET_KEY"]= "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.teardown_appcontext
def close_db_at_end_of_requests(e=None):
    close_db(e)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

@app.route("/")
def welcome():
    db = get_db()
    return render_template("welcome.html")

#milkchocolate
@app.route("/milkchocolate")
def milkchocolate():
    db = get_db()
    milkchocs = db.execute("""SELECT * FROM milkchoc;""").fetchall()
    return render_template("milkchocall.html", milkchocs=milkchocs)

@app.route("/milkchoc/<int:milk_choc_id>")
def milkchoc(milk_choc_id):
    db = get_db()
    milkchoc = db.execute("""SELECT * FROM milkchoc
                            WHERE milk_choc_id = ?;""", (milk_choc_id,)).fetchone()
    return render_template("milkchoc.html", milkchoc=milkchoc)

#darkchocolate
@app.route("/darkchocolate")
def darkchocolate():
    db = get_db()
    darkchocs = db.execute("""SELECT * FROM darkchoc;""").fetchall()
    return render_template("darkchocall.html", darkchocs=darkchocs)

@app.route("/darkchoc/<int:dark_choc_id>")
def darkchoc(dark_choc_id):
    db = get_db()
    darkchoc = db.execute("""SELECT * FROM darkchoc
                        WHERE dark_choc_id = ?;""", (dark_choc_id,)).fetchone()
    return render_template("darkchoc.html", darkchoc=darkchoc)

#whitechocolate
@app.route("/whitechocolate")
def whitechocolate():
    db = get_db()
    whitechocs = db.execute("""SELECT * FROM whitechoc;""").fetchall()
    return render_template("whitechocall.html", whitechocs=whitechocs)

@app.route("/whitechoc/<int:white_choc_id>")
def whitechoc(white_choc_id):
    db = get_db()
    whitechoc = db.execute("""SELECT * FROM whitechoc
                        WHERE white_choc_id = ?;""", (white_choc_id,)).fetchone()
    return render_template("whitechoc.html", whitechoc=whitechoc)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = str(form.password.data)
        password2 = str(form.password2.data)
        db = get_db()
        if db.execute("""SELECT * FROM users
                          WHERE user_id =?;""", (user_id,)).fetchone() is not None:
            form.user_id.errors.append("User ID already taken!")
        else:
            db.execute("""INSERT INTO users (user_name, admin_user, password)
                        VALUES (?, 0, ?);""",
                        (user_id, generate_password_hash(password)))
            db.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        user = db.execute("""SELECT * FROM users
                    WHERE user_name = ?;""", (user_id,)).fetchone()
        print(user['password'])
        if user is None:
            form.user_id.errors.append("Unknown user id")
        elif not check_password_hash(user["password"], password): 
            form.password.errors.append("Incorrect password")
        else:
            session.clear()
            session["user_id"] = user_id
            if user['admin_user']:
                session["admin_user"] = True
                next_page = url_for("admin")
                return redirect(next_page)
            else:
                session["admin_user"] = False
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("welcome")
            return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("welcome"))


@app.route("/cart")
@login_required
def cart():
    total = 0
    if "cart" not in session:
        session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc':{}, 
            'whitechoc':{} 
        }
    if 'milkchoc' not in session["cart"]:
        session["cart"]["milkchoc"] = {}
    if 'darkchoc' not in session["cart"]:
        session["cart"]["darkchoc"] = {}
    if 'whitechoc' not in session["cart"]:
        session["cart"]["whitechoc"] = {}
    names = {
        'milkchoc': {}, 
        'darkchoc':{}, 
        'whitechoc':{} 
    }
    db = get_db()
    for milk_choc_id in session["cart"]["milkchoc"]:
        sqlite_row = db.execute("""SELECT * FROM milkchoc
                            WHERE milk_choc_id = ?;""", (milk_choc_id, )).fetchone()
        names['milkchoc'][milk_choc_id] = sqlite_row
        total += float(sqlite_row['price'])
    for dark_choc_id in session["cart"]["darkchoc"]:
        sqlite_row = db.execute("""SELECT * FROM darkchoc
                            WHERE dark_choc_id = ?;""", (dark_choc_id, )).fetchone()
        names['darkchoc'][dark_choc_id] = sqlite_row
        total += float(sqlite_row['price'])
    for white_choc_id in session["cart"]["whitechoc"]:
        sqlite_row = db.execute("""SELECT * FROM whitechoc
                            WHERE white_choc_id = ?;""", (white_choc_id, )).fetchone()
        names['whitechoc'][white_choc_id] = sqlite_row
        total += float(sqlite_row['price'])
    print(names)
    return render_template("cart.html", cart=session["cart"], names=names, total=total)


@app.route("/add_to_milk_cart/<int:milk_choc_id>")
@login_required
def add_to_milk_cart(milk_choc_id):
    if "cart" not in session:
        session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc':{}, 
            'whitechoc':{} 
        }
    if milk_choc_id not in session["cart"]["milkchoc"]:
        session["cart"]["milkchoc"][milk_choc_id] = 0
    session["cart"]["milkchoc"][milk_choc_id] = session["cart"]["milkchoc"][milk_choc_id] + 1
    return redirect(url_for("cart") )


@app.route("/add_to_dark_cart/<int:dark_choc_id>")
@login_required
def add_to_dark_cart(dark_choc_id):
    if "cart" not in session:
        session["cart"] =  {
            "milkchoc": {}, 
            'darkchoc':{}, 
            'whitechoc':{} 
        }
    if dark_choc_id not in session["cart"]["darkchoc"]:
        session["cart"]["darkchoc"][dark_choc_id] = 0
    session["cart"]["darkchoc"][dark_choc_id] = session["cart"]["darkchoc"][dark_choc_id] + 1
    return redirect(url_for("cart") )

@app.route("/add_to_white_cart/<int:white_choc_id>")
@login_required
def add_to_white_cart(white_choc_id):
    if "cart" not in session:
        session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc': {}, 
            'whitechoc':{} 
        }
    if white_choc_id not in session["cart"]["whitechoc"]:
        session["cart"]["whitechoc"][white_choc_id] = 0
    session["cart"]["whitechoc"][white_choc_id] = session["cart"]["whitechoc"][white_choc_id] + 1
    return redirect(url_for("cart") )


@app.route("/remove_from_milk_cart/<int:milk_choc_id>")
def remove_from_milk_cart(milk_choc_id):
    if "cart" not in session:
        session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc': {}, 
            'whitechoc':{} 
        }
    if milk_choc_id in session["cart"]["milkchoc"]:
        session["cart"]["milkchoc"].pop(milk_choc_id)
    return redirect(url_for("cart") )

@app.route("/remove_one_from_milk_cart/<int:milk_choc_id>")
def remove_one_from_milk_cart(milk_choc_id):
    if "cart" not in session:
        session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc': {}, 
            'whitechoc':{} 
        }
    if milk_choc_id in session["cart"]["milkchoc"]:
        if session["cart"]["milkchoc"][milk_choc_id] == 1:
            session["cart"]["milkchoc"].pop(milk_choc_id)
        else:
            session["cart"]["milkchoc"][milk_choc_id] = session["cart"]["milkchoc"][milk_choc_id] - 1
    return redirect(url_for("cart") )

@app.route("/remove_from_white_cart/<int:white_choc_id>")
def remove_from_white_cart(white_choc_id):
    if "cart" not in session:
        session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc': {}, 
            'whitechoc':{} 
        }
    if white_choc_id in session["cart"]["whitechoc"]:
        session["cart"]["whitechoc"].pop(white_choc_id)
    return redirect(url_for("cart") )

@app.route("/remove_one_from_white_cart/<int:white_choc_id>")
def remove_one_from_white_cart(white_choc_id):
    if "cart" not in session:
        session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc': {}, 
            'whitechoc':{} 
        }
    if white_choc_id in session["cart"]["whitechoc"]:
        if session["cart"]["whitechoc"][white_choc_id] == 1:
            session["cart"]["whitechoc"].pop(white_choc_id)
        else:
            session["cart"]["whitechoc"][white_choc_id] = session["cart"]["whitechoc"][white_choc_id] - 1
    return redirect(url_for("cart") )

@app.route("/remove_from_dark_cart/<int:dark_choc_id>")
def remove_from_dark_cart(dark_choc_id):
    if "cart" not in session:
        session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc': {}, 
            'whitechoc':{} 
        }
    if dark_choc_id in session["cart"]["darkchoc"]:
        session["cart"]["darkchoc"].pop(dark_choc_id)
    return redirect(url_for("cart") )


@app.route("/remove_one_from_dark_cart/<int:dark_choc_id>")
def remove_one_from_dark_cart(dark_choc_id):
    if "cart" not in session:
        session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc': {}, 
            'whitechoc':{} 
        }
    if dark_choc_id in session["cart"]["darkchoc"]:
        if session["cart"]["darkchoc"][dark_choc_id] == 1:
            session["cart"]["darkchoc"].pop(dark_choc_id)
        else:
            session["cart"]["darkchoc"][dark_choc_id] = session["cart"]["darkchoc"][dark_choc_id] - 1
    return redirect(url_for("cart") )

@app.route("/clear_cart")
def clear_cart():
    session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc': {}, 
            'whitechoc':{} 
        }
    return redirect(url_for("cart") )

@app.route("/checkout")
def checkout():
    session["cart"] =  {
            'milkchoc': {}, 
            'darkchoc': {}, 
            'whitechoc':{} 
        }
    return redirect(url_for("welcome") )

@app.route("/review", methods=["GET", "POST"])
def review():
    form = ReviewForm()
    message = ""
    if form.validate_on_submit():
        chocolate = form.chocolate.data
        review = form.review.data
        if chocolate == "" and review =="":
            message = "Please let us know your thoughts by filling out both fields!"
        elif chocolate == "":
            message = "Please let us know your thoughts by filling out chocolate field!"
        elif review == "":
            message = "Please let us know your thoughts by filling out review field!"
        else:
            message = "Thanks for the feedback!"
    return render_template("review.html", form=form, message=message)


@app.route("/suggestion", methods=["GET", "POST"])
def suggestion():
    form = SuggestionForm()
    message = ""
    if form.validate_on_submit():
        suggestion = form.suggestion.data
        if suggestion != "":
            message = "Thanks for your great idea!"
        else:
            message = "Please enter your idea!"
    return render_template("suggestion.html", form=form, message=message)



@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    form = QuizForm()
    favorite = ''
    if form.validate_on_submit():
        first_question = form.first_question.data
        second_question = form.second_question.data
        third_question = form.third_question.data
        quiz_answers = {
            'q1':0,
            'q2':0,
            'q3':0
        }
        if first_question == "yes":
            quiz_answers['q1'] = 1
        elif first_question == "not really":
            quiz_answers['q1'] = 2
        elif first_question == "no":
            quiz_answers['q1'] = 3
        if second_question == "sweet":
            quiz_answers['q2'] = 1
        elif second_question == "savoury":
            quiz_answers['q2'] = 2
        elif second_question == "neither":
            quiz_answers['q2'] = 3
        if third_question == "everyday":
            quiz_answers['q3'] = 1
        elif third_question == "often":
            quiz_answers['q3'] = 2
        elif third_question == "never":
            quiz_answers['q3'] = 3
        milk_count = 0
        dark_count = 0
        white_count = 0
        for x in quiz_answers.values():
            if x == 1:
                milk_count += 1
            elif x == 2:
                dark_count += 1
            else:
                white_count += 1
        if milk_count > dark_count and milk_count > white_count:
            favorite = "You should try Milk Chocalate"
        elif dark_count > milk_count and dark_count > white_count:
            favorite = "You should try dark chocolate"
        elif white_count > milk_count and white_count > dark_count:
            favorite = "You should try white chocolate"
        else:
            favorite = "You should buy one of each!!"
    return render_template("quiz.html", title ="What's the best chocolate for you?", form=form,
            favorite=favorite)


@app.route("/game", methods=["GET", "POST"])
def game():
    form = GameForm()
    outcome = ""
    db = get_db()
    if form.validate_on_submit():
        top_choc = {'name': 'none', 'count': 0}
        chocolate = form.chocolate.data
        sqlite_rows = db.execute("""SELECT * FROM votes;""").fetchall()
        for x in sqlite_rows:
            if x['vote_count'] > top_choc['count']:
                print("setting new top choc")
                top_choc['name'] = x['chocolate']
                top_choc['count'] = x['vote_count']
        if chocolate == top_choc['name']:
            print("WINNER :D")
            outcome = "You're correct! it's " + top_choc['name'] + " with " + str(top_choc['count']) +  " votes"
        elif top_choc['count'] == 0:
            outcome = "Looks like no one voted yet."
        else:
            outcome = "Oops! You're wrong, try again!"
    return render_template("game_form.html", title ="What's our most popular chocolate?", form=form,
            outcome=outcome)

@app.route("/vote", methods=["GET", "POST"])
def vote():
    form = VoteForm()
    db = get_db()
    outcome = ""
    if form.validate_on_submit():
        vote = form.vote.data
        sqlite_row = db.execute("""SELECT vote_count FROM votes
                        WHERE chocolate = ?;""", (vote, )).fetchone()
        vote_count = str(int(sqlite_row['vote_count']) + 1)
        db.execute("""UPDATE votes SET vote_count = ? 
        WHERE chocolate = ?; """, (vote_count, vote))
        db.commit()
        outcome = "Thanks for voting"
    return render_template("vote.html", outcome=outcome, form=form)

    
@app.route("/admin", methods=["GET", "POST"])
def admin(): 
    print(session['admin_user'])
    if session['admin_user'] == True:
        return render_template("admin.html")
    else:
        return redirect(url_for("welcome"))

@app.route("/reset_vote", methods=["GET"])
def reset_vote():
    if session['admin_user'] == True:
        db = get_db()
        db.execute("""UPDATE votes SET vote_count = 0; """)
        db.commit()
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("welcome"))

@app.route("/list_products", methods=["GET"]) 
def list_products():
    if session['admin_user'] == True:
        db = get_db()
        milkchocs = db.execute("""SELECT * FROM milkchoc;""").fetchall()
        darkchocs = db.execute("""SELECT * FROM darkchoc;""").fetchall()
        whitechocs = db.execute("""SELECT * FROM whitechoc;""").fetchall()
        return render_template("admin_products.html", milkchocs=milkchocs, darkchocs=darkchocs, whitechocs=whitechocs)
    else:
        return redirect(url_for("welcome"))

@app.route("/remove_product_milk/<int:milk_choc_id>", methods=["GET", "POST"])
def remove_product_milk(milk_choc_id):
    if session['admin_user'] == True:
        db = get_db()
        db.execute("""DELETE FROM milkchoc WHERE milk_choc_id = ?;""", (str(milk_choc_id)))
        db.commit()
        return redirect(url_for("list_products"))
    else:
        return redirect(url_for("welcome"))

@app.route("/remove_product_dark/<int:dark_choc_id>", methods=["GET", "POST"])
def remove_product_dark(dark_choc_id):
    if session['admin_user'] == True:
        db = get_db()
        db.execute("""DELETE FROM darkchoc WHERE dark_choc_id = ?;""", (str(dark_choc_id)))    
        db.commit()
        return redirect(url_for("list_products"))
    else:
        return redirect(url_for("welcome"))

@app.route("/remove_product_white/<int:white_choc_id>", methods=["GET", "POST"])
def remove_product_white(white_choc_id):
    if session['admin_user'] == True:
        db = get_db()
        db.execute("""DELETE FROM whitechoc WHERE white_choc_id  = ?;""", (str(white_choc_id)))
        db.commit()
        return redirect(url_for("list_products"))
    else:
        return redirect(url_for("welcome"))
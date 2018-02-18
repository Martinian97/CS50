from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Change Password."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")
        # ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password")
        # ensure both passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Your passwords do not match")
    
        # update the new password in users table
        result = db.execute("UPDATE users SET hash = :hash WHERE id=:id" ,  id = session["user_id"] , hash = pwd_context.encrypt(request.form["password"]))
        
        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")

@app.route("/")
@login_required
def index():
    menu = []
    rows = db.execute("SELECT userid,symbol,shares FROM transactions WHERE userid=:userid" , userid=session["user_id"])
    # to check if you own any stocks
    if not rows:
        return apology("You own nothing")
    cash = db.execute("SELECT cash FROM users WHERE id=:id" , id=session["user_id"])
    # for each stock owned by the user
    for row in rows:
        stock = lookup(row["symbol"])
        if stock!=None:
            # save necessary details in a dictionary
            details = {"name" : stock["name"] , "price" : usd(stock["price"]) , "shares" : row["shares"] , "symbol" : row["symbol"].upper() , "total" : usd(row["shares"]*stock["price"])}
            # append it in a list
            menu.append(details.copy())
        
    return render_template("index.html" , menu=menu , balance=usd(cash[0]["cash"]))
        
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        # ensure symbol was submitted
        if not request.form.get("symbol"):    
            return apology("must provide the stock symbol")
        q = lookup(request.form.get("symbol"))
        if q == None:
            # ensure stock exists
            return apology("Stock doesn't exist")
        # ensure number of shares was submitted
        if not request.form.get("number"):    
            return apology("must provide the number of shares")
        # ensure number is a positive integer
        try:
            number = int(request.form.get("number"))
        except ValueError:
            return apology("Not a positive integer")
        else:
            if number<0:
                return apology("Not a positive integer")
        
        # total cost of the number of shares you want to buy
        amount = (q["price"]*int(request.form.get("number")))
        # cash a user currently has
        cash = db.execute("SELECT cash FROM users WHERE id = :id" , id = session["user_id"])    
        # to check if you have enough cash to buy the shares
        if cash[0]["cash"] >= amount:
            # update 'cash' in users table
            db.execute("UPDATE users SET cash = :cash WHERE id=:id" , id = session["user_id"] , cash = cash[0]["cash"] - amount)
            result = db.execute("SELECT symbol FROM transactions WHERE userid=:userid AND symbol=:symbol" , symbol = request.form.get("symbol") , userid=session["user_id"])
            old = db.execute("SELECT shares FROM transactions WHERE userid=:userid AND symbol=:symbol" , symbol = request.form.get("symbol") , userid=session["user_id"])
            db.execute("INSERT INTO history (userid,shares,price,symbol,type) VALUES (:userid,:shares,:price,:symbol,:type)" , symbol = request.form.get("symbol") , userid = session["user_id"] , shares = int(request.form.get("number")) , type = 'BUY' , price = q["price"])
            # to check if user already owns that stock
            if result:
                # then update the number of shares
                db.execute("UPDATE transactions SET shares=:shares WHERE userid=:userid AND symbol=:symbol" , symbol = request.form.get("symbol") , userid=session["user_id"] , shares = old[0]["shares"] + int(request.form.get("number")))
                return redirect(url_for("index"))
            
            #else insert this new stock details in the table        
            db.execute("INSERT INTO transactions (symbol,shares,price,userid) VALUES (:symbol , :shares , :price , :userid)" , symbol = request.form.get("symbol") , shares = int(request.form.get("number")) , price = q["price"] , userid = session["user_id"])
            return redirect(url_for("index"))
        else:
            return apology("Not enough cash")
    else:
        return render_template("buy.html")
    
@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    menu = []
    rows = db.execute("SELECT userid,symbol,shares,type,datetime FROM history WHERE userid=:userid" , userid=session["user_id"])
    # to check if any history exists for this account
    if not rows:
        return apology("No transactions done yet")
    # for each stock owned by the user
    for row in rows:
        stock = lookup(row["symbol"])
        if stock!=None:
            #store the neccesary details in a dictionary
            details = {"price" : usd(stock["price"]) , "shares" : row["shares"] , "symbol" : row["symbol"].upper() , "type" : row["type"] , "datetime" : row["datetime"]}
            #append it in a list
            menu.append(details.copy())
        
    return render_template("history.html" , menu=menu)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        #lookup that symbol's details
        q = lookup(request.form.get("symbol"))
        if q == None:
            # ensure stock exists
            return apology("Stock doesn't exist")
        
        return render_template("quoted.html" , data = q)
        @app.route("/quoted", methods=["GET", "POST"])
        @login_required
        def quoted():
            return render_template("quoted.html" , data = q)
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        
        # ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        # ensure both passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Your passwords do not match")
        
        result = db.execute("INSERT INTO users (username , hash) VALUES (:username , :hash)" , username = request.form["username"] , hash = pwd_context.encrypt(request.form["password"]))
        # query database for username
        if not result:
            return apology("Username already exists")
        
        # store the new user's id 
        session["user_id"] = result
        
        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # ensure symbol was submitted
        if not request.form.get("symbol"):    
            return apology("must provide the stock symbol")
        # lookup details of the stock's symbol
        q = lookup(request.form.get("symbol"))
        if q == None:
            # ensure stock exists
            return apology("Stock doesn't exist")
        
        # ensure number of shares was submitted
        if not request.form.get("number"):    
            return apology("must provide the number of shares")
        # to check if number is a positive integer
        try:
            number = int(request.form.get("number"))
        except ValueError:
            return apology("Not a positive integer")
        else:
            if number<0:
                return apology("Not a positive integer")
        
        # total cost of the shares user wants to sell
        amount = (q["price"]*int(request.form.get("number")))
        sold = int(request.form.get("number"))
        cash = db.execute("SELECT cash FROM users WHERE id = :id" , id = session["user_id"])
        shares = db.execute("SELECT shares FROM transactions WHERE userid = :userid AND symbol = :symbol" , symbol = request.form.get("symbol") , userid = session["user_id"])    
        symbol = db.execute("SELECT symbol FROM transactions WHERE userid = :userid AND symbol = :symbol" , symbol = request.form.get("symbol") , userid = session["user_id"])
        # to check if you own the stock or not
        if not symbol:
            return apology("You do not own this stock")
        
        # to check if you have enough shares
        if shares[0]["shares"] >= sold:
            # update all the necessary details
            db.execute("UPDATE users SET cash = :cash WHERE id=:id" , id = session["user_id"] , cash = cash[0]["cash"] + amount)
            db.execute("UPDATE transactions SET shares = :shares WHERE userid = :userid AND symbol = :symbol" , symbol = request.form.get("symbol") , userid = session["user_id"] , shares = shares[0]["shares"] - sold)
            db.execute("INSERT INTO history (userid,shares,price,symbol,type) VALUES (:userid,:shares,:price,:symbol,:type)" , symbol = request.form.get("symbol") , userid = session["user_id"] , shares = sold , type = 'SELL' , price = q["price"])
            return redirect(url_for("index"))
        else:
            return apology("Not enough shares")
    
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html")
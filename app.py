import os
import random
import math

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify
from datetime import *

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///vendor.db")

client_db = db.execute("SELECT name FROM client GROUP BY name;")

ROWS_PER_PAGE = 3

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# To display username on every HTML of navbar
@app.context_processor
def inject_user():
        user_id = session.get('user_id')
        if user_id:
            user = db.execute("SELECT username FROM users WHERE id = ?", user_id)
            if user:
                return {'username': user[0]['username']}
        return {}

# Main Page mainly to keep track of contract expiration
@app.route("/")
@login_required
def index():

    # To display x rows per page 
    per_page = 3
    total_rows = db.execute("SELECT COUNT(*) FROM tracking")
    total_pages = math.ceil(total_rows[0]["COUNT(*)"] / per_page)

    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * per_page

    transactions = db.execute(
        "SELECT id, serial_num, Device, ticket_ref, subs_type, expense_type, exp_date, client, addendum, created_at FROM tracking;")
        #   LIMIT (?) OFFSET (?);", per_page, offset)

    # Format date from YYYYMMDD extracted from database to YYYY-MM-DD
    for row in transactions:
        exp_date = row["exp_date"]
        
        year = exp_date // 10000
        month = (exp_date // 100) % 100
        day = exp_date % 100

        date_obj = date(year, month, day)
        row["expiry"] = date_obj
    
        # To calculate the number of days left to expiration
        expiration = date_obj - date.today()
        row["expiration"] = expiration.days

    sorted_transactions = sorted(transactions, key=lambda row: row["expiration"])
    
    transactions = sorted_transactions[offset:offset + per_page]

    return render_template("index.html", database=transactions, page=page, total_pages=total_pages)


@app.route("/insert", methods=["GET", "POST"])
@login_required
def insert():

    user_id = session["user_id"]

    # Randomly generate unique Serial Number 
    serial = luhn()
    sn_duplicate = db.execute("SELECT serial_num from tracking;")
    serial_list = [row['serial_num'] for row in sn_duplicate]
    while serial in serial_list:
        serial = luhn()

    if request.method == "POST":
        device = request.form.get("device")
        if not device:
            return apology("Must provide Device Model.")
        
        ref = request.form.get("ref")
        if not ref:
            return apology("Must provide Ticket Reference.")

        subtype = request.form.get("subtype")
        if not subtype:
            return apology("Must provide Subscription Type.")
        
        exptype = request.form.get("exptype")
        if not exptype:
            return apology("Must provide Expenditure Type.")
        
        # Change format of date to be same Data Type as database
        expiry = request.form.get("expiry")
        date_obj = datetime.strptime(expiry, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%Y%m%d')
        
        # Not allowing users to put a past date
        if date_obj <= datetime.today():
            flash("Expiry date not valid!")
            return redirect("/insert")
        
        if not expiry:
            return apology("Must provide Expiration Date.")
         
        client = request.form.get("client")
        if not client:
            return apology("Must provide client name.")
        
        add = request.form.get("add")
        if not add:
            return apology("Must provide Addendum.")

        db.execute("INSERT INTO tracking (serial_num, Device, ticket_ref, subs_type, expense_type, exp_date, client, Addendum, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   serial, device, ref, subtype, exptype, int(formatted_date), client, add, user_id)
    
        flash("Insert Successful!")
        return redirect("/")

    return render_template("insert.html", serial=serial, client_db = client_db)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():

    user_id = session["user_id"]

    # To retrieve data from database to HTML
    if request.method == "GET":
        try:
            id = request.args.get('id')
            edit = db.execute("SELECT * FROM tracking WHERE id = (?)", id)
            
            # Change date format from database to HTML compatible 
            db_date = edit[0]["exp_date"]
            date_obj = datetime.strptime(str(db_date), '%Y%m%d')
            formatted_date = date_obj.strftime('%Y-%m-%d')

            if edit[0]['user_id'] != user_id:
                return apology("This data does not belong to you.")

            return render_template("edit.html", edit=edit, client_db=client_db, formatted_date=formatted_date)
        
        except ValueError:
            pass

        return apology("Invalid Request")   

    # To edit and update data from HTML to database
    if request.method =='POST':
        serial = request.form.get("serial")
        edit = db.execute("SELECT * FROM tracking WHERE serial_num = (?)", serial)

        device = request.form.get("device")
        if not device:
            device = edit[0]['Device']
        
        ref = request.form.get("ref")
        if not ref:
            ref = edit[0]['ticket_ref']

        subtype = request.form.get("subtype")
        if not subtype:
            subtype = edit[0]['subs_type']
        
        exptype = request.form.get('exptype')
        if not exptype:
            exptype = edit[0]['expense_type'] 
        
        expiry = request.form.get("expiry")
        if not expiry:
            return apology("Must provide Expiration Date.")
        
        # Change format of date from HTML to database's Data Type
        date_obj = datetime.strptime(expiry, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%Y%m%d')
        if date_obj <= datetime.today():
            flash("Expiry date not valid!")
            return redirect("/insert")
         
        client = request.form.get("client")
        if not client:
            client = edit[0]['client']
        
        add = request.form.get("add")
        if not add:
            return apology("Must provide Addendum.")

        db.execute("UPDATE tracking SET Device = ?, ticket_ref = ?, subs_type = ?, expense_type = ?, exp_date = ?, client = ?, Addendum = ?, user_id = ? WHERE serial_num = ?",
           device, ref, subtype, exptype, formatted_date, client, add, user_id, serial)
        flash("Edit Successful!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    # Overview of data input by internal team
    # Only displaying 10 rows per page
    per_page = 10
    total_rows = db.execute("SELECT COUNT(*) FROM tracking")
    total_pages = math.ceil(total_rows[0]["COUNT(*)"] / per_page)

    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * per_page

    transactions = db.execute(
        "SELECT tracking.id AS tracking_id, * FROM tracking JOIN users on users.id = tracking.user_id;")
    
    # Formatting date of database to be compatible with HTML's
    for row in transactions:
        exp_date = row["exp_date"]
        
        year = exp_date // 10000
        month = (exp_date // 100) % 100
        day = exp_date % 100

        date_obj = date(year, month, day)
        row["expiry"] = date_obj

        expiration = date_obj - date.today()
        row["expiration"] = expiration.days

    transactions = transactions[offset:offset + per_page]

    return render_template("history.html", database=transactions, page=page, total_pages=total_pages)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/onboarding", methods=["GET", "POST"])
@login_required
def onboarding():

    # Onboarding new client's details
    countries = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

    if request.method == "POST":

        name = request.form.get("client_name")
        if not name:
            return apology("Must provide client's name!")
        
        contact_no = request.form.get("contact_no")
        if not contact_no:
            return apology("Must provide client's contact number!")
        
        address = request.form.get("address")
        if not address:
            return apology("Must provide client's address!")
        
        country = request.form.get("country")
        if not country:
            return apology("Must provide client's country!")
        
        city = request.form.get("city_name")
        if not city:
            return apology("Must provide client's city!")
        
        state = request.form.get("state")
        if not state:
            return apology("Must provide client's state!")
        
        postal_code = request.form.get("postal_code")
        if not postal_code:
            return apology("Must provide client's postal code!")

        db.execute("INSERT INTO client (name, contact_no, address, country, city, state, postal_code) VALUES (?, ?, ?, ?, ?, ?, ?);",
                   name, contact_no, address, country, city, state, postal_code)

        flash('Onboard Successfully!')
        return redirect("/client_list")
    
    else:
        return render_template("client_onboarding.html", countries=countries)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        # Ensure username was submitted
        if not username:
            return apology("Must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("Must provide password", 400)

        elif password != confirmation:
            return apology("Password do not match!", 400)

        # Query database for username
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?);", username, generate_password_hash(password))
        except:
            return apology("Username is taken, please try another username", 400)

        flash("Registered Successful!")
        # Redirect user to home page
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/client_list", methods=["GET", "POST"])
@login_required
def client_list():

    # Display all client list
    if request.method == "GET":
        database = db.execute("SELECT * FROM client;")
        return render_template("client_list.html", database = database)

    return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    """Register user"""
    user_id = session["user_id"]
    password = request.form.get("password")
    newpassword = request.form.get("newpassword")
    confirmation = request.form.get("confirmation")


    if request.method == "POST":
        # Ensure username was submitted
        if not password:
            return apology("Must provide password", 400)

        # Ensure password was submitted
        elif not newpassword:
            return apology("Must provide new password", 400)

        elif newpassword != confirmation:
            return apology("Password do not match!", 400)

        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Password incorrect!", 403)

        # Query database for username
        try:
            db.execute("UPDATE users SET hash = (?) WHERE id = (?);", generate_password_hash(newpassword), user_id)
        except:
            return apology("Please try again", 400)

        flash("Password change Successful!")
        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("change_password.html")
    

# Generate unique serial number
first_6= 1000
def luhn():
    global first_6  
    card_no = [int(i) for i in str(first_6)]  # To find the checksum digit on
    card_num = [int(i) for i in str(first_6)]  # Actual account number
    seventh_15 = random.sample(range(9), 9)  # Acc no (9 digits)
    for i in seventh_15:
        card_no.append(i)
        card_num.append(i)
    for t in range(0, 13, 2):  # odd position digits
        card_no[t] = card_no[t] * 2
    for i in range(len(card_no)):
        if card_no[i] > 9:  # deduct 9 from numbers greater than 9
            card_no[i] -= 9
    s = sum(card_no)
    mod = s % 10
    check_sum = 0 if mod == 0 else (10 - mod)
    card_num.append(check_sum)
    card_num = [str(i) for i in card_num]
    return 'DV' + ''.join(card_num)
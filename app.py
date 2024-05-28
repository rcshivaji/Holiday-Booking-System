import os
import sqlite3
import pytz
from flask import Flask, render_template,g,request,redirect,url_for,session
from datetime import datetime, timedelta, date

app = Flask(__name__)
app.secret_key = "jZuq3PpX9c3n@6b$yL@fR7YzQ2^H*sE5"

# Set up database
app.config['DATABASE'] = 'holiday_tracker.db'
# get the path of the current file
basedir = os.path.abspath(os.path.dirname(__file__))

# set the path to the SQLite database file
DATABASE = os.path.join(basedir, 'holiday_tracker.db')
users = {}

def connect_db():
    """Connect to the database and create the 'activities' table if it doesn't exist."""
    db = sqlite3.connect(app.config['DATABASE'])
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    return db


def get_db():
    """Get a connection to the database."""
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

# Close database connection on app teardown
@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request."""
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    industries = [
    "Agriculture",
    "Automotive",
    "Banking",
    "Biotechnology",
    "Chemicals",
    "Construction",
    "Consumer Goods",
    "Defense",
    "Education",
    "Energy",
    "Engineering",
    "Entertainment",
    "Financial Services",
    "Food and Beverage",
    "Healthcare",
    "Hospitality",
    "Information Technology",
    "Insurance",
    "Legal Services",
    "Logistics",
    "Manufacturing",
    "Media",
    "Mining",
    "Pharmaceuticals",
    "Real Estate",
    "Retail",
    "Telecommunications",
    "Transportation",
    "Travel and Tourism",
    "Utilities",
    "Other"
]
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        company = request.form['company']
        industry = request.form['industry']
        is_manager = request.form['is_manager']
        print(first_name,is_manager)
        db = get_db()
        cur = db.cursor()
        london_tz = pytz.timezone('Europe/London')
        current_time_london = datetime.now(london_tz)
        db.execute('INSERT INTO manager (first_name, last_name, email, password, company, industry, is_manager, creation, account_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [first_name, last_name, email, password, company, industry, is_manager, current_time_london, 1])
        db.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', industries = industries)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    london_tz = pytz.timezone('Europe/London')
    current_date_london = datetime.now(london_tz)
    db = get_db()
    db.row_factory = sqlite3.Row
    if 'user' in session:
        session.permanent = True
        return redirect(url_for('tasks'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        db.row_factory = sqlite3.Row
        user = db.execute('SELECT * FROM manager WHERE email = ?', [email]).fetchone()
        if user is None:
            error = 'User does not exist. Please create an account'
            return render_template('login.html', message=error)
        elif user[4] != password:
            error = 'Passwords do not match. Try again'
            return render_template('login.html', message=error)
        else:
            user = dict(user)
            session['user'] = user
            return redirect(url_for('home'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Home page
@app.route('/home', methods=['GET', 'POST'])
def homepage():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)

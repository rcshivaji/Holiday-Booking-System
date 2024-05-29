import os
import sqlite3
import pytz
import random
import pandas as pd
from flask import Flask, render_template,g,request,redirect,url_for,session,jsonify
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

def generate_random_six_digit_number():
    return random.randint(100000, 999999)

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
        return redirect(url_for('homepage'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        db.row_factory = sqlite3.Row
        user = db.execute('SELECT * FROM manager WHERE email = ?', [email]).fetchone()
        emp = db.execute('SELECT * FROM employee WHERE email = ?', [email]).fetchone()
        if user is None and emp is None:
            error = 'User does not exist. Please create an account'
            return render_template('login.html', message=error)
        else:
            if user is not None:
                if user[4] != password:
                    error = 'Passwords do not match. Try again'
                    return render_template('login.html', message=error)
                else:
                    user = dict(user)
                    session['user'] = user
                    return redirect(url_for('homepage'))
            else:
                if emp[4] != password:
                    error = 'Passwords do not match. Try again'
                    return render_template('login.html', message=error)
                else:
                    user = dict(emp)
                    session['user'] = user
                    return redirect(url_for('employee_home'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

events = [
    {"start": "2024-05-01", "end": "2024-05-02","name": "Shivaji", "tag": "Meeting", "description": "Project Meeting", "color": "#FF5733"},
    {"start": "2024-05-01", "end": "2024-05-02","name": "Rebecca", "tag": "Meeting2", "description": "Project Meeting", "color": "#FF5733"},
    {"start": "2024-05-09", "end": "2024-05-10","name": "Shrey", "tag": "Holiday", "description": "Public Holiday", "color": "#33FF57"},
    {"start": "2024-05-15", "end": "2024-05-17","name": "Shivaji", "tag": "Conference", "description": "Tech Conference", "color": "#3357FF"}
]

# Home page
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("home.html")

# Employee Home page
@app.route('/employee_home', methods=['GET', 'POST'])
def employee_home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("employee-home.html")

# Members page
@app.route('/members', methods=['GET', 'POST'])
def members():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.row_factory = sqlite3.Row
    members = db.execute('SELECT * FROM employee WHERE manager_id = ?', [session['user']['id']]).fetchall()
    member_ids = [member[0] for member in members]
    member_names = [member[1]+" "+member[2] for member in members]
    member_roles = [member[5] for member in members]
    # Create a dictionary from lists
    data = {
        'Member_ID': member_ids,
        'Member_Name': member_names,
        'Member_Role': member_roles
    }
    # Create DataFrame from dictionary
    members = pd.DataFrame(data)
    members = members.to_dict('records')
    return render_template("members.html", members = members)

@app.route('/events')
def get_events():
    return jsonify(events)

@app.route('/requests/count')
def get_request_count():
    # Assume you have a function `count_active_requests` to get the number of active requests
    #count = count_active_requests()
    count=1
    return jsonify({"count": count})

@app.route('/add_member', methods=['POST'])
def add_member():
    # Get data from the request
    data = request.json
    print("Received data:", data)
    db = get_db()
    cur = db.cursor()
    london_tz = pytz.timezone('Europe/London')
    current_time_london = datetime.now(london_tz)
    db.execute('INSERT INTO employee (first_name, last_name, email, password, role, department, creation, holidays, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [data["first-name"], data["last-name"], data["email"], generate_random_six_digit_number(), data["role"], data["department"], current_time_london, data["holidays"], session['user']['id']])
    db.commit()
    return jsonify({'message': 'Data received successfully'})

@app.route('/delete_member', methods=['POST'])
def delete_member():
    if request.method == 'POST':
        data = request.json
        member_id = data.get('member_id')
        db = get_db()
        cur = db.cursor()
        db.execute("DELETE FROM employee WHERE id = ?",[int(member_id)])
        db.commit()
        return "Member deleted successfully", 200
    else:
        return "Invalid request", 400

@app.route('/request_holiday', methods=['POST'])
def request_holiday():
    # Get data from the request
    data = request.get_json()
    print(data)
    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run(debug=True)

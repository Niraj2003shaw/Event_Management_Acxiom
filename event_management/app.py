from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secretkey"


# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
    ''')

    # Events table (Maintenance)
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            location TEXT
        )
    ''')

    # Transactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            amount REAL
        )
    ''')
    
    # Membership table
    c.execute('''
        CREATE TABLE IF NOT EXISTS membership (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_name TEXT,
            membership_type TEXT,
            status TEXT
        )
    ''')


    c.execute("INSERT OR IGNORE INTO users (id, username, password, role) VALUES (1, 'admin', 'admin', 'admin')")
    c.execute("INSERT OR IGNORE INTO users (id, username, password, role) VALUES (2, 'user', 'user', 'user')")


    conn.commit()
    conn.close()


# ---------------- ROUTES ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Check if user already exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            message = "Username already exists!"
        else:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",(username, password, role))
            conn.commit()
            message = "Registration Successful!"

        conn.close()

    return render_template('register.html', message=message)



@app.route('/')
def home():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        session['username'] = username
        session['role'] = user[3]
        return redirect('/dashboard')
    else:
        return "Invalid Credentials"


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template("dashboard.html", role=session['role'])


@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    message=""

    if 'username' not in session:
        return redirect('/')

    if session['role'] != 'admin':
        return "Access Denied"

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # ================= ADD EVENT =================
    if request.form.get('form_type') == 'event':
        name = request.form['name']
        date = request.form['date']
        location = request.form['location']

        if name and date and location:
            c.execute("INSERT INTO events (name, date, location) VALUES (?, ?, ?)",(name, date, location))
            conn.commit()
            message= "Event Added Successfully"

    # ================= ADD MEMBERSHIP =================
    if request.form.get('form_type') == 'membership':
        member_name = request.form['member_name']
        membership_type = request.form['membership_type']

        if member_name and membership_type:
            c.execute("INSERT INTO membership (member_name, membership_type, status) VALUES (?, ?, ?)",(member_name, membership_type, "Active"))
            conn.commit()
            message= "Membership Added Successfully "

    # ================= UPDATE MEMBERSHIP =================
    if request.form.get('form_type') == 'update_membership':
        member_id = request.form['member_id']
        action = request.form['action']

        if action == "extend":
            c.execute("UPDATE membership SET membership_type='6 Months Extended' WHERE id=?",(member_id,))
        elif action == "cancel":
            c.execute("UPDATE membership SET status='Cancelled' WHERE id=?",(member_id,))
        conn.commit()
        message= "Member Added Successfully"

    # ================= DELETE MEMBERSHIP =================
    if request.form.get('form_type') == 'delete_membership':
        member_id = request.form['member_id']
        c.execute("DELETE FROM membership WHERE id=?", (member_id,))
        conn.commit()
        message= "Membership Deleted Successfully"

    # Fetch updated data
    c.execute("SELECT * FROM events")
    events = c.fetchall()

    c.execute("SELECT * FROM membership")
    members = c.fetchall()

    conn.close()

    return render_template("maintenance.html",events=events,members=members,message=message)




@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if 'username' not in session:
        return redirect('/')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Insert transaction
    if request.method == 'POST':
        event_id = request.form['event_id']
        amount = request.form['amount']

        if event_id and amount:
            c.execute("INSERT INTO transactions (event_id, amount) VALUES (?, ?)",(event_id, amount))
            conn.commit()

    # Get all events for dropdown
    c.execute("SELECT * FROM events")
    events = c.fetchall()

    # Get all transactions
    c.execute("""
        SELECT transactions.id, events.name, transactions.amount
        FROM transactions
        JOIN events ON transactions.event_id = events.id
    """)
    all_transactions = c.fetchall()

    conn.close()

    return render_template("transactions.html",events=events,transactions=all_transactions)


@app.route('/reports')
def reports():
    if 'username' not in session:
        return redirect('/')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get all events
    c.execute("SELECT * FROM events")
    events = c.fetchall()

    # Get total revenue
    c.execute("SELECT SUM(amount) FROM transactions")
    total = c.fetchone()[0]

    if total is None:
        total = 0

    # Count transactions
    c.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = c.fetchone()[0]

    conn.close()

    return render_template("report.html",events=events,total=total,total_transactions=total_transactions)





@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------------- MAIN ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=False)

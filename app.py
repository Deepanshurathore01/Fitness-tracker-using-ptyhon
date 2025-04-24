from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Database connected successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT)')
    print("Table created successfully")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS fitness_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            steps INTEGER,
            distance REAL,
            calories REAL,
            heart_rate INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.close()

init_sqlite_db()

# Home Page
@app.route('/')
def home():
    logged_in = session.get('logged_in', False)
    username = session.get('user', '')
    return render_template('home.html', logged_in=logged_in, username=username)


# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
                con.commit()
                flash("Account created successfully!", "success")
                return redirect(url_for('login'))
        except Exception as e:
            con.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            con.close()

    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        con = sqlite3.connect('database.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()

        if user:
            session['logged_in'] = True
            session['user'] = user['username']
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password!", "danger")

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    username = session['user']

    # Fetch data from database
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("SELECT date('now') as date, steps, distance, calories, heart_rate FROM fitness_data")
    fitness_data = cur.fetchall()

    return render_template('dashboard.html', username=username, fitness_data=fitness_data)

@app.route('/submit', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        steps = request.form['steps']
        distance = request.form['distance']
        calories = request.form['calories']
        heart_rate = request.form['heart_rate']

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO fitness_data (steps, distance, calories, heart_rate) VALUES (?, ?, ?, ?)",
                (steps, distance, calories, heart_rate)
            )
            con.commit()

        # After saving, redirect back to home page
        return redirect(url_for('home'))

@app.route('/data')
def get_data():
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM fitness_data")
        rows = cur.fetchall()

        # Convert data to list of dictionaries
        data = []
        for row in rows:
            data.append({
                "id": row["id"],
                "steps": row["steps"],
                "distance": row["distance"],
                "calories": row["calories"],
                "heart_rate": row["heart_rate"],
                "date": row["date"]
            })

        return jsonify(data)


# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out!", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

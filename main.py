from types import MethodType
from flask import Flask, render_template, request, url_for, redirect, flash, session
import sqlite3
import os
app = Flask(__name__)
app.secret_key = 'asdfasdf'
def init_db():
  if not os.path.exists('data.db'):
      conn = sqlite3.connect('data.db')
      c = conn.cursor()
      c.execute('''
      CREATE TABLE users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          email TEXT NOT NULL,
          password TEXT NOT NULL,
          text TEXT
      )
      ''')
      conn.commit()
      conn.close()


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(
        """INSERT INTO users (
            email,
            password
        ) VALUES (?, ?)""",
        (email, password))
    conn.commit()
    conn.close()

    
    print(email + ' ' +password)



    
    return redirect(url_for('login'))
  return render_template('signup.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verbindung zur Datenbank
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE email = ? AND password = ?"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            # Speichern von Nutzerdaten in der Session
            session['email'] = email
            return redirect(url_for('home'))
        else:
            flash('Falsche E-Mail oder Passwort')
            return render_template('login.html')
    return render_template('login.html')


@app.route("/home")
def home():
    if 'email' in session:
        email = session['email']
        print(f"Email in Session gefunden: {email}")  # Debugging-Ausgabe
        return render_template('home.html', email=email)
    else:
        flash('Du bist nicht eingeloggt!')
        print("Keine Email in Session gefunden.")  # Debugging-Ausgabe
        return redirect(url_for('login'))




@app.route("/logout")
def logout():
    session.pop('email', None)  # Entfernt die E-Mail aus der Session
    flash('Erfolgreich ausgeloggt')
    return redirect(url_for('login'))

  

@app.route("/admin", methods=['POST', 'GET'])
def admin():
  if request.method == 'POST':
    password = request.form['password']
    if password == 'test':
      conn = sqlite3.connect('data.db')
      c = conn.cursor()
      c.execute("SELECT * FROM users")
      users = c.fetchall()
      conn.close()
      return render_template('admin_login.html', users=users)
    return render_template('admin.html')

  else:
    return render_template('admin.html')

if __name__ == "__main__":
    init_db()
    app.run(debug=False, port=8080, host='0.0.0.0')
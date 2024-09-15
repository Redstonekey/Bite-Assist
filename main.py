from flask import Flask, render_template, request, url_for, redirect, flash
import sqlite3
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'
def init_db():
  if not os.path.exists('data.db'):
      conn = sqlite3.connect('data.db')
      c = conn.cursor()
      c.execute('''
      CREATE TABLE users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          email TEXT NOT NULL,
          passwort TEXT NOT NULL,
          text TEXT NOT NULL
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

    try:
      conn = sqlite3.connect('data.db')
      c = conn.cursor()
      c.execute(
          """INSERT INTO users (
              email,
              password,
          ) VALUES (?, ?)""",
          (email, password))
      conn.commit()
      conn.close()
    except Exception as e:
      
      print(e)
      return render_template('signup.html')
    
    print(email + ' ' +password)



    
    return redirect(url_for('login'))
  return render_template('signup.html')

@app.route("/login")
def login():
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute("SELECT * FROM users")
  users = c.fetchall()
  conn.close()
  return render_template('login.html', users=users)


if __name__ == "__main__":
    init_db()
    app.run(debug=False, port=5000, host='0.0.0.0')
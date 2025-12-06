import os
from flask import Flask, request, jsonify, render_template_string
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'myappuser')
DB_PASS = os.getenv('DB_PASS', 'db_password')
DB_NAME = os.getenv('DB_NAME', 'myappdb')

# Simple login form template
login_form = """
<!doctype html>
<title>Login</title>
<h2>Login</h2>
<form method="post" action="/login">
  Username: <input type="text" name="username"><br><br>
  Password: <input type="password" name="password"><br><br>
  <input type="submit" value="Login">
</form>
{% if message %}
<p><strong>{{ message }}</strong></p>
{% endif %}
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(login_form)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return render_template_string(login_form, message="Login successful!")
        else:
            return render_template_string(login_form, message="Invalid credentials")
    except Exception as e:
        return render_template_string(login_form, message=f"Error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)


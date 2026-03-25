from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app=Flask(__name__)

# CREATE TABLE (PDF first block)
def init_db():
    conn = sqlite3.connect('user.db')
    conn.execute('CREATE TABLE IF NOT EXISTS user (name text, timestamp timestamp)')
    conn.close()

# HOME
@app.route("/", methods=["GET", "POST"])
def index():
	return(render_template("index.html"))

@app.route("/main", methods=["GET", "POST"])
def main():
	if request.method == "POST":
		username = request.form.get("username")
		if username:
			t = datetime.datetime.now()
			conn = sqlite3.connect('user.db')
			c = conn.cursor()
			c.execute('INSERT INTO user (name,timestamp) VALUES(?,?)',(username,t))
			conn.commit()
			c.close()
			conn.close()

	return(render_template("main.html"))

# TRANSFER PAGE
@app.route("/transferMoney", methods=["GET", "POST"])
def transferMoney():
	return(render_template("transferMoney.html"))

# DEPOSIT PAGE
@app.route("/depositMoney", methods=["GET", "POST"])
def depositMoney():
	return(render_template("depositMoney.html"))

# CHECK TABLE STRUCTURE (print description)
@app.route("/check")
def check():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('select * from user')
    desc = str(c.description)
    c.close()
    conn.close()
    return desc

# SELECT + PRINT USERS (PDF loop)
@app.route("/viewUsers")
def viewUsers():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('select * from user')
    r = ""
    for row in c:
        r += str(row) + "<br>"
    c.close()
    conn.close()
    return r

# DELETE USERS
@app.route("/deleteUsers")
def deleteUsers():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('DELETE FROM user')
    conn.commit()
    c.close()
    conn.close()
    return "All users deleted"

# MUST RUN ON IMPORT (Render + Gunicorn)
init_db()

if __name__ == "__main__":
	app.run()

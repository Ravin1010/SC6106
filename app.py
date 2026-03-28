from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app=Flask(__name__)

# CREATE TABLES
def init_db():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            wallet_address TEXT UNIQUE
        )
    ''')

    # Transactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            wallet_address TEXT,
            action TEXT,
            amount TEXT
        )
    ''')

    conn.commit()
    conn.close()

# HOME/INDEX
@app.route("/", methods=["GET", "POST"])
def index():
	return(render_template("index.html"))

# REGISTER OR LOGIN USER
@app.route("/registerLoginUser", methods=["POST"])
def registerLoginUser():
    data = request.json
    username = data.get("username")
    wallet = data.get("wallet")

    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    # Check if username exists
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user_by_name = c.fetchone()

    # Check if wallet exists
    c.execute('SELECT * FROM users WHERE wallet_address = ?', (wallet,))
    user_by_wallet = c.fetchone()

    # CASE 1: Both exist
    if user_by_name and user_by_wallet:
        if user_by_name[2] == wallet:
            conn.close()
            return jsonify({
                "status": "login",
                "message": "Welcome back"
            })
        else:
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Username or wallet already taken"
            })

    # CASE 2: One exists (conflict)
    elif user_by_name or user_by_wallet:
        conn.close()
        return jsonify({
            "status": "error",
            "message": "Username or wallet already taken"
        })

    # CASE 3: New user
    else:
        c.execute(
            'INSERT INTO users (username, wallet_address) VALUES (?, ?)',
            (username, wallet)
        )
        conn.commit()
        conn.close()

        return jsonify({
            "status": "register",
            "message": "New user registered"
        })

# MAIN
@app.route("/main", methods=["GET", "POST"])
def main():
	return(render_template("main.html"))

# TRANSFER MONEY PAGE
@app.route("/transferMoney", methods=["GET", "POST"])
def transferMoney():
	return(render_template("transferMoney.html"))

# DEPOSIT MONEY PAGE
@app.route("/depositMoney", methods=["GET", "POST"])
def depositMoney():
	return(render_template("depositMoney.html"))

# DATABASE FUNCTIONS PAGE
@app.route("/databaseFunctions", methods=["GET", "POST"])
def databaseFunctions():
	return(render_template("databaseFunctions.html"))

# VIEW USER
@app.route("/viewUser", methods=["POST"])
def viewUser():
    data = request.json
    username = data.get("username")

    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    c.execute('SELECT username, wallet_address FROM users WHERE username = ?', (username,))
    user = c.fetchone()

    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "username": user[0],
            "wallet": user[1]
        })
    else:
        return jsonify({
            "status": "error",
            "message": "User not found"
        })

# DELETE USER
@app.route("/deleteUser", methods=["POST"])
def deleteUser():
    data = request.json
    username = data.get("username")

    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()

    if not user:
        conn.close()
        return jsonify({
            "status": "error",
            "message": "User not found"
        })

    c.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "User deleted successfully"
    })

# VIEW TRANSACTIONS
@app.route("/viewTransactions", methods=["POST"])
def viewTransactions():
    data = request.json
    username = data.get("username")

    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    c.execute('SELECT action, amount FROM transactions WHERE username = ?', (username,))
    rows = c.fetchall()

    conn.close()

    transactions = []
    for row in rows:
        transactions.append({
            "action": row[0],
            "amount": row[1]
        })

    return jsonify({
        "status": "success",
        "transactions": transactions
    })

# LOG TRANSACTION
@app.route("/logTransaction", methods=["POST"])
def logTransaction():
    data = request.json

    username = data.get("username")
    wallet = data.get("wallet")
    action = data.get("action")
    amount = data.get("amount")

    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    c.execute(
        'INSERT INTO transactions (username, wallet_address, action, amount) VALUES (?, ?, ?, ?)',
        (username, wallet, action, amount)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Transaction logged"
    })

# MUST RUN ON IMPORT (Render + Gunicorn)
init_db()

if __name__ == "__main__":
	app.run()

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        acc_no TEXT PRIMARY KEY,
        name TEXT,
        pin TEXT,
        balance REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        acc_no TEXT,
        type TEXT,
        amount REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    acc_no = request.form["acc_no"]
    name = request.form["name"]
    pin = request.form["pin"]

    conn = sqlite3.connect("bank.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)",
                  (acc_no, name, pin, 0))
        conn.commit()
    except:
        conn.close()
        return "Account already exists!"

    conn.close()
    return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
    acc_no = request.form["acc_no"]
    pin = request.form["pin"]

    conn = sqlite3.connect("bank.db")
    c = conn.cursor()

    c.execute("SELECT * FROM accounts WHERE acc_no=? AND pin=?",
              (acc_no, pin))
    account = c.fetchone()

    conn.close()

    if account:
        session["acc_no"] = acc_no
        return redirect(url_for("dashboard"))
    else:
        return "Invalid Account Number or PIN"


@app.route("/dashboard")
def dashboard():

    if "acc_no" not in session:
        return redirect(url_for("home"))

    acc_no = session["acc_no"]

    conn = sqlite3.connect("bank.db")
    c = conn.cursor()

    c.execute("SELECT * FROM accounts WHERE acc_no=?", (acc_no,))
    account = c.fetchone()

    c.execute("""
        SELECT type, amount, date
        FROM transactions
        WHERE acc_no=?
        ORDER BY date DESC
    """, (acc_no,))
    history = c.fetchall()

    conn.close()

    return render_template("dashboard.html",
                           account=account,
                           history=history)


@app.route("/deposit", methods=["POST"])
def deposit():

    if "acc_no" not in session:
        return redirect(url_for("home"))

    acc_no = session["acc_no"]
    amount = float(request.form["amount"])

    conn = sqlite3.connect("bank.db")
    c = conn.cursor()

    c.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no=?",
              (amount, acc_no))

    c.execute("INSERT INTO transactions (acc_no, type, amount) VALUES (?, ?, ?)",
              (acc_no, "Deposit", amount))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


@app.route("/withdraw", methods=["POST"])
def withdraw():

    if "acc_no" not in session:
        return redirect(url_for("home"))

    acc_no = session["acc_no"]
    amount = float(request.form["amount"])

    conn = sqlite3.connect("bank.db")
    c = conn.cursor()

    c.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc_no,))
    balance = c.fetchone()[0]

    if balance >= amount:
        c.execute("UPDATE accounts SET balance = balance - ? WHERE acc_no=?",
                  (amount, acc_no))

        c.execute("INSERT INTO transactions (acc_no, type, amount) VALUES (?, ?, ?)",
                  (acc_no, "Withdraw", amount))

        conn.commit()

    conn.close()
    return redirect(url_for("dashboard"))


@app.route("/delete", methods=["POST"])
def delete():

    if "acc_no" not in session:
        return redirect(url_for("home"))

    acc_no = session["acc_no"]

    conn = sqlite3.connect("bank.db")
    c = conn.cursor()

    c.execute("DELETE FROM accounts WHERE acc_no=?", (acc_no,))
    c.execute("DELETE FROM transactions WHERE acc_no=?", (acc_no,))

    conn.commit()
    conn.close()

    session.clear()
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ---------------- CHATBOT ----------------

@app.route("/chat", methods=["POST"])
def chat():

    if "acc_no" not in session:
        return jsonify({"response": "Please login first."})

    user_message = request.form["message"].lower()
    acc_no = session["acc_no"]

    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc_no,))
    result = c.fetchone()
    conn.close()

    balance = result[0] if result else 0

    # RULE BASED RESPONSES
    # if "balance" in user_message:
    #     reply = f"Your current balance is ₹{balance}"

    # elif "deposit" in user_message:
    #     reply = "To deposit money, use the Deposit section above."

    # elif "withdraw" in user_message:
    #     reply = "To withdraw money, enter amount in Withdraw section."

    # elif "hello" in user_message:
    #     reply = "Hello! I am Smart Gullak Assistant 🤖"

    # elif "help" in user_message:
    #     reply = "You can ask about balance, deposit, withdraw, or account."

    # else:
    #     reply = "Sorry, I didn't understand that. Try asking about balance or deposit."

    # return jsonify({"response": reply})


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
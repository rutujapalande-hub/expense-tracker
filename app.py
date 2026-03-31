from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database connection
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount INTEGER,
    type TEXT
)
''')
conn.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = int(request.form['amount'])
        t_type = request.form['type']

        # Insert into DB
        cursor.execute("INSERT INTO transactions (amount, type) VALUES (?, ?)", (amount, t_type))
        conn.commit()

    # Fetch all data
    cursor.execute("SELECT amount, type FROM transactions")
    data = cursor.fetchall()

    transactions = [{"amount": row[0], "type": row[1]} for row in data]

    # Calculate totals
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")

    balance = total_income - total_expense

    return render_template('index.html',
                           transactions=transactions,
                           balance=balance)


if __name__ == '__main__':
    app.run(debug=True)

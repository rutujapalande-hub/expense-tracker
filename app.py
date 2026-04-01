from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# DB connection
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()

# Create table (with date + category)
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount INTEGER,
    type TEXT,
    category TEXT,
    date TEXT
)
''')
conn.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = request.form.get('amount')
        t_type = request.form.get('type')
        category = request.form.get('category')

        date = datetime.now().strftime("%d-%m-%Y %H:%M")

        if amount and t_type and category:
            cursor.execute(
                "INSERT INTO transactions (amount, type, category, date) VALUES (?, ?, ?, ?)",
                (amount, t_type, category, date)
            )
            conn.commit()

        return redirect('/')

    cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
    data = cursor.fetchall()

    transactions = []
    total_income = 0
    total_expense = 0

    for row in data:
        t = {
            "id": row[0],
            "amount": int(row[1]),
            "type": row[2].capitalize(),
            "category": row[3],
            "date": row[4]
        }
        transactions.append(t)

        if t["type"] == "Income":
            total_income += t["amount"]
        else:
            total_expense += t["amount"]

    balance = total_income - total_expense

    return render_template('index.html',
                           transactions=transactions,
                           balance=balance,
                           income=total_income,
                           expense=total_expense)


@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM transactions WHERE id=?", (id,))
    conn.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

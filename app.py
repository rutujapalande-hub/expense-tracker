from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DB setup
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()

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
        amount = request.form.get('amount')
        t_type = request.form.get('type')

        if amount and t_type:
            cursor.execute("INSERT INTO transactions (amount, type) VALUES (?, ?)", (amount, t_type))
            conn.commit()

        return redirect('/')   # IMPORTANT (refresh fix)

    # Fetch data
    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()

    transactions = []
    total_income = 0
    total_expense = 0

    for row in data:
        t = {"id": row[0], "amount": int(row[1]), "type": row[2]}
        transactions.append(t)

        if t["type"] == "income":
            total_income += t["amount"]
        else:
            total_expense += t["amount"]

    balance = total_income - total_expense

    return render_template('index.html',
                           transactions=transactions,
                           balance=balance,
                           income=total_income,
                           expense=total_expense)


# DELETE FEATURE (extra marks 🔥)
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM transactions WHERE id=?", (id,))
    conn.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

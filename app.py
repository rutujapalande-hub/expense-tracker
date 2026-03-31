from flask import Flask, render_template, request

app = Flask(__name__)

transactions = []

@app.route('/', methods=['GET', 'POST'])
def index():
    total = 0
    if request.method == 'POST':
        amount = int(request.form['amount'])
        t_type = request.form['type']
        transactions.append((amount, t_type))

    for amt, t in transactions:
        if t == 'income':
            total += amt
        else:
            total -= amt

    return render_template('index.html', total=total, data=transactions)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
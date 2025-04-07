from flask import Flask, render_template, request, redirect, url_for, session
import statistics

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input', methods=['POST'])
def input_values():
    choice = request.form['choice']
    count = int(request.form['count'])
    session['choice'] = choice
    session['count'] = count
    return render_template('input.html', choice=choice, count=count)

@app.route('/confirm', methods=['POST'])
def confirm_values():
    choice = session.get('choice')
    count = session.get('count')

    x_values = []
    y_values = []

    for i in range(count):
        if choice in ['x', 'both']:
            x_values.append(float(request.form.get(f'x{i}')))
        if choice in ['y', 'both']:
            y_values.append(float(request.form.get(f'y{i}')))

    session['x_values'] = x_values if x_values else None
    session['y_values'] = y_values if y_values else None

    return render_template('confirm.html', x_values=x_values, y_values=y_values, choice=choice)

@app.route('/result')
def result():
    choice = session.get('choice')
    x_values = session.get('x_values')
    y_values = session.get('y_values')

    table = []
    x_mean = statistics.mean(x_values) if x_values else None
    y_mean = statistics.mean(y_values) if y_values else None

    totals = {
        'xi': 0, 'x_dev': 0, 'x_dev2': 0,
        'yi': 0, 'y_dev': 0, 'y_dev2': 0,
        'xy_dev': 0
    }

    for i in range(len(x_values or y_values)):
        row = {}
        if x_values:
            xi = x_values[i]
            x_dev = xi - x_mean
            row['xi'] = xi
            row['x_dev'] = x_dev
            row['x_dev2'] = x_dev ** 2
            totals['xi'] += xi
            totals['x_dev'] += x_dev
            totals['x_dev2'] += x_dev ** 2

        if y_values:
            yi = y_values[i]
            y_dev = yi - y_mean
            row['yi'] = yi
            row['y_dev'] = y_dev
            row['y_dev2'] = y_dev ** 2
            totals['yi'] += yi
            totals['y_dev'] += y_dev
            totals['y_dev2'] += y_dev ** 2

        if x_values and y_values:
            xy_dev = (xi - x_mean) * (yi - y_mean)
            row['xy_dev'] = xy_dev
            totals['xy_dev'] += xy_dev

        table.append(row)

    return render_template(
        'result.html',
        table=table,
        choice=choice,
        x_mean=x_mean,
        y_mean=y_mean,
        totals=totals
    )

if __name__ == '__main__':
    app.run(debug=True)

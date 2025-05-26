from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta

app = Flask(__name__)

VOUCHER_FILE = 'data.json'

def load_vouchers():
    try:
        with open(VOUCHER_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_vouchers(vouchers):
    with open(VOUCHER_FILE, 'w') as f:
        json.dump(vouchers, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        code = request.form.get('voucher').strip()
        vouchers = load_vouchers()
        if code in vouchers:
            start_date = datetime.strptime(vouchers[code]['start'], '%Y-%m-%d')
            duration = vouchers[code]['days']
            end_date = start_date + timedelta(days=duration)
            today = datetime.today()
            remaining = (end_date - today).days
            if remaining < 0:
                message = f'Voucher expired on {end_date.strftime("%Y-%m-%d")}.'
            else:
                message = f'{remaining} day(s) remaining (until {end_date.strftime("%Y-%m-%d")})'
        else:
            message = 'Voucher not found.'
    return render_template('index.html', message=message)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        code = request.form['code'].strip()
        days = int(request.form['days'])
        start = request.form['start']
        vouchers = load_vouchers()
        vouchers[code] = {'start': start, 'days': days}
        save_vouchers(vouchers)
        return redirect(url_for('admin'))
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)

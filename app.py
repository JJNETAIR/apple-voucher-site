from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'

VOUCHER_FILE = 'data.json'
ADMIN_USER = 'admin'
ADMIN_PASS = 'pass123'

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        code = request.form['code'].strip()
        days = int(request.form['days'])
        start = request.form['start']
        vouchers = load_vouchers()
        vouchers[code] = {'start': start, 'days': days}
        save_vouchers(vouchers)
        return redirect(url_for('admin'))
    return render_template('admin.html')

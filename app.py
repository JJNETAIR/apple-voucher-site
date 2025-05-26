
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'supersecret'

VOUCHERS = {
    'ABC123': {'type': '15', 'start_date': '2024-05-20'},
    'XYZ789': {'type': '30', 'start_date': '2024-05-10'}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    code = request.form['code'].strip().upper()
    voucher = VOUCHERS.get(code)
    if voucher:
        start_date = datetime.strptime(voucher['start_date'], "%Y-%m-%d")
        duration = int(voucher['type'])
        end_date = start_date + timedelta(days=duration)
        remaining = (end_date - datetime.now()).days
        if remaining < 0:
            remaining = 0
        return render_template('index.html', result=True, code=code, remaining=remaining, end=end_date.strftime("%Y-%m-%d"))
    return render_template('index.html', error="Voucher not found")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'pass123':
            session['admin'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        code = request.form['code'].strip().upper()
        start_date = request.form['start_date']
        duration = request.form['duration']
        VOUCHERS[code] = {'type': duration, 'start_date': start_date}
    return render_template('admin.html', vouchers=VOUCHERS)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

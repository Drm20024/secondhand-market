from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# دیتابیس ساده برای ذخیره کاربران و کالاها
users = {}
items = []

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', items=items, username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return "نام کاربری یا رمز عبور اشتباه است"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        item_price = request.form['item_price']
        items.append({
            'name': item_name,
            'description': item_description,
            'price': item_price,
            'seller': session['username']
        })
        return redirect(url_for('home'))
    return render_template('add_item.html')

@socketio.on('message')
def handleMessage(msg):
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

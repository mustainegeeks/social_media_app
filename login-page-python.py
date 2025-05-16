from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import os
from datetime import timedelta

app = Flask(__name__)
# In a real application, use a strong random secret key from environment variables
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=7)
bcrypt = Bcrypt(app)

# This is a simple in-memory database for demonstration
# In a real application, you would use a proper database like SQLite, PostgreSQL, or MongoDB
users_db = {}

@app.route('/')
def home():
    if 'username' in session:
        return f'''
        <h1>Welcome to SocialConnect, {session['username']}!</h1>
        <p>You are logged in.</p>
        <a href="/logout">Logout</a>
        '''
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db:
            if bcrypt.check_password_hash(users_db[username]['password'], password):
                session.permanent = True
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if username in users_db:
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        # Hash password before storing
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Store user in our simple database
        users_db[username] = {
            'password': hashed_password,
            'email': email
        }
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Create templates directory and HTML files
if not os.path.exists('templates'):
    os.makedirs('templates')

# Create login.html
with open('templates/login.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SocialConnect - Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            width: 350px;
        }
        h1 {
            text-align: center;
            color: #1877f2;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #dddfe2;
            border-radius: 5px;
            box-sizing: border-box;
            font-size: 16px;
        }
        button {
            background-color: #1877f2;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            font-size: 16px;
            width: 100%;
            cursor: pointer;
            margin-bottom: 10px;
        }
        button:hover {
            background-color: #166fe5;
        }
        .register-link {
            text-align: center;
            margin-top: 15px;
        }
        .flash-messages {
            margin-bottom: 15px;
        }
        .flash-message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .flash-message.error {
            background-color: #ffebee;
            color: #c62828;
        }
        .flash-message.success {
            background-color: #e8f5e9;
            color: #2e7d32;
        }
        .flash-message.info {
            background-color: #e3f2fd;
            color: #1565c0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SocialConnect</h1>
        
        {% if get_flashed_messages() %}
        <div class="flash-messages">
            {% for category, message in get_flashed_messages(with_categories=true) %}
                <div class="flash-message {{ category }}">{{ message }}</div>
            {% endfor %}
        </div>
        {% endif %}
        
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        
        <div class="register-link">
            Don't have an account? <a href="/register">Register here</a>
        </div>
    </div>
</body>
</html>
    ''')

# Create register.html
with open('templates/register.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SocialConnect - Register</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            width: 350px;
        }
        h1 {
            text-align: center;
            color: #1877f2;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"],
        input[type="password"],
        input[type="email"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #dddfe2;
            border-radius: 5px;
            box-sizing: border-box;
            font-size: 16px;
        }
        button {
            background-color: #42b72a;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            font-size: 16px;
            width: 100%;
            cursor: pointer;
            margin-bottom: 10px;
        }
        button:hover {
            background-color: #36a420;
        }
        .login-link {
            text-align: center;
            margin-top: 15px;
        }
        .flash-messages {
            margin-bottom: 15px;
        }
        .flash-message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .flash-message.error {
            background-color: #ffebee;
            color: #c62828;
        }
        .flash-message.success {
            background-color: #e8f5e9;
            color: #2e7d32;
        }
        .flash-message.info {
            background-color: #e3f2fd;
            color: #1565c0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Create Account</h1>
        
        {% if get_flashed_messages() %}
        <div class="flash-messages">
            {% for category, message in get_flashed_messages(with_categories=true) %}
                <div class="flash-message {{ category }}">{{ message }}</div>
            {% endfor %}
        </div>
        {% endif %}
        
        <form method="POST" action="/register">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Register</button>
        </form>
        
        <div class="login-link">
            Already have an account? <a href="/login">Login here</a>
        </div>
    </div>
</body>
</html>
    ''')

if __name__ == '__main__':
    # In a production environment, do not use debug=True
    app.run(debug=True)

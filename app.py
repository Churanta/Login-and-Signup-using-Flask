# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

# Home page
@app.route('/')
def home():
    return render_template('home.html')


# User signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        photo = request.files['photo']
        mobile_number = request.form['mobile_number']

        # Check if passwords match
        if password != confirm_password:
            return jsonify({'message': 'Passwords do not match'})

        # Save user photo to a designated folder and get the file path
        photo_path = 'photos/' + photo.filename
        photo.save(photo_path)

        # Insert user data into the database
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password, photo, mobile_number) VALUES (%s, %s, %s, %s, %s)",
            (username, email, password, photo_path, mobile_number))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email and password match in the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # Set session variables or perform any desired action for successful login
            return redirect(url_for('home'))
        else:
            return jsonify({'message': 'Invalid email or password'})

    return render_template('login.html')



# Admin login
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if admin email and password match
        if email == 'admin@gmail.com' and password == 'admin':
            # Set session variables or perform any desired action for successful admin login
            return redirect(url_for('admin_dashboard'))
        else:
            return jsonify({'message': 'Invalid email or password'})

    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    # Fetch all user details from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()

    # Convert fetched tuples to dictionaries
    users_dict = []
    for user in users:
        user_dict = {
            'id': user[0],
            'username': user[1],
            'photo': user[4],
            'mobile_number': user[5]
        }
        users_dict.append(user_dict)

    return render_template('admin_dashboard.html', users=users_dict)



# Logout
@app.route('/logout')
def logout():
    # Perform logout actions, such as clearing session variables
    # Redirect to the login page or any other desired page
    return redirect(url_for('login'))


# Run the application
if __name__ == '__main__':
    app.run()

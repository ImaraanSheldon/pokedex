from flask import Flask, request, jsonify, redirect, url_for, render_template, flash,session, request
import mysql.connector
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


print("mysql.connector imported successfully!")
app = Flask(__name__)

app.config['SECRET_KEY'] = 'a19d95e9ced1189ab6263130317dd962'

# database config
def get_db_connection():
    return mysql.connector.connect(
        user = 'u4obdnrv7pxpyo8q',
        password = 'tQshayXuxd5zxZcOtfcm',
        host = 'b93jnnaq9y3ti1rnvjgc-mysql.services.clever-cloud.com',  # e.g., b1n2o3f4.clever-cloud.com
        database = 'b93jnnaq9y3ti1rnvjgc'
    )
    
@app.route('/pokeData')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Set dictionary=True to return rows as dictionaries
    cursor.execute('SELECT * FROM pokemon')
    pokemon = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pokeData.html', pokemon = pokemon)

@app.route("/")
def landing():
    return render_template("index.html")


@app.route("/home/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Set dictionary=True to return rows as dictionaries
    cursor.execute('SELECT * FROM pokemon')
    pokemon = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("home.html", pokemon = pokemon)
    
@app.route("/new.html/")
def new():
    return render_template("new.html")

@app.route('/signUp/', methods=['GET', 'POST'])
def signUp():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute('INSERT INTO users (user_name, email, password) VALUES (%s, %s, %s)', 
                       (form.username.data, form.email.data, hashed_password))

        # Commit the transaction
        conn.commit()
        
        # Close the connection
        cursor.close()
        conn.close()

        # Flash success message and redirect to home or login page
        flash('Account created successfully!', 'success')
        return redirect(url_for('home')) # Or 'login' if you want to redirect to login page after signup
    
    return render_template('signUp.html', title='Sign Up', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Make sure to fetch rows as dictionaries
        
        # Query the database to get the user by email
        cursor.execute('SELECT * FROM users WHERE email = %s', (form.email.data,))
        user = cursor.fetchone()  # Fetch the user

        if user and check_password_hash(user['password'], form.password.data):
            # If the password matches, store user info in the session
            session['user_id'] = user['user_id']
            session['user_name'] = user['user_name']
            session['email'] = user['email']
            flash(f'Welcome {user["user_name"]}!', 'success')
            return redirect(url_for('profile'))  # Or redirect to a user profile page

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

        cursor.close()
        conn.close()

    return render_template('login.html', title='Login', form=form)

@app.route('/logout/')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/profile/')
def profile():
    if 'user_id' not in session:
        flash('You must be logged in to view your profile', 'danger')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    # Fetch user details from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('profile.html', user=user)  # Pass the user to the template

@app.route('/update_profile/', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        flash('You must be logged in to update your profile', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    new_user_name = request.form['user_name']
    new_email = request.form['email']

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the user's information in the database
    cursor.execute('UPDATE users SET user_name = %s, email = %s WHERE user_id = %s',
                   (new_user_name, new_email, user_id))
    conn.commit()

    cursor.close()
    conn.close()

    flash('Your profile has been updated', 'success')
    return redirect(url_for('profile'))

@app.route('/delete_account/', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        flash('You must be logged in to delete your account', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    entered_password = request.form['password']

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the user's hashed password from the database
    cursor.execute('SELECT password FROM users WHERE user_id = %s', (user_id,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password'], entered_password):
        # If the password matches, delete the account
        cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        # Clear the session and show success message
        session.pop('user_id', None)
        session.pop('user_email', None)
        flash('Your account has been deleted', 'success')

        return redirect(url_for('home'))
    else:
        flash('Password is incorrect. Account deletion failed.', 'danger')
        cursor.close()
        conn.close()
        return redirect(url_for('profile'))
    

@app.route('/pokemon/<name>')
def pokemon(name):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch Pokémon data
    cursor.execute('SELECT * FROM pokemon WHERE name = %s', (name,))
    pokemon = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    # Check if Pokémon exists
    if not pokemon:
        return "Pokémon not found", 404
    
    return render_template('singular.html', pokemon=pokemon)


if __name__ == "__main__":
    app.run(debug = True)
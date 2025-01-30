from flask import Flask, request, jsonify, redirect, url_for, render_template
import mysql.connector


print("mysql.connector imported successfully!")


app = Flask(__name__)

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

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")


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

if __name__ == "__main__":
    app.run(debug = True)
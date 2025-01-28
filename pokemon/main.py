from flask import Flask, request, jsonify, redirect, url_for, render_template
import mysql.connector


print("mysql.connector imported successfully!")


app = Flask(__name__)

# database config
db_config = {
    'user': 'u4obdnrv7pxpyo8q',
    'password': 'tQshayXuxd5zxZcOtfcm',
    'host': 'b93jnnaq9y3ti1rnvjgc-mysql.services.clever-cloud.com',  # e.g., b1n2o3f4.clever-cloud.com
    'database': 'b93jnnaq9y3ti1rnvjgc',
    'port': '3306'
}

# Establish a database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route("/")
def landing():
    return render_template("index.html")


@app.route("/home.html/")
def home():
    return render_template("home.html")
    
@app.route("/new.html/")
def new():
    return render_template("new.html")

if __name__ == "__main__":
    app.run(debug = True)
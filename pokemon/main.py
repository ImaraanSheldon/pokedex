from flask import Flask, request, jsonify, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("index.html")

@app.route("/home.html/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug = True)
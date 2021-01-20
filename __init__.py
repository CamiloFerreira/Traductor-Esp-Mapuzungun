from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/Diccionario")
def dic():
	return render_template("dic.html")




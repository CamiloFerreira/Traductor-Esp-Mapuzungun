from flask import Flask, render_template,request,json
from traductor import Traducir


app = Flask(__name__)



@app.route("/")
def index():
	return render_template("index.html")


@app.route("/Diccionario")
def dic():
	return render_template("dic.html")

@app.route("/gText",methods=["POST"])

def gText():
	data = request.get_json()

	cadena = data['cadena']

	trad = Traducir(cadena,datos)
	return json.dumps({'status':'ok','t':trad})


if __name__ == "__main__":
	with open('json/dic.json') as file:
		#Carga el archivo json
		datos = json.load(file)

	app.run()

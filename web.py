from flask import Flask, render_template,request,json
from traductor import Traducir


app = Flask(__name__)



@app.route("/")
def index():
	return render_template("index.html")


@app.route("/Diccionario")
def dic():
	aLetras=[
		 'a','b','c','d','e','f','g','h','i','j',
		 'k','l','m','n','ñ','o','p','q','r','s',
		 't','u','v','w','x','y','z'
		 ]
	return render_template("dic.html",letras=aLetras,dic=datos)

@app.route("/gText",methods=["POST"])
def gText():
	data = request.get_json()

	cadena = data['cadena']

	trad = Traducir(cadena,datos)
	return json.dumps({'status':'ok','t':trad})

@app.route("/gDic",methods=["POST"])
def gDic():
	return json.dumps(datos)


if __name__ == "__main__":
	with open('json/dic.json') as file:
		#Carga el archivo json
		datos = json.load(file)

	app.run()

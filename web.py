# -*- coding: utf-8 -*-

from flask import Flask, render_template,request,json , jsonify
from traductor import Traducir
import json



app = Flask(__name__)


with open('json/dic_final.json') as file:
	#Carga el archivo json
	datos = json.load(file)
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
	trad = Traducir(cadena)
	return json.dumps({'status':'ok','t':trad})

@app.route("/gDic",methods=["POST"])
def gDic():
	return json.dumps(datos)

#Ruta que retorna el diccionario que actualmente se tiene
@app.route("/gDic2")
def getDic2():
	return jsonify(datos)

#Ruta que retorna las traducciones
@app.route("/gTrad",methods=["POST"])
def gTrad():
        data=request.get_json()
        object = json.loads(data)
        cadena = object['cadena']
        #cadena=data['cadena']
        t = Traducir(cadena)
        return jsonify({"traduccion": t})


if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0",port=5000)

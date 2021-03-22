# -*- coding: utf-8 -*-

from flask import Flask, render_template,request,json , jsonify
from traductor2 import Traducir
import json
import os



app = Flask(__name__)


with open(os.getcwd()+'/json/dic.json') as file:
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
	trad = Traducir(cadena,datos)
	return json.dumps({'status':'ok','t':trad})

@app.route("/gDic",methods=["POST"])
def gDic():
	return json.dumps(datos)



#Ruta que retorna el diccionario que actualmente se tiene
@app.route("/gDic2")
def getDic2():
	ListaPal = []
	i = 0 #Indice de la lista Lista pal 
	for letras in datos['Palabras']:
		#Se agrega los datos a listaPal 
		ListaPal.append({"letra":letras})
		aLetras = datos['Palabras'][letras]
		aPal = []
		for pal in aLetras:
			palabra     = pal[0]
			significado = pal[1] 
			aPal.append({"palabra":palabra,"significado":significado})
		ListaPal[i]['palabras'] = aPal
		aPal = []
		i +=1

	return jsonify(ListaPal)

#Ruta que retorna las traducciones
@app.route("/gTrad",methods=["POST"])
def gTrad():
        data=request.get_json()
        object = json.loads(data)
        cadena = object['cadena']
        #cadena=data['cadena']
        t = Traducir(cadena)
        return jsonify({"traduccion": t})

#Ruta que retorna json pero solo una key 
@app.route("/gSel/<string:letra>")
def gSel(letra):
	temp = datos['Palabras'][letra]
	dic =[]
	for i in range(len(temp)):
		dic.append({'Palabra':temp[i][0],"Significados":temp[i][1]})
	return jsonify(dic)	


if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0",port=5000)

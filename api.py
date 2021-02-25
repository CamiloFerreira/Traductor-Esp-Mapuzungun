from flask import Flask, render_template,request,json , jsonify
from traductor import Traducir
import json


#Se carga el json con el diccionario 
with open('json/dic.json') as file:
	#Carga el archivo json
	datos = json.load(file)


app = Flask(__name__)

#Ruta que retorna el diccionario que actualmente se tiene
@app.route("/gDic")
def getDic():
	return jsonify(datos['Palabras'])
#Ruta que retorna las traducciones 
@app.route("/gTrad/<string:text>")
def gTrad(text):
	t = Traducir(text, datos)
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
	app.run(debug=True,host="192.168.1.116",port=8080)



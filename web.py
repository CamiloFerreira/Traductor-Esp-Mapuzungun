# -*- coding: utf-8 -*-

from flask import Flask, render_template,request,json , jsonify
from traductor import Traducir
import json
import logging


app = Flask(__name__)

logging.basicConfig(filename='../logs/record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

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
	app.logger.info('palabra:'+cadena)
	app.logger.info('traduccion:'+trad)
	return json.dumps({'status':'ok','t':trad})

@app.route("/gDic",methods=["POST"])
def gDic():
	return json.dumps(datos)

#Ruta que retorna el diccionario que actualmente se tiene
@app.route("/gDic2",methods=["GET"])
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
        app.logger.info('palabra:'+cadena)
        app.logger.info('traduccion:'+t)
        return jsonify({"traduccion": t})


if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0",port=5000)
	


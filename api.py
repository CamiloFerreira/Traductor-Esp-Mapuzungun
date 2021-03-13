from flask import Flask, render_template,request,json , jsonify
from traductor import Traducir
import json



#Se carga el json con el diccionario 
with open('json/dic.json') as file:
	#Carga el archivo json
	datos = json.load(file)


app = Flask(__name__)

@app.route("/gDic")
def getDic():
        dic={}
        for letras in datos['Palabras']:
                dic[letras] = []
                aLetras = datos['Palabras'][letras]
                aPal = []
                for pal in aLetras:
                        palabra     = pal[0]
                        significado = pal[1] 
                        aPal.append({"palabra":palabra,"significado":significado})
                dic[letras] = aPal
                aPal = []
        return jsonify(dic)


#Ruta que retorna el diccionario que actualmente se tiene
@app.route("/gDic2")
def getDic():
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
	app.run(debug=False,host="192.168.1.254",port=5000)



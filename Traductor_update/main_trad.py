from function_trad import *
import spacy 
import json


#Se carga el nlp
nlp = spacy.load("es_core_news_lg")


#Se establecen los pronombres principales 
aPronombres=[
				#Pronombres singular
				{"palabra":"iñche","trad":"yo","tipo":"singular"},
				{"palabra":"eymi","trad":"tu","tipo":"singular"},
				{"palabra":"eymi","trad":"usted","tipo":"singular"},
				{"palabra":"fey","trad":"ella","tipo":"singular"},
				#Pronombres dual
				{"palabra":"iñchiw","trad":"nosotros dos","tipo":"dual"},
				{"palabra":"eymu","trad":"ustedes dos","tipo":"dual"},
				{"palabra":"feyegu","trad":"ellos dos","tipo":"dual"},
				#Pronombres plural
				{"palabra":"iñchiñ","trad":"nosotros","tipo":"plural"},
				{"palabra":"eymun","trad":"ustedes","tipo":"plural"},
				{"palabra":"feyegun","trad":"ellos","tipo":"plural"},
				{"palabra":"feyegun","trad":"ellas","tipo":"plural"}
			]

#Se carga el diccionario 

directorio= '../json/dic_final.json'

with open(directorio) as file:
	#Carga el archivo json
	datos = json.load(file)



cad_inicial = "Yo hablo bien"
cad_final   = ""
nlp = nlp(cad_inicial)

for token in nlp:
	
	text = token.text # Obtiene la palabra
	pos  = token.pos_ # Obtiene si es pronombre , verbo etc
	#Si detecta que el token es un pronombre
	#lo reemplaza por los que estan en el diccionario
	if(pos == "PRON"):
		pal = SearchPRON(aPronombres,text)
		cad_final += pal

	#Si detecta que el token es un verbo
	#Busca el token en el diccionario
	elif(pos == "VERB"):
		SearchToken(datos,text)

	else:
		cad_final += " "+text

print (cad_final)



import es_core_news_sm
import json 

def BuscarTraduccion(buscar):
	#Abre el archivo json
	with open('json/dic2.json') as file:
		
		#Carga el archivo json
		data = json.load(file)
		
		aPal = [] #Lista con las palabras

		for l in data['Palabras']:
			
			#Recorre el json de manera alfabetica
			lista = data['Palabras'][l]


			for pal in lista : 
				palabra = pal[0]
				significados = pal[1]

				for s in significados : 
					if(buscar.lower() == s.lower()):
						aPal.append(palabra)

		return aPal
			#print(lista)

#nlp = es_core_news_sm.load()
#doc = nlp("yo quiero caminar , pero no puedo")
#print([(w.text, w.pos_) for w in doc]
correr = True
while (correr):

	nlp = es_core_news_sm.load()
	text = input("Ingresa oracion : ")
	buscar = nlp(text)


	t = " "
	for w in buscar:
		print (w.text)
		if(BuscarTraduccion(w.text) != None):
			print(BuscarTraduccion(w.text))
		else : 
			print (w.text + ", No existe ! ")
	#print("Traduccion : ",t)

	#print(BuscarTraduccion(buscar))

	if(text == "fin"):
		correr = False
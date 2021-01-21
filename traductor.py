import es_core_news_sm
import json 

def BuscarTraduccion(buscar):
	#Abre el archivo json
	with open('json/dic.json') as file:
		
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

def Traducir(text):
	nlp = es_core_news_sm.load()
	buscar = nlp(text)
	t = " "
	for w in buscar:
		trad = BuscarTraduccion(w.text)
		if ( len(trad) > 0 ):
			t +=trad[0] + " "
		else:
			t += w.text + " " 
	return t 


print(Traducir("Esto es un poco de todo ! "))
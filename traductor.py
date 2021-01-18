import es_core_news_sm
import json 

def BuscarTraduccion(buscar):



	#Abre el archivo json
	with open('json/dic.json') as file:
		
		#Carga el archivo json
		data = json.load(file)
		

		for letra in data['Palabras']:
			
			#Recorre el json de manera alfabetica
			for pal in data['Palabras'][letra]:
				palabra = pal[0] #Se guarda la palabra 
				significado = pal[1][1:] # Se guarda su significado

				if (significado.find(",") > 0):
					sig = significado.split(",")
					#print(sig)
					#print(sig)				
					for s in sig:
						#print(sig)
						if(s.strip().lower() == buscar.lower()):
							#print(sig)
							return palabra
				else:
					#print(significado)
					if(significado.lower() == buscar.lower()):
						return palabra
						

#nlp = es_core_news_sm.load()
#doc = nlp("yo quiero caminar , pero no puedo")
#print([(w.text, w.pos_) for w in doc])

correr = True
while (correr):

	nlp = es_core_news_sm.load()
	text = input("Ingresa oracion : ")
	buscar = nlp(text)


	t = " "
	for w in buscar:
		print (w.text)
		if(BuscarTraduccion(w.text) != None):
			t += BuscarTraduccion(w.text)+" "
		else : 
			print (w.text + ", No existe ! ")
	print("Traduccion : ",t)

	#print(BuscarTraduccion(buscar))

	if(text == "fin"):
		correr = False
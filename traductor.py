#import es_core_news_sm
#nlp = es_core_news_sm.load()
#doc = nlp("El kenai traga pico")
#print([(w.text, w.pos_) for w in doc])


import json 


run = True
while(run):

	with open('json/dic.json') as file:
		data = json.load(file)

		buscar  = input("Ingresa una palabra: ")

		for letra in data['Palabras']:
			for pal in data['Palabras'][letra]:
				palabra = pal[0]
				significado = pal[1][1:]

				if (significado.find(",") > 1):
					sig = significado.split(",")
					
					for s in sig:
						if(s.strip().lower() == buscar.lower()):
							print(palabra)


				else:
					#print(significado)
					if(significado.lower() == buscar.lower()):
						print("Traduccion : ",palabra)

		if(buscar == "fin"):
			run = False
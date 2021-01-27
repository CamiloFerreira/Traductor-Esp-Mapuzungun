import es_core_news_sm
import json 


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ü","u")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def BuscarTraduccion(buscar,data):
	#Abre el archivo json
	aPal = [] #Lista con las palabras

	for l in data['Palabras']:
		#Recorre el json de manera alfabetica
		lista = data['Palabras'][l]
		for pal in lista : 
			palabra = pal[0]
			significados = pal[1]
			for s in significados : 
				if (s == buscar):
					aPal.append(palabra.strip())


			#Si son los pronombres los saca directos 
	if(buscar == "yo"):
		aPal = [aPal[0].split(",")[0]]
	return aPal
			#print(lista)

def Traducir(text,data):
	nlp = es_core_news_sm.load()
	buscar = nlp(text)
	variantes = []
	t = " "
	for w in buscar:
		n = normalize(w.text)
		trad = BuscarTraduccion(n,data)

		#Si existe solo una traduccion
		
		if( len(trad) == 1 or len(trad) == 0 ):
			
			#si no existe traduccion guarda la palabra original
			if(len(trad) == 0 ):
				t += w.text + " "
			else:
				t += trad[0] + " " 

		#Si existe mas de una 
		elif(len(trad) > 1 ):
			t += trad[0] + " " 
	return t.strip()


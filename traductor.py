import es_core_news_sm
import json 


#Cuando se inicie el script cargue el archivo json
if __name__ == '__main__':
	with open('json/dic.json') as file:
		#Carga el archivo json
		data = json.load(file)


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


def BuscarTraduccion(buscar):
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
						print("Son iguales")
		return aPal
			#print(lista)

def Traducir(text):
	nlp = es_core_news_sm.load()
	buscar = nlp(text)
	t = " "
	for w in buscar:
		n = normalize(w.text)
		trad = BuscarTraduccion(n)
		if ( len(trad) > 0 ):
			t +=trad[0] + " "
			print(trad)
		else:
			t += w.text + " " 
	return t 




print(Traducir("marido"))
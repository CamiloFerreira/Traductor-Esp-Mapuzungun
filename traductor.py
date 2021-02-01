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
	existe = False
	palExiste = False
	for l in data['Palabras']:
		#Recorre el json de manera alfabetica
		lista = data['Palabras'][l]
		for pal in lista : 
			palabra = pal[0]
			significados = pal[1]
			for s in significados : 
				#busca similitud de palabras
				if (s == buscar):
					aPal.append(palabra.strip())
					existe = True
					palExiste = True # Si existe la palabra

			#Si son los pronombres los saca directos 
	if(buscar == "yo"):
		aPal = [aPal[0].split(",")[0]]

	if(palExiste):
		return [aPal,existe]
	else:
		return [buscar,existe]	
		#print(lista)



def Traducir(text,data):

	print(text)
	#Primero realiza la busqueda con la oracion completa 
	trad_p = BuscarTraduccion(text,data)
	isAnswer = text.find("?") > 0 # Si es true , es porque es una pregunta
	isPron = False
	if(trad_p[1]):
		return trad_p[0]
	else:
		nlp = es_core_news_sm.load()
		buscar = nlp(text)
		variantes = []
		t = " "

		#Si es pregunta primero muestra el sujeto
		if(isAnswer):

			t = []
			for w in buscar:
				n = normalize(w.text)
				trad = BuscarTraduccion(n,data)[0]

				if(w.pos_ == "PRON"):
					isPron = True

				if(len(trad) == 1 ):
					#si existe pronombre lo mueve al principio
					if(isPron):
						t2 = []
						t2.append(trad[0])
						t2.append(" ")
						t = t2 + t
					else:
						t.append(trad[0])
						t.append(" ")
				else:
					if(len(trad) > 1):
						#si existe pronombre lo mueve al principio
						if(isPron):
							t2 = []
							t2.append(trad[0])
							t2.append(" ")
							t = t2 + t
							print(t)
						else:
							t.append(trad[0])
							t.append(" ")

				#Si detecta que es un pronombre
			t.append("?")
			
			cad = " "

			for c in t : 
				cad += c 

			return cad

		#Si no es pregunta
		else:
			pass


with open('json/dic.json','r') as file:
	data = json.load(file)


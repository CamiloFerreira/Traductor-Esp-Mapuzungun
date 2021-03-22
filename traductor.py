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
	buscar = normalize(buscar).lower()
	aPal = [] #Lista con las palabras
	palExiste = False
	for l in data['Palabras']:
		#Recorre el json de manera alfabetica
		lista = data['Palabras'][l]
		for pal in lista : 
			palabra = pal[0]
			significados = pal[1]
			for s in significados :
				s = normalize(s).lower() 
				#busca similitud de palabras
				if (s == buscar):
					aPal.append(palabra.strip().lower())
					palExiste = True # Si existe la palabra

			#Si son los pronombres los saca directos 
	if(buscar == "yo"):
		aPal = [aPal[0].split(",")[0]]

	if(palExiste):
		return [aPal,palExiste]
	else:
		return [None,palExiste]		

def BuscarxToken(buscar,data):
	nlp = es_core_news_sm.load()
	w = nlp(buscar) # convierte palabra en tokens
	t = " " 
	for token in w :
		text = token.text # guarda la palabra
		type = token.pos_ # establece el tipo de palabra 

		trad = BuscarTraduccion(text,data)[0] #Obtiene la traduccion

		#Si no existe traduccion 
		if(trad == None):
			t += text + " "
		#Si existe traduccion
		else:
			 #Si posee solo una traduccion osea una sola posicion el arreglo
			 if(len(trad) == 1):
			 	t += trad[0] + " "
			 else :
			 	t += trad[0] + " " 
	return t

def esPregunta(buscar,data):
	bToken = False
	#Primero busca la palabra completa 
	#si tiene "¿" al comienzo busca normal
	if(buscar.find("¿") >= 0):
		pal = BuscarTraduccion(buscar,data)[0]
		if(pal != None):
			return pal[0] + "?"
		else:
			bToken = True 
	else:
		ant = ""
		cad = ""
		for i in buscar:
			#Esta parte quita el posible espacio que existe entre la palabra y el signo
			if ( ant == " " and i == "?"):
				cad = cad[:len(cad)-1]
				cad +="?" 
			else:
				cad +=i
			ant = i 
		buscar = cad
		pal = BuscarTraduccion(buscar,data)[0]
		if(pal != None):
			return pal[0] + "?"
		else:
			bToken = True 
	if(bToken):
		return BuscarxToken(buscar,data)

def Traducir(text,data):
	#Primero realiza la busqueda con la oracion completa 
	trad_p = BuscarTraduccion(text,data)
	isAnswer = text.find("?") > 0 # Si es true , es porque es una pregunta
	
	if(trad_p[1]):
		if(isAnswer):
			return trad_p[0][0] +"?"
		else:
			return trad_p[0][0]
	else:
		t = " " # variable que contendra la traduccion
		#Primero pregunta si existe separacion por ","
		if(text.find(",") > 0):
			Ctext = text.split(",") # separa el texto por las comas
			#Recorre la lista del texto separado por comas
			for pal in Ctext:
				#Primero pregunta si la palabra es una pregunta 
				if(isAnswer):
					t += esPregunta(pal.strip(),data) + ","
				else :
					#Realiza primero la busqueda con la palabra sin operar con tokens
					tr = BuscarTraduccion(pal.strip(),data)
					if(tr[0] != None):
						aPal = list(set(tr[0])) # obtiene la lista de palabras y quita si existen palabras repetidas
						#Pregunta si tiene mas de un signficado
						if(len(aPal) == 1 ):
							t += aPal[0].strip() + "," 
						else:
							#print("TIene mas de uno")
							#print(aPal)
							t += aPal[0].strip() + "," 
					#Si no encuentra traduccion suma la palabra a la cadena
					else:
						#Si es la palabra que se encuentra al final de la lista no se agrega coma
						
						if(Ctext.index(pal) == len(Ctext)-1):
							t += BuscarxToken(pal.strip(),data)
						else :
							t += BuscarxToken(pal.strip(),data) + "," 
		#Si no existe separacion por "," continua con la busqueda
		else:
			#Pregunta si es una pregunta 
			if(isAnswer):
				t += esPregunta(text,data)				
			else:
				t += BuscarxToken(text,data)


	

	return t.strip()




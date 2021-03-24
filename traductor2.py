import es_core_news_sm as es_core
import json 

#----------------------------------
#Variables globales 
#---------------------------------

#Carga el archivo json con el diccionario
with open('json/dic2.json') as file:
	datos = json.load(file)

nlp = es_core.load()

aPalabras = [] # Lista que contiene el arreglo con las palabras 
for jsonObject in datos:
	aPalabras += jsonObject['palabras']

#------------------------------------
#------------------------------------



def normalize(s):
	"""
		Funcion que quita los ascentos y otros signos extraños 
		que contiene las palabras para retornar una vocal limpia y sin 
		caracteres extras 

		parametro_1 : s

		palabra a normalizar ejemplo "estás"
	""" 
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


def BuscarToken(token):
	'''
		Funcion que busca la palabra por token 
		ejemplo se ingresa la palabra "Hola " busca esa palabra en el diccionario
		y retorna "Foche"

		parametro_1 : token

		esta contiene la palabra a ingresar ejemplo "hola" , "como ", "te","llamas","?"

		parametro_2 : aPalabras

		arreglo que contiene el diccionario obtenido del json
	'''
	token = normalize(token.lower().strip())
	buscar = True
	i = 0 ; # indice de aPalabras
	i_sig = 0 ; # indice para buscar el el array de los significados

	tmpPal = "No existe";
	while buscar:
		pal = aPalabras[i]['palabra']
		sig = aPalabras[i]['significado'] # Array con significados
		palabra = normalize(sig[i_sig].lower().strip())

		if(palabra== token):
			tmpPal = pal
			buscar = False	 
		if(i_sig < len(sig)-1):
			i_sig +=1
		else:
			i_sig = 0 
			if(i < len(aPalabras)-1):
				i +=1
			else:
				buscar = False

	if(tmpPal == "No existe"):
		tmpPal =token
	

	return tmpPal.lower()




def isAnswer(palabra,aPal):
	"""
		Funcion que retorna la traduccion dependiendo si existe 
		un signo de pregunta en la oracion

		parametro_1 : palabra
		Esta siendo la oracion a recibir 
		parametro_2 : aPal
		Siendo el arreglo que contiene la tokenizacion de la oracion 
		con su respectiva clasificacion
    """
    
	cad = ""
	#Si contiene el signo "?" 
	if(palabra.find("?") > 0):
		existe = True

		#Pregunta si existe separacion por coma
		if(palabra.find(",") > 0):
			#Separa mediante split por coma
			aComa = palabra.split(",")
			trad =" "

			for i in range(len(aComa)):
				if(i == len(aComa)-1):
					trad = BuscarToken(aComa[i]).strip()
					#Si la cadena obtenida es igual a la original
					if(trad == aComa[i].strip()):
						w = nlp(aComa[i].strip())
						for text in w :
							cad += " "+BuscarToken(str(text))
					else:
						cad += trad
				else:
					trad = BuscarToken(aComa[i])
					print(trad)
					cad += trad+","




		#Si no existe separacion por coma
		else:

			#Primero realiza la traducion a la palabra completa 

			cad += BuscarToken(palabra)

			"""
				 Si detecta que la cadena obtenida es igual a la original realiza la traduccion
				 por tokens
			"""
			if(palabra == cad.strip()):
				cad = ""
				for pal in aPal:

					#if(pal[1] == "CCONJ"):
					
					cad += BuscarToken(str(pal[0]))+ " "
			else:
				cad = "¿"+cad

				cad +="?" 

	return cad

def Traducir(palabra):
	""" Realiza las traducciones obteniendo 
		la palabra y/o oracion completa a 	
		traducir 

		parametro_1 : palabra

		oracion a traduccir 

	"""

	

	cad = ""	   # variable que contendra la traduccion 

	# Realiza la normalizacion de la palabra y quita posibles espacios
	palabra = normalize(palabra.strip()) 
	w = nlp(palabra)
	
	#Crea lista con los tokens y su tipo  
	aPal = [ [text,text.pos_] for text in w]
	


	#Realiza la comprobacion si es pregunta
	esPregunta = palabra.find("?") > 0 


	if(esPregunta):
		#Llama a la funcion si es pregunta
		cad = isAnswer(palabra,aPal)

	else:
		"""
		Primero detecta si existe una coma para descubrir si 
		existe mas de una oracion 

		"""
	
		for pal in aPal:
			cad +=BuscarToken(str(pal[0]))+" " 


	return cad





cad = Traducir("soy camilo , como te llamas?")
print(cad)
import es_core_news_sm as es_core
import json 
#----------------------------------
#Variables globales 
#---------------------------------


nlp = es_core.load()

#with open('json/dic_final.json') as file:
with open('json/dic_febres1846_espmap_final.json') as file:
	#Carga el archivo json
	datos = json.load(file)

aPalabras = [] # Lista que contiene el arreglo con las palabras 


"""
	Se crea un arreglo con los pronombres personales 
	esto se hace para poder realizar el reemplazo sin tener que buscar en 
	el json y tambien para poder detectar de manera facil si existe un pronombre
	en la oracion 
"""

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
		pal = aPalabras[i]['palabra'][0]


		#print(pal)
		sig = aPalabras[i]['significado'] # Array con significados
		
		if(len(sig) == 0):
			sig = [""]

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
						for y in range(len(w)) :


							#Pregunta si el indice actual es igual al final
							if(y == len(w)-1 ):
							
								#Si encuentra que contiene un ? no lo agrega , ya que el token lo contiene
								if(str(w[y]) ==  "?"):
									cad += " "+BuscarToken(str(w[y]))
								else:
									cad += ""+BuscarToken(str(w[y]))+"?"
							else : 

								#Si no es igual primero pregunta si se encuentra en el indice 0 
								if(y == 0 ):

									cad += "¿"+BuscarToken(str(w[y]))
								else:
									cad += " "+BuscarToken(str(w[y]))
							
					else:
						if(cad.find("?") > 0 ):
							cad += trad + " "
						else: 
							cad += trad + "?"
						
				else:
					trad = BuscarToken(aComa[i])
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
	
	"""
		Bandera que detecta cuando una palabra es plurar,esto
		detectandose si contiene un pronombre plurar

	"""
	esPlurar = False 

	# Realiza la normalizacion de la palabra y quita posibles espacios
	palabra = normalize(palabra.strip().lower())

	"""
		Primero se realiza la pregunta si existen adjetivos antes de traducir donde 
		se reemplazara de manera inmediata si detecta que existen pronombres personales
	"""
	for pro in aPronombres:
		if(palabra.find(pro['trad'])!= -1):

			#Pregunta si utiliza un pronombre en plurar o dual

			if(pro['tipo'] == 'plural' or pro['tipo'] == 'dual'):
				esPlurar = True
			palabra = palabra.replace(pro['trad'],pro['palabra'])


	w = nlp(palabra)

	#Primero realiza la busqueda de la palabra completa , pero no debe ser pregunta
	if(BuscarToken(palabra) != palabra and palabra.find("?")<0):
		return BuscarToken(palabra)  
	else:

		#Crea lista con los tokens y su tipo  
		aPal = [ [text,text.pos_] for text in w]
		print(aPal)

		#Si la palabra contiene plurar , se debe quitar "s" y/o "es" 
		# se debe volver a singular
		if(esPlurar):
			for i in range(len(aPal)):
				pal = str(aPal[i][0]) # Se guarda la palabra
				tipo = aPal[i][1]
				"""
					Para de detectar si la palabra contiene plurar deberia contener "s" final , siendo esta plurar
				"""
				if(pal[len(pal)-2:].find("s")!= -1 and  tipo != "AUX"):
					pal = pal[:len(pal)-1]
					aPal[i][0] = pal
				
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


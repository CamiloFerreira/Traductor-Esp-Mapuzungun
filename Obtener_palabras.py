import requests as rq
from bs4 import BeautifulSoup 
import json

#-------------------------------------------
#Variables a utilizar 
#-------------------------------------------

iLetras = 0 # variable para recorrer arreglo letras
aLetras=[
		 'a','b','c','d','e','f','g','h','i','j',
		 'k','l','m','n','ñ','o','p','q','r','s',
		 't','u','v','w','x','y','z'
		 ]


#-----------------------------------------------
#-----------------------------------------------

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


def CargarWeb(url):
	r = rq.get(url)
	soup=BeautifulSoup(r.content,'html5lib')
	return soup

#Funcion para realizar busqueda en la pagina
#https://www.interpatagonia.com/mapuche/diccionario.html
def BuscarPalabras(iLetras,aLetras):

	#Carga la pagina y separa la seccion 
	web = CargarWeb("https://www.interpatagonia.com/mapuche/diccionario.html").find('section')

	pal = [] #Diccionario para establecer palabra + traduccion

	for i in aLetras : 
		pal.append({'letra':i,'palabras':[]})
	#-------------------------------------------------
	#Recopilacion de palabras para la primera pagina 
	#-------------------------------------------------
	#busca todas las etiquetas Ul de la pagina 
	for ul in web.findAll('ul'):
		#Busta todas las etiquetas li de la pagina
		for li in ul.findAll('li'):
			try : 
				
				palabra = li.strong.text.split(":")[0].strip() # Palabra en mapugundun
				letra = palabra[:1].lower() # Obtiene la primera letra 
				#traduccion = ''
				if ( len(li.text.split(":")) > 1 ):
					traduccion = li.text.split(":")[1].strip()
					if(traduccion != ""):
						#Se llena con los datos 
						for pos in pal:
							if(pos['letra'] == letra):
								pos['palabras'].append({'palabra':palabra,'significado':traduccion})
					#print(traduccion)
					#pal[letra].append([text,traduccion])
			except AttributeError:
				pass
	return pal
	#-----------------------------------------------------------------
	#Recopilacion de palabras fin primera pagina
	#-----------------------------------------------------------------



#Se cargan las palabras del txt que este contiene el diccionario obtenido 
# del pdf del gobierno con un diccionario amplio de mapudungn
def BuscarPalabras2(iLetras,aLetras):
	f = open("Documentos/Palabras.txt")

	iLetras = 0 # Inicia el indice en 0 
	aCad = []
	actual_pto = False # Bandera para detectar si existe dob punto en palabra actual
	sig_pto    = False # Bandera para detectar si existe dob punto en palabra siguiente
	
	for i in f.read().split('.'):
		cad = i.split('\n') #Obtiene un arreglo donde separa las palabras por los saltos de linea
		

		#Si al momento de separar las cadenas por salto de linea este presenta
		# mas de 2 posiciones en el arreglo se agrega la palabra dependiendo si esta posee ":" 
		#sino se agrega a la definicion anterior .
		if(len(cad)>2):
			#print("------------------------")
			for ind in range(len(cad)):
				if(cad[ind] != "\n" ):
					actual = ind #Indice del actual
					#Si existe siguiente ve si tiene ":" , sino concadena lo del siguiente con el actual
					if ( actual+1 < len(cad) and actual > 0):
						siguiente = actual+1

						for letras in cad[actual]:
							if(letras == ":"):
								actual_pto = True
						for letras in cad[siguiente]:
							if(letras == ":"):
								sig_pto = True

						#Si existe pto coma en el actual y el siguiente se guarda actual
						if(actual_pto == True and sig_pto == True):
							aCad.append(cad[actual])
							actual_pto = False
							sig_pto    = False
						#Si existe pto coma en el actual y el siguiente no 
						# se concatena con el actual
						if(actual_pto == True and sig_pto == False):
							pal = cad[actual] +" "+cad[siguiente]
							#print("Concatenacion: " , pal)
							aCad.append(pal)
							actual_pto = False
							sig_pto    = False

			#print("-----------------------")

		else:
		#Se guarda las palabras que no tengas mas de 1 posicion
			if(len(cad) > 1):
				aCad.append(cad[1]) 

	#--------------------------------------------------------------------------
	#Parte que regulariza el diccionario en Json por orden alfabetico 
	#-------------------------------------------------------------------------
	

	pal=[]
	#Crea las llaves para el diccionario 
	for i in aLetras:
		pal.append({'letra':i,'palabras':[]})


	for i in range(len(aCad)) : 
		separados = aCad[i].split(":") # Variable que separa la cadena por ":"
		if(len(separados) > 1):
			palabra     = separados[0]
			significado = separados[1]
			#Se obtiene la primera palabra para ordenar alfabeticamente
			letra = normalize(palabra[:1].lower())
			
			for pos in pal:
				if(pos['letra'] == letra):
					pos['palabras'].append({'palabra':palabra,'significado':significado})

	#---------------------------------------------------------------------

	return pal



#Funcion para realizar busqueda en la pagina
#https://www.mapuche.nl/espanol/idioma/index_idioma.htm

#Para esta pagina se le debe pasar como parametro la letra para el diccionario 
#https://www.mapuche.nl/espanol/idioma/"letra".htm <- tiene esa estructura
def BuscarPalabras3(iLetras,aLetras):

	pal = [] #Diccionario para establecer palabra + traduccion

	for i in aLetras:
		pal.append({'letra':i,'palabras':[]})

	for letra in aLetras:

		try:
			web = CargarWeb("https://www.mapuche.nl/espanol/idioma/"+letra+".htm")
			contenido = web.find("td",attrs={'width':'749'}).text.split("\n") # Obtiene la parte que contiene las palabras + traduccion
			for i in contenido:
				if(len(i.strip().split("-")) > 1):
					palabra = i.strip().split("-")[1].strip() # separa la palabra por la "-" y quita los espacios vacios
					letra = normalize(palabra[:1]).lower() # obtiene la primera letra de la palabra 
					traduccion = i.strip().split("-")[0].strip() # separa la traduccion por la "-" y quita los espacios vacios

					if(len(letra)>0):
						if(traduccion != ""):
							for pos in pal:
								if(pos['letra'] == letra):
									pos['palabras'].append({'palabra':palabra,'significado':traduccion})
			
		except Exception as e:
			pass

	return pal


def BuscarRepetidos(pal,pal2):
	"""
		Funcion que busca los repetidos de los 2 arreglo , llenando con valores sin tener ninguno repetido

	"""
	palabras1 = [pos['palabras'] for pos in pal] #Obtiene el arreglo de palabras 
	palabras2 = [pos['palabras'] for pos in pal2] # Obtiene el arreglo de palabras

	pal_final = [] #Arreglo donde se guardaran las palabras sin repetisione

	for i in pal:
		pal_final.append({'letra':i['letra'],'palabras':[]})

	for i in range(len(palabras1)):
		a_palabras1  = palabras1[i] #obtiene el arreglo para cada posicion
		a_palabras2  = palabras2[i] #obtiene el arreglo para cada posicion

		repetidos = False

		i_pal1 = 0 #Indice de a_palabras1 
		i_pal2 = 0 #Indice de a_palabras2 
		
		#Si el largo es mayor a  0 continua la busqueda
		if(len(a_palabras1) > 0 ):

			for i in a_palabras1:
				pal1 = i['palabra']     #Guarda palabra
				sig1 = i['significado'] #Guarda significado

				#print(sig1)
				for y in a_palabras2:
					pal2 = y['palabra']     #Guarda palabra
					sig2 = y['significado'] #Guarda significado		


					#Consulta si la palabras son iguales 
					if(normalize(pal1.lower()) == normalize(pal2.lower())):
						letra = pal1[:1].lower()
						cad = ""

						#Ve si tiene punto y si tiene lo elimina
						if(sig1.find(".") > 0 ):
							a = sig1.split(".")
							cad += a[0]
						else:
							cad += sig1
						#Ve si tiene punto y si tiene lo elimina
						if(sig2.find(".") > 0):
							a = sig2.split(".")
							cad +=","+a[0]
						else:
							cad +=","+sig2

						#Guarda el dato repetido
						for z in pal_final:
							if(z['letra'] == letra):
								z['palabras'].append({'palabra':pal1,'significado':cad})

	return pal_final	


#Funcion que guarda los valores restantes del diccionario
def llenar(pal,dic):
	existe = False

	palabras1 = [pos['palabras'] for pos in dic]

	palabras2 = [pos['palabras'] for pos in pal]	

	for i in range(len(palabras1)) :
		
		#Si la posicion de palabras1 esta vacio se llena automaticamente
		#con la de palabras2
		if(len(palabras1[i]) == 0):
			if(len(palabras2[i]) > 0):
				palabras1[i] = palabras2[i]
		else:
			pos1 = palabras1[i]
			pos2 = palabras2[i]
			for y in pos2:
				
				pal  = y['palabra']
				sig  = y['significado']
				for z in pos1:
					pal2 = z['palabra']
					if(normalize(pal.lower()) == normalize(pal2.lower())):
						existe = True
						break
				if(existe):
					#Si existe la palabra la salta
					existe=False
				else:
					#Si no existe la guarda
					palabras1[i].append({'palabra':pal,'significado':sig})


	for i in range(len(dic)):
		dic[i]['palabras'] = palabras1[i]

	return dic

#----------------------------------------------------------------
# Proceso de guardado de las palabras en json
#-------------------------------------------------------------------

print("Obteniendo palabras .....")
#Obtiene las palabras de la primera pagina
pal = BuscarPalabras(iLetras,aLetras)
#Obtiene las palabras del txt
pal2= BuscarPalabras2(iLetras,aLetras)
#Obtiene las palabras de la segunda pagina
pal3 = BuscarPalabras3(iLetras,aLetras)


#Busca los valores repetidos
d = BuscarRepetidos(pal,pal2)
d = BuscarRepetidos(d,pal3)

#Llena con las palabras que restan 
d = llenar(pal,d);d = llenar(pal2,d);d = llenar(pal3,d);

#Guarda el diccionario
with open('json/dic_inicial.json','w') as file:
	json.dump(d,file,indent=4)

print("Palabras obtenidas !! ")

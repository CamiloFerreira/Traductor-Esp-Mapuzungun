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

	pal = {} #Diccionario para establecer palabra + traduccion

	for i in aLetras : 
		pal[i]= []

	cambiar_letra = False # Bandera para cambiar indice de iLetras


	#-------------------------------------------------
	#Recopilacion de palabras para la primera pagina 
	#-------------------------------------------------
	aPalabras = []
	#busca todas las etiquetas Ul de la pagina 
	for ul in web.findAll('ul'):
		#Busta todas las etiquetas li de la pagina
		for li in ul.findAll('li'):
			try : 
				text = li.strong.text.split(":")[0]
				letra = text[:1].lower() # Obtiene la primera letra 
				traduccion = ''
				if ( len(li.text.split(":")) > 1 ):
					traduccion = li.text.split(":")[1]
					pal[letra].append({text:traduccion})
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
	dic  = {} 
	actual_pto = False # Bandera para detectar si existe dob punto en palabra actual
	sig_pto    = False # Bandera para detectar si existe dob punto en palabra siguiente
	
	#Crea las llaves para el diccionario 
	for i in aLetras:
		dic[i] = []

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
	for i in range(len(aCad)) : 
		separados = aCad[i].split(":") # Variable que separa la cadena por ":"
		if(len(separados) > 1):
			palabra     = separados[0]
			significado = separados[1]

			#Se obtiene la primera palabra para ordenar alfabeticamente
			p = normalize(palabra[:1].lower())
			dic[p].append({palabra : significado})
	#---------------------------------------------------------------------

	return dic




#----------------------------------------------------------------
# Proceso de guardado de las palabras en json
#-------------------------------------------------------------------

#Obtiene las palabras de la primera pagina
pal = BuscarPalabras(iLetras,aLetras)
#Obtiene las palabras del txt
pal2= BuscarPalabras2(iLetras,aLetras)

pal.update(pal2) # Se juntan los dos diccionarios



#Diccionario para guardar palabra + traduccion y convertir en json
dic = {'Palabras':pal}


#Guarda el diccionario
with open('json/dic.json','w') as file:
	json.dump(dic,file,indent=4)



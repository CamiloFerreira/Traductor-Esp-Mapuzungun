'''
	En este script se procesaran los datos obtenidos de 
	corlexim y se regularizaran en un solo json
'''
import json
import sys
import es_core_news_sm as es_core
from tqdm import tqdm

from textblob import TextBlob





nlp = es_core.load()

aLetras=[
		 'a','b','c','d','e','f','g','h','i','j',
		 'k','l','m','n','ñ','o','p','q','r','s',
		 't','u','v','w','x','y','z'
		 ]

dic_name = [
			"dic_Augusta2016_espmap",
			"dic_Augusta2016",
			"dic_Valdivia",
			"dic_febres1765",
			"dic_febres1846_espmap",
			"dic_febres1846"] # Nombres de los archivos 

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

def getIndice(letra):
	ind = 0 
	for i in range(len(aLetras)):
		if(aLetras[i] == letra):
			ind = i
	return ind

#Si encuentra una o pero debe detectar si es para realizar
#una separacion de ideas o palabras ( Como lo realizado en el comentario)
def SepararPorO(pal):
	pal1 = ""
	pal2 = ""
	if(pal.find("o") >= 0 ): 
		posicion_o = pal.find("o")					
		#Si detecta que antes de una "o" hay vacio y despues de esta hay vacio separa
		#la palabra
		if(pal[posicion_o-1] == " " and pal[posicion_o +1 ] == " "):
			pal1 = pal[:posicion_o-1].strip()
			pal2 = pal[posicion_o+1:].strip()
			#print("or :",pal)
			#print("pal1:",pal1)
			#print("pal2:",pal2)
	
	return [pal1,pal2]





pal = [] #Diccionario para establecer palabra + traduccion

for i in aLetras : 
	pal.append({'letra':i,'palabras':[]})

#Limpia el dic Febres que es de Español - mapudungn
def DicFebresEspMap():
	with open("json/"+dic_name[4]+".json") as file :
		datos = json.load(file)
		for i in range(len(datos)):
			#Palabra -> Palabra en mapudungun o palabras en mapudungun
			#Significado ->traduccion en español  
			significado     = datos[i]['palabra'].strip()
			palabra = datos[i]['significado']
			#Primero pregunta si el signficado presenta comas
			#Si encuentra coma separa las palabras 
			if(significado.find(",") > 0 ):
				aComa = significado.split(",")
				#For para quitar espacios y caracteres que no sirvan 
				#Para ser guardados en un diccionario
				for c in range(len(aComa)):
					aComa[c] = aComa[c].strip() # Quita el caracter vacio del comienzo
					#Si encuentra una o pero debe detectar si es para realizar
					#una separacion de ideas o palabras ( Como lo realizado en el comentario)
					sep = SepararPorO(aComa[c])
					if(sep[0] != "" and sep[1] != ""):
						aComa.pop(c) # Elimina la cadena original
						aComa.append(sep[0])
						aComa.append(sep[1])
				#guarda lo obtenido en aComa en singnificado
				significado = aComa
			else:	
				#print(significado)
				sep = SepararPorO(significado)
				#print(significado)
				if(sep[0] != "" and sep[1] !=""):
					significado = sep
				else :
					significado = [significado]




			#Pregunta si presenta separacion por comas , si es asi 
			#Realiza el procesado de las palabras para determinar y separar
			if(palabra.find(",") >= 0 ):
				
				aComa = palabra.split(",")
				#print("or :",aComa)

				fin = False;c = 0 
				while(fin == False):
					aComa[c] = aComa[c].strip()
					if(aComa[c].find(";")>=0):
							#print(aComa[c])
						p1 = aComa[c][:aComa[c].find(";")].strip() # Palabra
						p2 = aComa[c][aComa[c].find(";")+1:].strip() #Significado
							#print(p1[:1])
						pal[getIndice(p1[:1])]['palabras'].append({'palabra':p1,'significado':p2})
						aComa.pop(c)
						c = 0 
					else:
						 
						sep = SepararPorO(aComa[c])

						if(sep[0] != "" and sep[1] != ""):
							#print(aComa[c])
							aComa.pop(c) # Elimina la cadena original
							aComa.append(sep[0])
							aComa.append(sep[1])
						#Se quitan los puntos
						if(aComa[c].find(".") > 0):
							aComa[c] = aComa[c][:aComa[c].find(".")]
						#print(aComa[c])
						c += 1
						if(c > len(aComa)-1):
							fin=True 

				palabra = aComa

			else:
				
				palabra = [palabra]
			#Se guardan las palabras con sus significados
			pal[getIndice(palabra[0][:1])]['palabras'].append({'palabra':palabra,'significado':significado})



	with open('json/dic_febres1846_espmap_final.json','w') as file:
		json.dump(pal,file,indent=4)

			#print("fin:",aComa)
			#print("------------")









#Limpia el dic febres de mapudungun - Español
def DicValdiviaMapEsp():
	with open('json/dic_Valdivia.json') as  file:
		datos =	json.load(file)


		for d in datos :

			palabra = normalize(d['palabra'])
			significado = d['significado']

			#Se separan las palabras que estan unidas 

			if(palabra.find(",") > 0 ):


				sComa = palabra.split(",")

				for i in range(len(sComa)):
					sComa[i] = sComa[i].strip()

			else:
				palabra = [palabra]
				#print(palabra)



			if(significado.find(",") > 0):
				sComa = significado.split(",")

				for i in range(len(sComa)):
					sComa[i] = sComa[i].strip()
					if(sComa[i].find(".") > 0):
						sComa[i] = sComa[i][:sComa[i].find(".")]


				significado = sComa
			else:
				significado = significado[:significado.find(".")]

				sep = SepararPorO(significado)
				#print(significado)
				if(sep[0] != "" and sep[1] !=""):
					significado = sep
				else :
					significado = [significado]



			pal[getIndice(palabra[0][:1])]['palabras'].append({'palabra':palabra,'significado':significado})
				#print(sComa)
		#print(datos)

	with open('json/dic_Valdivia_espmap_final.json','w') as file:
		json.dump(pal,file,indent=4)


DicValdiviaMapEsp()

"""
		if(significado.find(",") >= 0 ):
			significado = significado.split(",")

			k = 0 ; #Indice de significado
			for s in significado :

			
				if ( s.find(";") >= 0 ):
					s_sep = s.split(";")
					
					palabra_2 = [s_sep[0].strip()]
					significado_2 = [s_sep[1].strip()]

					letra_in = palabra_2[:1]
					pal[getIndice(letra_in)]['palabras'].append({'palabra':palabra_2,'significado':significado_2})
					
					significado.remove(s)
				
		else:
			
			if(significado.find(".") > 0):
				
				aComa = significado.split(".")
				nList = [] # Se guardaran los valores que contienen  texto
				print(aComa)
				for c in range(len(aComa)):

					if(aComa[c] != ""):
						nList.append(aComa[c])
				print(nList)
				print("--------")
				significado = nList

			else :
				#Si no encuentra ; guarda de manera normal en un arreglo
				if(significado.find(";") < 0):
					#Quita los caracteres si existen en el significado
					significado = [significado]
		if(palabra.find(",") >=0):

			palabra = palabra.split(",")
			for j in range(len(palabra)):
				palabra[j] = palabra[j].strip()

		else:
			palabra = [palabra]


		letra_in = palabra[:1]		
		pal[getIndice(letra_in)]['palabras'].append({'palabra':significado,'significado':palabra})
			#print(significado)





"""

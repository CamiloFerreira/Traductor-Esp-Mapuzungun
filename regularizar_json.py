import json
import es_core_news_sm as es_core
from tqdm import tqdm
import sys


nlp = es_core.load()


def QuitarNumeros(pal):

	aNumeros=["1.","2.","3.","4.","5.","6.","7.","8.","9."]
	cad =""
	#Si detecta que existe un ";" quita los puntos y coma
	# y convierte la variable pal en lista 
	if(pal.find(";") > 0):
		pal = pal.split(";")

	#Si detecta que la variable es de tipo lista
	#Realiza la operacion de quitar los numeros , de lo contrario 
	#retorna la palabra normal
	if(  type(pal) == list ):
		#Recorre el arreglo pal
		for i in range(len(pal)) :
			#Recorre el arreglo que contiene los numeros
			for num in aNumeros:
				#Si encuentra un numero lo quita 
				if(pal[i].find(num) > 0 ):
					pal[i] = pal[i].split(num)[1].strip()

					#Si existen puntos lo elimina
					if(pal[i].find(".") > 0 ):
						pal[i] = pal[i].split(".")[1]						
			#quita los espacios vacios
			pal[i] = pal[i].strip().strip(")")

			#Agrega las comas en las palabras
			if(i == len(pal)-1):
				cad+= pal[i]
			else:
				cad+= pal[i] + ","

		return cad
	else:
		return pal
#Funcion que ordena el json , quitando tanto "," en una misma oracion y tambien como numeros 
#Esto permitiendo realizar una mejor busqueda a futuro y permitir realizar la busqueda de sinonimos
#Esta debe ejecutarse cuando se genera por primera vez el "obtener_palabras.py"
def OrdenarJson():
	with open('json/dic_inicial.json','r') as file:
		data = json.load(file)
	#Se va a generar un orden en el json 
	#Si presenta mas de un significado estos seran separados en un arreglo 
	#Separando mediante ","

	esPregunta = False # Bandera para determinar que una palabra es pregunta 
	aPalabras = [pos['palabras'] for pos in data]

	for pos in tqdm( range(len(aPalabras))):
		for fila in range(len(aPalabras[pos])):
			palabra  = aPalabras[pos][fila]['palabra']
			sig      = aPalabras[pos][fila]['significado']

			"""
				Realiza la tokenizacion de la palabra para quitar carcteres
				y guardar palabra en un arreglo
			"""
			##token = nlp(palabra)
			
			if(palabra.find("?") < 0):
				pal = []
				tmp_coma = [] # variable para guardar la separacion 

				if(palabra.find(",") > 0 ):

					#Realiza la separacion por comas
					s_coma = palabra.split(",")
					
					for i in range(len(s_coma)):
						if(s_coma[i] != ""):
							tmp_coma.append(s_coma[i].strip()) #Quita los espacios 
					aPalabras[pos][fila]['palabra'] = tmp_coma
		
				else:
					
					#Pregunta si se encuentra el caracter "o" en la palabra
					if(palabra.find(" ")> 0 ):
						s_car = palabra.split(" ") # contendra la lista con la separacion de las palabras
						tmp_car = []
						existe = False 
						for i in range(len(s_car)):
							if(s_car[i] == "o"):
								existe = True

							if(s_car[i] != "" and s_car[i] != "o"):
								tmp_car.append(s_car[i])
						
						#Si existe la separacion por coma guarda la lista 
						if(existe):
							aPalabras[pos][fila]['palabra'] = tmp_car
							existe = False
						else:
							aPalabras[pos][fila]['palabra'] = [palabra]
					else:
						aPalabras[pos][fila]['palabra'] = [palabra]
				"""for i in range(len(token)):
					w = token[i]
					if(w.text != "," and w.text!="." and w.text!="o" and w.text!="O"):
						pal.append(w.text.strip())
				"""


			else:
				#Si encuentra signo de pregunta en la palabra lo remueve
				s_signo = palabra.split("?")
				aPalabras[pos][fila]['palabra'] = [s_signo[0]]
			#Si encuentra separacion por coma 
			#separa los significados y los guarda en una lista




			if(sig.find(",") > 0):
				a_coma = sig.split(",")

				aComa = []
				for i in a_coma:
					if(i.find("?") > 0):
						esPregunta = True
					i = QuitarNumeros(i)
					#Revisa nuevamente que la palabra obtenida
					#no contenga comas 
					if(i.find(",")>0):
						c = i.split(",")
						for y in c :
							aComa.append(y)
					else:
						aComa.append(i)
				
				
				#Si es pregunta guarda la palabra de manera normal sin realizar separacion
				if(esPregunta):
					aPalabras[pos][fila]['palabra'] = [palabra]
				#Guarda los significados ya como lista
				aPalabras[pos][fila]['significado'] = aComa
			else:
				#Si no lo encuentra guarda el unico significado como una lista
				sig = QuitarNumeros(sig)


				#Si es pregunta guarda la palabra de manera normal sin realizar separacion
				if(sig.find("?") > 0):
					aPalabras[pos][fila]['palabra'] = [palabra]


				if(sig.find(",") > 0):
					aComa = sig.split(",")
					aPalabras[pos][fila]['significado'] = aComa
				else:

					#Ve si tiene puntos 
					if(sig.find(".") > 0):
						s_punto = sig.split(".")

						aPunto = []
						for p in range(len(s_punto)):
							if(s_punto[p]!= ""):

								#Si contiene los parentesis en la misma posicion
								if(s_punto[p].find("(") >= 0 and s_punto[p].find(")") >= 0):

									cadena = s_punto[p][s_punto[p].find("("):s_punto[p].find(")")+1] # guarda lo que encuentra dentro de los parentesis

									aPunto.append(s_punto[p].replace(cadena,""))
									aPunto.append(cadena)
								else:

									#Si contiene el parentesis "(" solamente y la siguiente posicion contiene ")"
									
									if(s_punto[p].find("(")>=0): 
										if( p+1 < len(s_punto)):
											if(s_punto[p+1].find(")")>=0):
												a = s_punto[p][:s_punto[p].find("(")]
												b = s_punto[p][s_punto[p].find("("):]
												c = s_punto[p+1][:s_punto[p+1].find(")")+1]
												d = s_punto[p+1][s_punto[p+1].find(")")+1:]
												aPunto.append(a)
												aPunto.append(b+c)
												if(d != ""):
													aPunto.append(d)	
									else:
										aPunto.append(s_punto[p])
						aPalabras[pos][fila]['significado'] = aPunto
					else:	

						aPalabras[pos][fila]['significado'] = [ sig]
	for i in range(len(data)):
		#Guarda los cambios en la variable dataQ
		data[i]['palabras'] = aPalabras[i] 		

	#Guarda el diccionario
	with open('json/dic_final.json','w') as file:
		json.dump(data,file,indent=4)


OrdenarJson()

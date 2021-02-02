import requests as rq
from bs4 import BeautifulSoup 
import json
from tqdm import tqdm
import sys

def CargarWeb(url):
	r = rq.get(url)
	soup=BeautifulSoup(r.content,'html5lib')
	return soup

def QuitarNumeros(pal):
	aNumeros=["1.","2.","3.","4.","5.","6.","7.","8.","9."]
	normal = False
	for i in aNumeros:
		#Detecta si existe alguno , si existe para la ejecucion de la funcion
		if(len(pal.split(i))>1):
			return(pal.split(i)[1].strip())
			break
		else:
			normal = True

	if(normal):
		return pal

#Funcion que ordena el json , quitando tanto "," en una misma oracion y tambien como numeros 
#Esto permitiendo realizar una mejor busqueda a futuro y permitir realizar la busqueda de sinonimos
#Esta debe ejecutarse cuando se genera por primera vez el "obtener_palabras.py"
def OrdenarJson():
	with open('json/dic.json','r') as file:
		data = json.load(file)
	#Se va a generar un orden en el json 
	#Si presenta mas de un significado estos seran separados en un arreglo 
	#Separando mediante ","
	guardar = False # bandera para realizar un guardado con pal o pal2 
	ejecutado = True # bandera para saber si el codigo fue ejecutado anteriormente
	for l in tqdm(data["Palabras"],ascii=True,desc="Ordenando json"):
		lista = data["Palabras"][l] # guarda la lista de una letra - ejemplo todas las "a" o todas las "b"
		#Recorre la lista de palabras teniendo como indice el (i)
		for i in range(len(lista)):
			palabra = lista[i][0]
			significado = lista[i][1]
			#Si detecta que el lista es una cadena significa que el script se ejecuto por primera vez
			if (type(significado) == str):

				ejecutado =False  # No se ha ejecutado el codigo 
				#Para poder buscar los sinonimos correctamente hay que eliminar tanto los "," , "." y ";"
				#print("Palabra:", palabra)
				#Retirar los ";" y numeros  
				if(significado.find(";")> 1):
					separado = significado.split(";")
					aSig = [] #Guarda los significados en lista
					#Quita los numeros que se encuentran
					for s in separado:
						p = QuitarNumeros(s.strip()) 
						if(len(p.split(","))>1):
							for coma in p.split(","):
								#print(coma.strip())
								aSig.append(coma.strip())
						else:
							aSig.append(p.strip())
					data["Palabras"][l][i] = [palabra,aSig] 

				#Separa mas de un significado dependiendo si tiene ","
				elif(significado.find(",")>1):
					separado = significado.split(",")
					aSig=[] #Guarda los significados en lista
					for s in separado:
						p = QuitarNumeros(s.strip())
						#Vuelve a quitar numeros por si quedo alguno
						p = QuitarNumeros(p)
						aSig.append(p)
					data["Palabras"][l][i]=[palabra,aSig]

				else:
					#Si no cumple la condicion se edita igualmente
					data["Palabras"][l][i]=[palabra,[significado]]

			#De lo contrario si es otro tipo de variable es porque se ha ejecutado anteriormente 
			else:
				for y in range(len(significado)):
					pal = significado[y]
					#detecta si existe numeros 
					pal = QuitarNumeros(pal.strip()) 
					
					#Si detecta que existen comas 
					if(pal.find("(")>= 0 and pal.find(")") >= 0 and len(pal)):
						inicio = pal.find("(")
						fin    = pal.find(")")
						buscar  = pal[inicio:fin+1]

						if(len(pal) > len(buscar)):	
							#Guarda lo que se encuentra en "(" , ")" pero en una posicion distinta
							significado.append(buscar)
						
							pal = pal.replace(buscar," ")			
					
					#Pregunta si existe "." en la palabra 
					elif(pal.find(".") > 0):
						#Separa la cada por el "."
						pal2 = []

						for p in pal.split(".") :
							if (p != ""):
								pal2.append(p.strip())
								
						guardar = True #Activa la bandera para guardar los significados sin "."

					#Cuando las operaciones terminen se escribe nuevamente el signficado
					if(guardar):
						#Si la palabra a guardar es una cadena 
						if(type(pal2) == str):
							significado[y] = pal2
						else:
							#Si la palabra a guardar se convirtio en una lista
							significado.pop(y)# se borra la palabra original
							# se agregan a significado
							for p in pal2 :
									significado.append(p)
						guardar = False
					else:	
						significado[y] = pal

				significado = list(set(significado)) #sirve para eliminar palabras repetidas
				data["Palabras"][l][i] = [palabra,significado]


	#quitar palabras repetidas 
	buscar = True
	

	#Mientras existan palabras repetidas
	while buscar:
		cont = 0 ;
		for l in data["Palabras"]:
			lista = data["Palabras"][l]
			existe =False # variable para confirmar si la palabra anterior es igual a la actual
			for i in range(len(lista)):
				sig = lista[i][1]
				ant = " " #variable para guardar palabra anterior
				for y in range (len(sig)):
					#print (sig[y])
					if(sig[y] == ant):
						existe = True
					ant = sig[y]

				if(existe):
					cont +=1 
					#elimina el repetido
					data["Palabras"][l][i][1].remove(sig[y])
					existe = False
		if(cont == 0): # si el contador aumenta , significa que aun quedan palabras repetidas
			buscar = False ;
				

		
	#Guarda el diccionario
	with open('json/dic.json','w') as file:
		json.dump(data,file,indent=4)

	return ejecutado


def ObtenerSinonimos():
	with open('json/dic.json','r') as file:
		data = json.load(file)


	for l in tqdm(data["Palabras"],ascii=True,desc="Progreso total"):
		lista = data["Palabras"][l]
		cad = "__Buscando Sinonimos para la letra "+l
		for i in tqdm(range(len(lista)),ascii=True,desc=cad):
			palabra = lista[i][0]
			significado = lista[i][1]
			aSin = []

			for sig in significado : 			
				# Se obtendran los sinonimos de wordreference , donde a su pagina se pasa como parametro la palabra 
				url = "https://www.wordreference.com/sinonimos/"+sig
				web = CargarWeb(url)
				
				try :
						#Carga los sinonimos 
					sinonimos = web.find("div",attrs={"class":"trans clickable"}).findAll("li")
					#Si existen sinonimos 
					aSin.append(sig)
					#print(aSin)
					for S in sinonimos:
						for s in S.text.split(","):
							aSin.append(s.strip())

					data["Palabras"][l][i] = [palabra,aSin]
				except Exception as e:
					pass

	with open('json/dicSin.json','w') as file:
		json.dump(data,file,indent=4)

if(len(sys.argv) == 2):
	num = sys.argv[1]
	if(int(num) == 1 ):
		ejecutado = OrdenarJson()
		#Si no se ha ejecutado , lo vuelve a realizar
		if(ejecutado == False):
			OrdenarJson()
	elif(int(num) == 2):
		ObtenerSinonimos()

else:
	print("Error al ingresar parametros , solo debes ingresar uno !!")


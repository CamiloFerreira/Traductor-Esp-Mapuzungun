import requests as rq
from bs4 import BeautifulSoup 
import json
from tqdm import tqdm

#Variables a utilizar 

aLetras=[
		 'a','b','c','d','e','f','g','h','i','j',
		 'k','l','m','n','ñ','o','p','q','r','s',
		 't','u','v','w','x','y','z'
		 ]



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
	existe = False # bandera para detectar si existe un " " o vacio 
	for l in data["Palabras"]:
		lista = data["Palabras"][l] # guarda la lista de una letra - ejemplo todas las "a" o todas las "b"

		#Recorre la lista de palabras teniendo como indice el (i)
		for i in range(len(lista)):
			palabra = lista[i][0]
			significado = lista[i][1]
			#Si detecta que el lista es una cadena significa que el script se ejecuto por primera vez
			if (type(significado) == str):
				#Para poder buscar los sinonimos correctamente hay que eliminar tanto los "," , "." y ";"
				#print("Palabra:", palabra)
				#Retirar los ";" y numeros  
				if(significado.find(";")> 1):
					separado = significado.split(";")
					aSig = [] #Guarda los significados en lista
					#print(separado)

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
					#print(significado)
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
					#print(pal)
					pal = QuitarNumeros(pal.strip()) 
					
					#Si detecta que existen comas 
					if(pal.find("(")>= 0 and pal.find(")") >= 0):
						inicio = pal.find("(")
						fin    = pal.find(")")
						buscar  = pal[inicio:fin+1]

						#Guarda lo que se encuentra en "(" , ")" pero en una posicion distinta
						significado.append(buscar)
					
						pal = pal.replace(buscar,"")
					#elif(pal.find(",") > 0):
					#	pass
					#elif (pal.find(";") > 0):
						
					elif(pal.find(".") > 0):
						
						pal2 = pal.split(".")

						for p in pal2 :
							if (p == ""):
								existe = True
								break
						#quitar las posiciones que se encuentren vacias ( Si existe alguna)
						if(existe):
							pal2.remove("")
						guardar = True
					#Cuando las operaciones terminen se escribe nuevamente el signficado

					if(guardar == False):
						significado[y] = pal
					else:
						significado[y] = pal2
					#print(pal)
				
				for p in significado :
					if(p == ""):
						existe = True
						break

				if(existe == True):
					significado.remove("")
					existe=False
				data["Palabras"][l][i] = [palabra,significado]

	data = QuitarRepetidos(data)
	#Guarda el diccionario
	with open('json/dic.json','w') as file:
		json.dump(data,file,indent=4)


#Funcion que quita valroes repetidos del json0
def QuitarRepetidos(d2):
	aLetras=[
		 'a','b','c','d','e','f','g','h','i','j',
		 'k','l','m','n','ñ','o','p','q','r','s',
		 't','u','v','w','x','y','z'
		 ]
	d={}
	for l in aLetras:
		d[l] = []
	repetido = False
	for l in d2 :
		for i in range(len(d2[l])):
			pal = d2[l][i]
			for le in d :
				#si no existen datos en el diccionario "D" se llena con el primero
				if(len(d[le]) == 0 ):
					d[le].append(pal)
				else:
					#carga las palabras del segundo diccionario 
					#si detecta un valor repetido sube la bandera y termina el bucle
					for y in range(len(d[le])):
						pal2 = d[le][y]
						if(pal2[0].lower() == pal[0].lower()):
							repetido = True
							break
					if(repetido):
						palabra = pal[0]
						if(pal2[1] != pal[1]):
							sig = pal2[1]+"," + pal[1]
							d[le][y] = [palabra,sig] 
						repetido = False
					else:
						d[le].append(pal)
	return d





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

print("Seleccione Operacion : ")
print("1. Ordenar Json")
print("2. Buscar sinonimos")


t = input("Ingrese numero : ")


if(int(t) == 1 ):
	OrdenarJson()
	print("Json ordenado")
elif(int(t) == 2):
	ObtenerSinonimos()

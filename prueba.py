import json


with open('json/pal.json') as file:
	#Carga el archivo json
	pal = json.load(file)
with open('json/pal2.json') as file:
	#Carga el archivo json
	pal2 = json.load(file)
with open('json/pal3.json') as file:
	#Carga el archivo json
	pal3 = json.load(file)


def BuscarRepetidos(pal,pal2):
	dic = {}
	existe = False

	#Primero guarda los valores que son iguales en ambos diccionarios
	for key in pal : 
		lista = pal[key]
		dic[key] = []
		#Carga el primer diccionario
		for x in range(len(lista)):
			pal_palabra = lista[x][0].strip().upper()
			pal_sig     = lista[x][1].lower().strip()
			#Carga el segundo diccionario utilizando la key del primer diccionario
			lista2 = pal2[key]
			for y in range(len(lista2)):
				pal2_palabra = lista2[y][0].strip().upper()
				pal2_sig      = lista2[y][1].lower().strip()
				#Comprueba si la palabra son iguales
				if(pal2_palabra.lower() == pal_palabra.lower() ):
					#para esto se debe quitar tanto puntos , como otros carateres que molesten.
					if(pal_sig.find(".") > 0):
						pal_sig = pal_sig.split(".")
						#quita los espacios en " " en blanco o vacio
						cad = ""
						for p in pal_sig:
							if(p != ""):
								cad += p + " " 
						pal_sig = cad
						#con la cadena limpia de caracteres se agrega a pal2_sig y se guarda
						pal2_sig += "," +cad 
						dic[key].append([pal_palabra,pal2_sig])
					#Si no tiene puntos se guarda 
					else:
						pal_sig += ","+pal2_sig 
						dic[key].append([pal_palabra,pal_sig])

					break
	return dic
#Luego guarda los valores restantes del diccionario 

#para el primer diccionario

def llenar(pal,dic):
	existe = False
	for key in pal:
		lista = pal[key]
		lista2 = dic[key]
		for i in range(len(lista)): 
			pal_palabra = lista[i][0]
			pal_sig     = lista[i][1]
			for y in range(len(lista2)):
				pal2_palabra = lista2[y][0]
				pal2_sig     = lista2[y][1]	
				#si existe la palabra levanta la bandera 
				if(pal2_palabra == pal_palabra):
					existe = True
					break
			#Mientras no existe el valor se guarda
			if(existe == False):
				if(pal_sig != ""):
					dic[key].append([pal_palabra,pal_sig])
				else:
					print("NO tiene nadaaa")
			else:
				existe = False
	return dic 

dic = BuscarRepetidos(pal,pal2)
dic = BuscarRepetidos(dic,pal3)
dic = llenar(pal,dic);dic = llenar(pal2,dic);dic = llenar(pal3,dic)




for key in dic : 
	lista = dic[key]

	for i in range(len(lista)):
		if(lista[i][0].lower() == "fey"):
			print(lista[i][1])

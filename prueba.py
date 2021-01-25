import json



with open('json/dic.json','r') as file:
	data = json.load(file)

d = {}


for l in data["Palabras"]:
	d[l] = []


for l in data["Palabras"] :
	lista = data["Palabras"][l]
	for i in range(len(lista)):
		palabra = lista[0] # Guarda la palabra 
		significado = lista[1] #Guarda el significado 

		#Recorre el diccionario nuevo
		lista2 = d[l]
		
		#Pregunta si existe un valor en el diccionario
		print(lista2)
print(d)

f = open("Documentos/Palabras.txt")

aCad = []
actual_pto = False
sig_pto    = False
for i in f.read().split('.'):
	cad = i.split('\n') #Obtiene un arreglo donde separa las palabras por los saltos de linea
	

	#Si al momento de separar las cadenas por salto de linea este presenta
	# mas de 2 posiciones en el arreglo se agrega la palabra dependiendo si esta posee ":" 
	#sino se agrega a la definicion anterior .
	if(len(cad)>2):
		print("------------------------")
		for ind in range(len(cad)):
			if(cad[ind] != "\n" ):
				actual = ind #Indice del actual

				#Si existe siguiente ve si tiene ":" , sino concadena lo del siguiente con el actual
				if ( actual+1 < len(cad) and actual > 0):
					siguiente = actual+1
					#print("Completo ", cad)
					#print("Actual : ",cad[actual])
					#print("Siguiente :",cad[siguiente])
					#Detecta si existe un ":"
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

				#print("Indice :",ind)
				#print (cad[ind])
		print("-----------------------")

	else:
	#Se guarda las palabras que no tengas mas de 1 posicion
		if(len(cad) > 1):
			aCad.append(cad[1]) 


for i in range(len(aCad)):
	print(aCad[i])
	pass
	#print(aCad[i])


def QuitarNumeros(pal):

	aNumeros=["1.","2.","3.","4.","5.","6.","7.","8.","9."]
	cad =""

	if(  type(pal) == list ):
		#Recorre el arreglo pal
		for i in range(len(pal)) :
			#Recorre el arreglo que contiene los numeros
			for num in aNumeros:
				#Si encuentra un numero lo quita 
				if(pal[i].find(num) > 0 ):
					pal[i] = pal[i].split(num)[1].strip()

			#quita los espacios vacios
			pal[i] = pal[i].strip()

			if(i == len(pal)-1):
				cad+= pal[i]
			else:
				cad+= pal[i] + ","

		return cad
	else:
		return pal
cad =" apremiar; 2. acomodar; 3. acostumbrar"
cad2 = "hola"
if(cad.find(";") > 0):
	s_punto = cad.split(";")
	
	s_punto = QuitarNumeros(s_punto)

#cad = QuitarNumeros(cad,False)
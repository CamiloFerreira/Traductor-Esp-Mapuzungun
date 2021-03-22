import es_core_news_sm as es_core
import json 

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


def BuscarToken(token,aPalabras):
	'''
		Funcion que busca la palabra por token 
		ejemplo se ingresa la palabra "Hola " busca esa palabra en el diccionario
		y retorna "Foche"
	'''
	token = normalize(token.lower().strip())
	buscar = True
	i = 0 ; # indice de aPalabras
	i_sig = 0 ; # indice para buscar el el array de los significados

	tmpPal = "No existe";
	while buscar:
		pal = aPalabras[i]['palabra']
		sig = aPalabras[i]['significado'] # Array con significados
		palabra = normalize(sig[i_sig].lower().strip())

		if(palabra== token):
			tmpPal = pal
			buscar = False	 
		if(i_sig < len(sig)-1):
			i_sig +=1
		else:
			i_sig = 0 
			if(i < len(aPalabras)-1):
				i +=1
			else:
				buscar = False

	if(tmpPal == "No existe"):
		tmpPal =token
	return tmpPal.lower()

def Traducir(palabra):
	nlp = es_core.load()
	with open('json/dic2.json') as file:
		#Carga el archivo json
		datos = json.load(file)
	'''
		Se cargan las palabras en un arreglo para 
		realizar las busquedas mas simples 
	'''

	cad = " "
	aPalabras = []
	for jsonObject in datos:
		aPalabras += jsonObject['palabras']

	w = nlp(palabra)

	#Pregunta si existe el signo de pregunta
	if(palabra.find("?") > 0):
		#Pregunta si existe separacion por coma
		if(palabra.find(",") > 0):
			#Separa mediante split por coma
			aComa = palabra.split(",")
			for i in range(len(aComa)):
				if(i == len(aComa)-1):
					cad += "¿"+BuscarToken(aComa[i],aPalabras)+"?"
				else:
					cad += BuscarToken(aComa[i],aPalabras)+","
		else:
			cad ="¿"+BuscarToken(palabra,aPalabras)+"?"
	else:
		#Si no existe traduce token x token
		for token in w :
			cad +=BuscarToken(str(token),aPalabras)

	return cad

	#inicio = time.process_time()
	#print(BuscarToken(token,aPalabras))
	#final = time.process_time() - inicio

	#inicio_1 = time.process_time()
	#print(BuscarFor(token,aPalabras))
	#final_2 = time.process_time() - inicio_1

	#print("Velocidad while : ",final)
	#print("Velocidad for :",final_2)
	#print("While es mas veloz : " ,final < final_2)

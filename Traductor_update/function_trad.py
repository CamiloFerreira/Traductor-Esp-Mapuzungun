
def SearchPRON(aPronombres,token):
	"""
		Busca el pronombre que se encuentre en el diccionario
		aPronombres y retorna la palabra en mapudungun
		----------------------------------
		value 1 - aPronombres
		Diccionario que contiene los pronombres español y mapudungun
		value 2 - Token
		Palabra que buscara para retornar el pronombre en mapudungun
		-----------------------------------
	"""
	pal = ""
	for i in range(len(aPronombres)):
		elemento = aPronombres[i]

		if(elemento['trad'].lower() == token.lower()):
			pal = elemento['palabra']

	return pal



def SearchToken(Dic,token):
	"""
		Busca en el diccionario si existe similitud y retorna la
		palabra en mapudungun del token que fue recibido

		------------------------
		value 1 - Diccionario Mapudungun - español 

		value 2 - Token: palabra a buscar o oracion a buscar
	"""
	
	for lista in Dic:
		palabras = lista['palabras']
		for pal in palabras:

			palabra     = pal['palabra']
			significado = pal['significado']

			for sig in significado:

				sig = sig.strip()
				#print(sig)
				if(sig.find("hablar") != -1):
					print(sig)
					


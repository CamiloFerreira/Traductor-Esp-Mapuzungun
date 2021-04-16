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



def getIndice(letra):
	ind = 0 

	for i in range(len(aLetras)):
		if(aLetras[i] == letra):
			ind = i
	return ind


pal = [] #Diccionario para establecer palabra + traduccion

for i in aLetras : 
	pal.append({'letra':i,'palabras':[]})


with open("json/"+dic_name[4]+".json") as file :

	datos = json.load(file)

	for i in range(len(datos)):


		palabra     = datos[i]['palabra']
		significado = datos[i]['significado']

		if(significado.find(",") >= 0 ):
			significado = significado.split(",")
			for s in significado :
				if ( s.find(";") >= 0 ):
					s_sep = s.split(";")
					
					palabra_2 = [s_sep[0].strip()]
					significado_2 = [s_sep[1].strip()]

					letra_in = palabra_2[:1]
					pal[getIndice(letra_in)]['palabras'].append({'palabra':palabra_2,'significado':significado_2})
					
					significado.remove(s)
		else:
			
			if(significado.find(";") < 0):
				significado = [significado]
		if(palabra.find(",") >=0):

			palabra = palabra.split(",")

		else:
			palabra = [palabra]


		letra_in = palabra[:1]		
		pal[getIndice(letra_in)]['palabras'].append({'palabra':significado,'significado':palabra})
			#print(significado)



with open('json/dic_febres1846_espmap_final.json','w') as file:
	json.dump(pal,file,indent=4)


"""

		#Separa las palabras
		if( palabra.find(",") >= 0):
			palabra = palabra.split(",")
		else:
			palabra = [palabra]
"""

	#for words in f.words : 
	#	print(words)
	#	print("idioma:" +words.detect_language())

						



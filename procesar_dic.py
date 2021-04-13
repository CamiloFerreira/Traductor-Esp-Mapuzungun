'''
	En este script se procesaran los datos obtenidos de 
	corlexim y se regularizaran en un solo json
'''
import json
import sys
import es_core_news_sm as es_core
from tqdm import tqdm


nlp = es_core.load()

dic_name = [
			"dic_Augusta1916",
			"dic_Augusta2016",
			"dic_Valdivia",
			"dic_febres1765",
			"dic_febres1846"] # Nombres de los archivos 

aPal2 = []
with open("json/"+dic_name[0]+".json") as file :

	datos = json.load(file)

	for i in range(len(datos)):

		palabra = datos[i]['palabra']
		significado = datos[i]['significado']


		'''
			Se quitan los caracteres especiales tanto 
			como '+' , '*', entre otros caracteres que se 
			encuentran en la 'palabra'
		'''
		if( palabra.find("*") > 0 ):
			palabra = palabra[:palabra.find("*")]

		if(palabra.find("+") > 0 ):
			palabra = palabra[:palabra.find("+")]

		if(palabra.find("(") > 0 ):
			palabra = palabra[:palabra.find("(")]

		

		if(significado.find("\u2013") >= 0):
			
			print("---------")
			print("           ")
			#print("sig_or:",significado)


			s_sep = significado.split("\u2013")

			
			print(s_sep)
			print("           ")
	

			
			for i in range(len(s_sep)):
				if(s_sep[i] != ""):
					print(i,s_sep[i])

					sig = s_sep[i]
					
					p_add = ""


					#Recorre letra por letra de la oracion
					for p in sig:
						if (p == " " or p =="*" or p =="+" or p == ","):
							break
						else:
							p_add +=p 
					p_add = p_add.replace("adj.","")
					p_add = p_add.replace("s.","")
					print(palabra+p_add)


						



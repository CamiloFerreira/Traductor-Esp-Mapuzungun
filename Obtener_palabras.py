#Paginas a utilizar 
#https://www.interpatagonia.com/mapuche/diccionario.html

import requests as rq
from bs4 import BeautifulSoup 
import json


def CargarWeb(url):
	r = rq.get(url)
	soup=BeautifulSoup(r.content,'html5lib')
	return soup


#Carga la pagina y separa la seccion 
web = CargarWeb("https://www.interpatagonia.com/mapuche/diccionario.html").find('section')


#-------------------------------------------
#Variables a utilizar 
#-------------------------------------------

iLetras = 0 # variable para recorrer arreglo letras
aLetras=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z']

pal = {} #Diccionario para establecer palabra + traduccion
cambiar_letra = False # Bandera para cambiar indice de iLetras
#_--------------------------------------------


aPalabras = []
#busca todas las etiquetas Ul de la pagina 
for ul in web.findAll('ul'):
	#Busta todas las etiquetas li de la pagina
	
	for li in ul.findAll('li'):
		try : 
			text = li.strong.text.split(":")[0]

			letra = text[:1] # Obtiene la primera letra 
			traduccion = ''
			if ( len(li.text.split(":")) > 1 ):
				traduccion = li.text.split(":")[1]
			#Activa la bandera cuando la letra es distinto de vacio Y son disntitos tanto aLetras y letra
			if(letra != '' and aLetras[iLetras].upper() != letra.upper()):
				cambiar_letra = True

			if(cambiar_letra):
				#Cambia el indice hasta que encuentra una letra similar 
				while (aLetras[iLetras].upper() != letra.upper()):
					iLetras +=1
				#print(aLetras[iLetras],' ',letra)
				cambiar_letra=False


			#Guarda la palabra en la lista 
			aPalabras.append({text:traduccion})
			traduccion = ''
		except AttributeError:
			pass
	pal[aLetras[iLetras]] = aPalabras
	aPalabras = []


#Diccionario para guardar palabra + traduccion y convertir en json
dic = {'Palabras':pal}



with open('json/dic.json','w') as file:
	json.dump(dic,file,indent=4)



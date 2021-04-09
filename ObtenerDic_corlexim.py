import requests as rq
from bs4 import BeautifulSoup 
import json
from tqdm import tqdm
import sys


url = "http://corlexim.cl/aug1916mapcas&comp"

user     = sys.argv[1]
password = sys.argv[2]

#Datos para iniciar sesion
form_data={
	'name':user,
	'pass': password,
	'form_build_id': 'form-OTXF0WYiwhYAxXD6YyyUWVcaLiKNJ1jFQqIHb0isdDI',
	'form_id': 'user_login',
	'op': 'Iniciar sesión'
}


def ObtenerDic(url,name_json):
	response = rq.post(url,form_data)
	soup=BeautifulSoup(response.content,'html5lib')
	#Busca la tabla , por la clase 
	#Siendo la tabla que contiene los significados y traducciones
	table = soup.find('table',{'class':['views-table','sticky-enabled','tableheader-processed','sticky-table']})
	#Se saca el contenido de la tabla 
	tbody = table.find('tbody')
	#Se sacan todas las etiquetas tr de la tabla
	aTr = tbody.find_all('tr')
	dic = []
	for i in tqdm(range(len(aTr)),ascii=True,desc=name_json):
		#Se obtiene la palabra 
		
		if(aTr[i].find('td',{'class':'entry'}) !=None):
			palabra    = aTr[i].find('td',{'class':'entry'}).find("a").getText()
		else:
			palabra = aTr[i].find('td',{'class':'entrymap'}).find('strong').getText()



		if(aTr[i].find('td',{'class':'views-field-description'}).find("p") != None):
			significado = aTr[i].find('td',{'class':'views-field-description'}).find("p").getText()

			dic.append({'palabra':palabra,'significado':significado})
	#Guarda el diccionario
	with open('json/'+name_json+'.json','w') as file:
		json.dump(dic,file,indent=4)



#Guardar todos los diccionarios de corlexim


url = "http://corlexim.cl/aug1916mapcas&comp"
name_json = "dic_Augusta1916"
ObtenerDic(url,name_json)


url = "http://corlexim.cl/es/aug2016mapcas"
name_json = "dic_Augusta2016"
ObtenerDic(url,name_json)


url = "http://corlexim.cl/vald1606mapcas&comp"
name_json = "dic_Valdivia"
ObtenerDic(url,name_json)


url = "http://corlexim.cl/febr1882mapcas&comp"
name_json = "dic_febres1765"
ObtenerDic(url,name_json)


url = "http://corlexim.cl/febr1846mapcas&comp"
name_json = "dic_febres1846"
ObtenerDic(url,name_json)

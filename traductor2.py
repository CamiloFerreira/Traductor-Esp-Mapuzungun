import psutil
import es_core_news_sm as es_core
import json 
import traductor as td
import time



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



class Traductor():

	data = "" #Variable que guardara los datos del json
	letras =[
		 'a','b','c','d','e','f','g','h','i','j',
		 'k','l','m','n','ñ','o','p','q','r','s',
		 't','u','v','w','x','y','z'
		 ]
	aPalabras = []

	
	def __init__(self, data):
		self.nlp =es_core.load()
		""" Instancia la clase traductor
			Parametros data -- json que contiene el diccionario
		"""
		self.data = data
		for jsonObject in self.data:
			for palabras in jsonObject['palabras']:
				self.aPalabras.append(palabras)
	def BuscarPal(self,pal):
		
		buscar = True




	def getTrad(self,oracion):
		"""Funcion que busca la traduccion teniendo 
		   como parametro la oracion
			1. Busca la oracion completa para ver si existe 
			
		"""
		
		w =self.nlp(oracion)
		for text in w :
			print(text)
		


	def getData(self):
		return self.data




with open('json/dic2.json') as file:
	#Carga el archivo json
	datos = json.load(file)

with open('json/dic.json') as file:
	#Carga el archivo json
	data = json.load(file)
traductor = Traductor(datos)

cadena = "Hola , como te llamas?"


inicio_1 = time.process_time()
traductor.getTrad(cadena)
final_1  = time.process_time() - inicio_1
#inicio_2 = time.process_time()
#td.Traducir(cadena,data)
#final_2  = time.process_time() - inicio_2


print("Ejecutar con clase : ",final_1)
#print("Codigo anterior :",final_2)
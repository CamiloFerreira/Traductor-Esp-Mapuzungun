from traductor import *


iniciar = True
while iniciar :
	cad = input("Palabra a traducir : ")
	pal = Traducir(cad)
	if(cad == "fin123"):
		iniciar = False
	print(pal)	
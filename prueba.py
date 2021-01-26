import sys


print (sys.argv)


if(len(sys.argv) == 2):
	num = sys.argv[1]
	print(num)
else:
	print("Error al ingresar parametros , solo debes ingresar uno !!")
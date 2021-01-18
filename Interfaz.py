from tkinter import *
from traductor import BuscarTraduccion


#Llama al traductor
def enviar():

	buscar = text1.get("1.0",END)
	
	buscar = buscar.split("\n")[0]

	texto= StringVar()

	palabra = BuscarTraduccion(buscar)
	
	if(palabra == None):
		texto.set("No existe")
	else:
		texto.set(palabra)

	
	
	text2.config(textvariable=texto)
	
		




#Creacion de una ventana
vt = Tk()


vt.title("Traductor")
vt.geometry("600x300")

btn = Button(vt,text="Traduccir" , command=enviar)
btn.place(x=400,y=250)


#Seccion para introducir el texto
text1 = Text(vt,heigh=10,width=30)
text1.place(x=10,y=60)

#Seccion para mostrar la traduccion
text2 = Label(vt,text = "AQUI VA LA TRADUCION")

text2.place(x=300,y=60)



vt.mainloop()
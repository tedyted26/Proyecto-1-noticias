from tkinter import *
from tkinter import ttk
import sys
import os

# código copiado de GeeksforGeeks.org para conseguir importar archivos fuera de la carpeta
  
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)

class Clasificador_frame(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()

    def set_controller(self, controller):
        self.controller = controller     

    def create_widgets(self):

        # titulos
        label_configuracion = Label(self, text="Configuración:", font='bold')
        label_configuracion.place(relx=0.05 , rely=0.035)

        label_resultados = Label(self, text="Resultados de la clasificación:", font='bold')
        label_resultados.place(relx=0.05 , rely=0.25)

        label_resumen = Label(self, text="Resumen:", font='bold')
        label_resumen.place(relx=0.7 , rely=0.25)

        label_guardar = Label(self, text="Guardar los resultados:", font='bold')
        label_guardar.place(relx=0.05 , rely=0.861)

        # seleccionar noticias
        label_noticias = Label(self, text="Noticias para clasificar:")
        label_noticias.place(relx=0.05 , rely=0.091)

        texto_noticias = Text(self)
        texto_noticias.place(relx=0.2, rely=0.09, relwidth=0.6, relheight=0.04)

        boton_abrir_noticias = Button(self, text="Seleccionar carpeta")
        boton_abrir_noticias.place(relx=0.82, rely=0.085, relwidth=0.13)

        # seleccionar modelo
        label_modelo = Label(self, text="Modelo clasificador:")
        label_modelo.place(relx=0.05 , rely=0.14)

        texto_modelo = Text(self)
        texto_modelo.place(relx=0.2, rely=0.14, relwidth=0.6, relheight=0.04)

        boton_abrir_modelo = Button(self, text="Seleccionar carpeta")
        boton_abrir_modelo.place(relx=0.82, rely=0.14, relwidth=0.13)

        # boton de ejecutar o entrenar
        boton_clasificar = Button(self, text="Clasificar")
        boton_clasificar.place(relx=0.45, rely=0.2, relwidth=0.13)

        # tabla de noticias
        self.lista_noticias = ttk.Treeview(self, column=("tit", "odio", "ver"), show='headings', height=5, selectmode=BROWSE)

        self.lista_noticias.column('#0', width=0, stretch=NO)
        self.lista_noticias.column('tit', width=200, anchor=W)
        self.lista_noticias.column('odio', width=1, anchor=CENTER)
        self.lista_noticias.column('ver', width=1, anchor=CENTER)

        self.lista_noticias.heading("tit", text="Noticia", anchor=CENTER)
        self.lista_noticias.heading("odio", text="Odio", anchor=CENTER)   
        self.lista_noticias.heading("ver", text="Ver", anchor=CENTER)

        self.lista_noticias.place(relx=0.05, rely= 0.31, relheight=0.53, relwidth=0.61)
        #self.lista_noticias.bind("<<TreeviewSelect>>", self.mostrar_texto)

        sb = Scrollbar(self)
        sb.place(relx=0.66, rely= 0.31, relheight=0.53, relwidth=0.02)

        self.lista_noticias.config(yscrollcommand=sb.set)
        sb.config(command=self.lista_noticias.yview)

        # resumen
        label_ejemplares_odio = Label(self, text='Noticias "Odio":')
        label_ejemplares_odio.place(relx=0.7 , rely=0.306)

        texto_ejemplares_odio = Text(self, state="disabled")
        texto_ejemplares_odio.place(relx=0.85, rely=0.305, relwidth=0.1, relheight=0.04)

        label_ejemplares_no_odio = Label(self, text='Noticias "No Odio":')
        label_ejemplares_no_odio.place(relx=0.7, rely=0.355)

        texto_ejemplares_no_odio = Text(self, state="disabled")
        texto_ejemplares_no_odio.place(relx=0.85, rely=0.354, relwidth=0.1, relheight=0.04)

        label_total = Label(self, text="Total:")
        label_total.place(relx=0.7 , rely=0.404)

        texto_total = Text(self, state="disabled")
        texto_total.place(relx=0.85, rely=0.403, relwidth=0.1, relheight=0.04)

        label_algoritmo_seleccionado = Label(self, text="Tiempo:")
        label_algoritmo_seleccionado.place(relx=0.7 , rely=0.453)

        texto_algoritmo_seleccionado = Text(self, state="disabled")
        texto_algoritmo_seleccionado.place(relx=0.85, rely=0.453, relwidth=0.1, relheight=0.04)

        # grafico de resumen
        grafico = Frame(self, bg="white")
        grafico.place(relx=0.7 , rely=0.51, relheight=0.33, relwidth=0.25)

        # guardar resultados
        label_guardar_resultados = Label(self, text="Ruta de guardado:")
        label_guardar_resultados.place(relx=0.05 , rely=0.921)

        texto_guardar_resultados = Text(self)
        texto_guardar_resultados.place(relx=0.2, rely=0.92, relwidth=0.48, relheight=0.04)

        boton_ruta_resultados = Button(self, text="Seleccionar carpeta")
        boton_ruta_resultados.place(relx=0.7, rely=0.915, relwidth=0.13)

        boton_guardar = Button(self, text="Guardar")
        boton_guardar.place(relx=0.85, rely=0.915, relwidth=0.1)

    def borrar_contenido(self):
        print("borrar contenido del frame")

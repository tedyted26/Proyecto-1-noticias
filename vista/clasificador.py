from tkinter import *
from tkinter import ttk
import sys
import os
from tkinter import filedialog
from pathlib import Path
from functools import partial
from Classify import Classify

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
        self.path_inicial = os.getcwd()
        self.resultados = None
        self.cfy = Classify()

    def set_controller(self, controller):
        self.controller = controller     

    def create_widgets(self):

        # titulos
        self.label_configuracion = Label(self, text="Configuración:", font='bold')
        self.label_configuracion.place(relx=0.05 , rely=0.035)

        self.label_resultados = Label(self, text="Resultados de la clasificación:", font='bold')
        self.label_resultados.place(relx=0.05 , rely=0.25)

        self.label_resumen = Label(self, text="Resumen:", font='bold')
        self.label_resumen.place(relx=0.7 , rely=0.25)

        self.label_guardar = Label(self, text="Guardar los resultados:", font='bold')
        self.label_guardar.place(relx=0.05 , rely=0.861)

        # mensaje de error
        self.label_error = Label(self, text="", fg="red")
        self.label_error.place(relx=0.2, rely=0.035, relwidth=0.6)

        self.label_error_2 = Label(self, text="", fg="red")
        self.label_error_2.place(relx=0.25, rely=0.861, relwidth=0.55)

        # seleccionar noticias
        self.label_noticias = Label(self, text="Noticias para clasificar:")
        self.label_noticias.place(relx=0.05 , rely=0.091)

        self.texto_noticias = Text(self)
        self.texto_noticias.place(relx=0.2, rely=0.09, relwidth=0.6, relheight=0.04)

        self.boton_abrir_noticias = Button(self, text="Seleccionar carpeta", command=partial(self.seleccionar_carpeta, "noticias"))
        self.boton_abrir_noticias.place(relx=0.82, rely=0.085, relwidth=0.13)

        # seleccionar modelo
        self.label_modelo = Label(self, text="Modelo clasificador:")
        self.label_modelo.place(relx=0.05 , rely=0.14)

        self.texto_modelo = Text(self)
        self.texto_modelo.place(relx=0.2, rely=0.14, relwidth=0.6, relheight=0.04)

        self.boton_abrir_modelo = Button(self, text="Seleccionar carpeta", command=partial(self.seleccionar_carpeta, "modelo"))
        self.boton_abrir_modelo.place(relx=0.82, rely=0.14, relwidth=0.13)

        # boton de ejecutar o entrenar
        self.boton_clasificar = Button(self, text="Clasificar", command=self.clasificar_noticias)
        self.boton_clasificar.place(relx=0.45, rely=0.2, relwidth=0.13)

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
        self.label_ejemplares_odio = Label(self, text='Noticias "Odio":')
        self.label_ejemplares_odio.place(relx=0.7 , rely=0.306)

        self.texto_ejemplares_odio = Text(self, state="disabled")
        self.texto_ejemplares_odio.place(relx=0.85, rely=0.305, relwidth=0.1, relheight=0.04)

        self.label_ejemplares_no_odio = Label(self, text='Noticias "No Odio":')
        self.label_ejemplares_no_odio.place(relx=0.7, rely=0.355)

        self.texto_ejemplares_no_odio = Text(self, state="disabled")
        self.texto_ejemplares_no_odio.place(relx=0.85, rely=0.354, relwidth=0.1, relheight=0.04)

        self.label_total = Label(self, text="Total:")
        self.label_total.place(relx=0.7 , rely=0.404)

        self.texto_total = Text(self, state="disabled")
        self.texto_total.place(relx=0.85, rely=0.403, relwidth=0.1, relheight=0.04)

        self.label_tiempo = Label(self, text="Tiempo:")
        self.label_tiempo.place(relx=0.7 , rely=0.453)

        self.texto_tiempo = Text(self, state="disabled")
        self.texto_tiempo.place(relx=0.85, rely=0.453, relwidth=0.1, relheight=0.04)

        # grafico de resumen
        self.grafico = Frame(self, bg="white")
        self.grafico.place(relx=0.7 , rely=0.51, relheight=0.33, relwidth=0.25)

        # guardar resultados
        self.label_guardar_resultados = Label(self, text="Ruta de guardado:")
        self.label_guardar_resultados.place(relx=0.05 , rely=0.921)

        self.texto_guardar_resultados = Text(self)
        self.texto_guardar_resultados.place(relx=0.2, rely=0.92, relwidth=0.6, relheight=0.04)

        self.boton_guardar = Button(self, text="Guardar", command=self.guardar_resultados)
        self.boton_guardar.place(relx=0.82, rely=0.915, relwidth=0.13)


    def seleccionar_carpeta(self, origin):      
        if origin=="noticias":
            carpeta = filedialog.askdirectory(initialdir=self.path_inicial)
            self.texto_noticias.delete(1.0, "end")
            self.texto_noticias.insert(1.0, carpeta)
        elif origin=="modelo":
            pathmodelo = filedialog.askopenfile(initialdir=self.path_inicial).name
            self.texto_modelo.delete(1.0, "end")
            self.texto_modelo.insert(1.0, pathmodelo)


    def clasificar_noticias(self):
        # recogemos los datos
        self.label_error.config(text="")
        self.label_error_2.config(text="")
        ruta_noticias = self.texto_noticias.get(1.0, "end-1c")
        ruta_modelo = self.texto_modelo.get(1.0, "end-1c")

        if ruta_noticias == "" or ruta_modelo == "" or not Path(ruta_noticias).exists() or not Path(ruta_modelo).exists():
            self.label_error.config(text = "Comprueba los campos. No se ha proporcionado una ruta correcta.")
            return

        lista_noticias = os.listdir(ruta_noticias)
        num_noticias = len([x for x in lista_noticias if x.endswith(".txt") or x.endswith(".TXT")])

        if num_noticias == 0:
            self.label_error.config(text = "Noticias no proporcionadas.")
            return

        modelo = self.cfy.openModel(ruta_modelo)

        if modelo is None:
            self.label_error.config(text = "Error en la carga del modelo. Compruebe su extensión.")
            return

        self.resultados, tiempo = self.cfy.classifyNews(ruta_noticias, modelo)  

        if self.resultados is None:
            self.label_error.config(text = "Se ha producido un error al clasificar.")
            return      

        # dividir los resultados en odio y no odio
        num_odio = 0
        num_no_odio = 0
        
        for key in self.resultados:
            if key[1] == 1:
                num_odio +=1
            elif key[1] == -1:
                num_no_odio +=1
       
        # mostramos en vista previa
        self.texto_ejemplares_odio.config(state = 'normal')
        self.texto_ejemplares_no_odio.config(state = 'normal')
        self.texto_tiempo.config(state = 'normal')
        self.texto_total.config(state = 'normal')

        self.texto_ejemplares_odio.delete(1.0, "end")
        self.texto_ejemplares_no_odio.delete(1.0, "end")
        self.texto_tiempo.delete(1.0, "end")
        self.texto_total.delete(1.0, "end")

        self.texto_ejemplares_odio.insert(1.0, num_odio)
        self.texto_ejemplares_no_odio.insert(1.0, num_no_odio)
        self.texto_tiempo.insert(1.0, tiempo)
        self.texto_total.insert(1.0, num_noticias)

        self.texto_ejemplares_odio.config(state = 'disabled')
        self.texto_ejemplares_no_odio.config(state = 'disabled')
        self.texto_tiempo.config(state = 'disabled')
        self.texto_total.config(state = 'disabled')

        # rellenar el treeview

        # TODO en base al objeto resultados


    def guardar_resultados(self):
        if self.resultados is not None:
            # FIXME comprobar la extensión del archivo del resultado
            f = filedialog.asksaveasfile(defaultextension=".csv", initialdir=self.path_inicial, filetypes=[("Comma separated value", "*.csv")])
            if f is None:
                return
            f.write(self.resultados)
            f.close()
        # si no, mensaje de error
        else:
            self.label_error_2.config(text = "No existen resultados que guardar.")

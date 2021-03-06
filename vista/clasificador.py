from tkinter import *
from tkinter import ttk
import sys
import os
from datetime import datetime
from tkinter import filedialog
from pathlib import Path
from functools import partial

from matplotlib.figure import Figure
from Classify import Classify
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import shutil # Para gestion de copias de archivos

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

        # mensaje de error
        self.label_error = Label(self, text="", fg="red")
        self.label_error.place(relx=0.2, rely=0.035, relwidth=0.6)

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

        self.boton_abrir_modelo = Button(self, text="Seleccionar modelo", command=partial(self.seleccionar_carpeta, "modelo"))
        self.boton_abrir_modelo.place(relx=0.82, rely=0.14, relwidth=0.13)

        # boton de ejecutar o entrenar
        self.boton_clasificar = Button(self, text="Clasificar", command=self.clasificar_noticias)
        self.boton_clasificar.place(relx=0.45, rely=0.2, relwidth=0.13)

        # tabla de noticias
        self.lista_noticias = ttk.Treeview(self, column=("tit", "res"), show='headings', height=5, selectmode=BROWSE)

        self.lista_noticias.column('#0', width=0, stretch=NO)
        self.lista_noticias.column('tit', width=200, anchor=W)
        self.lista_noticias.column('res', width=1, anchor=CENTER)

        self.lista_noticias.heading("tit", text="Archivo", anchor=CENTER)
        self.lista_noticias.heading("res", text="Tipo", anchor=CENTER)

        self.lista_noticias.place(relx=0.05, rely= 0.31, relheight=0.54, relwidth=0.61)

        sb = Scrollbar(self)
        sb.place(relx=0.66, rely= 0.31, relheight=0.57, relwidth=0.02)

        self.lista_noticias.config(yscrollcommand=sb.set)
        sb.config(command=self.lista_noticias.yview)

        sb_x = Scrollbar(self, orient="horizontal")
        sb_x.place(relx=0.05, rely= 0.85, relheight=0.03, relwidth=0.61)

        self.lista_noticias.config(xscrollcommand=sb_x.set)
        sb_x.config(command=self.lista_noticias.xview)

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
        self.grafico.place(relx=0.7 , rely=0.51, relheight=0.37, relwidth=0.25)

        # ver noticia
        self.boton_guardar = Button(self, text="Ver archivo seleccionado", command=self.mostrar_archivo)
        self.boton_guardar.place(relx=0.05, rely=0.915, relwidth=0.2)

        # copiar/mover noticias en otro lado

        self.boton_copiar = Button(self, text="Copiar noticias a...", command=self.guardar_noticias_clasificadas_por_carpetas)
        self.boton_copiar.place(relx=0.34, rely=0.915, relwidth=0.15)

        self.isMover = BooleanVar()
        self.check_mover = Checkbutton(self, text='Mover en vez de copiar', variable=self.isMover, onvalue=True, offvalue=0)
        self.check_mover.place(relx=0.5, rely=0.92)

        # guardar resultados
        self.boton_guardar = Button(self, text="Guardar resultados como...", command=self.guardar_resultados)
        self.boton_guardar.place(relx=0.725, rely=0.915, relwidth=0.2)


    def seleccionar_carpeta(self, origin):      
        if origin=="noticias":
            carpeta = filedialog.askdirectory(initialdir=self.path_inicial)
            if carpeta != "":
                self.texto_noticias.delete(1.0, "end")
                self.texto_noticias.insert(1.0, carpeta)
        elif origin=="modelo":
            pathmodelo = filedialog.askopenfile(initialdir=self.path_inicial).name
            if pathmodelo != "":
                self.texto_modelo.delete(1.0, "end")
                self.texto_modelo.insert(1.0, pathmodelo)

    def guardar_noticias_clasificadas_por_carpetas(self):
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y_%H_%M_%S")

        dic_resultados = self.resultados
        carpeta = str(filedialog.askdirectory(initialdir=self.path_inicial))
        nueva_carpeta = carpeta + "/" + current_time
        if not Path(nueva_carpeta).exists():
            os.mkdir(nueva_carpeta)
        ruta_antigua = self.texto_noticias.get(1.0, "end-1c")
        for key, value in dic_resultados.items():
            tipo = "Pred_Odio" if value == 1 else "Pred_No_Odio"
            archivo_a_copiar = str(ruta_antigua)+"/"+key

            carpeta_tipo = nueva_carpeta + "/" + tipo
            if not Path(carpeta_tipo).exists():
                os.mkdir(carpeta_tipo)
            if self.isMover.get():
                shutil.move(archivo_a_copiar, carpeta_tipo)
            else:
                shutil.copy(archivo_a_copiar, carpeta_tipo)

    def clasificar_noticias(self):
        # recogemos los datos
        self.label_error.config(text="")
        ruta_noticias = self.texto_noticias.get(1.0, "end-1c")
        ruta_modelo = self.texto_modelo.get(1.0, "end-1c")
        self.lista_noticias.delete(*self.lista_noticias.get_children())
        self.lista_noticias.focus(None)
        self.resultados = None

        ruta_complementariaIDF_Wordlist = str(Path(ruta_modelo).parent.absolute())
        ruta_IDFlist = ruta_complementariaIDF_Wordlist + "\\IDFlist.txt"
        ruta_Wordlist = ruta_complementariaIDF_Wordlist + "\\diccionario.txt"

        if not Path(ruta_IDFlist).exists() or not Path(ruta_Wordlist).exists():
            self.label_error.config(text="El archivo IDFlist.txt y diccionario.txt deben encontrarse en la carpeta del modelo.")
            return
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
        self.cfy.carpeta_pathModeloNueva = Path(ruta_modelo).parent.absolute()
        self.resultados, tiempo = self.cfy.classifyNews(ruta_noticias, modelo, ruta_IDFlist, ruta_Wordlist)

        if self.resultados is None:
            self.label_error.config(text = "Error al clasificar. Si el error persiste entrene de nuevo.")
            return      

        # dividir los resultados en odio y no odio
        num_odio = 0
        num_no_odio = 0
        
        for key in self.resultados:
            if self.resultados[key] == 1:
                num_odio +=1
            elif self.resultados[key] == -1:
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
        self.texto_total.insert(1.0, num_odio + num_no_odio)

        self.texto_ejemplares_odio.config(state = 'disabled')
        self.texto_ejemplares_no_odio.config(state = 'disabled')
        self.texto_tiempo.config(state = 'disabled')
        self.texto_total.config(state = 'disabled')

        # rellenar el treeview
        i = 0
        for key in self.resultados:            
            if self.resultados[key] == 1:
                res = "Odio"
            elif self.resultados[key] == -1:
                res = "No odio"
            self.lista_noticias.insert(parent="", index="end", iid = i, values=(key, res))
            i = i+1

        # crear grafica
        self.grafico.destroy()

        self.grafico = Frame(self, bg="white")
        self.grafico.place(relx=0.7 , rely=0.51, relheight=0.37, relwidth=0.25)

        fig = Figure(figsize=(4,4), dpi=70) # create a figure object
        ax = fig.add_subplot(111) # add an Axes to the figure

        ax.pie([num_no_odio, num_odio], radius=1, labels=["No odio", "Odio"], colors = ["#57a8ef", "#13426c"])

        canvas = FigureCanvasTkAgg(fig, self.grafico)
        canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH)

        # self.guardar_noticias_clasificadas_por_carpetas(self.resultados, ruta_noticias)

    def mostrar_archivo(self):
        if self.lista_noticias.focus():
            # get archivo
            index_archivo = int(self.lista_noticias.focus())
            nombre_archivo_seleccionado = list(self.resultados)[index_archivo]
            path_archivo_seleccionado = self.texto_noticias.get(1.0, "end-1c") + "/" + nombre_archivo_seleccionado
            print(path_archivo_seleccionado)

            # abrir pop up (unico) con el archivo ya abierto
            top = Toplevel(self)
            top.geometry("750x850")
            top.title("Visualizar noticia")
            
            top_label_path_archivo = Label(top, text="Ruta de la noticia:")
            top_label_path_archivo.place(relx=0.05, rely=0.05, relwidth=0.9)

            top_path_archivo = Text(top)
            top_path_archivo.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.1)
            top_path_archivo.insert(1.0, path_archivo_seleccionado)
            top_path_archivo.config(state="disabled")

            with open(path_archivo_seleccionado, "r") as f:
                texto_archivo_seleccionado = f.read()

            top_label_path_archivo = Label(top, text="Texto de la noticia:")
            top_label_path_archivo.place(relx=0.05, rely=0.25, relwidth=0.9)

            top_text_archivo = Text(top)
            top_text_archivo.place(relx=0.05, rely=0.3, relwidth=0.87, relheight=0.65)
            top_text_archivo.insert(1.0, texto_archivo_seleccionado)
            top_text_archivo.config(state="disabled")

            sb = Scrollbar(top)
            sb.place(relx=0.92, rely= 0.3, relheight=0.65, relwidth=0.03)

            top_text_archivo.config(yscrollcommand=sb.set)
            sb.config(command=top_text_archivo.yview)

            self.label_error.config(text = "")

        else:
            self.label_error.config(text = "No hay ningún archivo seleccionado.")


    def guardar_resultados(self):
        if self.resultados is not None:
            f = filedialog.asksaveasfile(defaultextension=".csv", initialdir=self.path_inicial, filetypes=[("Comma separated value", "*.csv")])
            if f is None:
                return
            self.cfy.saveResult(f.name, self.resultados)
            self.label_error.config(text = "Resultados guardados.")
        # si no, mensaje de error
        else:
            self.label_error.config(text = "No existen resultados que guardar.")

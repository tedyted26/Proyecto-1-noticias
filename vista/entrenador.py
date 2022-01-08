from tkinter import *
from functools import partial
from tkinter import ttk
from tkinter import filedialog
import os
from pathlib import Path

class Entrenador_frame(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()
        self.path_inicial = os.getcwd()
        self.modelo_entrenado = None

    def set_controller(self, controller):
        self.controller = controller

    def create_widgets(self):

        # titulos
        self.label_configuracion = Label(self, text="Configuración:", font='bold')
        self.label_configuracion.place(relx=0.05 , rely=0.035)

        self.label_vista_previa = Label(self, text="Vista previa de los datos seleccionados:", font='bold')
        self.label_vista_previa.place(relx=0.05 , rely=0.27)

        self.label_resultado = Label(self, text="Resultado del entrenamiento:", font='bold')
        self.label_resultado.place(relx=0.05 , rely=0.533)

        self.label_guardar = Label(self, text="Guardar el modelo:", font='bold')
        self.label_guardar.place(relx=0.05 , rely=0.861)

        # seleccionar noticias de odio
        self.label_noticias_odio = Label(self, text="Noticias de Odio:")
        self.label_noticias_odio.place(relx=0.05 , rely=0.091)

        self.texto_noticias_odio = Text(self)
        self.texto_noticias_odio.place(relx=0.2, rely=0.09, relwidth=0.6, relheight=0.04)

        self.boton_abrir_odio = Button(self, text="Seleccionar carpeta", command=partial(self.seleccionar_carpeta, "odio"))
        self.boton_abrir_odio.place(relx=0.82, rely=0.085, relwidth=0.13)

        # seleccionar noticias de no odio
        self.label_noticias_no_odio = Label(self, text="Noticias de No Odio:")
        self.label_noticias_no_odio.place(relx=0.05 , rely=0.14)

        self.texto_noticias_no_odio = Text(self)
        self.texto_noticias_no_odio.place(relx=0.2, rely=0.14, relwidth=0.6, relheight=0.04)

        self.boton_abrir_no_odio = Button(self, text="Seleccionar carpeta", command=partial(self.seleccionar_carpeta, "noodio"))
        self.boton_abrir_no_odio.place(relx=0.82, rely=0.14, relwidth=0.13)

        # seleccionar algoritmo
        self.algoritmos = ["Árbol de clasificación", "K-NN", "Naive Bayes", "Redes Neuronales", "Regresión Logística", "SVM"]

        self.label_algoritmo = Label(self, text="Seleccionar algoritmo:")
        self.label_algoritmo.place(relx=0.05 , rely=0.21)

        self.combobox_algoritmos = ttk.Combobox(self, values=self.algoritmos, state="readonly")
        self.combobox_algoritmos.current(0)
        self.combobox_algoritmos.place(relx=0.2, rely=0.21)

        # boton de ejecutar o entrenar
        self.boton_entrenar = Button(self, text="Entrenar", command=self.entrenar_modelo)
        self.boton_entrenar.place(relx=0.82, rely=0.2, relwidth=0.13)        

        # vista previa
        self.label_ejemplares_odio = Label(self, text='Ejemplares "Odio":')
        self.label_ejemplares_odio.place(relx=0.05 , rely=0.326)

        self.texto_ejemplares_odio = Text(self, state="disabled")
        self.texto_ejemplares_odio.place(relx=0.2, rely=0.325, relwidth=0.2, relheight=0.04)

        self.label_ejemplares_no_odio = Label(self, text='Ejemplares "No Odio":')
        self.label_ejemplares_no_odio.place(relx=0.05 , rely=0.375)

        self.texto_ejemplares_no_odio = Text(self, state="disabled")
        self.texto_ejemplares_no_odio.place(relx=0.2, rely=0.374, relwidth=0.2, relheight=0.04)

        self.label_total = Label(self, text="Total ejemplares:")
        self.label_total.place(relx=0.05 , rely=0.424)

        self.texto_total = Text(self, state="disabled")
        self.texto_total.place(relx=0.2, rely=0.423, relwidth=0.2, relheight=0.04)

        self.label_algoritmo_seleccionado = Label(self, text="Algoritmo seleccionado:")
        self.label_algoritmo_seleccionado.place(relx=0.05 , rely=0.473)

        self.texto_algoritmo_seleccionado = Text(self, state="disabled")
        self.texto_algoritmo_seleccionado.place(relx=0.2, rely=0.473, relwidth=0.2, relheight=0.04)

        # mensaje de error
        self.label_error = Label(self, text="", fg="red")
        self.label_error.place(relx=0.45, rely=0.4, relwidth=0.45)

        # resultado
        self.frame_resultado = Frame(self, bg="white")
        self.frame_resultado.place(relx=0.05 , rely=0.589, relwidth=0.9, relheight=0.26)

        # guardar modelo
        self.label_guardar_modelo = Label(self, text="Ruta de guardado:")
        self.label_guardar_modelo.place(relx=0.05 , rely=0.921)

        self.texto_guardar_modelo = Text(self)
        self.texto_guardar_modelo.place(relx=0.2, rely=0.92, relwidth=0.6, relheight=0.04)

        self.boton_guardar = Button(self, text="Guardar", command=self.guardar_modelo)
        self.boton_guardar.place(relx=0.82, rely=0.915, relwidth=0.13)


    def seleccionar_carpeta(self, origin):      
        carpeta = filedialog.askdirectory(initialdir=self.path_inicial)
        if origin=="odio" and carpeta != "":
            self.texto_noticias_odio.delete(1.0, "end")
            self.texto_noticias_odio.insert(1.0, carpeta)
        elif origin=="noodio" and carpeta != "":
            self.texto_noticias_no_odio.delete(1.0, "end")
            self.texto_noticias_no_odio.insert(1.0, carpeta)


    def entrenar_modelo(self):
        # recogemos los datos
        self.label_error.config(text="")
        ruta_odio = self.texto_noticias_odio.get(1.0, "end-1c")
        ruta_no_odio = self.texto_noticias_no_odio.get(1.0, "end-1c")
        indice_algoritmo = self.combobox_algoritmos.current()

        if ruta_odio == "" or ruta_no_odio == "" or not Path(ruta_odio).exists() or not Path(ruta_no_odio).exists():
            self.label_error.config(text = "Comprueba los campos. No se ha proporcionado una ruta correcta.")
            return

        # mostramos en vista previa
        lista_files_odio = os.listdir(ruta_odio)
        lista_files_no_odio = os.listdir(ruta_no_odio)

        num_txt_odio = len([x for x in lista_files_odio if x.endswith(".txt") or x.endswith(".TXT")])
        num_txt_no_odio = len([x for x in lista_files_no_odio if x.endswith(".txt") or x.endswith(".TXT")])

        self.texto_ejemplares_odio.config(state = 'normal')
        self.texto_ejemplares_no_odio.config(state = 'normal')
        self.texto_algoritmo_seleccionado.config(state = 'normal')
        self.texto_total.config(state = 'normal')

        self.texto_ejemplares_odio.delete(1.0, "end")
        self.texto_ejemplares_no_odio.delete(1.0, "end")
        self.texto_algoritmo_seleccionado.delete(1.0, "end")
        self.texto_total.delete(1.0, "end")

        self.texto_ejemplares_odio.insert(1.0, num_txt_odio)
        self.texto_ejemplares_no_odio.insert(1.0, num_txt_no_odio)
        self.texto_algoritmo_seleccionado.insert(1.0, self.algoritmos[indice_algoritmo])
        self.texto_total.insert(1.0, num_txt_odio + num_txt_no_odio)

        self.texto_ejemplares_odio.config(state = 'disabled')
        self.texto_ejemplares_no_odio.config(state = 'disabled')
        self.texto_algoritmo_seleccionado.config(state = 'disabled')
        self.texto_total.config(state = 'disabled')

        # entrenar segun el modelo elegido
        # TODO quitar los prints y poner en cada if el algoritmo
        # lo suyo sería que devolviera un objeto que se guardase en modelo_entrenado, para así luego poder guardarlo en la otra función
        # lo inicializo arriba (init) con None solo para que se vea

        if indice_algoritmo==0: 
            print("Arbol de clasificacion")
        elif indice_algoritmo==1:
            print("K-NN")
        elif indice_algoritmo==2:
            print("Naive Bayes")
        elif indice_algoritmo==3:
            print("Redes Neuronales")
        elif indice_algoritmo==4:
            print("Regresión Logística")
        elif indice_algoritmo==5:
            print("SVM")           


    def guardar_modelo(self):
        # si se ha entrenado un modelo intentar guardarlo
        if self.modelo_entrenado is not None:
            # FIXME comprobar la extensión del archivo del modelo
            f = filedialog.asksaveasfile(defaultextension=".txt", initialdir=self.path_inicial)
            if f is None:
                return
            f.write(self.modelo_entrenado)
            f.close()
        # si no, mensaje de error
        else:
            self.label_error.config(text = "No existe modelo que guardar.")

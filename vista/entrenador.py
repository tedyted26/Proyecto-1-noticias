from tkinter import *
from functools import partial
from tkinter import ttk
from tkinter import filedialog
import os
from pathlib import Path
from matplotlib.pyplot import figure
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import sys
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

import tratamientoNoticias as tn

import algoritmos_teo
import Training as tr

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
        self.label_vista_previa.place(relx=0.05 , rely=0.285)

        self.label_resultado = Label(self, text="Gráfica del resultado:", font='bold')
        self.label_resultado.place(relx=0.5 , rely=0.285)

        self.label_resultado = Label(self, text="Resultado del entrenamiento:", font='bold')
        self.label_resultado.place(relx=0.05 , rely=0.6)

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
        self.label_noticias_no_odio.place(relx=0.05 , rely=0.15)

        self.texto_noticias_no_odio = Text(self)
        self.texto_noticias_no_odio.place(relx=0.2, rely=0.15, relwidth=0.6, relheight=0.04)

        self.boton_abrir_no_odio = Button(self, text="Seleccionar carpeta", command=partial(self.seleccionar_carpeta, "noodio"))
        self.boton_abrir_no_odio.place(relx=0.82, rely=0.145, relwidth=0.13)

        # seleccionar algoritmo
        self.algoritmos = ["Árbol de clasificación", "K-NN", "Naive Bayes", "Redes Neuronales", "Regresión Logística", "SVM"]

        self.label_algoritmo = Label(self, text="Seleccionar algoritmo:")
        self.label_algoritmo.place(relx=0.05 , rely=0.22)

        self.combobox_algoritmos = ttk.Combobox(self, values=self.algoritmos, state="readonly")
        self.combobox_algoritmos.current(0)
        self.combobox_algoritmos.place(relx=0.2, rely=0.22)

        # boton de ejecutar o entrenar
        self.boton_entrenar = Button(self, text="Entrenar", command=self.entrenar_modelo)
        self.boton_entrenar.place(relx=0.82, rely=0.21, relwidth=0.13)        

        # vista previa
        self.label_ejemplares_odio = Label(self, text='Ejemplares "Odio":')
        self.label_ejemplares_odio.place(relx=0.05 , rely=0.349)

        self.texto_ejemplares_odio = Text(self, state="disabled")
        self.texto_ejemplares_odio.place(relx=0.2, rely=0.349, relwidth=0.2, relheight=0.04)

        self.label_ejemplares_no_odio = Label(self, text='Ejemplares "No Odio":')
        self.label_ejemplares_no_odio.place(relx=0.05 , rely=0.408)

        self.texto_ejemplares_no_odio = Text(self, state="disabled")
        self.texto_ejemplares_no_odio.place(relx=0.2, rely=0.408, relwidth=0.2, relheight=0.04)

        self.label_total = Label(self, text="Total ejemplares:")
        self.label_total.place(relx=0.05 , rely=0.467)

        self.texto_total = Text(self, state="disabled")
        self.texto_total.place(relx=0.2, rely=0.467, relwidth=0.2, relheight=0.04)

        self.label_algoritmo_seleccionado = Label(self, text="Algoritmo seleccionado:")
        self.label_algoritmo_seleccionado.place(relx=0.05 , rely=0.529)

        self.texto_algoritmo_seleccionado = Text(self, state="disabled")
        self.texto_algoritmo_seleccionado.place(relx=0.2, rely=0.529, relwidth=0.2, relheight=0.04)

        # mensaje de error
        self.label_error = Label(self, text="", fg="red")
        self.label_error.place(relx=0.05, rely=0.8)

        # resultado
        self.label_precision = Label(self, text="Precisión: ")
        self.label_precision.place(relx=0.05 , rely=0.661)

        self.texto_precision = Text(self, state="disabled")
        self.texto_precision.place(relx=0.2, rely=0.66, relwidth=0.2, relheight=0.04)

        self.label_recall = Label(self, text="Recall o exhaustividad:")
        self.label_recall.place(relx=0.05 , rely=0.721)

        self.texto_recall = Text(self, state="disabled")
        self.texto_recall.place(relx=0.2, rely=0.72, relwidth=0.2, relheight=0.04)

        # grafico
        self.frame_resultado = Frame(self, bg="white")
        self.frame_resultado.place(relx=0.5 , rely=0.345, relwidth=0.45, relheight=0.52)

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

        algoritmos_disponibles = ["arbol", "knn",
                                  'nb', 'perceptron',
                                  'reglog', 'svm']
        algortimo_elegido = algoritmos_disponibles[indice_algoritmo]
        tr_o = tr.Training()
        self.modelo_entrenado, cm = tr_o.train(algortimo_elegido, ruta_no_odio, ruta_odio)
        # cm, self.modelo_entrenado = algoritmos_teo.funcion_de_antes("a", "a", "a") # para probar
        print(cm)

        # teniendo ya la matriz de confusion y el modelo, mostrar la gráfica y hacer los cálculos para rellenar los resultados:

        self.texto_precision.config(state = 'normal')
        self.texto_recall.config(state = 'normal')

        self.texto_precision.delete(1.0, "end")
        self.texto_recall.delete(1.0, "end")

        precision_odio = cm[1,1]/(cm[1,1]+cm[0,1]) # true odio clasificados como odio / total clasificados como odio
        recall_odio = cm[1,1]/(cm[1,1]+cm[1,0]) # true odio clasificados como odio / total true odio

        precision_no_odio = cm[0,0]/(cm[0,0]+cm[1,0]) # true no odio clasificados como no odio / total clasificados como no odio
        recall_no_odio = cm[0,0]/(cm[0,0]+cm[0,1]) # true no odio clasificados como no odio / total true no odio

        self.texto_precision.insert(1.0, round((precision_odio+precision_no_odio)*50, 2)) # media y pasado a porcentajes con 2 decimales
        self.texto_recall.insert(1.0, round((recall_odio+recall_no_odio)*50, 2))

        self.texto_precision.config(state = 'disabled')
        self.texto_recall.config(state = 'disabled')

        fig = Figure(figsize = (7,5), dpi = 70)
        ax1 = fig.add_subplot(111)
        ax1.set_title('Matriz de confusión')

        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Odio", "Odio"])
        
        canvas = FigureCanvasTkAgg(fig, master = self.frame_resultado)
        canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH)

        disp.plot(ax=ax1)
        


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

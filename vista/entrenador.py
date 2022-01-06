from tkinter import *
from functools import partial
from tkinter import ttk

class Entrenador_frame(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()

    def set_controller(self, controller):
        self.controller = controller

    def create_widgets(self):

        # titulos
        label_configuracion = Label(self, text="Configuración:", font='bold')
        label_configuracion.place(relx=0.05 , rely=0.035)

        label_vista_previa = Label(self, text="Vista previa de los datos seleccionados:", font='bold')
        label_vista_previa.place(relx=0.05 , rely=0.27)

        label_resultado = Label(self, text="Resultado del entrenamiento:", font='bold')
        label_resultado.place(relx=0.05 , rely=0.533)

        label_guardar = Label(self, text="Guardar el modelo:", font='bold')
        label_guardar.place(relx=0.05 , rely=0.861)

        # seleccionar noticias de odio
        label_noticias_odio = Label(self, text="Noticias de Odio:")
        label_noticias_odio.place(relx=0.05 , rely=0.091)

        texto_noticias_odio = Text(self)
        texto_noticias_odio.place(relx=0.2, rely=0.09, relwidth=0.6, relheight=0.04)

        boton_abrir_odio = Button(self, text="Seleccionar carpeta")
        boton_abrir_odio.place(relx=0.82, rely=0.085, relwidth=0.13)

        # seleccionar noticias de no odio
        label_noticias_no_odio = Label(self, text="Noticias de No Odio:")
        label_noticias_no_odio.place(relx=0.05 , rely=0.14)

        texto_noticias_no_odio = Text(self)
        texto_noticias_no_odio.place(relx=0.2, rely=0.14, relwidth=0.6, relheight=0.04)

        boton_abrir_no_odio = Button(self, text="Seleccionar carpeta")
        boton_abrir_no_odio.place(relx=0.82, rely=0.14, relwidth=0.13)

        # seleccionar algoritmo
        self.algoritmos = ["Árbol de clasificación", "K-NN", "Naive Bayes", "Redes Neuronales", "Regresión Logística", "SVM"]

        label_algoritmo = Label(self, text="Seleccionar algoritmo:")
        label_algoritmo.place(relx=0.05 , rely=0.21)

        combobox_algoritmos = ttk.Combobox(self, values=self.algoritmos, state="readonly")
        combobox_algoritmos.current(0)
        combobox_algoritmos.place(relx=0.2, rely=0.21)

        # boton de ejecutar o entrenar
        boton_entrenar = Button(self, text="Entrenar")
        boton_entrenar.place(relx=0.82, rely=0.2, relwidth=0.13)        

        # vista previa
        label_ejemplares_odio = Label(self, text='Ejemplares "Odio":')
        label_ejemplares_odio.place(relx=0.05 , rely=0.326)

        texto_ejemplares_odio = Text(self, state="disabled")
        texto_ejemplares_odio.place(relx=0.2, rely=0.325, relwidth=0.2, relheight=0.04)

        label_ejemplares_no_odio = Label(self, text='Ejemplares "No Odio":')
        label_ejemplares_no_odio.place(relx=0.05 , rely=0.375)

        texto_ejemplares_no_odio = Text(self, state="disabled")
        texto_ejemplares_no_odio.place(relx=0.2, rely=0.374, relwidth=0.2, relheight=0.04)

        label_total = Label(self, text="Total ejemplares:")
        label_total.place(relx=0.05 , rely=0.424)

        texto_total = Text(self, state="disabled")
        texto_total.place(relx=0.2, rely=0.423, relwidth=0.2, relheight=0.04)

        label_algoritmo_seleccionado = Label(self, text="Algoritmo seleccionado:")
        label_algoritmo_seleccionado.place(relx=0.05 , rely=0.473)

        texto_algoritmo_seleccionado = Text(self, state="disabled")
        texto_algoritmo_seleccionado.place(relx=0.2, rely=0.473, relwidth=0.2, relheight=0.04)

        # resultado
        frame_resultado = Frame(self, bg="white")
        frame_resultado.place(relx=0.05 , rely=0.589, relwidth=0.9, relheight=0.26)

        # guardar modelo
        label_guardar_modelo = Label(self, text="Ruta de guardado:")
        label_guardar_modelo.place(relx=0.05 , rely=0.921)

        texto_guardar_modelo = Text(self)
        texto_guardar_modelo.place(relx=0.2, rely=0.92, relwidth=0.49, relheight=0.04)

        boton_ruta_modelo = Button(self, text="Seleccionar carpeta")
        boton_ruta_modelo.place(relx=0.71, rely=0.915, relwidth=0.13)

        boton_guardar = Button(self, text="Guardar")
        boton_guardar.place(relx=0.86, rely=0.915, relwidth=0.09)


    def borrar_contenido(self):
        print("borrar contenido del frame")

import sys
from tkinter import *
from tkinter import ttk
from entrenador import Entrenador_frame
from clasificador import Clasificador_frame

class App_clasificador(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        #contenedor principal
        container = Frame(self)
        container.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.geometry("1200x800")
        self.title("App Clasificador")
        self.resizable(0,0)

        #configurar ventana para que salga centrada respecto a la pantalla
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height =   self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - win_width // 2
        y = self.winfo_screenheight() // 2 - win_height // 2
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.deiconify()

        #paginas del programa
        self.tabs = {}

        tabControl = ttk.Notebook(self)

        for F in (Entrenador_frame, Clasificador_frame):
            page_name = F.__name__
            tab = F(parent=tabControl)
            self.tabs[page_name] = tab
            self.tabs[page_name].set_controller(controller=container)
            self.tabs[page_name].create_widgets()
      
        
        tabControl.add(self.tabs["Entrenador_frame"], text=" Entrenar modelo ")
        tabControl.add(self.tabs["Clasificador_frame"], text=" Clasificar noticias ")
        
        tabControl.pack(expand=1, fill="both")

    #mostrar las paginas
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() 

#insertar menú en la ventana
app = App_clasificador()

def on_closing():
    app.destroy()
    sys.exit()

app.protocol("WM_DELETE_WINDOW", on_closing)

#visualizar
app.mainloop()

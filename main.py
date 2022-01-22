import vista.app_clasificador as app
import sys


#crear la ventana del programa
app = app.App_clasificador()

def on_closing():
    app.destroy()
    sys.exit()

app.protocol("WM_DELETE_WINDOW", on_closing)

#visualizar
app.mainloop()
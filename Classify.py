import pickle
import tratamientoNoticias as tn


class Classify():
    def __init__(self):
        print("algo")

    def classifyNews(self, pathNoticias, model):
        # estaria bien que fuera un diccionario de clave valor, siendo el valor si es de odio o no, y la clave la ruta de la noticia
        # importante guardar el tiempo que tarda el algoritmo en ejecutarse
        vectores = []
        paths = tn.getAllNewsUrlList(pathNoticias)[:10]
        for n, i in enumerate(paths):
            try:
                textoNoticia = tn.leerNoticia(i[0])
                vectores.append(tn.generarVectorDeTexto(textoNoticia, True, i[1], odio= -1))
            except:
                print(f"Error generando vector en archivo: {i[1]}")

        lista_valores = model.predict(X)
        resultados = {}
        tiempo = 0


        return resultados, tiempo
    
    def openModel(self, filepath):
        if filepath.endswith(".pickle") or filepath.endswith(".PICKLE"):
            with open(filepath, 'rb') as f:
                model = pickle.load(f)
                return model
        else:
            return None
    
    def saveResult(self, filepath, result):
        print("guardo como csv")

import pickle
import tratamientoNoticias as tn
import os
import numpy

class Classify():
    def __init__(self):
        self.pathNoticias = ''
        self.matrizNoticias = []

    def checkPaths(self, pathNoticias, pathModelo):
        # If we haven't created a matrix with the results of TF-IDF with these paths
        if (pathNoticias != self.pathNoticias):
            self.pathNoticias = pathNoticias

            # Open dictionary 
            if os.path.exists("diccionario.txt"):
                diccionario = tn.getWordList()
            else:
                print("Error abriendo el diccionario. Archivo inexistente. Prueba a entrenar otra vez.") 
                return   

            # Open IDFList from training matrix
            if os.path.exists("IDFList.txt"):
                listaIDF = numpy.loadtxt("IDFList.txt")
            else:
                print("Error abriendo la lista IDF. Archivo inexistente. Prueba a entrenar otra vez.") 
                return

            # Create the matrix with the new news
            vectores = []

            paths = tn.getAllNewsUrlList(pathNoticias)[:10]
            for n, i in enumerate(paths):
                try:
                    textoNoticia = tn.leerNoticia(i[0])
                    vectores.append(tn.generarVectorDeTexto(textoNoticia, False, i[1], odio= 0))
                except:
                    print(f"Error generando vector en archivo: {i[1]}")

            for v in vectores:
                self.matriz = tn.addVectorToMatriz(self.matriz, v)
            
            tn.saveMatrizToFile(self.matriz, "matriz.txt")
            
            m1_tf = tn.tfidf.matrixToTFIDF(self.matriz)
            self.df = tn.transformMatrizToPandasDataFrame(m1_tf)

            self.df.fillna(0, inplace=True)
            df2 = self.df.drop("nombre_", axis=1)
            self.X = df2.drop("odio_", axis=1)
            self.y = df2['odio_']
            
        # If we have a saved matrix but hasn't been imported
        elif len(self.matriz) == 0:
            # Import the saved matrix
            self.matriz = tn.generarMatriz("matriz.txt")
            m1_tf = tn.tfidf.matrixToTFIDF(self.matriz)
            self.df = tn.transformMatrizToPandasDataFrame(m1_tf)
            self.df.fillna(0, inplace=True)
            df2 = self.df.drop("nombre_", axis=1)
            self.X = self.df2.drop("odio_", axis=1)
            self.y = self.df2['odio_']
        
        return self.matrizNoticias

    def classifyNews(self, pathNoticias, model):
        # estaria bien que fuera un diccionario de clave valor, siendo el valor si es de odio o no, y la clave la ruta de la noticia
        # importante guardar el tiempo que tarda el algoritmo en ejecutarse
        matrizNoticias = self.checkPaths(pathNoticias, model)
        model = None 
        cm = None
        vectores = []
        paths = tn.getAllNewsUrlList(pathNoticias)[:10]

       

        #for vector in vectores:
        #    for item in vector:
        #        if item 
        #lista_valores = model.predict(X)
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

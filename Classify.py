import pickle
import time
import tratamientoNoticias as tn
import os
import numpy

class Classify():
    def __init__(self):
        self.pathNoticias = ''
        self.matriz = []
        self.df_with_name = None

    def checkPaths(self, pathNoticias, pathModelo):
        # If we haven't created a matrix with the results of TF-IDF with these paths
        if (pathNoticias != self.pathNoticias and os.path.exists("IDFList.txt")):
            self.pathNoticias = pathNoticias

            # Open dictionary 
            if os.path.exists("diccionario.txt"):
                diccionario = tn.getWordList()
                dic_length = len(diccionario)
            else:
                print("Error abriendo el diccionario. Archivo inexistente. Prueba a entrenar otra vez.") 
                return

            # Create the matrix with the new news
            vectores = []

            paths = tn.getAllNewsUrlList(pathNoticias)[:10]
            for n, i in enumerate(paths):
                try:
                    textoNoticia = tn.leerNoticia(i[0])

                    vectorNoticia = tn.generarVectorDeTexto(textoNoticia, False, i[1], odio= 0)
                    
                    if len(vectorNoticia) > dic_length:
                        vectorNoticia = vectorNoticia[:dic_length+2]

                    vectores.append(vectorNoticia)
                except:
                    print(f"Error generando vector en archivo: {i[1]}")
            
            self.matriz = []

            for v in vectores:
                self.matriz = tn.addVectorToMatriz(self.matriz, v)
            
            # create matrix tf idf with news
            matriz_tfidf = tn.tfidf.matrixToTFIDF(self.matriz)

            # convert it into datafame
            self.df_with_name = tn.transformMatrizToPandasDataFrame(matriz_tfidf)
            self.df_with_name.fillna(0, inplace=True)

            # save the original matrix for later
            tn.saveMatrizToFile(self.matriz, "matrizUnkwnNews.txt")        
            
        # If we have a saved matrix but hasn't been imported
        elif len(self.matriz) == 0:
            # Import the saved matrix
            self.matriz = tn.generarMatriz("matrizUnkwnNews.txt")
            # transform to tfidf
            m1_tf = tn.tfidf.matrixToTFIDF(self.matriz)
            # convert into dataframe
            self.df_with_name = tn.transformMatrizToPandasDataFrame(m1_tf)
            self.df_with_name.fillna(0, inplace=True)


    def classifyNews(self, pathNoticias, model):
        # estaria bien que fuera un diccionario de clave valor, siendo el valor si es de odio o no, y la clave la ruta de la noticia
        # importante guardar el tiempo que tarda el algoritmo en ejecutarse
        self.checkPaths(pathNoticias, model) 
        resultados = {}
        tiempo = 0
        
        df = self.df_with_name.drop(["odio_", "nombre_"], axis=1)

        t0 = time.time()
        raw_resultados = model.predict(df)
        t1 = time.time()

        fila = 0
        for res in raw_resultados:
            res_name = self.df_with_name.at[fila, 'nombre_']
            resultados[res_name] = res
            fila += 1

        tiempo = round(t1-t0, 5)
        
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

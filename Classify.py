import pickle
import time
import tratamientoNoticias as tn
import os

from sklearn import preprocessing
from pathlib import Path

class Classify():
    def __init__(self):
        self.pathNoticias = ''
        self.carpeta_pathModelo = ''
        self.carpeta_pathModeloNueva = ""
        self.matriz = []
        self.df_with_name = None

    def checkPaths(self, pathNoticias,
                   pathIDFlist= "IDFList.txt", pathWordlist= "diccionario.txt"):
        # If we haven't created a matrix with the results of TF-IDF with these paths

        if ((pathNoticias != self.pathNoticias or self.carpeta_pathModelo != self.carpeta_pathModeloNueva) and os.path.exists(pathIDFlist)):
            self.pathNoticias = pathNoticias


            # Open dictionary 
            if os.path.exists(pathWordlist):
                diccionario = tn.getWordList(pathWordlist)
                dic_length = len(diccionario)
            else:
                print("Error abriendo el diccionario. Archivo inexistente. Prueba a entrenar otra vez.") 
                return

            # Create the matrix with the new news
            vectores = []

            paths = tn.getAllNewsUrlList(pathNoticias)[:50]
            for n, i in enumerate(paths):
                try:
                    textoNoticia = tn.leerNoticia(i[0])

                    vectorNoticia = tn.generarVectorDeTexto(textoNoticia, False, i[1], odio= 0, rutaWordList=pathWordlist)
                    
                    if len(vectorNoticia) > dic_length:
                        vectorNoticia = vectorNoticia[:dic_length+2]

                    vectores.append(vectorNoticia)
                except:
                    print(f"Error generando vector en archivo: {i[1]}")
            
            self.matriz = []

            for v in vectores:
                self.matriz = tn.addVectorToMatriz(self.matriz, v)
            
            # create matrix tf idf with news
            matriz_tfidf = tn.tfidf.matrixToTFIDF(self.matriz, pathIDFlist, pathWordlist)

            # convert it into datafame
            self.df_with_name = tn.transformMatrizToPandasDataFrame(matriz_tfidf, pathWordlist)
            self.df_with_name.fillna(0, inplace=True)

            # save the original matrix for later
            # tn.saveMatrizToFile(self.matriz, "matrizUnkwnNews.txt")
            
        # If we have a saved matrix but hasn't been imported
        elif len(self.matriz) == 0:
            # Import the saved matrix
            # self.matriz = tn.generarMatriz("matrizUnkwnNews.txt")
            # transform to tfidf
            m1_tf = tn.tfidf.matrixToTFIDF(self.matriz)
            # convert into dataframe
            self.df_with_name = tn.transformMatrizToPandasDataFrame(m1_tf)
            self.df_with_name.fillna(0, inplace=True)
        self.carpeta_pathModelo = self.carpeta_pathModeloNueva

    def classifyNews(self, pathNoticias, model,
                   pathIDFlist= "IDFList.txt", pathWordlist= "diccionario.txt"):
        # estaria bien que fuera un diccionario de clave valor, siendo el valor si es de odio o no, y la clave la ruta de la noticia
        # importante guardar el tiempo que tarda el algoritmo en ejecutarse
        self.checkPaths(pathNoticias, pathIDFlist, pathWordlist)
        resultados = {}
        tiempo = 0
        
        df = self.df_with_name.drop(["odio_", "nombre_"], axis=1)
        modelos_escalados = ["KNeighborsClassifier", "LogisticRegression", "SVC"]
        if str(type(model).__name__) in modelos_escalados:
            df = preprocessing.scale(df)
        try:
            t0 = time.time()
            raw_resultados = model.predict(df)
            t1 = time.time()

            fila = 0
            for res in raw_resultados:
                res_name = self.df_with_name.at[fila, 'nombre_']
                resultados[res_name] = res
                fila += 1

            tiempo = round(t1-t0, 5)
        except:
            resultados = None      
        
        return resultados, tiempo
    
    def openModel(self, filepath):
        if filepath.endswith(".pickle") or filepath.endswith(".PICKLE"):
            with open(filepath, 'rb') as f:
                model = pickle.load(f)
                return model
        else:
            return None
    
    def saveResult(self, filepath, result):
        with open(filepath, "w") as f:   
            for row in result:
                if result[row] == -1:
                    res = 'No odio'
                elif result[row] == 1:
                    res = 'Odio'
                f.write(res + ";" + row + "\n")
        
            
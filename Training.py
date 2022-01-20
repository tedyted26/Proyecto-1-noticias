import tratamientoNoticias as tn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
# Algoritmos de ML
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn import tree
import os
import sys
from copy import deepcopy

class Training:

    def __init__(self):
        self.pathNoOdio = ''
        self.pathOdio = ''
        self.matriz = []
        self.df = None
        self.X = None
        self.y = None

    def checkPaths(self, pathNoOdio, pathOdio):
        # If we haven't created a matrix with these paths
        if (pathNoOdio != self.pathNoOdio or pathOdio == self.pathOdio ):
            self.pathNoOdio = pathNoOdio
            self.pathOdio = pathOdio
            # Create the matrix with the new news
            vectores = []
            paths = tn.getAllNewsUrlList(pathNoOdio)[:10]
            for n, i in enumerate(paths):
                try:
                    textoNoticia = tn.leerNoticia(i[0])
                    vectores.append(tn.generarVectorDeTexto(textoNoticia, True, i[1], odio= -1))
                except:
                    print(f"Error generando vector en archivo: {i[1]}")
            
            paths = tn.getAllNewsUrlList(pathOdio)[:10]
            for i in paths:
                try:
                    textoNoticia = tn.leerNoticia(i[0])
                    vectores.append(tn.generarVectorDeTexto(textoNoticia, True, i[1], odio= 1))
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


    def train(self, algorithm: str, pathNoOdio: str, pathOdio: str):
        self.checkPaths(pathNoOdio, pathOdio)
        model = None 
        cm = None
        if algorithm == 'arbol':
            model = tree.DecisionTreeClassifier()
        elif algorithm == 'knn':
            pass
        elif algorithm == 'nb':
            model = GaussianNB()
        elif algorithm == 'perceptron':
            model = Perceptron(tol=1e-3, random_state=0)
        elif algorithm == 'reglog':
            pass
        elif algorithm == 'svm':
            model = SVC(kernel="linear")

        
        if model != None:
            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size =.3)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            cm = confusion_matrix(y_test, predictions, labels=model.classes_)
        
        return model, cm

    def saveModel(self, path:str, modelname:str, model):
        with open(path+'\\'+modelname+'.pickle', 'wb') as f:
            pickle.dump(model, f)

    def graphConfusionMatrix(self, cm): 
        categories = ['No Odio', 'Odio']
        group_names = ['True Neg','False Pos','False Neg','True Pos']
        group_counts = ['{0:0.0f}'.format(value) for value in cm.flatten()]
        group_percentages = ['{0:.2%}'.format(value) for value in cm.flatten()/np.sum(cm)]
        labels = [f'{v1}\n{v2}\n{v3}' for v1, v2, v3 in zip(group_names,group_counts,group_percentages)]
        labels = np.asarray(labels).reshape(2,2)
        sns.heatmap(cm, annot=labels, fmt='', cmap='Blues', xticklabels=categories,yticklabels=categories)

        plt.show()
    
    def crossValidation(self, model):
        kf = KFold(n_splits = 10, shuffle = True)
        kf.get_n_splits(self.X)
        resultados = 0.0
        for train_index, test_index in kf.split(self.X):
            X_train, X_test = self.X.loc[train_index,], self.X.loc[test_index,]
            y_train, y_test = self.y[train_index], self.y[test_index]
            model.fit(X_train, y_train)
            predicciones = model.predict(X_test)
            score = model.score(X_test, y_test)
            resultados += score
            print(score)

        print('Average Accuracy: ', (resultados/10))


# Ejemplo
training = Training()
model, cm = training.train('nb', '/Noticias/NoOdio', '/Noticias/Odio')
training.graphConfusionMatrix(cm)



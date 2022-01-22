import tratamientoNoticias as tn
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
# Algoritmos de ML
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn import preprocessing # Preprocesado para SVM
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
        if (pathNoOdio != self.pathNoOdio or pathOdio != self.pathOdio ):
            if os.path.exists("diccionario.txt"):
                os.remove("diccionario.txt")
            if os.path.exists("IDFlist.txt"):
                os.remove("IDFlist.txt")

            self.pathNoOdio = pathNoOdio
            self.pathOdio = pathOdio
            
            # Create the matrix with the new news
            self.matriz = tn.addVectoresToMatrizByFolderPath(pathNoOdio, self.matriz, -1, 10)
            self.matriz = tn.addVectoresToMatrizByFolderPath(pathOdio, self.matriz, 1, 10)

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
            self.X = df2.drop("odio_", axis=1)
            self.y = df2['odio_']
        


    def train(self, algorithm: str, pathNoOdio: str, pathOdio: str):
        self.checkPaths(pathNoOdio, pathOdio)
        model = None 
        cm = None
        if algorithm == 'arbol':
            model = tree.DecisionTreeClassifier()
        elif algorithm == 'knn':
            model = KNeighborsClassifier(n_neighbors = 3, n_jobs = -1)
        elif algorithm == 'nb':
            model = GaussianNB()
        elif algorithm == 'perceptron':
            model = Perceptron(tol=1e-3, random_state=0)
        elif algorithm == 'reglog':
            model = LogisticRegression()
        elif algorithm == 'svm':
            model = SVC(kernel="linear")

        
        if model != None:
            # Crea una copia del dataframe X, para poder escalarlo
            # en caso de usar SVM
            X_local = self.X
            if algorithm in ["svm", "reglog", "knn"]:
                X_local = self.X.copy(deep=True)
                X_local = preprocessing.scale(X_local)

            X_train, X_test, y_train, y_test = train_test_split(X_local, self.y, test_size =.3)

            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            cm = confusion_matrix(y_test, predictions, labels=model.classes_)
        
        return model, cm

    def saveModel(self, file, model):
        with open(file, 'wb') as f:
            pickle.dump(model, f)

    def graphConfusionMatrix(self, cm): 
        plt.close("all")

        categories = ['No Odio', 'Odio']
        group_names = ['True Neg','False Pos','False Neg','True Pos']
        group_counts = ['{0:0.0f}'.format(value) for value in cm.flatten()]
        group_percentages = ['{0:.2%}'.format(value) for value in cm.flatten()/np.sum(cm)]
        labels = [f'{v1}\n{v2}\n{v3}' for v1, v2, v3 in zip(group_names,group_counts,group_percentages)]
        labels = np.asarray(labels).reshape(2,2)

        plot, ax = plt.subplots(figsize = (7,5), dpi = 70)

        sns.heatmap(cm, annot=labels, fmt='', cmap='Blues', xticklabels=['pred. NoOdio', 'pred. Odio'],yticklabels=['True NoOdio', 'True Odio'])
        
        return plot
    
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

    def countProcessedNews(self):
        noodio = (self.df.odio_ == '-1').sum()
        odio = (self.df.odio_ == '1').sum()
        return noodio, odio


# Ejemplo
'''training = Training()
training.pathNoOdio = '/Users/sol/Documents/UEM_3ero/ProyectoI/Proyecto-1-noticias/Noticias/NoOdio'
training.pathOdio = '/Users/sol/Documents/UEM_3ero/ProyectoI/Proyecto-1-noticias/Noticias/Odio'
model, cm = training.train('nb', '/Users/sol/Documents/UEM_3ero/ProyectoI/Proyecto-1-noticias/Noticias/NoOdio', '/Users/sol/Documents/UEM_3ero/ProyectoI/Proyecto-1-noticias/Noticias/Odio')
#training.graphConfusionMatrix(cm)
print(training.countProcessedNews())'''



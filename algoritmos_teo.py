# pip install -U scikit-learn
from sklearn import preprocessing
# pip install pandas
import pandas as pd
import numpy as np
from tratamientoNoticias import transformMatrizToPandasDataFrame as df_from_matriz

import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import os
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

def funcion_de_antes(ruta1, ruta2, algoritmo):
    m1 = tn.generarMatriz("matriz2.txt")
    df = tn.transformMatrizToPandasDataFrame(m1)
    '''m1 = tn.generarMatriz("matrizTFIDF2.txt")
    df = tn.transformMatrizToPandasDataFrame(m1)'''
    df.fillna(0, inplace=True)

    cm, modelo = reg_log(df)

    return cm, modelo
    # comprobar lo de la matriz
    # crear un dataframe a partir de la matriz: dataframe = matriz_to_df()
    # segun algoritmo llamar a una funcion u otra: matriz_confusion, modelo = k_nn(dataframe)
    # hacer return de matriz_confusion, modelo
    # ya en la interfaz recoger estos valores, mostrar uno y guardar el otro

def k_nn(dataframe):
    nbrs = KNeighborsClassifier(n_neighbors = 3, n_jobs = -1)

    df2 = dataframe.drop("nombre_", axis=1)
    X = df2.drop("odio_", axis=1)
    y = df2['odio_']
    
    # Dividir conjunto de datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =.5)

    # Entrenar
    nbrs.fit(X_train, y_train)
    predictions = nbrs.predict(X_test)

    # Matriz de confusión
    cm = confusion_matrix(y_test, predictions, labels=nbrs.classes_)
    
    print(np.mean(predictions == y_test))

    return cm, nbrs

def reg_log(dataframe):
    logreg = LogisticRegression()

    df2 = dataframe.drop("nombre_", axis=1)
    X = df2.drop("odio_", axis=1)
    y = df2['odio_']
    
    # Dividir conjunto de datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =.5)

    # Entrenar
    logreg.fit(X_train, y_train)
    predictions = logreg.predict(X_test)

    # Matriz de confusión
    cm = confusion_matrix(y_test, predictions, labels=logreg.classes_)

    print(np.mean(predictions == y_test))

    return cm, logreg

# funcion_de_antes("a","a","a")
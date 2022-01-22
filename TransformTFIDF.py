import math
import pandas as pd
import tratamientoNoticias as tn
import numpy
import os
# LEER PARA USAR:
'''
matrixToTFIDF: para transformar la matriz
listToTFIDF: para transformar una lista externa
indexListToTFIDF: para transformar solo una fila de la matriz
'''
IDF_FILE_RPATH = "IDFlist.txt"

# Devuelve la matriz entera en TFIDF
def matrixToTFIDF(m, pathIDFlist= "IDFList.txt", pathWordlist= "diccionario.txt"):
    new_m = []
    df = m
    if type(m) == list:
        df = tn.transformMatrizToPandasDataFrame(m, pathWordlist)

    IDFlist = None
    if os.path.isfile(pathIDFlist):
        print("holi")
        listaIDF = numpy.loadtxt(pathIDFlist)
    else:
        listaIDF = getIDFlistOfMatriz(df)
        numpy.savetxt(IDF_FILE_RPATH, listaIDF)

    for i in range(len(df)):
        print("Posicion de lista operandose TFIDF:", i)
        new_m.append(indexListToTFIDF(df, i, listaIDF))

    return new_m
#Para transformar una fila de una matriz en TFIDF
def indexListToTFIDF(matriz, index: int, listaIDF: list):
    v = matriz.iloc[index, 2:]
    new_list = list(matriz.iloc[index, :2])  # Lista a devolver, conteniendo odio y fichero de base

    if len(matriz.iloc[0, 2:]) == len(v):
        n_words = sum(v)
        for i, w in enumerate(v):
            tf = w / n_words
            idf = listaIDF[i]
            result = tf * idf
            # numpy.append(new_list,result)
            new_list.append(result)
    return new_list

def getIDFlistOfMatriz(matriz: pd.DataFrame):
    lista = list(matriz.iloc[:, 2:].gt(0).sum())
    n_lista = []
    for w_counter in lista:
        oper = len(matriz.index) / w_counter
        idf = math.log10(oper)
        n_lista.append(idf)
    return n_lista

# Devuelve una lista externa a la matriz en TFIDF
def listToTFIDF(m, extVector: list):
    new_list = []  # Lista a devolver
    matriz = m.copy()
    v = extVector.copy()
    if len(matriz[0]) == len(v):
        matriz.append(v)
        n_words = sum(v)
        for i, w in enumerate(v):
            tf = w / n_words

            w_in_docs_counter = 0
            for row in matriz:
                if row[i] > 0:
                    w_in_docs_counter += 1

            oper = len(matriz)/w_in_docs_counter

            idf = math.log10(oper)
            result = tf * idf
            new_list.append(result)

    return new_list



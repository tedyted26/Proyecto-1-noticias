import math

# LEER PARA USAR:
'''
matrixToTFIDF: para transformar la matriz
listToTFIDF: para transformar una lista externa
indexListToTFIDF: para transformar solo una fila de la matriz
'''


# Devuelve la matriz entera en TFIDF
def matrixToTFIDF(matriz):
    new_m = []
    listaIDF = getIDFlistOfMatriz(matriz)
    for i in range(len(matriz)):
        print("Posicion de lista operandose TFIDF:", i)
        new_m.append(indexListToTFIDF(matriz, i, listaIDF))
    return new_m
#Para transformar una fila de una matriz en TFIDF
def indexListToTFIDF(matriz, index: int, listaIDF: list):
    v = matriz[index][2:]
    new_list = matriz[index][:2]  # Lista a devolver, conteniendo odio y fichero de base
    if len(matriz[0]) - 2 == len(v):
        n_words = sum(v)
        for i, w in enumerate(v):
            tf = w / n_words
            idf = listaIDF[i]
            result = tf * idf
            new_list.append(result)
    return new_list

def getIDFlistOfMatriz(matriz):
    lista = []
    for i in range(len(matriz[0][2:])):
        print("    + Columna:", i)
        w_in_docs_counter = 0
        for row in matriz:
            r = row[2:]
            if r[i] > 0:
                w_in_docs_counter += 1

        oper = len(matriz) / w_in_docs_counter

        idf = math.log10(oper)
        lista.append(idf)
    return lista

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



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
    for i in range(len(matriz)):
        new_m.append(indexListToTFIDF(matriz, i))
    return new_m
#Para transformar una fila de una matriz en TFIDF
def indexListToTFIDF(matriz, index: int):
    new_list = [] # Lista a devolver

    v = matriz[index]
    if len(matriz[0]) == len(v):
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

def testTransformations():
    m = [[1, 0 ,0],
         [0, 1, 0],
         [3, 1, 1]]
    m2 = m.copy()
    for i in range(len(m)):
        print(f"indexList:{indexListToTFIDF(m2, i)}")

    n = [[1, 0 ,0],
         [0, 1, 0]]
    v = [3, 1, 1]
    print(f"list:{listToTFIDF(n, v)}")

    print(f"matrix:{matrixToTFIDF(m2)}")




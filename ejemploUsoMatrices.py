import tratamientoNoticias as tn
from copy import deepcopy

def introducir_Noticias_unlabeled_En_La_Matriz_y_guardar():
    m1 = tn.generarMatriz("matriz2.txt")

    m1 = tn.addVectoresToMatrizByFolderPath("/Noticias/unlabeled", m1, 0)

    tn.saveMatrizToFile(m1, "matriz2.txt")

def introducir_10_Noticias_odio_En_La_Matriz_y_guardar_forma_manual():
    m1 = tn.generarMatriz("matriz2.txt")

    paths = tn.getAllNewsUrlList("/Noticias/NoOdio")[:200]

    vectores = []
    for n, i in enumerate(paths):
        try:
            print(n)
            textoNoticia = tn.leerNoticia(i[0])
            vectores.append(tn.generarVectorDeTexto(textoNoticia, True, i[1], odio= -1))
        except:
            print(f"Error generando vector en archivo: {i[1]}")
    m2 = deepcopy(m1)
    for n, v in enumerate(vectores):
        print(n)
        m2 = tn.addVectorToMatriz(m2, v)

    tn.saveMatrizToFile(m2, "matriz2.txt")

def transformar_y_mostrar_matriz_en_TFIDF():
    print("inicio")
    m1 = tn.generarMatriz("matriz2.txt")
    print("fin")
    m1_tf = tn.tfidf.matrixToTFIDF(m1)
    print("fin tfdif")
    print(m1_tf)
    tn.saveMatrizToFile(m1_tf, "matrizTFIDF2.txt")

# introducir_10_Noticias_odio_En_La_Matriz_y_guardar_forma_manual()
transformar_y_mostrar_matriz_en_TFIDF()
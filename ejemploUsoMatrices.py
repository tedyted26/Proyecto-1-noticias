import tratamientoNoticias as tn

def introducir_Noticias_NoOdio_En_La_Matriz_y_guardar():
    m1 = tn.generarMatriz("matriz.txt")

    m1 = tn.addVectoresToMatrizByFolderPath("/Noticias/NoOdio")
    
    tn.saveMatrizToFile(m1, "matriz.txt")

def transformar_y_mostrar_matriz_en_TFIDF():
    m1 = tn.generarMatriz("matriz.txt")
    m1_tf = tn.tfidf.matrixToTFIDF(m1)
    print(m1_tf)
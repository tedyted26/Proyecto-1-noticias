import tratamientoNoticias as tn

def introducir_10_Noticias_Odio():
    m1 = tn.generarMatriz("matriz.txt")
    # m1_tf = tfidf.matrixToTFIDF(m1)
    # print()
    paths = tn.getAllNewsUrlList("/Noticias/NoOdio")[:10]

    vectores = []
    for i in paths:
        textoNoticia = tn.leerFichero(i[0])
        vectores.append(tn.generarVectorDeTexto(textoNoticia, True, i[1], odio=-1))

    for v in vectores:
        m1 = tn.addVectorToMatriz(m1, v)
    tn.saveMatrizToFile(m1, "matriz.txt")

m1 = tn.generarMatriz("matriz.txt")
m1_tf = tn.tfidf.matrixToTFIDF(m1)
print()
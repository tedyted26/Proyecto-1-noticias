import os
import re
import spacy
import numpy
from copy import deepcopy
import TransformTFIDF as tfidf

rutaListaParada = "listaParada.txt"
rutaWordList = "diccionario.txt"

# Metodos de Tratamiento de ficheros
def tokenizacion(texto):
    nlp = spacy.load('es_core_news_sm')

    doc = nlp(texto)  # Crea un objeto de spacy tipo nlp
    tokens = [t.orth_ for t in doc]  # Crea una lista con las palabras del texto
    return tokens


def tratamientoBasico(tokens):
    caracteres = "0123456789ºª!·$%&/()=|@#~€¬'?¡¿`+^*[]´¨}{,.-;:_<>\n \""
    listaTratada = []
    for token in tokens:
        for i in range(len(caracteres)):
            token = token.replace(caracteres[i], "")
        if (token != ""):
            listaTratada.append(token.lower())
    return listaTratada


def listaParada(tokens):
    listaParada = tratamientoBasico(tokenizacion(rutaListaParada))
    listaDepurada = []
    for token in tokens:
        encontrado = False
        i = 0
        while (encontrado == False and i < len(listaParada)):
            if (token == listaParada[i]):
                encontrado = True
            i += 1
        if encontrado == False and len(token) > 2:
            listaDepurada.append(token)
    return listaDepurada


def lematizacion(tokens):
    nlp = spacy.load('es_core_news_sm')
    texto = ""
    for token in tokens:
        texto += token + " "
    doc = nlp(texto)
    lemmas = [tok.lemma_ for tok in doc]
    return lemmas
def leerNoticia(rutaFichero):
    f = open(rutaFichero, 'r')
    texto = f.read()
    if ";-;" in texto:
        texto = texto.replace("titulo;-;url;-;url_completa;-;autor;-;fecha;-;hora;-;subtitulo;-;texto", "")
        texto = texto.replace(";-;"," ")
    else:
        texto = re.sub("##+", " ", texto)
    return texto

def leerFichero(rutaFichero):
    f = open (rutaFichero,'r')
    texto = f.read()
    f.close()
    return texto

def tratarTexto(t):
    tokens = tokenizacion(t)
    print(f"TOKENS:{tokens}\n")
    tBasico = tratamientoBasico(tokens)
    print(f"TRAT BASICO:{tBasico}\n")
    t_postListaParada = listaParada(tBasico)
    print(f"LISTA:{t_postListaParada}\n")
    lemas = lematizacion(t_postListaParada)
    print(f"LEMAS:{lemas}\n")
    return lemas

def generarVectorDeTexto(t: str, saveWorlist: bool):
    t2 = tratarTexto(t)

    wordlist = []
    vector = []
    if os.path.isfile(rutaWordList):  # Compruebo si existe el fichero
        wordlist = leerFichero(rutaWordList).splitlines()
        vector = [0 for i in range(len(wordlist))]
    # Por cada palabra de la noticia, añadimos las nuevas al diccionario y al vector
    # correspondiente a la matriz
    for token in t2:
        if token not in wordlist:
            wordlist.append(token)
            vector.append(1)
        else:
            for i, word in enumerate(wordlist):
                if word == token:
                    vector[i] += 1
    if saveWorlist:
        f = open(rutaWordList, "w")
        for elemento in wordlist:
            f.write(elemento + "\n")
        f.close()
    return vector

def generarMatriz(fichero: str):
    rutaMatriz = fichero
    matriz = []
    if os.path.isfile(rutaMatriz):  # Compruebo si existe el fichero
        f = open(rutaMatriz)
        filas = f.read().split(";\n")
        matriz = [[int(val) for val in fila.split(" ")] for fila in filas]
    return matriz

def addVectorToMatriz(matriz, v):
    m = deepcopy(matriz)
    idma=id(matriz)
    idm = id(m)
    if len(m) > 0:
        diffMatrizVector = len(v) - len(m[0])
        for row in m:
            row += [0 for i in range(diffMatrizVector)]

    m.append(v)
    return m
def saveMatrizToFile(m, file):
    f = open(file, "w")
    for i,fila in enumerate(m):
        str_fila = [str(ele) for ele in fila]
        res = " ".join(str_fila)
        if i > 0:
            res = ";\n" + res
        f.write(res)
    f.close()


def getAllNewsUrlList(newsFolderPath):
    r = os.getcwd() + newsFolderPath
    return [r+"/"+i for i in os.listdir(r)]

m1 = generarMatriz("matriz.txt")
m1_tf = tfidf.matrixToTFIDF(m1)
print()



# paths= getAllNewsUrlList("/Noticias/unlabeled")

# textosNoticias = [leerFichero(i) for i in paths]
# vectores = [generarVectorDeTexto(t, True) for t in textosNoticias]

# for v in vectores:
#     m1 = addVectorToMatriz(m1, v)
# saveMatrizToFile(m1,"matriz.txt")
print()


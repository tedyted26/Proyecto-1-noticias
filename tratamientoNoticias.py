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
    '''Lee un archivo de noticia, devolviendo el texto al completo'''
    f = open(rutaFichero, 'r')
    texto = f.read()
    if ";-;" in texto:
        texto = texto.replace("titulo;-;url;-;url_completa;-;autor;-;fecha;-;hora;-;subtitulo;-;texto", "")
        texto = texto.replace(";-;"," ")
    else:
        texto = re.sub("##+", " ", texto)
    return texto

def leerFichero(rutaFichero):
    '''Lee el fichero y devuelve el texto segun la ruta'''
    f = open (rutaFichero,'r')
    texto = f.read()
    f.close()
    return texto

def tratarTexto(t):
    '''Aplica un tratamiento al texto, segmentandolo en una lista de palabras con la que poder
    despues añadir el texto a una matriz.'''
    tokens = tokenizacion(t)
    print(f"TOKENS:{tokens}\n")
    tBasico = tratamientoBasico(tokens)
    print(f"TRAT BASICO:{tBasico}\n")
    t_postListaParada = listaParada(tBasico)
    print(f"LISTA:{t_postListaParada}\n")
    lemas = lematizacion(t_postListaParada)
    print(f"LEMAS:{lemas}\n")
    return lemas

def generarVectorDeTexto(t: str, saveWordlist: bool, file: str,odio: int = 0):
    '''Genera un vector de texto a partir del texto/string "t" proporcionado, tratandolo
    en el proceso y elminando terminos superfluos.
    Los argumentos son los siguientes:

    - t: El texto a transformar

    - saveWordlist: Este booleano determina si las nuevas palabras descubiertas deben ser añadidas
    al archivo de wordlist. Esto sirve para poder generar vectores y palabras permanentes en la matriz
    o para generar vectores temporales que puedan operar con los resultados anteriores de la matriz.

    - file: el archivo del que proviene el texto, el cual se almacena en la 2da posicion del vector

    - odio: determina si la noticia es de odio (1), no odio (-1) o desconocida (0), almacenandose
    en la 1ª posicion del vector'''
    t2 = tratarTexto(t)

    wordlist = []
    vector = []
    '''Añade al vector si es de odio, no odio o desconocido y el nombre del archivo'''
    vector += [odio, file]

    if os.path.isfile(rutaWordList):  # Compruebo si existe el fichero
        wordlist = leerFichero(rutaWordList).splitlines()
        vector += [0 for i in range(len(wordlist))]
    # Por cada palabra de la noticia, añadimos las nuevas al diccionario y al vector
    # correspondiente a la matriz
    for token in t2:
        if token not in wordlist:
            wordlist.append(token)
            vector.append(1)
        else:
            for i, word in enumerate(wordlist):
                if word == token:
                    vector[i+2] += 1
    if saveWordlist:
        f = open(rutaWordList, "w")
        for elemento in wordlist:
            f.write(elemento + "\n")
        f.close()

    return vector

def generarMatriz(fichero: str):
    '''Genera y devuelve la matriz a partir del fichero seleccionado
    -fichero: ruta y nombre del archivo (ejemplo: "matriz.txt")'''
    rutaMatriz = fichero
    matriz = []
    if os.path.isfile(rutaMatriz):  # Compruebo si existe el fichero
        f = open(rutaMatriz)
        filas = f.read().split(";\n")
        matriz = []
        for fila in filas:
            filaSp = fila.split(" ")
            matriz.append([val for val in filaSp[0:2]] + [int(val) for val in filaSp[2:]])

        # matriz = [[int(val) for val in fila.split(" ")] for fila in filas]
    return matriz

def addVectorToMatriz(matriz, v):
    '''Devuelve una matriz, producto de la suma de una copia de la matriz proporcionada y 
    de un vector "v".
    En caso del que el vector sea mayor que el tamaño de las filas de la matriz, amplia la matriz
    añadiendo tantos "0" a la derecha como diferencia haya.'''
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
    '''Guarda la matriz en un archivo, separando los valores de cada fila con
    espacios y las filas con ";\n"'''
    f = open(file, "w")
    for i,fila in enumerate(m):
        str_fila = [str(ele) for ele in fila]
        res = " ".join(str_fila)
        if i > 0:
            res = ";\n" + res
        f.write(res)
    f.close()


def getAllNewsUrlList(newsFolderPath):
    '''Devuelve una lista rellena de tuplas: (pathcompleto, nombre)
    Esta lista contiene todos los archivos encontrados en la carpeta proporcionada,
    la cual debe ser una carpeta en la que se almacenen las noticias'''
    r = os.getcwd() + newsFolderPath
    return [(r+"/"+i, i) for i in os.listdir(r)]

def addVectoresToMatrizByFolderPath(path: str, m: list, odio: int):
    '''Devuelve una nueva matriz con las noticias proporcionadas a traves la carpeta en la que
    se encuentran.
    
    -path: la carpeta donde se encuentran las noticias (ej:"/Noticias/NoOdio)
    -m: la matriz inicial
    -odio: Si la noticia es de odio (1), no odio (-1) o desconocida (0)"'''
    paths = getAllNewsUrlList(path)
    m1 = m

    vectores = []
    for i in paths:
        textoNoticia = leerFichero(i[0])
        vectores.append(generarVectorDeTexto(textoNoticia, True, i[1], odio= odio))

    for v in vectores:
        m1 = addVectorToMatriz(m1, v)
    return m1




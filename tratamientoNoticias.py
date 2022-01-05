import os
import re
import spacy
import numpy

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
    fichero = texto.splitlines()
    return fichero

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
        wordlist = leerFichero(rutaWordList)
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

def generarMatriz():
    rutaMatriz = "matriz.txt"
    matriz = []
    if os.path.isfile(rutaMatriz):  # Compruebo si existe el fichero
        f = open(rutaMatriz)
        filas = f.read().split(";\n")
        matriz = [fila.split(" ") for fila in filas]
    return matriz

def addVectorToMatriz(m, v):
    if len(m) > 0:
        diffMatrizVector = len(v) - len(m[0])
        for row in m:
            row += [0 for i in range(diffMatrizVector)]

    m.append(v)
# t = leerNoticia("Noticias/unlabeled/odio20Minutos-Homofobia-agoney-sobre-el-estreno-de-tu-cara-me-suena-vuelvo-a-la-tele-pero-no-useis-la-homofobia-como-arma-en-mi-contra.txt")
# t = leerNoticia("Noticias/unlabeled/odioLaRazon_20211201_0_40.txt")
t = "Hola que chuliguapi la caravana de la caravana, ojo que guay la caravana "

v = generarVectorDeTexto(t, False)
m = generarMatriz()
addVectorToMatriz(m, v)
print()

# SVM y arboles
import tratamientoNoticias as tn
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas

import time

def train_SVM(dframe: pandas.DataFrame):
    '''Toma el dataframe y entrena mediante SVM, devolviendo una
    tupla (matriz de confusión, modelo)'''
    df = dframe.sample(frac=1)
    df.fillna(0, inplace=True)

    df_train, df_test = train_test_split(df, test_size=0.2)

    X = preprocessing.scale(df_train.drop(["nombre_", "odio_"], axis=1))
    y = df_train['odio_'] == 1
    X_test = preprocessing.scale(df_test.drop(["nombre_", "odio_"], axis=1))
    y_test = df_test['odio_'] == 1

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    Y_pred_test = clf.predict(X_test)

    print(np.mean(y_test == Y_pred_test))
    print(list(y_test))
    print(list(Y_pred_test))

    cm = confusion_matrix(y_test, Y_pred_test, labels= clf.classes_)
    return cm, clf


def test_train_SVM():
    t_ini = time.time()
    m2 = tn.addVectoresToMatrizByFolderPath("/Noticias/Odio", [], 1, max_noticias=40)
    t_med = time.time()
    m2 = tn.addVectoresToMatrizByFolderPath("/Noticias/NoOdio", m2, -1, max_noticias=40)
    t_fin = time.time()
    print(f"Tiempo 50 primeras: {t_med-t_ini}\n"
          f"Tiempo 50 restantes: {t_fin-t_med}\n"
          f"Tiempo total: {t_fin-t_ini}\n")
    m1_tfidf = tn.tfidf.matrixToTFIDF(m2)
    df = tn.transformMatrizToPandasDataFrame(m1_tfidf)
    print(train_SVM(df))

test_train_SVM()

# SVM y arboles
import tratamientoNoticias as tn
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import numpy as np
import pandas

import time

def train_SVM(dframe: pandas.DataFrame):
    df = dframe.sample(frac=1)
    df.fillna(0, inplace=True)

    df_train, df_test = train_test_split(df, test_size=0.2)

    X = preprocessing.scale(df_train.drop(["nombre_", "odio_"], axis=1))
    y = df_train['odio_'] == "1"
    X_test = preprocessing.scale(df_test.drop(["nombre_", "odio_"], axis=1))
    y_test = df_test['odio_'] == "1"

    clf = SVC(kernel="linear")  # Probad con los distintos kernels: kernel = "linear"; kernel = "poly"; kernel = "rbf"; kernel = "sigmoid"
    clf = clf.fit(X, y)
    Y_pred_test = clf.predict(X_test)

    print(np.mean(y_test == Y_pred_test))
    print(list(y_test))
    print(list(Y_pred_test))


print("\u2018 hi \u2019")

t_ini = time.time()
m2 = tn.addVectoresToMatrizByFolderPath("/Noticias/Odio", [], 1, max_noticias=20)
t_med = time.time()
m2 = tn.addVectoresToMatrizByFolderPath("/Noticias/NoOdio", m2, -1, max_noticias=20)
t_fin = time.time()
print(f"Tiempo 50 primeras: {t_med-t_ini}\n"
      f"Tiempo 50 restantes: {t_fin-t_med}\n"
      f"Tiempo total: {t_fin-t_ini}\n")
tn.saveMatrizToFile(m2, "m_tocha.txt")

df = tn.transformMatrizToPandasDataFrame(m2)
# m2 = tn.generarMatriz("m_normal.txt")
# m1_tfidf = tn.tfidf.matrixToTFIDF(m2)
# tn.saveMatrizToFile(m1_tfidf, "m_tfidf.txt")
# m1_tfidf = tn.generarMatriz("m_tfidf.txt")
# df = tn.transformMatrizToPandasDataFrame(m1_tfidf)
#
# train_SVM(df)



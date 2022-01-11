import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
import tratamientoNoticias as tn

m1 = tn.generarMatriz("matriz2.txt")
df = tn.transformMatrizToPandasDataFrame(m1)
'''m1 = tn.generarMatriz("matrizTFIDF2.txt")
df = tn.transformMatrizToPandasDataFrame(m1)'''
df.fillna(0, inplace=True)

df2 = df.drop("nombre_", axis=1)
X = df2.drop("odio_", axis=1)
y = df2['odio_']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
gnb = GaussianNB()

# Ajustamos el modelo con fit
gnb.fit(X_train, y_train)
# Obtenemos las predicciones
Y_pred = gnb.predict(X_test)

# 95,59% de las predicciones es correcta. Vemos en qué caso nuestras predicciones coinciden con el valor real.
print(np.mean(Y_pred == y_test))

confusion_matrix = confusion_matrix(y_test, Y_pred)
print(confusion_matrix)


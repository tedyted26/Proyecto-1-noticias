import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import os
import sys

# código copiado de GeeksforGeeks.org para conseguir importar archivos fuera de la carpeta
  
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)

import tratamientoNoticias as tn


m1 = tn.generarMatriz("matriz.txt")
m1_tf = tn.tfidf.matrixToTFIDF(m1)
df = tn.transformMatrizToPandasDataFrame(m1_tf)
'''m1 = tn.generarMatriz("matrizTFIDF2.txt")
df = tn.transformMatrizToPandasDataFrame(m1)'''
df.fillna(0, inplace=True)

df2 = df.drop("nombre_", axis=1)
X = df2.drop("odio_", axis=1)
y = df2['odio_']

gnb = GaussianNB()

# Cross-validation  
kf = KFold(n_splits = 10, shuffle = True)
kf.get_n_splits(X)
resultados = 0.0
for train_index, test_index in kf.split(X):
    X_train, X_test = X.loc[train_index,], X.loc[test_index,]
    y_train, y_test = y[train_index], y[test_index]
    gnb.fit(X_train, y_train)
    predicciones = gnb.predict(X_test)
    score = gnb.score(X_test, y_test)
    resultados += score
    print(score)

print('Average Accuracy: ', (resultados/10))


# Graficar la matriz
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =.5)
gnb.fit(X_train, y_train)
predictions = gnb.predict(X_test)
cm = confusion_matrix(y_test, predictions, labels=gnb.classes_)

import seaborn as sns
import numpy as np

categories = ['No Odio', 'Odio']
group_names = ['True Neg','False Pos','False Neg','True Pos']
group_counts = ['{0:0.0f}'.format(value) for value in cm.flatten()]
group_percentages = ['{0:.2%}'.format(value) for value in cm.flatten()/np.sum(cm)]
labels = [f'{v1}\n{v2}\n{v3}' for v1, v2, v3 in zip(group_names,group_counts,group_percentages)]
labels = np.asarray(labels).reshape(2,2)
sns.heatmap(cm, annot=labels, fmt='', cmap='Blues', xticklabels=categories, yticklabels=categories)

plt.show()
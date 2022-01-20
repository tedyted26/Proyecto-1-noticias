import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
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

# os.chdir("D:\\David\\Documentos\\UNI\\UNI 3\\SIyRC\\proyecto1\\repoGit\\Proyecto-1-noticias")
# print(os.getcwd())
import tratamientoNoticias as tn


m1 = tn.generarMatriz("matriz2.txt")
df = tn.transformMatrizToPandasDataFrame(m1)
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
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=gnb.classes_)
disp.plot()

print('Informe de clasificación:\n\n', classification_report(y_true=y_test, y_pred=predictions, target_names=['No odio', 'Odio'])) 

plt.show()


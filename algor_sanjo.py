# SVM y arboles
import tratamientoNoticias as tn
m1 = tn.generarMatriz("matriz2.txt")
df = tn.transformMatrizToPandasDataFrame(m1)
print(df.columns)

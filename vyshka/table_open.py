import pandas as pd
data = pd.read_excel('Tablitsa.xls', "Игра №1", usecols=[2, 6, 7, 8, 9, 10, 11, 12, 16], skiprows=2)
data_dropna = data.dropna()
print(data_dropna)
import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


'''
ZADANIE 1
'''
excel_data = pd.read_excel(r'dane.xlsx', sheet_name='Dane')
data = pd.DataFrame(excel_data, columns=['Wiek', 'Masa', 'F_ram', 'F_łop', 'F_biod', 'F_gol'])
select_data = data.loc[(data['Wiek'] < 12.51) & (data['Wiek'] >= 11.50)].copy()
select_data.loc[:, 'F_sr'] = select_data[['F_ram', 'F_łop', 'F_biod', 'F_gol']].mean(axis=1)
final_data = select_data[['Masa', 'F_sr']]
np.savetxt(r'dane.txt', final_data.values, fmt='%1.2f')

dane_fs = []
dane_masa = []

with open("dane.txt", 'r') as fi:
    for line in fi:
        if line.split():
            data = [float(x) for x in line.split()]
            dane_masa.append(data[0])
            dane_fs.append(data[1])

print("Dane dla fs:", dane_fs)
print("Dane dla masa:", dane_masa)

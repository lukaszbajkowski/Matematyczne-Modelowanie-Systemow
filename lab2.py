import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def create_series(data, h, x01):
    maximum = np.max(data)
    x11 = x01
    compartments = []
    numbers = []
    ranges = [x01]
    centers = []
    while x11 < maximum:
        x11 = x01 + h
        n1 = len([x for x in data if (x01 <= x < x11)])
        compartments.append([x01, x11])
        numbers.append(n1)
        ranges.append(x11)
        centers.append((x01 + x11) / 2)
        x01 = x11
    return compartments, numbers, ranges, centers


def determine_cumulative(abundance):
    cumulative = [abundance[0]]
    for items in range:
        cumulative.append(cumulative[items - 1] + abundance[items])
    return cumulative


'''
ZADANIE 1
'''
excel_data = pd.read_excel(r'dane.xlsx',sheet_name='Dane')
data = pd.DataFrame(excel_data, columns=['Wiek', 'Wys', 'Masa'])
select_data = data.loc[(data['Wiek'] < 13) & (data['Wiek'] >= 12)]
final_data = select_data[['Wys', 'Masa']]
final_data_no_weight = select_data[['Wys', 'Masa']]

np.savetxt(r'dane.txt', final_data.values, fmt='%1.2f')

dane_sz = []
with open("dane.txt", 'r') as fi:
    for line in fi:
        if line.split():
            line = [float(x) for x in line.split()]
            dane_sz.append(line)

dane = []
for item in dane_sz:
    for number in item:
        dane.append(number)

'''
ZADANIE 2
'''
rohrer_coefficient = []
for item in dane_sz:
    rohrer_coefficient.append((item[1] * 100000) / (item[0] ** 3))

'''
ZADANIE 4, ZADANIE 5
'''
minimum = np.min(rohrer_coefficient)
maximum = np.max(rohrer_coefficient)
n = len(rohrer_coefficient)
rozstep = maximum - minimum
k_rob = round(n ** 0.5, 1)
print("Minimum, Maximum, N, Rozstęp")
print(minimum, maximum, n, rozstep)

k0 = math.sqrt(n)
h_rob = rozstep / k0
print("Wyliczone h:", h_rob)
h0 = h_rob
x01_rob = (minimum - h0 / 2)
print("Wyliczone x01:", x01_rob)
h = 0.01
x01 = 0.8656509748671193

compartments, numbers, ranges, centers = create_series(rohrer_coefficient, h, x01)
print("Liczebności: ", numbers)
print("Przedziały: ", compartments)
print("Zakresy: ", ranges)
print("Środki: ", centers)

skumulowany = determine_cumulative(numbers)
print("Skumulowany: ", skumulowany)

plt.figure(figsize=(12, 3))
plt.hist(rohrer_coefficient, bins=ranges, edgecolor='black')
plt.show()

plt.figure(figsize=(12, 3))
plt.bar(centers, numbers, width=h, edgecolor='black')
plt.plot(centers, numbers, color='red')
plt.show()

plt.figure(figsize=(12, 3))
plt.bar(centers, skumulowany, width=h, edgecolor='black')
plt.plot(centers, skumulowany, color='red')
plt.show()

pr_empiryczne = [x / n for x in numbers]
print("Prawdopodobieństwa empiryczne: ", pr_empiryczne)

plt.figure(figsize=(12, 3))
plt.plot(centers, pr_empiryczne, color='red')
plt.show()

dystr_empiryczna = [x / n for x in skumulowany]
print("Dystrybuanta empiryczna: ", dystr_empiryczna)

plt.figure(figsize=(12, 3))
plt.plot(centers, dystr_empiryczna, color='red')
plt.show()

srednia_lista = [a * b for a, b in zip(centers, numbers)]
srednia = np.sum(srednia_lista) / n
sr_p = np.mean(rohrer_coefficient)
blad_sr = abs(srednia - sr_p) / sr_p
print("Średnia z szeregu: ", srednia)
print("Średnia z próby: ", sr_p)
print("Błąd oszacowania średniej: ", blad_sr)

kwadr_lista = [(x - srednia) ** 2 for x in centers]
war_lista = [a * b for a, b in zip(kwadr_lista, numbers)]
wariancja = np.sum(war_lista) / n
odchylenie_stand = wariancja ** 0.5
std_p = np.std(rohrer_coefficient)
blad_std = abs(odchylenie_stand - std_p) / std_p
print("Odchylenie standardowe z szeregu: ", odchylenie_stand)
print("Odchylenie standardowe z próby: ", std_p)
print("Błąd oszacowania odchylenia: ", blad_std)

'''
ZADANIE 7, ZADANIE 8
'''
classes_lundman = {
    'Bardzo lekka': {'min': float('-inf'), 'max': 1.15},
    'Lekka': {'min': 1.15, 'max': 1.25},
    'Średnia': {'min': 1.25, 'max': 1.35},
    'Ciężka': {'min': 1.35, 'max': 1.45},
    'Bardzo ciężka': {'min': 1.45, 'max': float('inf')}
}

counters_classes = {classes: 0 for classes in classes_lundman}

for coefficient in rohrer_coefficient:
    for class_counter, range in classes_lundman.items():
        if range['min'] <= coefficient < range['max']:
            counters_classes[class_counter] += 1
            break

print("Grupy według klasyfikacji Lundmana i ich liczność",counters_classes)
classes = list(counters_classes.keys())
numbers_objects = list(counters_classes.values())

plt.bar(classes, numbers_objects)
plt.show()

klasy_lundmana = [(float('-inf'), 1.15), (1.15, 1.25), (1.25, 1.35), (1.35, 1.45), (1.45, float('inf'))]

plt.figure(figsize=(12, 3))

for i, (lower, upper) in enumerate(klasy_lundmana):
    if lower == float('-inf'):
        lower = np.min(rohrer_coefficient)
    if upper == float('inf'):
        upper = np.max(rohrer_coefficient)
    plt.axvspan(lower, upper, color='C{}'.format(i), alpha=0.3)

plt.hist(rohrer_coefficient, bins=np.arange(min(rohrer_coefficient), max(rohrer_coefficient) + 0.05, 0.05)
         , edgecolor='black', width=0.05)
plt.legend(['< 1.15', '1.15 - 1.25', '1.25 - 1.35', '1.35 - 1.45', '> 1.45'], loc='upper right')
plt.show()

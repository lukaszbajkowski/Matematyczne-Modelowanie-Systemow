import math
import numpy as np
import pandas as pd
import statistics as stat
from scipy.stats import pearsonr


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
    for item in range(1, len(abundance)):
        cumulative.append(cumulative[item - 1] + abundance[item])
    return cumulative


excel_data = pd.read_excel(r'dane.xlsx', sheet_name='Dane')
data = pd.DataFrame(excel_data, columns=['Wiek', 'Masa', 'F_ram', 'F_łop', 'F_biod', 'F_gol'])
select_data = data.loc[(data['Wiek'] < 12.51) & (data['Wiek'] >= 11.50)].copy()
select_data.loc[:, 'F_sr'] = select_data[['F_ram', 'F_łop', 'F_biod', 'F_gol']].mean(axis=1)
final_data = select_data[['Masa', 'F_sr']]
np.savetxt(r'dane.txt', final_data.values, fmt='%1.2f')

dane_fsr = []
dane_masa = []

with open("dane.txt", 'r') as fi:
    for line in fi:
        if line.split():
            data = [float(x) for x in line.split()]
            dane_masa.append(data[0])
            dane_fsr.append(data[1])

print("Dane dla fs:", dane_fsr)
print("Dane dla masy:", dane_masa)

# dane = dane_masa
dane = dane_fsr

minimum = np.min(dane)
maximum = np.max(dane)
n = len(dane)
range_data = maximum - minimum
k_temp = round(n ** 0.5, 1)
print("Minimum:", minimum)
print("Maximum:", maximum)
print("N:", n)
print("Rozstęp:", range_data)

k0 = math.sqrt(n)
h_temp = range_data / k0
print("Wyliczone h:", h_temp)
h0 = h_temp
x01_rob = (minimum - h0 / 2)
print("Wyliczone x01:", x01_rob)

# Masa
# h = 3.58
# x01 = 24.81

# FS
h = 2.18
x01 = 3.4

interval, abundance, scope, appropriations = create_series(dane, h, x01)
cumulative = determine_cumulative(abundance)
print("Liczebności: ", abundance)
print("Zakresy: ", np.round(scope, 2))
print("Skumulowany: ", cumulative)

mean_list = [a * b for a, b in zip(appropriations, abundance)]
mean_p = np.mean(dane)
mean = np.sum(mean_list) / n
mean_error = abs(mean - mean_p) / mean_p
print("Średnia z próby: ", mean_p)
print("Średnia z szeregu: ", mean)
print("Błąd oszacowania średniej: ", mean_error)

squared_list = [(x - mean) ** 2 for x in appropriations]
product_list = [a * b for a, b in zip(squared_list, abundance)]
variance = np.sum(product_list) / n
std_deviation = variance ** 0.5
std_deviation_p = np.std(dane)
std_error = abs(std_deviation - std_deviation_p) / std_deviation_p
print("Odchylenie standardowe z próby: ", std_deviation_p)
print("Odchylenie standardowe z szeregu: ", std_deviation)
print("Błąd oszacowania odchylenia: ", std_error)

empirical_distribution = [x / n for x in cumulative]
rob_ind = [0 if x < 0.5 else 1 for x in empirical_distribution]
m = rob_ind.index(1)
x0m = interval[m][0]
nm = abundance[m]
hm = interval[m][1] - interval[m][0]
n_sk_1 = cumulative[m - 1]
print("Liczebność próby: ", n)
print("Numer klasy, dla której po raz pierwszy dystrybuanta empiryczna ma wartość większą lub równą 1/2: ", m)
print("Lewy koniec klasy o numerze m: ", x0m)
print("Liczebność klasy o numerze m: ", nm)
print("Liczebność skumulowana o numerze m-1: ", n_sk_1)
print("Długość klasy o numerze m: ", hm)
median_p = np.percentile(dane, 50)
median = x0m + (n / 2 - n_sk_1) * hm / nm
median_error = abs(median_p - median) / median_p
print("Mediana z próby: ", median_p)
print("Mediana: ", median)
print("Błąd oszacowania mediany: ", median_error)

maximum_dominant = np.max(abundance)
d = abundance.index(maximum_dominant)
x0d = interval[d][0]
nd = abundance[d]
hd = interval[d][1] - interval[d][0]
nd_minus1 = abundance[d - 1]
nd_plus1 = abundance[d + 1]
print("Numer klasy, która jest najbardziej liczna: ", d)
print("Lewy koniec klasy o numerze d: ", x0d)
print("Liczebność klasy o numerze d-1: ", nd_minus1)
print("Liczebność klasy o numerze d: ", nd)
print("Liczebność klasy o numerze d+1: ", nd_plus1)
print("Długość klasy o numerze d: ", hd)
dominant_p = stat.mode(dane)
dominant = x0d + (nd - nd_minus1) * hd / (nd - nd_minus1 + nd - nd_plus1)
dominant_error = abs(dominant_p - dominant) / dominant
print("Dominanta z próby: ", dominant_p)
print("Dominanta: ", dominant)
print("Błąd oszacowania dominanty: ", dominant_error)

asymmetry_coefficient_p = (mean_p - dominant_p) / std_deviation_p
asymmetry_coefficient = (mean - dominant) / std_deviation
print("Współczynnik asymetrii z próby: ", asymmetry_coefficient_p)
print("Współczynnik asymetrii: ", asymmetry_coefficient)

mixed_asymmetry_coefficient_p = 3 * (mean_p - median_p) / std_deviation_p
mixed_asymmetry_coefficient = 3 * (mean - median) / std_deviation
print("Mieszany współczynnik asymetrii z próby: ", mixed_asymmetry_coefficient_p)
print("Mieszany współczynnik asymetrii: ", mixed_asymmetry_coefficient)

coefficient_of_variation_p = std_deviation_p / mean_p
coefficient_of_variation = std_deviation / mean
print("Współczynnik zmienności z próby: ", coefficient_of_variation_p)
print("Współczynnik zmienności: ", coefficient_of_variation)

t1_l = round(mean_p - std_deviation_p, 2)
t1_p = round(mean_p + std_deviation_p, 2)
typical1 = [x for x in dane if (t1_l < x < t1_p)]
p_t1 = round(len(typical1) / len(dane), 3)
t2_l = round(mean_p - 2 * std_deviation_p, 2)
t2_p = round(mean_p + 2 * std_deviation_p, 2)
typical2 = [x for x in dane if (t2_l < x < t2_p)]
p_t2 = round(len(typical2) / len(dane), 3)
print("Procent wartości typowe 1: ", p_t1)
print("Procent wartości typowe 2: ", p_t2)

outliers_left = len([x for x in dane if (x <= t2_l)])
outliers_right = len([x for x in dane if (x >= t2_p)])
print("Liczba wartości odstających po lewej stronie: ", outliers_left)
print("Liczba wartości odstających po prawej stronie: ", outliers_right)

corr, p_value = pearsonr(dane_masa, dane_fsr)
print("Współczynnik korelacji Pearsona: ", corr)
print("P value: ", p_value)

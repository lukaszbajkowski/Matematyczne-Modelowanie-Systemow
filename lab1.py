import numpy as np

data_all = []

with open("lab1_dane.txt", 'r') as fi:
    for line in fi:
        if line.split():
            line = [float(x) for x in line.split()]
            data_all.append(line)

set1 = []
set2 = []
set3 = []
set4 = []

for item in data_all:
    set1.append(item[0])
    set2.append(item[1])
    set3.append(item[2])
    set4.append(item[3])

data = set1

x_sr = round(np.mean(data), 2)
s = round(np.std(data), 2)
s_p = round(np.std(data, ddof=1), 2)
w_p = round(np.var(data), 2)
w = round(np.var(data, ddof=1), 2)
Q1 = round(np.percentile(data, 25), 2)
M = round(np.percentile(data, 50), 2)
Q3 = round(np.percentile(data, 75), 2)
minimum = np.min(data)
maximum = np.max(data)

print("Liczebność próby: ", len(data))
print("Średnia: ", x_sr)
print("Wariancja populacji: ", w_p)
print("Odchylenie standardowe populacji: ", s)
print("Wariancja z próby: ", w)
print("Odchylenie standardowe z próby: ", s_p)
print("Kwartyl 1: ", Q1)
print("Mediana: ", M)
print("Kwartyl 3: ", Q3)
print("Minimum: ", minimum)
print("Maximum: ", maximum)

t1_l = round(x_sr - s, 2)
t1_p = round(x_sr + s, 2)
typowe1 = [x for x in data if (t1_l < x < t1_p)]
print("Typowe 1")
print("Lewy Kraniec: " + str(t1_l) + " Prawy Kraniec: " + str(t1_p) + " Wartości: " + str(typowe1))

t2_l = round(x_sr - 2 * s, 2)
t2_p = round(x_sr + 2 * s, 2)
typowe2 = [x for x in data if (t2_l < x < t2_p)]
print("Typowe 2")
print("Lewy Kraniec: " + str(t2_l) + " Prawy Kraniec: " + str(t2_p) + " Wartości: " + str(typowe2))

p_t1 = round(len(typowe1) / len(data), 3)
print("Procent Typowe 1: ", p_t1)
p_t2 = round(len(typowe2) / len(data), 3)
print("Procent Typowe 2: ", p_t2)

odstajace = [x for x in data if (x <= t2_l or x >= t2_p)]
print("Wartości odstające: ", odstajace)

kwz = round(s / x_sr, 2)
print("Klasyczny współczynnik zmienności: ", kwz)

Q = round((Q3 - Q1) / 2, 2)
K_typowe1_l = M - Q
K_typowe1_p = M + Q
K_typowe1 = [x for x in data if (K_typowe1_l < x < K_typowe1_p)]
K_typowe2_l = round(Q3 - 3 * Q, 2)
K_typowe2_p = round(Q3 + 3 * Q, 2)
K_typowe2 = [x for x in data if (K_typowe2_l < x < K_typowe2_p)]
K_odstajace = [x for x in data if (x <= K_typowe2_l or x >= K_typowe2_p)]

print("Odchylenie Ćwiartkowe: ", Q)
print("Kwartylowe Typowe 1")
print("Lewy Kraniec: " + str(K_typowe1_l) + " Prawy Kraniec: " + str(K_typowe1_p) + " Wartości: " + str(K_typowe1))
print("Kwartylowe Typowe 2")
print("Lewy Kraniec: " + str(K_typowe2_l) + " Prawy Kraniec: " + str(K_typowe2_p) + " Wartości: " + str(K_typowe2))
print("Kwartylowe wartości odstające: ", K_odstajace)

v = round(Q / M, 2)
As = round((Q3 - M) - (M - Q1) / 2 * (Q3 - Q1), 2)
mAs = round(3 * (x_sr - M) / s, 2)

print("Kwartylowy współczynnik zmienności: ", v)
print("Kwartylowy współczynnik asymetrii: ", As)
print("Mieszany współczynnik asymetrii: ", mAs)

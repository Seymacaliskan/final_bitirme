
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IPython.display import clear_output
import time

sayilar = []
with open('noktalar.txt', 'r') as file:
    for satir in file:
        satir_sayilar = [float(sayi.strip()) for sayi in satir.strip().split(',')]
        sayilar.append(satir_sayilar)

flat_sayilar = [sayi for satir in sayilar for sayi in satir]
x = flat_sayilar[::6]
y = flat_sayilar[1::6]
dx = flat_sayilar[2::6]
dy = flat_sayilar[3::6]
cx = flat_sayilar[4::6]
cy = flat_sayilar[5::6]

n = 10  # Kaç parçaya bölünecek

# Parçaların uzunluğunu hesapla
length = len(x)
k, m = divmod(length, n)

# Liste 1 parçalama
xs = [x[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]
ys = [y[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]
dxs = [dx[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]
dys = [dy[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]
cxs = [cx[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]
cys = [cy[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

fig, ax = plt.subplots()

for t in range(n):
    ax.cla()

    # Noktaları çiz
    ax.scatter(xs[t], ys[t], color='blue', marker='o', s=5)

    # Çemberleri ekle
    for i in range(len(cxs[t])):
        cember = patches.Circle((cxs[t][i], cys[t][i]), 100,
                                 edgecolor='green', facecolor='none', linewidth=1)
        ax.add_patch(cember)

    ax.set_title(f"Adım {t}")
    ax.set_aspect('equal')
    ax.set_xlim(min(x) - 100, max(x) + 100)
    ax.set_ylim(min(y) - 100, max(y) + 100)
    print(len([x for x in cys[t] if x != 0]))
    plt.pause(0.2)  # animasyon etkisi
"""fig, ax = plt.subplots()

num = 2
for t in range(num):
    plt.clf() 
    plt.scatter(xs[t], ys[t], color='blue', marker='o',s=5)
    for i in range(len(cxs[0])):
            cember = patches.Circle((cxs[t][i], cys[t][i]), 100, edgecolor='green', facecolor='none', linewidth=1)
            ax.add_patch(cember)
    plt.pause(0.2)
"""


"""
plt.xlabel('X')
plt.ylabel('Y')
plt.title('X-Y Nokta Grafiği')

plt.grid(True)
plt.axis('equal')
plt.show()
"""
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# definicje funkcji wykorzystanych w programie

def oblicz_Sl(pos):
    d = 0
    for i in pos:
        d += i**2
    d = d ** (1/2)
    Sl = np.mean(d)
    return round(Sl,2)


def oblicz_RP(pos):
    d = 0
    for i in pos:
        d_mean = np.mean(i)
        d += (i - d_mean)**2

    RP = np.std(d ** (1/2))
    return round(RP,2)


def oblicz_tau(pos):
    d = 0
    for i in pos:
        d_mean = np.mean(i)
        d += (i - d_mean)**2

    tau = np.mean(d ** (1/2))
    return round(tau, 2)


# Sciezka do folderu z plikiem csv
file_folder = "D:\\roboty przemyslowe 1\\trasa 2"
# Nazwy plików
file_name1 = "dataLog_Omron-LD_260319_140332.csv"
file_path1 = os.path.join(file_name1)

file_name2 = "encoder_xy_tf.csv"
file_path2 = os.path.join(file_name2)

# Odczytanie plików
df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)
df3 = pd.read_csv(file_path1)

# Wybranie wartosci z przejazdu Trasy 1
df1 = df1[df1["ModeName  (string)"] == "Patrolling route Trasa-gr3"]
df3 = df3[df3["ModeStatus  (string)"] == "Waiting"]

x_robot = np.array(df1['RobotX  (mm)']).reshape((-1, 1))
y_robot = np.array(df1['RobotY  (mm)']).reshape((-1, 1))
th_robot = np.array(df1['RobotTh  (degrees)']).reshape((-1, 1))

x_encoder = np.array(df1['EncoderX  (mm)']).reshape((-1, 1))
y_encoder = np.array(df1['EncoderY  (mm)']).reshape((-1, 1))
th_encoder = np.array(df1['EncoderTh  (degrees)']).reshape((-1, 1))

x_laser = np.array(df1['LaserLocalization_X  (mm)']).reshape((-1, 1))
y_laser = np.array(df1['LaserLocalization_Y  (mm)']).reshape((-1, 1))
th_laser = np.array(df1['LaserLocalization_Th  (degrees)']).reshape((-1, 1))

x_encoder2 = np.array(df2['X']).reshape((-1, 1))
y_encoder2 = np.array(df2['Y']).reshape((-1, 1))

x_w_r = np.array(df3['RobotX  (mm)']).reshape((-1, 1))
y_w_r = np.array(df3['RobotY  (mm)']).reshape((-1, 1))
th_w_r = np.array(df3['RobotTh  (degrees)']).reshape((-1, 1))
# Wyswietlenie danych

width = 1

plt.subplot(1, 2, 1)

plt.plot(x_laser, y_laser, c="r", lw=width*2)
plt.plot(x_robot, y_robot, c="g", lw=width)
plt.plot(x_encoder, y_encoder, c="b", lw=width)
plt.legend(("dane z lasera","dane z czujników robota","dane z enkodera"))
plt.title('z dataLog')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')


plt.subplot(1, 2, 2)

plt.plot(x_laser, y_laser, c="r", lw=width*2)
plt.plot(x_robot, y_robot, c="g", lw=width)
plt.plot(x_encoder2, y_encoder2, c="b", lw=width)
plt.legend(("dane z lasera","dane z czujników robota","dane z enkodera"))
plt.title('z encoder')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')

# Obliczyc dokladnosc

print("dokladnosc położenia z enkodera z pliku 2 –", oblicz_Sl([x_robot - x_encoder2, y_robot - y_encoder2]), "mm")
print("dokladnosc położenia z enkodera z pliku 1 –", oblicz_Sl([x_robot - x_encoder, y_robot - y_encoder]), "mm")
print("dokladnosc położenia z lasera –", oblicz_Sl([x_robot - x_laser, y_robot - y_laser]), "mm")
print("dokladnosc orientacji z enkodera z pliku 1 –", oblicz_Sl([th_robot - th_encoder]), "deg")
print("dokladnosc orientacji z lasera –", oblicz_Sl([th_robot - th_laser]), "deg")

# Obliczyc powtarzalnosc

print("powtarzalnosc położenia –",oblicz_tau([x_w_r,y_w_r]), "±",oblicz_RP([x_w_r,y_w_r])*3, "mm")
print("powtarzalnosc orientacji –",oblicz_tau([th_w_r]), "±",oblicz_RP([th_w_r])*3, "deg")



plt.show()

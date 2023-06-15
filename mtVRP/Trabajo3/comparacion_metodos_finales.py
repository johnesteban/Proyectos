import os 
import matplotlib.pyplot as plt 
path=r"C:\Users\johne\OneDrive - Universidad EAFIT\Documentos universidad\2023-1\Heuristica\Trabajo 1\Códigos\mtVRP Instances"
dir_list=os.listdir(path)

def gap(cota_inferior,arreglo):
    gap=0
    for i in range(len(cota_inferior)):
        gap+=(arreglo[i]-cota_inferior[i])/(cota_inferior[i])
    gap_final=gap/len(cota_inferior)
    return gap_final

constructivo=[797.81,1775.94,1546.48,1145.65,1491.60,1259.39,1426.92,1271.15,1336.87,1674.26,2014.86,1898.33]
grasp=[954.82,1485.81,1424.13,1364.37,1657.25,1685.47,1687.91,1917.35,1923.34,2854.63,3768.01,3943.61]
noisy=[711.43,1654.38,1192.62,1115.95,1276.20,1221.30,1189.58,1210.91,1201.26,1634.13,1804.84,1741.56]
distanciasT=[667.65,1654.38,1194.02,1090.34,1276.20,1116.73,1189.58,1210.91,1201.26,1634.13,1811.90,1832.33]
distanciasAB=[593.41,1546.86,1034.56,1009.74,1036.02,1010.79,1022.82,1029.80,1047.81,1347.42,1843.45,1736.65]
cota_inferior=[384.48,336.44,395.03,395.03,515.34,515.34,515.34,585.74,585.74,596.49,658.59,658.59]
genetico=[637.20,1575.61,1124.30,1076.03,1044.83,1073.97,1042.32,1065.88,1053.83,1463.45,1861.05,1850.22]

#Comparacion con los metodos anteriores 
plt.scatter(dir_list,cota_inferior,label="Cota inferior")
plt.scatter(dir_list,constructivo,label="Constructivo")
plt.scatter(dir_list,grasp,label="GRASP")
plt.scatter(dir_list,noisy,label="Noisy")
plt.scatter(dir_list,distanciasT,label="VND")
plt.scatter(dir_list,distanciasAB,label="Algoritmo de búsqueda")
plt.scatter(dir_list,genetico, label="Evolutivo híbrido")
plt.xlabel('Conjuntos de datos')
plt.ylabel('Distancia total')
plt.legend()
plt.show()

print(gap(cota_inferior,constructivo)*100)
print(gap(cota_inferior,grasp)*100)
print(gap(cota_inferior,noisy)*100)
print(gap(cota_inferior,distanciasT)*100)
print(gap(cota_inferior,distanciasAB)*100)
print(gap(cota_inferior,genetico)*100)

tiempos_limites=[300,450,600,300,300,450,600,450,300,450,450,450]
tiemposconstructivo=[0.0034847000206355,0.0146295000158716, 0.004955099982908,0.00434779998613521,0.00174279999919236,0.00139620000845753,0.00168320001102984,0.00295319998986088,0.00285140000050888,0.00695399998221546,0.0089102000056300,0.00891020000563003]
tiemposgrasp=[0.330316099996708,1.61284789999991,1.1210018999991,1.14706220000153,0.67682209999839,0.646464900000865,0.657405499998276,1.13518630000181,1.14814769999793,2.64529129999937,4.49840649999896,4.61405939999895]
tiemposnoisy=[1.42138239999986,7.37168999999994,5.57028790000186,5.19561480000266,2.80401020000136,2.79379700000209,2.71788649999871,4.67018170000301,4.70983789999809,10.3593739000025,19.1913220000024,29.1837877000034]
tiemposvecindariosT=[1.4740856999997,9.01214540000365,6.50927769999544,5.70380669999577,5.00878639999428,4.88277490000473,5.35848409999744,7.67063020000933,6.16948649998812,14.2857547000021,29.5352958000003,36.571222700004]
tiemposgenetico=[302.163268566131,452.953112840653,612.408871412277,304.687690019607,302.930095911026,461.698593378067,608.050133943557,452.088021993637,300.753979206085,516.099073648452,452.049332618713,452.800538539886]
print("TIEMPOS")
print(sum(tiemposconstructivo))
print(sum(tiemposgrasp))
print(sum(tiemposnoisy))
print(sum(tiemposvecindariosT))
print(sum(tiempos_limites))
print(sum(tiemposgenetico))
plt.scatter(dir_list,tiemposconstructivo,label="Constructivo")
plt.scatter(dir_list,tiemposgrasp,label="GRASP")
plt.scatter(dir_list,tiemposnoisy,label="Noisy")
plt.scatter(dir_list,tiemposvecindariosT,label="VND")
plt.scatter(dir_list,tiempos_limites,label="Algoritmo de búsqueda")
plt.scatter(dir_list,tiemposgenetico, label="Evolutivo híbrido")
plt.xlabel('Conjuntos de datos')
plt.ylabel('Tiempo total (s)')
plt.legend()
plt.show()
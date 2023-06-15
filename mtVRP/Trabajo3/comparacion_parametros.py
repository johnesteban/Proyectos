import os
import matplotlib.pyplot as plt  
path=r"C:\Users\johne\OneDrive - Universidad EAFIT\Documentos universidad\2023-1\Heuristica\Trabajo 1\Códigos\mtVRP Instances"
dir_list=os.listdir(path)
#Variación poblacion con mutacion=0.3
cota_inferior=[384.48,336.44,395.03,395.03,515.34,515.34,515.34,585.74,585.74,596.49,658.59,658.59]
poblacion5=[654.79,1714.67,1230.69,1140.80,1099.01,1113.53,1129.85,1143.60,1083.38,1527.80,1944.35,1882.19]
poblacion10=[659.29,1703.00,1160.42,1083.25,1103.11,1073.24,1084.71,1114.16,1142.47,1528.57,1881.28,1885.42]
poblacion20=[638.69,1652.06,1107.11,1109.96,1095.90,1092.42,1062.02,1103.20,1062.64,1488.64,1858.97,1852.87]
poblacion30=[631.42,1667.87,1183.56,1047.57,1079.52,1103.62,1051.67,1105.27,1075.05,1482.22,1889.58,1814.04]
poblacion50=[644.84,1646.87,1164.76,1059.41,1064.46,1069.81,1093.93,1093.21,1092.29,1488.18,1861.50,1867.35]
poblacion100=[637.76,1676.06,1147.92,1054.84,1069.52,1068.31,1051.58,1038.83,1079.38,1471.41,1848.31,1863.41]

plt.scatter(dir_list,poblacion5,label="5 individuos")
plt.scatter(dir_list,poblacion10,label="10 individuos")
plt.scatter(dir_list,poblacion20,label="20 individuos")
plt.scatter(dir_list,poblacion30,label="30 individuos")
plt.scatter(dir_list,poblacion50,label="50 individuos")
plt.scatter(dir_list,poblacion100,label="100 individuos")
plt.scatter(dir_list,cota_inferior,label="Cota inferior")
plt.xlabel('Conjuntos de datos')
plt.ylabel('Distancia total')
plt.legend()
plt.show()

def gap(cota_inferior,arreglo):
    gap=0
    for i in range(len(cota_inferior)):
        gap+=(arreglo[i]-cota_inferior[i])/(cota_inferior[i])
    gap_final=gap/len(cota_inferior)
    return gap_final
print(gap(cota_inferior,poblacion5)*100)
print(gap(cota_inferior,poblacion10)*100)
print(gap(cota_inferior,poblacion20)*100)
print(gap(cota_inferior,poblacion30)*100)
print(gap(cota_inferior,poblacion50)*100)
print(gap(cota_inferior,poblacion100)*100)

p01=[645.07,1683.10,1218.41,1107.95,1087.33,1082.80,1072.93,1082.58,1085.85,1486.34,1865.65,1910.64]
p02=[645.37,1603.73,1171.22,1101.13,1073.75,1077.54,1072.82,1088.25,1084.85,1462.45,1903.22,1855.35]
p03=[644.94,1691.76,1139.22,1134.99,1093.91,1096.69,1063.00,1096.18,1090.51,1433.30,1875.85,1877.99]
p05=[637.23,1623.58,1083.77,1118.47,1035.38,1090.75,1087.26,1128.34,1085.89,1460.00,1902.31,1914.23]
p07=[659.99,1674.62,1231.03,1187.32,1048.94,1072.57,1113.49,1107.56,1098.90,1487.07,1890.12,1895.33]
p09=[638.51,1661.29,1180.98,1008.29,1095.34,1095.30,1074.67,1076.43,1112.21,1506.72,1911.96,1868.36]
plt.scatter(dir_list,p01,label="0.1")
plt.scatter(dir_list,p02,label="0.2")
plt.scatter(dir_list,p03,label="0.3")
plt.scatter(dir_list,p05,label="0.5")
plt.scatter(dir_list,p07,label="0.7")
plt.scatter(dir_list,p09,label="0.9")
plt.scatter(dir_list,cota_inferior,label="Cota inferior")
plt.xlabel('Conjuntos de datos')
plt.ylabel('Distancia total')
plt.legend()
plt.show()

print("hola")
print(gap(cota_inferior,p01)*100)
print(gap(cota_inferior,p02)*100)
print(gap(cota_inferior,p03)*100)
print(gap(cota_inferior,p05)*100)
print(gap(cota_inferior,p07)*100)
print(gap(cota_inferior,p09)*100)

tiempos10=[645.37,1603.73,1171.22,1101.13,1073.75,1077.54,1072.82,1088.25,1084.85,1462.45,1903.22,1855.35]
tiempos5=[658.01,1645.34,1179.83,1139.43,1047.07,1062.77,1114.87,1066.65,1065.95,1507.04,1862.89,1850.50]
tiempos2=[621.97,1643.34,1177.81,1122.91,1054.39,1099.06,1105.84,1110.09,1102.69,1462.98,1906.02,1871.74]
tiemposo=[637.20,1575.61,1124.30,1076.03,1044.83,1073.97,1042.32,1065.88,1053.83,1463.45,1861.05,1850.22]
plt.scatter(dir_list,tiempos10,label="1/10")
plt.scatter(dir_list,tiempos5,label="1/5")
plt.scatter(dir_list,tiempos2,label="1/2")
plt.scatter(dir_list,tiemposo,label="Tiempos originales")
plt.scatter(dir_list,cota_inferior,label="Cota inferior")
plt.xlabel('Conjuntos de datos')
plt.ylabel('Distancia total')
plt.legend()
plt.show()
print("hola")
print(gap(cota_inferior,tiempos10)*100)
print(gap(cota_inferior,tiempos5)*100)
print(gap(cota_inferior,tiempos2)*100)
print(gap(cota_inferior,tiemposo)*100)

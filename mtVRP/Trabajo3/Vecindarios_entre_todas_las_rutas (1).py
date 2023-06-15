import math 
import noisy1
import numpy as np
import graficador
import time 
import random

def calcular_distancia(data,nodo_i, nodo_j):
    new_arr = data[1:] 
    positions= new_arr[:, [1,2]] 
    x_i, y_i = positions[nodo_i,:]
    x_j, y_j = positions[nodo_j,:]
    distancia = math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2)
    return distancia

def calcular_demanda(data,ruta):
    new_arr = data[1:] 
    demandas=new_arr[:,[3]] 
    demanda_acumulada = 0
    for nodo in ruta:
        demanda_acumulada += demandas[nodo]
    return demanda_acumulada

def calcular_distancia_ruta(data,ruta):
    if ruta is None:
        return 0
    distancia_total = 0
    for i in range(len(ruta) - 1):
        distancia_total += calcular_distancia(data,ruta[i], ruta[i+1])
    return distancia_total

def calcular_distancia_total(data,rutas):
    if not isinstance(rutas, list):
        rutas = [rutas]  # convierte ruta en una lista si no lo es
    distancia_total = 0
    for ruta in rutas:
        distancia_total += calcular_distancia_ruta(data,ruta)
    return distancia_total

def verificar_capacidad_rutas(data, rutas):
    capacidad_maxima=float(data[0,2])
    new_arr = data[1:] 
    demandas=new_arr[:,[3]] 
    for ruta in rutas:
        demanda_total = sum(demandas[i] for i in ruta[1:])
        if (demanda_total> capacidad_maxima).any():
            return False
    return True
def capacidad_valida(data,ruta):
    capacidades=float(data[0,2])
    new_arr = data[1:] 
    demandas=new_arr[:,[3]] 
    demanda_total = sum(demandas[i] for i in ruta)
    return demanda_total <= capacidades

# Vecindario 1: intercambio entre todas las rutas
def intercambio_entre_todas_rutas(data,solucion_actual):
    mejor_solucion = solucion_actual.copy()
    mejor_distancia = calcular_distancia_total(data,solucion_actual)
    for i in range(len(solucion_actual)):
        for j in range(i+1, len(solucion_actual)):
            for k in range(1, len(solucion_actual[i])-1):
                for l in range(1, len(solucion_actual[j])-1):
                    # Verificar si la capacidad despues del intercambio es valida
                    nueva_ruta_i = solucion_actual[i][:k] + solucion_actual[j][l:]
                    nueva_ruta_j = solucion_actual[j][:l] + solucion_actual[i][k:]
                    if capacidad_valida(data,nueva_ruta_i) and capacidad_valida(data,nueva_ruta_j):
                        # Calcular la nueva distancia total despues del intercambio
                        nueva_solucion = solucion_actual[:i] + [nueva_ruta_i] + solucion_actual[i+1:j] + [nueva_ruta_j] + solucion_actual[j+1:]
                        nueva_distancia = calcular_distancia_total(data,nueva_solucion)
                        # Verificar si es mejor solucion que la actual
                        if nueva_distancia < mejor_distancia:
                            mejor_solucion = nueva_solucion
                            mejor_distancia = nueva_distancia
    return mejor_solucion


#Vecindario 2: 2-opt entre todas las rutas
def two_opt_entre_todas_rutas(data,rutas):
    num_rutas = len(rutas)
    new_arr = data[1:] 
    demandas=new_arr[:,[3]] 
    for i in range(num_rutas):
        for j in range(i+1, num_rutas):
            ruta1 = rutas[i]
            ruta2 = rutas[j]
            for k in range(1, len(ruta1)-1):
                for l in range(1, len(ruta2)-1):
                    nueva_ruta1 = ruta1[:k] + ruta2[l::-1] + ruta1[k+1:]
                    nueva_ruta2 = ruta2[:l] + ruta1[k::-1] + ruta2[l+1:]
                    if capacidad_valida(data,nueva_ruta1) and capacidad_valida(data,nueva_ruta2) and set(nueva_ruta1[1:-1]) == set(nueva_ruta2[1:-1]) == set(range(1, len(demandas))):
                        nueva_distancia = calcular_distancia_ruta(data,nueva_ruta1) + calcular_distancia_ruta(data,nueva_ruta2)
                        if nueva_distancia < calcular_distancia_ruta(data,ruta1) + calcular_distancia_ruta(data,ruta2):
                            rutas[i], rutas[j] = nueva_ruta1, nueva_ruta2
    return rutas

def insercion_entre_todas_rutas_ruido(data,solucion_actual,ruido): #en este caso si ruido es por ejm 10 se agrega 10% del valor actual 
    mejor_solucion = solucion_actual.copy()
    mejor_distancia = calcular_distancia_total(data,solucion_actual)
    ruido1 = random.uniform(0, 1) * (mejor_distancia / ruido) 
    mejor_distancia_ruido=calcular_distancia_total(data,mejor_solucion)+ruido1
    for i in range(len(solucion_actual)):
        for j in range(1, len(solucion_actual[i])-1):
            for k in range(len(solucion_actual)):
                if i == k:
                    continue
                for l in range(1, len(solucion_actual[k])):
                    nueva_ruta_i = solucion_actual[i][:j] + solucion_actual[i][j+1:]
                    nueva_ruta_k = solucion_actual[k][:l] + [solucion_actual[i][j]] + solucion_actual[k][l:]
                    if capacidad_valida(data,nueva_ruta_i) and capacidad_valida(data,nueva_ruta_k) and nueva_ruta_i != [] and nueva_ruta_k != []:
                        nueva_solucion = solucion_actual[:i] + [nueva_ruta_i] + solucion_actual[i+1:k] + [nueva_ruta_k] + solucion_actual[k+1:]
                        ruido1 = random.uniform(0, 1) * (mejor_distancia / ruido) 
                        nueva_distancia = calcular_distancia_total(data,nueva_solucion)
                        nueva_distancia_ruido=calcular_distancia_total(data,nueva_solucion)+ruido1
                        if nueva_distancia_ruido < mejor_distancia_ruido:
                            mejor_distancia = nueva_distancia
                            mejor_distancia_ruido=nueva_distancia_ruido 
                            mejor_solucion = nueva_solucion
    return mejor_solucion

def obtener_distancias_rutas(data,solucion):
    distancias = []
    for ruta in solucion:
        distancia_ruta = calcular_distancia_ruta(data,ruta)
        distancias.append(distancia_ruta)
    return distancias

def optimizar(data,solucion,ruido):
    R=int(data[0,1]) 
    Q=float(data[0,2]) 
    Th=float(data[0,3]) 
    new_arr = data[1:] 
    positions= new_arr[:, [1,2]] 
    tiempo_total=0
    inicio_tiempo=time.perf_counter()
    #ruta,distanc,posi,restric,restricc=noisy1.mejor_solucion(data,niter,media,desviacion_estandar)
    ruta=solucion
    rutas_iniciales=ruta
    mejor_solucion = rutas_iniciales.copy()
    mejor_distancia = calcular_distancia_total(data,mejor_solucion)
    j = 1
    fin_tiempo=time.perf_counter()
    tiempo_total+=(fin_tiempo-inicio_tiempo)
    while j <= 3:
        inicio_tiempo=time.perf_counter()
        if j == 1:
            nueva_solucion = insercion_entre_todas_rutas_ruido(data,mejor_solucion,ruido)
        elif j == 2:
            nueva_solucion = intercambio_entre_todas_rutas(data,mejor_solucion)
        elif j == 3:
            nueva_solucion = two_opt_entre_todas_rutas(data,mejor_solucion)
        nueva_distancia = calcular_distancia_total(data,nueva_solucion)
        if nueva_distancia < mejor_distancia:
            if nueva_solucion is not None:
                j = 1
                mejor_solucion = nueva_solucion.copy()
                mejor_distancia = nueva_distancia
        else:
            j += 1
        fin_tiempo=time.perf_counter()
        tiempo_total+=(fin_tiempo-inicio_tiempo)
    distancias=obtener_distancias_rutas(data,mejor_solucion)
    restricciones=np.zeros(R) 
    for i in range(R): 
        if(distancias[i]>Th):
            restricciones[i]=1
        else:
            restricciones[i]=0
    restrit=0
    if 1 in restricciones:
        restrit=1
    else:
        restrit=0
    return mejor_solucion,positions, distancias, restricciones, restrit

""""
data= np.loadtxt('mtVRP Instances/mtVRP1.txt')
niter=500
media=0
desviacion_estandar=0.01
ruta,posi,distanc,restric,restricc=optimizar(data,niter,media,desviacion_estandar,20)
grafica=graficador.grafica_rutas(posi,ruta)
"""



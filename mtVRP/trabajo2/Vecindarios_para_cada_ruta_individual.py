import math 
import noisy1
import numpy as np
import time

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
    distancia_total = 0
    for i in range(len(ruta) - 1):
        distancia_total += calcular_distancia(data,ruta[i], ruta[i+1])
    return distancia_total

def calcular_distancia_total(data,rutas):
    distancia_total = 0
    for ruta in rutas:
        distancia_total += calcular_distancia_ruta(data,ruta)
    return distancia_total

def insercion(data,ruta):
    mejor_ruta = ruta.copy()
    mejor_distancia = calcular_distancia_ruta(data,ruta)
    Q=float(data[0,2])
    for i in range(1, len(ruta)-1):
        for j in range(1, len(ruta)):
            if j != i and j != i+1:
                nueva_ruta = ruta[:i] + ruta[i+1:j] + [ruta[i]] + ruta[j:]
                nueva_distancia = calcular_distancia_ruta(data,nueva_ruta)
                if nueva_distancia < mejor_distancia and calcular_demanda(data,nueva_ruta) <= Q:
                    mejor_ruta = nueva_ruta
                    mejor_distancia = nueva_distancia
    return mejor_ruta

def intercambio(data,ruta):
    mejor_ruta = ruta.copy()
    mejor_distancia = calcular_distancia_ruta(data,ruta)
    Q=float(data[0,2])
    for i in range(1, len(ruta)-1):
        for j in range(i+1, len(ruta)-1):
            nueva_ruta = ruta[:i] + [ruta[j]] + ruta[i+1:j] + [ruta[i]] + ruta[j+1:]
            nueva_distancia = calcular_distancia_ruta(data,nueva_ruta)
            if nueva_distancia < mejor_distancia and calcular_demanda(data,nueva_ruta) <= Q:
                mejor_ruta = nueva_ruta
                mejor_distancia = nueva_distancia
    return mejor_ruta

def two_opt(data,ruta):
    mejor_ruta = ruta.copy()
    mejor_distancia = calcular_distancia_ruta(data,ruta)
    Q=float(data[0,2])
    for i in range(1, len(ruta)-2):
        for j in range(i+1, len(ruta)-1):
            nueva_ruta = ruta[:i] + ruta[i:j][::-1] + ruta[j:]
            nueva_distancia = calcular_distancia_ruta(data,nueva_ruta)
            if nueva_distancia < mejor_distancia and calcular_demanda(data,nueva_ruta) <= Q:
                mejor_ruta = nueva_ruta
                mejor_distancia = nueva_distancia
    return mejor_ruta

def obtener_distancias_rutas(data,solucion):
    distancias = []
    for ruta in solucion:
        distancia_ruta = calcular_distancia_ruta(data,ruta)
        distancias.append(distancia_ruta)
    return distancias

def VND(data,niter,media,desviacion_estandar,iter,tiempo_limite):
    R=int(data[0,1]) 
    Q=float(data[0,2]) 
    Th=float(data[0,3]) 
    new_arr = data[1:] 
    positions= new_arr[:, [1,2]] 
    tiempo_total=0
    inicio_tiempo=time.perf_counter()
    ruta,distanc,posi,restric,restricc=noisy1.mejor_solucion(data,niter,media,desviacion_estandar)
    solucion_inicial=ruta
    mejor_solucion=solucion_inicial.copy()
    mejor_distancia=calcular_distancia_total(data,solucion_inicial)
    iteraciones = 0
    num_vehiculos=int(data[0,1])
    fin_tiempo=time.perf_counter()
    tiempo_total+=(fin_tiempo-inicio_tiempo)
    while iteraciones < iter:
        if tiempo_total>=tiempo_limite:
            break 
        inicio_tiempo=time.perf_counter()
        vecindario = [insercion, intercambio, two_opt]
        for operador in vecindario:
            for i in range(num_vehiculos):
                nueva_ruta = operador(data,mejor_solucion[i])
                nueva_solucion = mejor_solucion.copy()
                nueva_solucion[i] = nueva_ruta
                nueva_distancia = calcular_distancia_total(data,nueva_solucion)
                if nueva_distancia < mejor_distancia:
                    mejor_solucion = nueva_solucion.copy()
                    mejor_distancia = nueva_distancia
        iteraciones += 1
        fin_tiempo=time.perf_counter()
        tiempo_total+=(fin_tiempo-inicio_tiempo)
        if tiempo_total>=tiempo_limite:
            break 
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
ruta,posi,distanc,restric,restricc=VND(data,niter,media,desviacion_estandar,20)
grafica=graficador.grafica_rutas(posi,ruta)
"""
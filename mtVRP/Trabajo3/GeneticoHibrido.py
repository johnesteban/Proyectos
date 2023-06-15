from itertools import chain
import random
import time
import AlgoritmoBusqueda
import Vecindarios_entre_todas_las_rutas
import noisy1
import math 
import numpy as np 
import graficador 

#Funciones auxiliares
def verificar_capacidad_rutas(data, rutas):
    capacidad_maxima=float(data[0,2])
    new_arr = data[1:] 
    demandas=new_arr[:,[3]] 
    for ruta in rutas:
        demanda_total = sum(demandas[i] for i in ruta[1:])
        if (demanda_total> capacidad_maxima).any():
            return False
    return True

def calcular_distancia(data,nodo_i, nodo_j):
    new_arr = data[1:] 
    positions= new_arr[:, [1,2]] 
    x_i, y_i = positions[nodo_i,:]
    x_j, y_j = positions[nodo_j,:]
    distancia = math.sqrt((x_i - x_j)**2 + (y_i - y_j)**2)
    return distancia

def calcular_distancia_ruta(data,ruta):
    if ruta is None:
        return 0
    distancia_total = 0
    for i in range(len(ruta) - 1):
        distancia_total += calcular_distancia(data,ruta[i], ruta[i+1])
    return distancia_total

def obtener_distancias_rutas(data,solucion):
    distancias = []
    for ruta in solucion:
        distancia_ruta = calcular_distancia_ruta(data,ruta)
        distancias.append(distancia_ruta)
    return distancias

# Función de evaluación de la aptitud (utilizando VND)
def evaluar_aptitud(data,solucion,ruido):
    ruta,positions,distanc,restric,restricc=Vecindarios_entre_todas_las_rutas.optimizar(data,solucion,ruido)
    return ruta 

# Operador de cruce
def cruzar(data,solucion1, solucion2):
    arreglo_unificado = [elemento for subarreglo in solucion1 for elemento in subarreglo]
    padre1 = [elemento for elemento in arreglo_unificado if elemento != 0]
    arreglo_unificado1 = [elemento for subarreglo in solucion2 for elemento in subarreglo]
    padre2 = [elemento for elemento in arreglo_unificado1 if elemento != 0]
    maximo=len(padre1)
    k=random.randint(1, maximo-1)
    j=random.randint(k+1, maximo)
    nuevo_arreglo=[]
    nuevo_arreglo.extend(padre1[k:j])
    for numero in padre2:
        if numero not in nuevo_arreglo:
            nuevo_arreglo.append(numero)
    capacidad_acumulada = 0
    resultado = []
    capacidad_limite=float(data[0,2])
    new_arr = data[1:] 
    demanda=new_arr[:,[3]]
    demandas=demanda.ravel().astype(int)
    for elemento in nuevo_arreglo:
        capacidad_acumulada +=demandas[elemento]
        if capacidad_acumulada>capacidad_limite:
            resultado.extend([0,elemento])
            capacidad_acumulada=demandas[elemento]
        else:
            resultado.append(elemento)
    resultado.insert(0, 0) 
    resultado.append(0) 
    distancia_acumulada=0
    arreglofinal=[]
    Th=float(data[0,3]) 
    R=int(data[0,1])
    contador=0
    for i in range(len(resultado)-1): 
        distancia_acumulada+=calcular_distancia(data,resultado[i],resultado[i+1])
        if distancia_acumulada>Th:
            arreglofinal.append(resultado[contador:i])
            contador=i
            distancia_acumulada=calcular_distancia(data,resultado[i],resultado[i+1])
    arreglofinal.append(resultado[contador:])
    while len(arreglofinal)<R:
        arreglofinal.extend([[0,0]])
    ultimo_subarreglo = arreglofinal[R-1] 
    if len(arreglofinal) > R:
        arreglobien = [elemento for subarreglo in arreglofinal[R:] for elemento in subarreglo]
        ultimo_subarreglo.extend(arreglobien)   
    listafinal = arreglofinal[:R]
    for i in range(len(listafinal)):
        if listafinal[i][0] != 0:
            listafinal[i].insert(0, 0)  # Agregar 0 al inicio si no está presente
        if listafinal[i][-1] != 0:
            listafinal[i].append(0)  # Agregar 0 al final si no está presente
    return listafinal

# Operador de mutación (utilizando perturbación ILS)
def mutar(data,solucion):
    solucion1=AlgoritmoBusqueda.perturbacion_ILS(data,solucion)
    return solucion1

# Función para generar una solución inicial aleatoria
def generar_solucion_inicial(data,niter,media,desviacion_estandar):
    ruta,distanc,posi,restric,restricc=noisy1.mejor_solucion(data,niter,media,desviacion_estandar)
    return ruta 

# Funcion para elegir los mejores individuos de una poblacion 
def sobrevivientes(data, poblacion,n):
    distancias = [(sum(obtener_distancias_rutas(data,sub_arreglo)), sub_arreglo) for sub_arreglo in poblacion]
    distancias.sort(key=lambda x: x[0])
    distanciasn=[sub_arreglo for _, sub_arreglo in distancias[:n]]
    return distanciasn

# Algoritmo evolutivo híbrido
def algoritmo_evolutivo_hibrido(data,niter,media,desviacion_estandar,ruido,tamano_poblacion,tiempo_limite,probabilidad):
    R=int(data[0,1]) 
    Q=float(data[0,2]) 
    Th=float(data[0,3]) 
    poblacion = []
    new_arr = data[1:] 
    positions= new_arr[:, [1,2]] 
    for _ in range(tamano_poblacion):
        solucion = generar_solucion_inicial(data,niter,media,desviacion_estandar)  # Generar una solución inicial con ayuda de noisy
        poblacion.append(solucion)
    mejor_solucion = None
    tiempo_inicial=time.time()
    while ((time.time() - tiempo_inicial) < tiempo_limite):
        padre1 = random.choice(poblacion)
        poblacion_sin_padre1 = poblacion.copy()
        poblacion_sin_padre1.remove(padre1)
        padre2 = random.choice(poblacion_sin_padre1)
        hijo = cruzar(data,padre1, padre2)  # Cruce entre dos individuos seleccionados
        if random.random() < probabilidad:  # Probabilidad de mutación del 20%
            hijo = mutar(data,hijo)  # Mutación del hijo generado
        hijo_educado=evaluar_aptitud(data,hijo,ruido) #Se educa al hijo
        poblacion.append(hijo_educado)  
        poblacion=sobrevivientes(data,poblacion,tamano_poblacion) #Elección de sobrevivientes
    mejor_solucion=sobrevivientes(data,poblacion,1)
    mejor_solucion1 = list(chain(*mejor_solucion))
    distancias=obtener_distancias_rutas(data,mejor_solucion1)
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
    return mejor_solucion1,distancias, restricciones, restrit,tiempo_inicial,positions

""""
data= np.loadtxt('mtVRP1.txt')
niter=100
media=1
desviacion_estandar=2
ruido=10
tamano_poblacion=100
probabilidad=0.2
tiempo_limite=300
ruta,distancias,restric,restricc,tiempo,positions=algoritmo_evolutivo_hibrido(data,niter,media,desviacion_estandar,ruido,tamano_poblacion,tiempo_limite,probabilidad)
grafica=graficador.grafica_rutas(positions,ruta)
print(sum(distancias))
"""
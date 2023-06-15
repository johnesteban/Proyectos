import math 
import noisy1
import numpy as np
import graficador
import random
import time 
import copy 

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

def obtener_distancias_rutas(data,solucion):
    distancias = []
    for ruta in solucion:
        distancia_ruta = calcular_distancia_ruta(data,ruta)
        distancias.append(distancia_ruta)
    return distancias

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

def perturbacion_ILS(data,solucion1):
    solucion=copy.deepcopy(solucion1)
    nuevas_rutas=[]
    capacidad=float(data[0,2])
    new_arr = data[1:] 
    demandas=new_arr[:,[3]] 
    for ruta in solucion:
        indices_no_nulos = [i for i in range(len(ruta)) if ruta[i] != 0]
        if len(indices_no_nulos) > 0:
            indice_eliminar = random.choice(indices_no_nulos)
            nodo_eliminado=ruta.pop(indice_eliminar)
            nuevas_rutas.append(nodo_eliminado)
    nueva_ruta=[]
    capacidad_actual=0
    for ruta in nuevas_rutas:
        capacidad_actual+=demandas[ruta]
        if capacidad_actual<=capacidad:
            nueva_ruta.append(ruta)
        else: 
            nueva_ruta.extend([0, ruta])
            capacidad_actual=demandas[ruta]
    nueva_ruta.append(0)
    distancias=[]
    for ruta in solucion: 
        distancias.append(calcular_distancia_ruta(data,ruta))
    distancias_ordenadas= sorted(distancias)
    indice=distancias.index(distancias_ordenadas[0])
    solucion[indice-1].extend(nueva_ruta)
    return solucion

def VND(data, tiempo_inicial, tiempo_limite,ruido,media,desviacion_estandar,niter):
    R=int(data[0,1]) 
    Q=float(data[0,2]) 
    Th=float(data[0,3]) 
    new_arr = data[1:] 
    positions= new_arr[:, [1,2]] 
    solucion_final=[]
    while ((time.time()-tiempo_inicial)<tiempo_limite):
        rut,distan,pos,restri,restrit=noisy1.mejor_solucion(data,niter,media,desviacion_estandar)
        mejor_solucion=rut
        mejor_distancia=sum(distan)
        j=1
        while((time.time()-tiempo_inicial)<tiempo_limite and j<=3):
            if j == 1:
                nueva_solucion = insercion_entre_todas_rutas_ruido(data,mejor_solucion,ruido)
            elif j == 2:
                nueva_solucion=intercambio_entre_todas_rutas(data,mejor_solucion)
            elif j == 3:
                nueva_solucion = perturbacion_ILS(data,mejor_solucion)  
            nueva_distancia = calcular_distancia_total(data,nueva_solucion)
            if nueva_distancia < mejor_distancia:
                if nueva_solucion is not None:
                    j = 1
                    mejor_solucion = nueva_solucion.copy()
                    mejor_distancia = nueva_distancia
            else:
                j += 1
        solucion_final.append((mejor_distancia,mejor_solucion))
    ordenadas=sorted(solucion_final,key=lambda x :x[0])
    distancia=ordenadas[0][0]
    solucion=ordenadas[0][1]
    distancias1=obtener_distancias_rutas(data,solucion)
    restricciones=np.zeros(R) 
    for i in range(R): 
        if(distancias1[i]>Th):
            restricciones[i]=1
        else:
            restricciones[i]=0
    restrit=0
    if 1 in restricciones:
        restrit=1
    else:
        restrit=0
    return solucion,positions, distancias1, restricciones, restrit
""""
data= np.loadtxt('mtVRP Instances/mtVRP1.txt')
start_time=time.time()
ruta,posi,distanc,restric,restricc=VND(data,start_time,300,10,5,2,100)
print(sum(distanc))
grafica=graficador.grafica_rutas(posi,ruta)
"""
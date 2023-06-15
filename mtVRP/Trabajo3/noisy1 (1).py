import numpy as np 
#from scipy.spatial.distance import pdist, squareform
import math
import random
import time 
import dist

def distancia_euclidiana(punto1, punto2):
    distancia = 0.0
    for i in range(len(punto1)):
        distancia+=(punto1[i] - punto2[i]) ** 2
    return math.sqrt(distancia)

def dist1(positions,media,desviacion_estandar):
    n=len(positions)
    dist_matrix = [[0.0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d = distancia_euclidiana(positions[i], positions[j])
            dist_matrix[i][j] = d
            dist_matrix[j][i] = d
        dist_matrix[i][i] = math.inf
    variable_aleatoria = np.random.normal(media, desviacion_estandar, size=(n, n))
    matriz_con_variable_aleatoria = dist_matrix + variable_aleatoria
    return matriz_con_variable_aleatoria

def proceso_general(data,media,desviacion_estandar):
    new_arr = data[1:] 
    nodes=new_arr[:,[0]] 
    positions= new_arr[:, [1,2]] 
    demandas=new_arr[:,[3]]
    n=int(data[0,0]) 
    R=int(data[0,1]) 
    Q=float(data[0,2]) 
    Th=float(data[0,3]) 
    dist_matrixn=dist1(positions,media, desviacion_estandar) 
    dist_matrix=dist.dist(positions,n) 

    distancias=[]
    visitados={i for i in range(1,int(n)+1)} 
    rutas=[]
    node=nodes[0] 
    i=1
    capacidades_vehiculos=[] #agregada
    nodes1=[]#agregada
    while i<=R: 
        q_actual=Q 
        node=nodes[0] 
        ruta=[0] 
        DistanciaTotal=0  
        while(DistanciaTotal<Th): 
            if(len(visitados)==0): 
                break
            next=int(node)  
            for j in visitados:
                if ((new_arr[j,3]<=q_actual) and (dist_matrixn[int(node),j]<=dist_matrixn[int(node),next])):
                    next=j
            if(next==int(node)): 
                next=0 
                q_actual=Q
                DistanciaTotal=DistanciaTotal+dist_matrix[int(node),next] 
            else:
                q_actual=q_actual-new_arr[next,3] 
                DistanciaTotal=DistanciaTotal+dist_matrix[int(node),next] 
                visitados.remove(next)  
            ruta.append(next) 
            node=next 
        capacidades_vehiculos.append(q_actual) #agregada
        nodes1.append(node) #agregada
        i=i+1   
        rutas.append(ruta)
        distancias.append(DistanciaTotal)
        if(len(visitados)==0):
            break 
    while(len(visitados)>0): 
        VehiculoConMenorRecorrido=min(distancias) 
        Vehiculo=distancias.index(VehiculoConMenorRecorrido)
        q_actual=capacidades_vehiculos[Vehiculo] #agregada
        node=nodes1[Vehiculo]
        next=int(node) #modificada
        for j in visitados: 
            if ((new_arr[j,3]<=q_actual) and (dist_matrixn[int(node),j]<=dist_matrixn[int(node),next])):
                next=j
        if(next==int(node)):
            next=0
            q_actual=Q
            distancias[Vehiculo]=distancias[Vehiculo]+dist_matrix[int(node),next] 
        else:
            q_actual=q_actual-new_arr[next,3] 
            distancias[Vehiculo]=distancias[Vehiculo]+dist_matrix[int(node),next] 
            visitados.remove(next) 
        rutas[Vehiculo].append(next) 
        node=nodes[next] 
        nodes1[Vehiculo]=nodes[next] 
        capacidades_vehiculos[Vehiculo]=q_actual

    while(len(rutas)<R):
        rutas.append([0])
        distancias.append(0)
        
    for i in range(R): 
        if(rutas[i][-1]!=0):
            distancias[i]+=dist_matrix[rutas[i][-1],0]
            rutas[i].append(0)
            
    restricciones=np.zeros(R) 
    for i in range(R): 
        if(distancias[i]>Th):
            restricciones[i]=1
        else:
            restricciones[i]=0
    return rutas, distancias,positions,restricciones

def mejor_solucion(data,niter,media, desviacion_estandar):
    inicial=math.inf
    distanciaInicial=math.inf
    restrit=0
    for j in range(niter):
        r,d,p,rest=proceso_general(data,media,desviacion_estandar)
        if (sum(rest)<inicial) or ((sum(rest)==inicial) & (sum(d)<distanciaInicial)):
            inicial=sum(rest)  
            rut=r
            distan=d
            restri=rest
            distanciaInicial=sum(d) 
    if 1 in restri:
        restrit=1
    else:
        restrit=0
    return rut,distan,p,restri,restrit
import numpy as np 
import pandas as pd 
import math
import random
#import xlsxwriter
#import time
import dist 

def proceso_general(data,k):
    new_arr = data[1:] 
    nodes=new_arr[:,[0]] 
    positions= new_arr[:, [1,2]] 
    demandas=new_arr[:,[3]]
    n=int(data[0,0]) 
    R=int(data[0,1]) 
    Q=float(data[0,2]) 
    Th=float(data[0,3]) 
    dist_matrix=dist.dist(positions,n) 

    distancias=[]
    visitados={i for i in range(1,int(n)+1)} 
    rutas=[]
    node=nodes[0] 
    i=1
    while i<=R: 
        q_actual=Q 
        node=nodes[0] 
        ruta=[0] 
        DistanciaTotal=0  
        while(DistanciaTotal<Th): 
            if(len(visitados)==0): 
                break
            next=int(node)  
            nexts=[]
            contador=0
            for j in visitados:
                if ((new_arr[j,3]<=q_actual) and (dist_matrix[int(node),j]<=dist_matrix[int(node),next]) and (j not in nexts) and (contador<k)):
                    contador=contador+1
                    next=j
                    nexts.append(j) 
            if len(nexts)>1:
                aleatorio=random.randint(1,len(nexts))
                next=nexts[aleatorio-1]   
            elif len(nexts)==1:
                next=nexts[0]
            else: 
                next=int(node)    
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
        i=i+1   
        rutas.append(ruta)
        distancias.append(DistanciaTotal)
        if(len(visitados)==0):
            break 
    while(len(visitados)>0): 
        VehiculoConMenorRecorrido=min(distancias) 
        Vehiculo=distancias.index(VehiculoConMenorRecorrido)
        next=int(node) 
        nexts=[]
        contador=0
        for j in visitados: 
            if ((new_arr[j,3]<=q_actual) and (dist_matrix[int(node),j]<=dist_matrix[int(node),next]) and (j not in nexts) and (contador<k)):
                contador=contador+1
                next=j
                nexts.append(j) 
        if len(nexts)>1:
            aleatorio=random.randint(1,len(nexts))
            next=nexts[aleatorio-1]  
        elif len(nexts)==1:
            next=nexts[0]
        else: 
            next=int(node)
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

def mejor_solucion(data,niter,k):
    inicial=math.inf
    distanciaInicial=math.inf
    restrit=0
    for j in range(niter):
        r,d,p,rest=proceso_general(data,k)
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
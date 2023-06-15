import numpy as np 
#import pandas as pd 
#import xlsxwriter
import dist 

def proceso_general(data):
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
            for j in visitados:
                if ((new_arr[j,3]<=q_actual) and (dist_matrix[int(node),j]<=dist_matrix[int(node),next])):
                    next=j 
            if(next==int(node)):
                next=0
                q_actual=Q
                DistanciaTotal=DistanciaTotal+dist_matrix[int(node),next] 
            else:
                q_actual=q_actual-new_arr[next,3] 
                new_arr[next,3]=0 
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
        for i in visitados:
            if ((i!=int(node)) & (new_arr[i,3]<=q_actual) & (dist_matrix[int(node),i]<=dist_matrix[int(node),next])):
                next=i 
        if(next==int(node)):
            next=0
            q_actual=Q
            distancias[Vehiculo]=distancias[Vehiculo]+dist_matrix[int(node),next] 
        else:
            q_actual=q_actual-new_arr[next,3] 
            new_arr[next,3]=0 
            distancias[Vehiculo]=distancias[Vehiculo]+dist_matrix[int(node),next] 
            visitados.remove(next)
        rutas[Vehiculo].append(next) 
        node=nodes[next] 

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
    restritot=0
    if 1 in restricciones:
        restritot=1
    else:
        restritot=0
    return rutas, distancias,positions,restricciones,restritot


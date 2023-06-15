import os 
import time 
import numpy as np
import pandas as pd 
import AlgoritmoBusqueda

def write_file(path, instances):
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    for sheet_name, df in instances.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    writer.close()

path=r"C:\Users\johne\OneDrive - Universidad EAFIT\Documentos universidad\2023-1\Heuristica\Trabajo 1\Códigos\mtVRP Instances"
dir_list=os.listdir(path)
niter=500
nois={}
media=8
desviacion_estandar=1
tiempos_limites=[300,450,600,300,300,450,600,450,300,450,450,450]
#n_iter=20,40,60,80,100,120,140
#ruido=2,5,10,20
#media=0,2,4,5,8,10
#desviacion_estandar=0.01,1,2,4,6,9
n_iter=100
ruido=20
for i in range(len(dir_list)):
    data=np.loadtxt(rf"C:\Users\johne\OneDrive - Universidad EAFIT\Documentos universidad\2023-1\Heuristica\Trabajo 1\Códigos\mtVRP Instances\{dir_list[i]}")
    start_time=time.time()
    ruta,positions,distanc,restric,restricc=AlgoritmoBusqueda.VND(data,start_time,tiempos_limites[i],ruido,media,desviacion_estandar,n_iter)
    finn=time.time()
    ansn=[]
    for j in range(len(ruta)):
        ruta[j].append(np.round(distanc[j],2))
        ruta[j].append(np.round(restric[j],0))
        ansn.append(ruta[j])
    genn=[np.round(sum(distanc),2), finn-start_time, np.round(restricc,0)]
    ansn.append(genn)
    ansn=pd.DataFrame(ansn)
    nois[dir_list[i]]=ansn
    print(i)
path3="C:/Users/johne/OneDrive - Universidad EAFIT/Documentos universidad/2023-1/Heuristica/Trabajo 2/Resultados/mtVRP_JohnEstebanCastro_AlgoritmoBusqueda.xlsx"
write_file(path3,nois)
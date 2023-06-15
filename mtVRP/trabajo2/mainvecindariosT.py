import os 
import time 
import numpy as np
import pandas as pd 
import Vecindarios_entre_todas_las_rutas

def write_file(path, instances):
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    for sheet_name, df in instances.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    writer.close()

path=r"C:\Users\johne\OneDrive - Universidad EAFIT\Documentos universidad\2023-1\Heuristica\Trabajo 1\Códigos\mtVRP Instances"
dir_list=os.listdir(path)
niter=500
nois={}
media=0
desviacion_estandar=0.01
tiempos_limites=[300,450,600,300,300,450,600,450,300,450,450,450]
n_iter=10
for i in range(len(dir_list)):
    data=np.loadtxt(rf"C:\Users\johne\OneDrive - Universidad EAFIT\Documentos universidad\2023-1\Heuristica\Trabajo 1\Códigos\mtVRP Instances\{dir_list[i]}")
    inicion=time.perf_counter()
    ruta,positions,distanc,restric,restricc=Vecindarios_entre_todas_las_rutas.optimizar(data,niter,media,desviacion_estandar,n_iter,tiempos_limites[i])
    finn=time.perf_counter()
    ansn=[]
    for j in range(len(ruta)):
        ruta[j].append(np.round(distanc[j],2))
        ruta[j].append(np.round(restric[j],0))
        ansn.append(ruta[j])
    genn=[np.round(sum(distanc),2), finn-inicion, np.round(restricc,0)]
    ansn.append(genn)
    ansn=pd.DataFrame(ansn)
    nois[dir_list[i]]=ansn
    print(i)
path3="C:/Users/johne/OneDrive - Universidad EAFIT/Documentos universidad/2023-1/Heuristica/Trabajo 2/Resultados/mtVRP_JohnEstebanCastro_VecindariosT.xlsx"
write_file(path3,nois)
import os 
import time 
import numpy as np
import pandas as pd 
import GeneticoHibrido

def write_file(path, instances):
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    for sheet_name, df in instances.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    writer.close()

path=r"C:\Users\johne\OneDrive - Universidad EAFIT\Documentos universidad\2023-1\Heuristica\Trabajo 1\Códigos\mtVRP Instances"
dir_list=os.listdir(path)
niter=100
nois={}
media=1
desviacion_estandar=2
tiempos_limites=[300,450,600,300,300,450,600,450,300,450,450,450]
ruido=10
tamano_poblacion=100
probabilidad=0.2
for i in range(len(dir_list)):
    data=np.loadtxt(rf"C:\Users\johne\OneDrive - Universidad EAFIT\Documentos universidad\2023-1\Heuristica\Trabajo 1\Códigos\mtVRP Instances\{dir_list[i]}")
    ruta,distanc,restric,restricc,tiempoinicial,positions=GeneticoHibrido.algoritmo_evolutivo_hibrido(data,niter,media,desviacion_estandar,ruido,tamano_poblacion,tiempos_limites[i],probabilidad)
    finn=time.time()
    ansn=[]
    for j in range(len(ruta)):
        ruta[j].append(np.round(distanc[j],2))
        ruta[j].append(np.round(restric[j],0))
        ansn.append(ruta[j])
    genn=[np.round(sum(distanc),2), finn-tiempoinicial, np.round(restricc,0)]
    ansn.append(genn)
    ansn=pd.DataFrame(ansn)
    nois[dir_list[i]]=ansn
    print(i)
path3="C:/Users/johne/OneDrive - Universidad EAFIT/Documentos universidad/2023-1/Heuristica/Trabajo 3/Resultados/mtVRP_JohnEstebanCastro_Genetico.xlsx"
write_file(path3,nois)


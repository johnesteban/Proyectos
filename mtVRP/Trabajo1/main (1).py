import os 
import time 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import constructive 
import graficador 
import grasp
import noisy 

def write_file(path, instances):
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    for sheet_name, df in instances.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    
    writer.close()

path=r"C:\Users\johne\OneDrive - Universidad EAFIT\Documentos universidad\2023-1\Heuristica\Trabajo 1\Códigos\mtVRP Instances"
dir_list=os.listdir(path)
k=8
niter=500
media=0
desviacion_estandar=0.01

cons={}
grsp={}
nois={}
for i in range(len(dir_list)):
    data=np.loadtxt(rf"C:\Users\johne\OneDrive - Universidad EAFIT\Documentos universidad\2023-1\Heuristica\Trabajo 1\Códigos\mtVRP Instances\{dir_list[i]}")
    #print("Estoy recorriendo el mtVRP"+str({dir_list[i]}))
    inicio=time.perf_counter()
    r,d,p,rest,restritot=constructive.proceso_general(data)
    fin = time.perf_counter()
    ans=[]
    for j in range(len(r)):
        r[j].append(np.round(d[j],2))
        r[j].append(np.round(rest[j],0))
        ans.append(r[j])
    gen=[np.round(sum(d),2), fin-inicio, np.round(restritot,0)]
    ans.append(gen)
    ans=pd.DataFrame(ans)
    cons[dir_list[i]]=ans
    #grafica=graficador.grafica_rutas(p,r) 
    iniciog=time.perf_counter()
    rut,distan,pos,restri,restrit=grasp.mejor_solucion(data,niter,k)
    fing= time.perf_counter()
    ansg=[]
    for j in range(len(rut)):
        rut[j].append(np.round(distan[j],2))
        rut[j].append(np.round(restri[j],0))
        ansg.append(rut[j])
    geng=[np.round(sum(distan),2), fing-iniciog, np.round(restrit,0)]
    ansg.append(geng)
    ansg=pd.DataFrame(ansg)
    grsp[dir_list[i]]=ansg
    #grafica=graficador.grafica_rutas(pos,rut)
    inicion=time.perf_counter()
    ruta,distanc,posi,restric,restricc=noisy.mejor_solucion(data,niter,media,desviacion_estandar)
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
    #grafica=graficador.grafica_rutas(posi,ruta)

path1="C:/Users/johne/OneDrive - Universidad EAFIT/Documentos universidad/2023-1/Heuristica/Trabajo 1/Resultados/mtVRP_JohnEstebanCastro_constructivo.xlsx"
path2="C:/Users/johne/OneDrive - Universidad EAFIT/Documentos universidad/2023-1/Heuristica/Trabajo 1/Resultados/mtVRP_JohnEstebanCastro_grasp.xlsx"
path3="C:/Users/johne/OneDrive - Universidad EAFIT/Documentos universidad/2023-1/Heuristica/Trabajo 1/Resultados/mtVRP_JohnEstebanCastro_ruido.xlsx"

write_file(path1,cons)
write_file(path2,grsp)
write_file(path3,nois)

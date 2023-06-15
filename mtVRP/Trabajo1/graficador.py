import matplotlib.pyplot as plt 
import random

def grafica_rutas(positions,rutas):
    fig, ax = plt.subplots()
    ax.scatter(positions[1:, 0], positions[1:, 1])  
    ax.scatter(positions[0, 0], positions[0, 1], color='red')  
    colors = []
    for i in range(len(rutas)): 
        color_code = random.randint(0, 0xFFFFFF)
        color_hex = '#' + hex(color_code)[2:].zfill(6)
        colors.append(color_hex)
    for i in range(len(rutas)):
        ruta = rutas[i]
        color=colors[i]
        x=positions[ruta,0]
        y=positions[ruta,1]
        ax.plot(x, y, color=color, label="Vehiculo"+str(i+1))
    ax.set_xlabel('Posición X')
    ax.set_ylabel('Posición Y')
    ax.set_title('Rutas')
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    return plt.show()
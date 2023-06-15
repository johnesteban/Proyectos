#histograma
hist(promedios_cada_trayectoria,col = "#40E0D0",main="Histogram of the average nickel price \n for each Monte Carlo generated trajectory",xlab="Average nickel price") #en este histograma tengo el promedio de cada una de las trayectorias
#del promedio de las 1000 trayectorias saco el promedio 
promedio<-mean(promedios_cada_trayectoria) #este será más o menos el precio promedio de un año 

#MEDIA DE LOS ULTIMOS 10 AÑOS sin incluir el año simulado
ultimos_años<-segunda_col[278:397]
#Calculo percentiles 
cuantil65<-quantile(ultimos_años,0.65)
cuantil75<-quantile(ultimos_años,0.75)

#decir el porcentaje de impuesto que se tendrá que pagar
if (promedio<cuantil65){
  print("El impuesto sobre renta que deberá pagar es del 35%, no se aplica ninguna sobretasa.")
} else if(promedio>=cuantil65 & promedio<=cuantil75){
  print("El impuesto sobre renta que deberá pagar es del 40%, se aplico una sobretasa del 5%.")
} else{
  print("El impuesto sobre renta que deberá pagar es del 45%, se aplico una sobretasa del 10%.")
}
#decir en terminos de probabilidades, en cada caso cual es la probabilidad de pagar
cantidad_de_datos_bajo_65<-sum(promedios_cada_trayectoria<cuantil65)
cantidad_de_datos_entre_65_75<-sum(promedios_cada_trayectoria>=cuantil65 & promedios_cada_trayectoria<=cuantil75)
cantidad_por_encima_75<-sum(promedios_cada_trayectoria>cuantil75)
resultado1<-paste("Pagará un impuesto sobre renta del 35%, sin aplicar ninguna sobretasa con una probabilidad de ",(cantidad_de_datos_bajo_65)/10000)
resultado2<-paste("Pagará un impuesto sobre renta del 40%, teniendo en cuenta que se le aplico una sobretasa del 5%, con una probabilidad de ",(cantidad_de_datos_entre_65_75)/10000)
resultado3<-paste("Pagará un impuesto sobre renta del 45%, teniendo en cuenta que se le aplico una sobretasa del 10%, con una probabilidad de ",(cantidad_por_encima_75)/10000)
print(resultado1)
print(resultado2)
print(resultado3)
meses<-c(1:397)
meses1<-c(397:409)
plot(meses,segunda_col,type='l',xlim=c(0,409),xlab="Months",ylab="Price of Nickel")
abline(v = 397, lty = 2)
#parametros estimados: mu=0.0816, sigma=0.2535, lambda=0.5436, gamma=0.0158, delta=0.1625
#GRAFICA NORMAL
S <- matrix(nrow = 10000, ncol = 13)
for(i in 1:10000){
  S[i,]<-c(segunda_col[397],sim.jump.diff.merton(c(0.0816, 0.2535, 0.5436, 0.0158, 0.1625),12,1/12,segunda_col[397],F))
  col <- rainbow(10000)[i]
  lines(meses1,S[i,],col=col)
}

#PARA OBSERVAR MEJOR LA GRAFICA (las simulaciones del año que hice)
plot(meses,segunda_col,type='l',xlim=c(390,410),xlab="Months",ylab="Price of Nickel")
abline(v = 397, lty = 2)
S2 <- matrix(nrow = 10000, ncol = 13)
promedios_cada_trayectoria<-vector("numeric",10000)
for(i in 1:10000){
  S2[i,]<-c(segunda_col[397],sim.jump.diff.merton(c(0.0816, 0.2535, 0.5436, 0.0158, 0.1625),12,1/12,segunda_col[397],F))
  col <- rainbow(10000)[i]
  lines(meses1,S2[i,],col=col)
  #Obtener los valores finales
  promedios_cada_trayectoria[i]<-mean(S2[i,]) #obtener los promedios de cada trayectoria
}



est.cdf <- function( x, cont=1 , graph=0){
  #  Estimation of the distribution function
  #  and construction of a 95 percent confidence band
  #
  #  Input: x: iid sample (n x 1 vector)
  #         cont: 1 if the Edf is assumed continuous (default), 0 otherwise
  #         graph: 1 if graph is needed, 0 otherwise (default).
  #
  # output: Edf: Estimated distribution function at the x
  #         FMin: 95# level lower bound of the confidence band
  #         FMax: 95# level upper bound of the confidence band.
  
  ## Printed output
  
  n <- length(x)
  
  Edf <- mat.or.vec(n,1)
  
  if(cont){
    pts <- sort( x )
    Edf <- (1:n) / n
  }else{
    
    pts <- x
    
    for(i in 1:n){
      Edf[i] <- mean ( (x <= x[i]) )
    }
  }
  
  # 1.358 corresponds to the 95% quantile of the K-S limiting distribution
  EdfMin <- Edf - 1.358 / sqrt(n)  
  EdfMax <- Edf + 1.358 / sqrt(n)
  ## Printed output
  if(graph){
    library('ggplot2')
    library('reshape')
    previous_theme <- theme_set(theme_bw())
    tmp <- data.frame(pts=pts, Edf=Edf, EdfMin = EdfMin, EdfMax=EdfMax)
    names(tmp) <- c('p','Empirical','Lower bound', 'Upper bound')
    framed.data <- melt(tmp, id='p')    
    values.graph <- ggplot(framed.data,aes(x=p, y=value, group=variable, colour=variable))
    
    values.graph <- values.graph + geom_line() +
      ggtitle("Empirical distribution function and 95%% uniform band")

    
    print(values.graph)

  }
  
  return(list(pts=pts, Edf=Edf, EdfMin = EdfMin, EdfMax=EdfMax))
}
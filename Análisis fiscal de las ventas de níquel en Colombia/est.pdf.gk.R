require(moments)
require(ggplot2)
require(pracma)
require(reshape)
est.pdf.gk <- function(x, m, comp=F){
  # This function compute the nonparametric estimation of the density with 
  # the Gaussian kernel, and makes graphical comparison with the following 
  # densities:Gaussian, Johnson_SU and Student. 
  # It also compute goodness-of-fit tests for the Gaussian distribution:
    # Jarque-Berra, revisited Jarque-Berra, corrected Kolmogorov-Smirnov and
  # Cramer-von Mises type tests.
  #
  # Input:  x: data (assumed i.i.d.) (n x 1 vector);
  #         m: number of points for the graphs;
  #         comp: F(FALSE) (default) or T(TRUE), if one wants the comparisons with
  #               the Gaussian, Johnson_SU and Student densities.
  #
  # Output: x: points at which the density is estimated;
  #        fn: estimation of the density at points x;
  #      stat: tests statistics for the following tests of normality: 
  #            Jarque-Berra (JB), revisited Jarque-Berra (JBR), corrected 
  #            Kolmogorov-Sminorv (K)  and Cramer-von Mises (CVM);
  #      pval: pvalue (%) for the following tests of normality: 
  #            Jarque-Berra (JB), revisited Jarque-Berra (JBR), corrected 
  #            Kolmogorov-Sminorv (K)  and Cramer-von Mises (CVM).
  #
  # Modified October 1, 2013
  
  stat   = NULL;
  pvalue = NULL;

  n   <- length(x)
  mu  <- mean(x)   #mean
  std.x  <- sd(x)    #standard deviation
  h   <- std.x * n^-0.2
  
  t <- seq(from = min(x), to= max(x), by=((max(x)-min(x))/m))
  nbPoints <- length( t )
  y <- mat.or.vec( nbPoints, 1 )
  
  for(i in 1:nbPoints){
  y[i] <- mean( dnorm( (x-t[i])/h)) / h
  }
  
  #Printing of graph
 # library('ggplot2')
  previous_theme <- theme_set(theme_bw())
 # library('reshape')
  tmp <- data.frame(t=t, y=y)
  framed.data <- melt(tmp, id='t')
  
  nonparametric.graph <- ggplot(framed.data,
                         aes(x=t, y=value, group=variable, colour=variable))
  nonparametric.graph <- nonparametric.graph + geom_line() + 
    ggtitle('Nonparametric density')
  
  print(nonparametric.graph)
  
  if(comp){
   # library('moments')
    ## Gaussian
    z <- dnorm((t-mu)/std.x)/std.x
    
    ## Johnson-SU
    sk <- skewness(x)
    ku <- kurtosis(x)
    moments <- c(mu,std.x,sk,ku)
    
    ## get parameters
    param.j <- est.johnson.su(moments)$parameters
    a <- param.j[1]
    b <- param.j[2]
    c <- param.j[3] 
    d <- param.j[4]
    
    ## compute density
    v <- ( t - a ) / b
    vv <- sqrt( 1 + v ^ 2 )
    lawJ <- (d / b) * dnorm( c + d * log( v + vv ) ) / vv
    
    ## Student t
    if(ku > 3){ 
    
    # estimate degrees of freedom 
    r <- 4 + 6 / ( ku - 3 )
    
    # compute density
    vol <- std.x * sqrt( (r-2) / r )          
    lawT <- dt( (t-mu) / vol, r,0 ) / vol  
    
    }
    
   
    
    ## Graphs
    #library('ggplot2')
    previous_theme <- theme_set(theme_bw())
    #library('reshape')
    
    if(ku > 3){
    tmp <- data.frame(t=t,y=y,z=z, lawT=lawT, lawJ=lawJ)
    names(tmp) <- c('t','Nonparametric','Gaussian', 'Student','Johnson')
    }else{
      tmp <- data.frame(t=t,y=y,z=z,  lsawJ=lawJ)
      names(tmp) <- c('t','Nonparametric','Gaussian', 'Johnson')
    }
    
    framed.data = melt(tmp, id='t')
    
    values.graph <- ggplot(framed.data,
                           aes(x=t, y=value, group=variable, colour=variable))
    values.graph <- values.graph + geom_line() + 
      ggtitle('Graph of estimated densities')
    print(values.graph)
    
    ## GOF tests
    pval.1   <- 2 * ( 1 - pnorm( sqrt( n / 6 ) * abs( sk ) ) )
    pval.2   <- 2 * ( 1 - pnorm( sqrt( n / 24 ) * abs( ku - 3 ) ) )
    jbr     <- - 2 * log( pval.1 ) - 2 * log( pval.2 ) #Improved Jarque-Berra test statistic
    jbr.pval <- 100*(1-pchisq(jbr,4) )# Improved Jarque-Berra test P-value
    jb      <- n * ( sk^2 / 6 + ( ku - 3 )^2 / 24 ) #Jarque-Berra test statistic
    jb.pval  <- 100*(1 - pchisq( jb, 2 )) #Jarque-Berra test P-value
    
    source('gof.gauss.1d.cvm.R')
    source('gof.gauss.1d.ks.R')
    
    cvm    <- gof.gauss.1d.cvm( x, 1000 );
    ks     <- gof.gauss.1d.ks( x, 1000 );
    
    ## Output for parameters
    cat(sprintf('\n'))
    cat(sprintf('estimated mean  %8f \n',mu))
    cat(sprintf('estimated standard deviation: %8f \n', std(x)))
    cat(sprintf('Skewness = %5f , p-value = %3.2f%% \n',sk,100*pval.1))
    cat(sprintf('Kurtosis = %5f , p-value = %3.2f%% \n',ku, 100*pval.2))
    if(ku > 3){ 
      cat(sprintf('estimated sigma for Student model: %8f \n', vol))
      cat(sprintf('estimated degrees of freedom for the Student distribution (method of moments) = %g \n',r))
  }
    
    ## Output for Gof tests
    cat(sprintf('\n\nGoodness-of-fit tests for the Gaussian distribution\n\n'))
    cat(sprintf('Jarque-Berra test         : jb  = %5.2f , P-value = %3.2f%% \n',jb, jb.pval))
    cat(sprintf('Improved Jarque-Berra test: jbr = %5.2f , P-value = %3.2f%% \n',jbr, jbr.pval))
    cat(sprintf('Lilliefors test           : KS  = %5.2f , P-value = %3.2f%% \n',ks$stat, ks$pvalue))
    cat(sprintf('Cramer-von Mises test     : CVM = %5.2f , P-value = %3.2f%% \n',cvm$stat, cvm$pvalue))
    cat(sprintf('\n\n1000 iterations were used to approximate the P-values of the Lilliefors and CVM tests\n'))
    cat(sprintf('\n'))
    stat = list(JB = jb, JBR = jbr, KS = ks$stat, CVM = cvm$stat)
    pvalue = list(JB = jb.pval,JBR = jbr.pval, KS = ks$pvalue, CVM = cvm$pvalue)
  }
  
  return(list(x=t,fn=y,stat=stat,pvalue=pvalue))
  
}
############################################################################################################

est.johnson.su <- function(estimated.moments){
  est.skew.kurt <- estimated.moments[3:4]
  library('pracma')
  
  param <- fsolve(function(x) inv.johnson.skew.kurt(x,c(0,1)),est.skew.kurt,maxiter = 10000)
  
  c <- param$x[1]
  d <- param$x[2]
  
  v1 <- exp(1/(2*d^2))*sinh(-c/d)
  v2 <- 0.5*(exp(2/(d^2))*cosh(2*c/d)-1)
  sigma0 <- sqrt(v2-v1^2)
  
  
  b <- estimated.moments[2]/sigma0
  
  a <- estimated.moments[1]-b*v1
  parameters <- mat.or.vec(1,4)
  
  parameters[2] = b
  parameters[1] = a
  
  parameters[3] = c
  parameters[4] = d
  johnson.moments <- mat.or.vec(1,4)
  johnson.moments[1] = a+b*v1
  johnson.moments[2] = b*sqrt(v2-v1^2)
  moments=inv.johnson.skew.kurt(param$x,est.skew.kurt)
  johnson.moments[3] = moments[1]+est.skew.kurt[1]
  johnson.moments[4] = moments[2]+est.skew.kurt[2]
  return(list(parameters=parameters, johnson.moments=johnson.moments))
}
###################################################################################################

inv.johnson.skew.kurt <- function(param,est){
  c <-param[1]
  d <-param[2]
  
  v1 <-exp(1/(2*d^2))*sinh(-c/d)
  v2 <-0.5*(exp(2/(d^2))*cosh(2*c/d)-1)
  v3 <-0.25*(exp(9/(2*d^2))*sinh(-3*c/d)-3*exp(1/(2*d^2))*sinh(-c/d))
  v4 <-(1/16)*(2*exp(8/(d^2))*cosh(4*c/d)-8*exp(2/(d^2))*cosh(2*c/d)+6)
  
  sigma0 <- sqrt(v2-v1^2)
  skew0 <- (v3-3*v1*v2+2*v1^3)/sigma0^3
  
  kurt0 <- (v4-4*v1*v3+6*v2*v1^2-3*v1^4)/sigma0^4
  
  return(c(skew0, kurt0)-est)
}
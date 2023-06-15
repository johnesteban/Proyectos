merton.pdf <- function(x,param,h,graph = FALSE){
  
  ##
  mu     <- param[1]
  sigma  <- param[2]
  lambda <- param[3]
  gamma  <- param[4]
  delta  <- param[5]
  
  
  mu1             <- mu * h
  sig1            <- sigma * sqrt( h )
  jumpIntensity   <- (lambda * h)
  kappa           <- exp( gamma + delta^2 / 2 ) - 1
  
  a <-     mu1 - jumpIntensity * kappa - 0.5*sig1^2 
  
  ##
  K <- 1
  err <-  Error(sig1,K,jumpIntensity,delta)
  
  while (err > 1E-10){
    K <- K+1
    err <-  Error(sig1,K,jumpIntensity,delta) #para ver a donde converge
  }
  
  ##
  tt <- (0:K)
  
  prob <- dpois(tt,jumpIntensity)
  
  
  mu2 <- a+tt*gamma
  sig2 <- sqrt(sig1^2+tt*delta^2)
  
  
  m <- length(x)
  
  xmat <- x %*% matrix(1,1,K+1)
  mumat <- matrix(1,m,1) %*% mu2
  
  sigmat <- matrix(1,m,1) %*% sig2
  
  z <- (xmat-mumat) / sigmat
  
  P <- exp(-0.5*z^2) / sigmat /sqrt(2*pi)
  
  f <- P %*% prob
  ##
  if(graph){
    plot(x,f,'l')
  }
  
  return(f)
}
##
Error <- function(sig1,k,jumpIntensity,delta){
  
  err <- (1-ppois(k,jumpIntensity))/sqrt(2*pi)/sqrt(sig1^2+k*delta^2)
  return(err)
}

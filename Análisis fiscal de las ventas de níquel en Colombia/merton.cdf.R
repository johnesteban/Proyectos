merton.cdf <- function(x,param,h,graph = FALSE){
  
  ##
  mu     <- param[1]
  sigma  <- param[2]
  lambda <- param[3]
  gamma  <- param[4]
  delta  <- param[5]
  
  
  mu1             <- mu * h
  sig1            <- sigma * sqrt( h )
  jumpIntensity   <- lambda * h
  kappa           <- exp( gamma + delta^2 / 2 ) - 1
  
  a <-     mu1 - jumpIntensity * kappa - 0.5*sig1^2 
  
  ##
  K <- qpois(1-1E-10,jumpIntensity)
  
  
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
  
  P <- pnorm(z)
  
  F <- P %*% prob
  ##
  if(graph){
    plot(x,F,'l')
  }
  return(F)
}

source('num.jacobian.R')
source('merton.pdf.R')
source('merton.cdf.R')
source('est.pdf.gk.R')
source('est.cdf.R')
require('ggplot2')
library('MASS')

est.merton2 <- function( data, method ='Hessian', h=1/12, significanceLevel=0.95 ){
  # This function estimates the parameters of the Merton Jump-Diffusion
  # model using a numerical method to maximize the likelihood. Fisher information
  # can be estimated with the Hessian matrix (fminunc output) or with the 
  # numerical gradients. See Appendix B.5.1 for more details.
  # 
  # Input    
  #           data: prices (column vector)
  #           method: 'Hessian' (default), 'num'
  #           h: time scale for daily data, h<-1/252 (default)
  #           significanceLevel (95# default).
  #
  # Output:   param: estimation of the parameter (annual time scale):
  #            mu, sigma, lambda, gamma, delta
  #           error:  significanceLevel# CI error for the parameters
  #           V: estimation of covariance matrix.
  # Example: 
  #  out <- est.merton(ApplePrices)
  
  
  ## compute and plot log-returns
  returns <- diff( log( data ), 1 )
  n       <- length( returns )
  
  ## PRE-OPTIMIZATION
  #theta <- (mu, log(sigma),log(lambda),gamma,log(delta))
  
  
  #do not start with a too small value we are working on the annual time scale for the likelihood
  initialGuess    <- mat.or.vec(5,1) # Initial values of the parameters
  #initialGuess[3] <- log(1/h)  # 5 per day
  
  ## OPTIMIZATION
  optim.results <- optim(initialGuess, function(x) sum(LogLikMerton( x, returns,h)), hessian=TRUE, method='BFGS' )
  
  ## OUTPUT
  theta <- optim.results$par
  hessian <- optim.results$hessian
  param <- TT(theta)
  
  cat(sprintf('\n\n'))
  
  lmin <- min(eigen(hessian)$values)
  if(lmin<0){
    cat(sprintf('\n The Hessian is not positive definite. Estimation errors are not reliable. The numerical method will be used instead\n\n'))
    method <- 'num'
  }
  
  if(method == 'Hessian'){
    FI <- hessian/n
    cat(sprintf('\n Fisher information computed with the numerical Hessian from fminunc (Appendix B.5.1)\n\n'))
  }else{ if(method == 'num'){
    J <- num.jacobian(function(x) LogLikMerton(x,returns,h),theta,0.001)
    cat(sprintf('\n Fisher information computed with the numerical gradient (App}ix B.5.1)\n\n'))
    FI <- cov(J)
  }}
  
  
  ## Corrections
  
  D <- Jacob(theta) #Jacobian matrix of the transformation for positiveness
  
  
  
  V <- D%*%ginv(FI)%*%D
  
  
  ## Precision
  
  criticalValue <- qnorm( 0.5 *(1+significanceLevel) )
  
  error  <- criticalValue * sqrt( diag(V) / n )
  
  
  
  names <- c('mu    ','sigma ','lambda','gamma ','delta ')
  ## Print output
  cat(sprintf(' %d%% Confidence Intervals for the parameters\n\n',100*significanceLevel))
  
  for(j in 1:5){
    cat(sprintf('%6s   %4.4f      +/-  %4.4f \n',names[j],param[j],error[j]))
  }
  
  
  x <- sort(returns)
  paramTrue <- c(0.08, 0.22, 100, 0.05, 0.005)
  
  est.res <- est.pdf.gk( x,250)
  t <- est.res$x
  g <- est.res$fn
  f   <- merton.pdf(t,param,h)
  fTrue   <- merton.pdf(t,paramTrue,h)
  
  
  tmp <- data.frame(x=t, f=f, g = g, true=fTrue)
  names(tmp) <- c('x','MertonEst','EstGK','MertonTrue')
  framed.data = melt(tmp, id='x')
  
  values.graph <- ggplot(framed.data,
                         aes(x=x, y=value, group=variable, colour=variable))
  
  values.graph <- values.graph + geom_line() + 
    ggtitle(sprintf('Comparaison of densities'))
  
  print(values.graph)
  
  
  pseudos <- merton.cdf(x,param,h)
  ret <- est.cdf( x )
  Edf <-ret$Edf
  pts <- ret$pts
  
  tmp <- data.frame(x=x, pseudos=pseudos, Edf = Edf)
  names(tmp) <- c('x','Merton','Empirical')
  framed.data = melt(tmp, id='x')
  
  values.graph <- ggplot(framed.data,
                         aes(x=x, y=value, group=variable, colour=variable))
  
  values.graph <- values.graph + geom_line() + 
    ggtitle(sprintf('Comparaison of distribution functions'))
  
  print(values.graph)
  return(list(param=param, error=error))
  
}

##  transformation of parameters
TT <-function(theta){
  
  param    <- exp(theta)
  param[1] <- theta[1]
  param[4] <- theta[4]
  return(param)
}

##  Jacobian matrix
Jacob <- function(theta){
  
  param <- TT(theta)
  
  D <- diag(param)
  D[1,1] <- 1
  D[4,4] <- 1
  return(D)
}


##
LogLikMerton <- function( theta, returns, h){
  # This function computes minus the log-likelihoods 
  #
  # Input
  #        theta <- (mu, log(sigma),log(lambda),gamma,log(delta))
  #        returns
  #        n (length of returns )
  #
  # Output
  #        LL: -log-likelihood
  #
  
  n <- length(returns)
  
  param <- TT(theta)
  
  # if(param(3) < 10)
  #  LL <- 1.0e+20*ones(n,1)
  #  return
  # end
  
  LL <- -log(merton.pdf(returns, param, h))
  
  if(any(is.infinite( LL )) || any(is.nan( LL )) || any(is.complex( LL ))){
    LL <- 1.0e+20*matrix(1,n-1,1)
    return(LL)
  }
  return(LL)
}
#out1<-est.merton2(segunda_col)
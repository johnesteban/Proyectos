sim.jump.diff.merton <- function(param, n, h=1/252,So, graph=FALSE ){
  # Simulation of a path of Merton's Jump Diffusion with Gaussian jumps of
  # mean gamma and variance delta^2 observed at periods $kh$.
  #
  # Input
  #       param: mu, sigma>0, lambda>0, gamma, delta>0 (annual parameters)
  #       n: number of observations
  #       h: time between observations (default h <-1/252 corresponding to
  #       daily onservations)
  #       graph: T if graph is requires, F(FALSE) otherwise (default).
  #
  #  Output
  #       S: prices, with S(0) <- 100.
  #
  # Example:
  #   S <- sim.jump.diff.merton(c(0.08,0.12,1000,-0.02,0.01),500,1/252,T)
  
  
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
  
  nbJumps         <- rpois(n, jumpIntensity)
  Z               <-a + gamma * nbJumps +  sqrt( sig1^2 + delta^2 * nbJumps ) * rnorm( n)
  S               <- So * exp( cumsum( Z ) )
  
  if(graph){
    plot(S,type='l',xlab="Time",ylab="Price")
    title(sprintf('Merton jump diffusion with \u03BC = %2.2f, \u03C3 = %2.2f,  \u03BB = %2.2f, 
                and Gaussian jump parameters \u03B3 = %2.2f,  \u03B4 = %3.3f',mu,sigma,lambda, gamma, delta))
    
  }
  return(S)
}
S1 <- sim.jump.diff.merton(c(0.08, 0.22, 100, 0.05, 0.005),500,1/252,100,T)
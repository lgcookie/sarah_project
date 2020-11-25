# python files with the aerodynamics coefficients
# at discrete values of the angle of attack alpha and
# elevator angle delta_el
 
 
# importing modules
import numpy as np
import math
 
alpha = np.array([-16,-12,-8,-4,-2,0,2,4,8,12])
delta_el  = np.array([-20,-10,0,10,20])
 
CD = np.array([
    0.115000000000000
  , 0.079000000000000
  , 0.047000000000000
  , 0.031000000000000
  , 0.027000000000000
  , 0.027000000000000
  , 0.029000000000000
  , 0.034000000000000
  , 0.054000000000000
  , 0.089000000000000
  ])
 
 
CL = np.array([
   -1.421000000000000
  ,-1.092000000000000
  ,-0.695000000000000
  ,-0.312000000000000
  ,-0.132000000000000
  , 0.041000000000000
  , 0.218000000000000
  , 0.402000000000000
  , 0.786000000000000
  , 1.186000000000000
  ])
 
CM = np.array([
    0.077500000000000
  , 0.066300000000000
  , 0.053000000000000
  , 0.033700000000000
  , 0.021700000000000
  , 0.007300000000000
  ,-0.009000000000000
  ,-0.026300000000000
  ,-0.063200000000000
  ,-0.123500000000000
  ])
 
CL_el = np.array([
   -0.051000000000000
  ,-0.038000000000000
  ,                 0
  , 0.038000000000000
  , 0.052000000000000
  ])
 
CM_el = np.array([
    0.084200000000000
  , 0.060100000000000
  ,-0.000100000000000
  ,-0.060100000000000
  ,-0.084300000000000
  ])
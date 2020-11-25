# importing modules
import numpy as np
import math
from scipy import optimize
#--------------------------------------
# Importing experimental data to calculate coefficients
import aero_table

# Defining the function which will be used to fit the experimental data and give coefficients
def curve_fit(function, ind_var1, ind_var2, initial_guess): 
    # The results of curve_fit give two variables of two lists, the first list we assign to params, the second to params_cov
    params, params_covariance = optimize.curve_fit(function, ind_var1, ind_var2, p0= initial_guess)
    
    # Create an empty list which we will then add the coefficients to
    coeffs =[]
    for i in range(0,len(params)): 
        coeffs.append(params[i])
    return coeffs

# Determine each coefficient by giving it the relevant functional form, independant variable data and guesses

CL_0, CL_alpha = curve_fit(lambda x,a,b: a+b*x, (math.pi/180) *aero_table.alpha, aero_table.CL, (0.0410,0.1))
CL_delta = (curve_fit(lambda x,a: a*x, (math.pi/180) * aero_table.delta_el, aero_table.CL_el, (0.003)))[0]
CD_0, CD_k = curve_fit(lambda x,a,b: a+b*x**2, aero_table.CL, aero_table.CD, (0.026,0.045))
CM_0, CM_alpha = curve_fit(lambda x,a,b: a+b*x, (math.pi/180) * aero_table.alpha, aero_table.CM, (0,-0.01))
CM_delta= curve_fit(lambda x,a: a*x, (math.pi/180) * aero_table.delta_el,  aero_table.CM_el, (-0.004))[0]

# Store the set of coefficients as a dictionary which can then be accessed when working out trim conditions
set_coeffs = {
                'CL_0':CL_0,
                'CL_alpha': CL_alpha,
                'CL_delta': CL_delta,
                'CD_0': CD_0,
                'CD_k': CD_k,
                'CM_0': CM_0,
                'CM_alpha': CM_alpha,
                'CM_delta': CM_delta
                }





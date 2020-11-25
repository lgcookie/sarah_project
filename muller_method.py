# This module is used to store the Muller Method, we can therefore call it in the initial_trim module to work out alpha
import numpy as np



class MullerClass():
    
    def __init__(self):
        pass
       
    # This function creates the function which we then solve for alpha
    def alpha_func(self,aero_coeffs):
        C = 0.5*self.wing_sur*self.air_density*self.velocity**2
        W = self.weight
        f = lambda a: -C*(aero_coeffs['CL_0']+ aero_coeffs['CL_alpha']*a + aero_coeffs['CL_delta']*(-(aero_coeffs['CM_0'] + aero_coeffs['CM_alpha']*a)/aero_coeffs['CM_delta']))*np.cos(a) - C*(aero_coeffs['CD_0'] + aero_coeffs['CD_k']*(aero_coeffs['CL_0'] + aero_coeffs['CL_alpha']*a + aero_coeffs['CL_delta']*(-(aero_coeffs['CM_0'] + aero_coeffs['CM_alpha']*a)/aero_coeffs['CM_delta']))**2)*np.sin(a) + W*np.cos((a+self.flight_path_angle))
        return f
        
    # This function will execute the muller method on the function we provide it
    def muller_meth(f,xr,h,epsilon,N):
        for i in range(1,N+1):

            #x2 is set to the first estimate of root xr

            x2 = xr

            x1 = xr + h*xr

            x0 = xr - h*xr

            # Stores two step sizes in h variables

            h0 = x1-x0

            h1 = x2-x1
            # Calculate two slopes
            f0 = f(x0)
            f1 = f(x1)
            f2 = f(x2)

            delta_0 = (f1-f0)/h0

            delta_1 = (f2-f1)/h1

            # Calculate three coefficients of test polynomial

            a = (delta_1-delta_0)/(h1+h0)

            b = a*h1 + delta_1

            c = f2

            rad = np.sqrt(b*b - 4*a*c)

           

            if (abs(b+rad) > abs(b-rad)):

                den=(b+rad)

            else:

                den=(b-rad)

               

            dxr=-2*c/den

            xr=float(x2+dxr)

            # print(f'Iteration {i}: Estimate of Root {xr}')

           

            if abs(dxr)<epsilon or i>=N:

                break

           

            x0=x1

            x1=x2

            x2=xr

           

        return xr, i


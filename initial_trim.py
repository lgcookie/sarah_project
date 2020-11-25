import numpy as np
import aero_coeff
from muller_method import MullerClass

class Trim_Conditions(): 

	def __init__(self, aero_coeffs, velocity, flight_path_angle, altitude=2000): 

		# Starting values, import aero_coeffs
		self.velocity = velocity
		self.flight_path_angle = flight_path_angle
		self.wing_sur = 20
		self.cbar = 1.75
		self.acMass = 1300
		self.inertia_yy = 7000
		self.gravity =9.81
		self.weight = self.gravity*self.acMass
		self.air_density = 1.0065
		self.M = 0
		self.Cm = 0
		self.q = 0
		self.x_pos = 0
		self.z_pos = 0
		self.altitude = altitude
		self.ze = -altitude

		# Find alpha
		self.alpha = self.alpha_calculator(aero_coeffs)

		# Find remaining results
		self.remaining_parameters(aero_coeffs)

		# Create dictionary for results 
		self.results = self.collect_results(aero_coeffs)


		
		

		# Calculates alpha using Muller method
	def alpha_calculator(self, aero_coeffs): 
		# Calculate alpha from Muller Class
		func = MullerClass.alpha_func(self,aero_coeffs)
		# self.alpha = MullerClass.MullerFunc(self,0, 0.01, 0.02, 0.1, 1000)
		alpha = MullerClass.muller_meth(func,0.1,0.9,0.000000001,10)[0] 
		return alpha
		
		# Calculates remaining parameters after finding alpha
	def remaining_parameters(self, aero_coeffs):
		#∫Calculate remaining parameters
		self.delta = self.delta_calc(aero_coeffs)
		self.Cl = self.Cl_calc(aero_coeffs)
		self.Cd = self.Cd_calc(aero_coeffs)
		self.drag = self.drag_calc()
		self.lift = self.lift_calc()
		self.thrust = self.thrust_calc()
		self.h_vel = self.h_vel_calc()
		self.v_vel = self.v_vel_calc()
		self.pitch_angle = self.theta_calc()
		self.theta = self.theta_calc()
	
	# Calculates delta after determining alpha 
	def delta_calc(self, aero_coeffs):
		delta = -(aero_coeffs['CM_0']+aero_coeffs['CM_alpha']*self.alpha)/aero_coeffs['CM_delta']
		return delta

	# Calculates CL after getting delta and alpha
	def Cl_calc(self, aero_coeffs):
		alpha = float(self.alpha)
		CL= aero_coeffs['CL_0']+alpha*aero_coeffs['CL_alpha']+self.delta*aero_coeffs['CL_delta']
		return CL

	# Calculates lift after Cl
	def lift_calc(self):
		lift = 0.5*self.air_density*self.wing_sur*self.Cl*(self.velocity*self.velocity)
		return lift

	# Calculates Cd after getting delta 
	def Cd_calc(self, aero_coeffs):
		CD = aero_coeffs['CD_0']+aero_coeffs['CD_k']*self.Cl**2
		return CD

	# Calculates drag after getting Cd
	def drag_calc(self):
		drag = 0.5*self.air_density*self.wing_sur*self.Cd*(self.velocity*self.velocity)
		return drag



	# Calculates thrust after getting delta and alpha
	def thrust_calc(self):
		thrust= self.weight*np.sin(self.flight_path_angle+self.alpha)+self.drag*np.cos(self.alpha)-self.lift*np.sin(self.alpha)
		return thrust

	# Calculates horizontal velocity after getting alpha

	def h_vel_calc(self):
		h_vel= np.cos(self.alpha)*self.velocity
		return h_vel

	# Calculates vertical velocity after getting alpha
	def v_vel_calc(self):
		v_vel = np.sin(self.alpha)*self.velocity
		return v_vel

	# Calculates theta
	def theta_calc(self): 
		theta = self.alpha + self.flight_path_angle
		return theta

	# Calculates pitch angle after getting alpha
	def theta_calc(self): 
		theta = self.alpha + self.flight_path_angle
		return theta

	# Create dictionary for trim condition and adds it to aero_coefficient results
	def collect_results(self, aero_coeffs): 
		results = {**vars(self), **aero_coeffs}
		return results

	# Print results to screen
	def print_results(self): 
		for key, value in self.results.items(): 
			print(f"\n{key} = {value}")
		return self.results




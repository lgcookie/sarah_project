from math import sin, cos, tan, asin, acos, atan, sqrt, ceil, radians
import matplotlib.pyplot as plt 
import ODE_graph

class CommandChange(): 

	def __init__(self, initial_trim, aero_coeffs, delta_change, thrust_change, time_change, sim_time, step_change, alt_target, graph_output = True):
		
		self.results = initial_trim

		# Creates dictionary with lists for each set of results, updates new thrust and time_change
		self.results = self.ind_lists(thrust_change, delta_change, time_change)

		# Creates dictionary to store derivatives 
		self.dt = self.dt_values()

		# Changes non ode vars given new thurst and delta
		self.results = self.update_non_ode_vals(aero_coeffs, step_change)
		self.results['time'][-1]= time_change
		self.results['velocity'][-1]= 100

		# Populates results with oscillatory values for pre-specified sim_time
		self.results = self.get_transient_vals(aero_coeffs, sim_time, step_change, alt_target)

		if graph_output:
			ODE_graph.ODE_graphs(self.results)
		


	def ind_lists(self, thrust_change, delta_change, time_change): 
		
		# Creates individual lists for each variable within the big dictionary which stores all the variables
		for key, value in self.results.items(): 
			self.results[key] = list()
			for i in range(time_change):
				self.results[key].append(value)

		# Creates time index for before command change and updates thrust and delta
		self.results['time']=[t for t in range(time_change)]
		self.results['thrust'][-1] = self.results['thrust'][-1]*thrust_change
		self.results['delta'][-1] = self.results['delta'][-1]*delta_change
		return  self.results

	def get_transient_vals(self,aero_coeffs, sim_time, step_change, alt_target):

		if sim_time:
			iterations= ceil(sim_time/step_change)

			for x in range(iterations):
				# Populates the derivative dictionary using prior trim condition
				self.fill_dt_dict()
				# Adds the change in parameter to prior value to get new value
				self.ode_new_val(step_change)
				
				# Changes values for non dof variables
				self.update_non_ode_vals(aero_coeffs, step_change)
		
		elif alt_target:
			while self.results['altitude'][-1] <alt_target: 
				self.fill_dt_dict()
				# Adds the change in parameter to prior value to get new value
				self.ode_new_val(step_change)
				
				# Changes values for non dof variables
				self.update_non_ode_vals(aero_coeffs, step_change)
				altitude = self.results['altitude'][-1]

		return self.results
		
	def dt_values(self):
		# Creates an empty dictionary for storing derivative values, note this is 0 for non ODE variables.
		dt = {}
		for key in self.results.keys(): 
			dt[key]=[]
		return dt

	def fill_dt_dict(self):
		# Calculates the derivative based on the last set of values
		self.dt['q'].append(self.d_func_q())
		self.dt['theta'].append(self.d_func_theta())
		self.dt['h_vel'].append(self.d_func_hvel())
		self.dt['v_vel'].append(self.d_func_vvel())
		self.dt['x_pos'].append(self.d_func_x_position())
		self.dt['altitude'].append(-self.d_func_z_position())
		self.dt['ze'].append(self.d_func_z_position())


	def ode_new_val(self, step): 
		# This calculates the variables that have a dof, by adding the recent derivative value to its last value
		self.dof_vars = ['q', 'theta', 'h_vel', 'v_vel', 'x_pos', 'altitude', 'ze']
		for key, value in self.dt.items(): 
			if key in self.dof_vars:
				new_val = self.results[key][-1] + value[-1]*step
				self.results[key].append(new_val)
		return self.results

	def update_non_ode_vals(self, aero_coeffs, step_change): 
		# Calculates non_ode values given ode values
		
		self.results['velocity'].append(self.velocity_calc())
		self.results['time'].append((self.results['time'][-1]+step_change))
		self.results['alpha'].append(self.alpha_calc())
		self.results['flight_path_angle'].append(self.results['theta'][-1]-self.results['alpha'][-1])
		self.results['Cl'].append(self.Cl_calc(aero_coeffs))
		self.results['Cd'].append(self.Cd_calc(aero_coeffs))
		self.results['Cm'].append(self.Cm_calc(aero_coeffs))
		self.results['drag'].append(self.Drag_calc())
		self.results['lift'].append(self.Lift_calc())
		self.results['M'].append(self.M_calc())
		
		return self.results

	def velocity_calc(self): 
		last = self.results
		squared_sum = last['h_vel'][-1]**2 + last['v_vel'][-1]**2
		velocity = sqrt(squared_sum)
		return velocity

	def alpha_calc(self): 
		last = self.results
		alpha = atan(last['v_vel'][-1]/last['h_vel'][-1])
		return alpha


	def d_func_theta(self):
		last = self.results
		d_theta = last['q'][-1]
		return d_theta

	def d_func_q(self): 
		last = self.results
		d_q = last['M'][-1]/last['inertia_yy'][-1]
		return d_q

	def d_func_hvel(self): 
		last = self.results
		d_hvel = ((last['lift'][-1])*sin(last['alpha'][-1]))-(last['drag'][-1]*cos(last['alpha'][-1]))-(last['q'][-1]*last['v_vel'][-1]*last['acMass'][-1])-(last['weight'][-1]*sin(last['theta'][-1]))+(last['thrust'][-1])
		d_hvel = (1/last['acMass'][-1])*d_hvel
		
		return d_hvel

	def d_func_vvel(self): 
		last = self.results
		d_vvel = -((last['lift'][-1])*cos(last['alpha'][-1]))-((last['drag'][-1])*sin(last['alpha'][-1]))+(last['q'][-1]*last['h_vel'][-1]*last['acMass'][-1])+(last['weight'][-1])*cos(last['theta'][-1])
		d_vvel = d_vvel*(1/last['acMass'][-1])
		
		return d_vvel

	def d_func_x_position(self): 
		last = self.results
		d_x_position = last['h_vel'][-1]*cos(last['theta'][-1])+last['v_vel'][-1]*sin(last['theta'][-1])
		
		return d_x_position

	def d_func_z_position(self): 
		last = self.results
		d_z_position = -last['h_vel'][-1]*sin(last['theta'][-1])+last['v_vel'][-1]*cos(last['theta'][-1])
		return d_z_position

	def Cl_calc(self, aero_coeffs):
		last = self.results
		CL= aero_coeffs['CL_0']+(last['alpha'][-1]*aero_coeffs['CL_alpha'])+(last['delta'][-1]*aero_coeffs['CL_delta'])
		return CL

	def Cd_calc(self, aero_coeffs):
		last = self.results
		CD = aero_coeffs['CD_0']+(aero_coeffs['CD_k']*last['Cl'][-1]**2)
		return CD

	def Cm_calc(self, aero_coeffs):
		last = self.results
		Cm = aero_coeffs['CM_0']+(last['alpha'][-1]*aero_coeffs['CM_alpha'])+(last['delta'][-1]*aero_coeffs['CM_delta'])
		return Cm

	def Drag_calc(self):
		last = self.results
		drag = 0.5*last['air_density'][-1]*last['wing_sur'][-1]*last['Cd'][-1]*(last['velocity'][-1]**2)
		return drag

	def Lift_calc(self):
		last = self.results
		lift = 0.5*last['air_density'][-1]*last['wing_sur'][-1]*last['Cl'][-1]*(last['velocity'][-1]**2)
		return lift

	def M_calc(self):
		last = self.results
		M = 0.5*last['wing_sur'][-1]*last['air_density'][-1]*last['Cm'][-1]*(last['velocity'][-1]**2)*last['cbar'][-1]
		return M







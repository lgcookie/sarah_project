from initial_trim import Trim_Conditions
import aero_coeff
import aero_table
import math

import matplotlib.pyplot as plt 
import graph_creator

class VelocityVary():

	def __init__(self, aero_coeff, start_vel, flight_path_angle):
		# Creates empty data list which will store all trim conditions 
		self.data = []

		# Works out initial trim and adds this to data list
		self.initial_trim = Trim_Conditions(aero_coeff, start_vel, flight_path_angle)
		self.data.append(self.initial_trim.results)

		# Checks if first trim does not violate physical constraints
		self.constraint_check()

		# Adjusts the velocity, holding flight angle constant, and calculates trim
		self.velocity_adjustment(aero_coeff, start_vel, flight_path_angle, 1)

		# Calculates trim in opposite direction (decreases velocity holding angle constant)
		self.constraint =True
		self.velocity_adjustment(aero_coeff, start_vel, flight_path_angle, -1)

		# Produces data that can be used for graphs
		self.list_generator()

		# Produces graph given user input

		# graph_creator.plot_generator(self, vel_vary=True)
		self.vel_vary1, self.vel_vary2 = graph_creator.plot_generator(self, vel_vary=True)
		


		

	def velocity_adjustment(self, aero_coeff, start_vel, flight_path_angle, direction):
		velocity = start_vel 

		# While the current trim conditions do not violate any physical constraints, this will change velocity
		while self.constraint:

			# Increments velocity then calculates new trim
			velocity = velocity + direction
			new_trim = Trim_Conditions(aero_coeff, velocity, flight_path_angle)

			# Adds new trim results to existing data set
			self.data.append(new_trim.results)
			self.all_alphas.append(new_trim.results['alpha'])
			self.all_deltas.append(new_trim.results['delta'])

			# Checks if new trim does not violate physical constraints, repeats if not.
			self.constraint_check()


	def constraint_check(self): 
		# Creates list for each parameter in every trim condition collected.
		self.all_alphas = [x['alpha'] for x in self.data]
		self.all_deltas = [x['delta'] for x in self.data]
		self.all_thrust = [x['thrust'] for x in self.data]
		self.all_h_vel =[x['h_vel'] for x in self.data]
		self.all_v_vel =[x['v_vel'] for x in self.data]

		# Ensures alpha and delta are within experimental range. 
		alpha_cond = [x*(math.pi/180) for x in aero_table.alpha]
		delta_cond = [x*(math.pi/180) for x in aero_table.delta_el] 

		# Sets constraint to True so it can run first iteration. (Probably possible to bug it if you fed it data which already violates it...)
		self.constraint = True
		
		# Checks that current trim conditions do not violate physical constraints.
		if (self.all_alphas[-1] > min(alpha_cond) and self.all_alphas[-1] < max(alpha_cond) 
		and self.all_deltas[-1] > min(delta_cond) and self.all_deltas[-1] < max(delta_cond) 
		and self.all_thrust[-1] >0 and self.all_h_vel[-1]>0 and self.all_v_vel[-1]>0): 
			self.constraint = True 
		else: 
			self.constraint = False
			# Removes the last entry as this trim condition violates the constraints.
			del self.data[-1]

		return self.constraint

	def list_generator(self):
		# Generates lists of data for graphs from list of dictionaries
		self.data = sorted(self.data, key=lambda k: k['velocity'])
		self.all_vels = [x['velocity'] for x in self.data]
		self.all_alphas = [x['alpha'] for x in self.data]
		self.all_deltas = [x['delta'] for x in self.data]
		self.all_thrusts = [x['thrust'] for x in self.data]
		self.all_angles = [x['flight_path_angle'] for x in self.data]
		
		
















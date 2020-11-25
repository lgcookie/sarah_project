from initial_trim import Trim_Conditions
import aero_coeff
import aero_table
from flight_path_angle_adjustment import AngleVary
from ODE import CommandChange
import initial_trim
from velocity_adjustment import VelocityVary
import matplotlib.pyplot as plt 
import ODE_graph
from math import sin, cos, tan, asin, acos, atan, sqrt, ceil, radians
import complete_sim_graphs

def B2(aero_coeffs, start_vel, step_change, trim_change = 10):
	
	# Find three trim conditions 
	first_trim = initial_trim.Trim_Conditions(aero_coeffs, start_vel, 0, 1000)
	second_trim = initial_trim.Trim_Conditions(aero_coeffs, start_vel, 0.02, 1000)
	third_trim = initial_trim.Trim_Conditions(aero_coeffs, start_vel, 0, 2000)

	# Find increases in delta and thurst from trim 1 to trim 2. 
	delta_change = second_trim.results['delta']/first_trim.results['delta']
	thrust_change = second_trim.results['thrust']/first_trim.results['thrust']

	# Simulate new system, do not pass it a simulation time as it simulates until new altitude reached
	changed_commands = CommandChange(first_trim.results, aero_coeffs, delta_change, thrust_change, trim_change, False, 0.01, 2000, False)
	
	time_taken = ceil(changed_commands.results['time'][-1]- trim_change)
	print(f"Time taken to reach 2000m altitude:{time_taken}seconds")

	# Collects new starting information for final command change
	changed_trim = {} 
	for key, value in changed_commands.results.items(): 
		changed_trim[key] = value[-1]
	
	# Reverse back to original trim conditions
	final_commands = CommandChange(changed_trim, aero_coeffs, 1/delta_change, 1/thrust_change, 1, 500, 0.01, False, False)

	# Adjusts time variable 
	final_commands.results['time'] = [t + trim_change + time_taken for t in final_commands.results['time']]
	
	complete_simulation = {}
	for key in final_commands.results.keys(): 
		complete_simulation[key] = changed_commands.results[key]+final_commands.results[key]

	complete_sim_graphs.simulation_graphs(complete_simulation)



from initial_trim import Trim_Conditions
import aero_coeff
import aero_table
from flight_path_angle_adjustment import AngleVary
from ODE import CommandChange
import initial_trim
from velocity_adjustment import VelocityVary
import matplotlib.pyplot as plt 
import ODE_graph
import part_b2


def menu(aero_coeffs):

	while True: 
		user_choice = input("""
			Enter a to view aero-coefficients derived from data (part A.1)
			Enter i to calculate an initial trim (Part A.2)
			Enter c to run simulation with delta and thrust change (Part A.3)
			Enter r to trim plane for range of velocities (Part B.1)
			Enter s to run simulation with altitude change (Part B.2)
			Enter q to quit
			""")	

		if user_choice =="a": 
			for key, value in aero_coeffs.items(): 
				print(f"{key}:{value}")

		if user_choice == "i": 
			start_vel = float(input("what is starting velocity"))
			start_angle = float(input("What is starting angle"))
			int_trim = initial_trim.Trim_Conditions(aero_coeffs, start_vel, start_angle)
			for key, value in int_trim.results.items(): 
				print(f"{key}:{value}")

				
		if user_choice == "r":
			start_vel = float(input("what is starting velocity"))
			start_angle = float(input("What is starting angle"))
			int_trim = initial_trim.Trim_Conditions(aero_coeffs, start_vel, start_angle)
			for key, value in int_trim.results.items(): 
				print(f"{key}:{value}")
			vel_change = VelocityVary(aero_coeffs, start_vel, start_angle)
			angle_change = AngleVary(aero_coeffs, start_vel, start_angle)

		if user_choice == "c": 
			start_vel = float(input("what is starting velocity?"))
			start_angle = float(input("What is starting angle?"))
			trim_to_change = initial_trim.Trim_Conditions(aero_coeffs, start_vel, start_angle)
			print(f"Here is the initial trim conditions for the flight \n {trim_to_change.results}")
			delta_change = float(input("What is the factor delta change (10% increase = 1.1)?"))
			thrust_change = float(input("What is the factor thrust change (10% increase = 1.1)?"))
			time_change = int(input("What time does change occur?"))
			sim_time = int(input("How long is simulation?"))
			change = CommandChange(trim_to_change.results, aero_coeffs, delta_change, thrust_change, time_change, sim_time, 0.01, False)

		if user_choice == "s": 
			print("""
				Simulation at V=(100+ U)m/s at 0rad flight path angle for 10 seconds, 
				Thrust and delta changed to values in trim condition for V=(100+ U)m/s and 2rad flight path angle, 
				Simulation continues until altitude reaches 2000m, time for this is returned, 
				Revert back to initial delta and thrust until oscillations dumped. 
				U = oldest group members day of birth.
				""")
			date_of_birth = int(input("The oldest group member was born on what day of the month?(6)"))
			start_vel = 100 + date_of_birth
			simulation = part_b2.B2(aero_coeffs, start_vel, 0.01, 10)

		if user_choice == "q": 
			break 

menu(aero_coeff.set_coeffs)







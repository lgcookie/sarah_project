import matplotlib.pyplot as plt 




def plot_generator(self, vel_vary):


	if vel_vary == False:
		x_title, y_title, constant, x_data, y_data =  "Flight Path Angle \u03C0", "Thrust (m/s)", "Velocity (m/s)", self.all_angles, self.all_thrusts
		fig_1 = plot_constructor(x_title, y_title, constant, x_data, y_data)

		x_title, y_title, constant, x_data, y_data = "Flight Path Angle \u03C0", "Delta \u03C0", "Velocity (m/s)", self.all_angles, self.all_deltas
		fig_2 = plot_constructor(x_title, y_title, constant, x_data, y_data)


	else:
		x_title, y_title, constant, x_data, y_data = "Velocity (m/s)", "Thrust(m/s)", "Flight Path Angle \u03C0", self.all_vels, self.all_thrusts
		fig_1 = plot_constructor(x_title, y_title, constant, x_data, y_data)

		x_title, y_title, constant, x_data, y_data = "Velocity (m/s)", "Delta \u03C0", "Flight Path Angle \u03C0", self.all_vels, self.all_deltas
		fig_2 = plot_constructor(x_title, y_title, constant, x_data, y_data)

		


	return fig_1, fig_2
		


def plot_constructor(x_title, y_title, constant, x_data, y_data): 
		plt.style.use('seaborn-whitegrid')
		f, ax = plt.subplots()
		ax.scatter(x_data, y_data)
		

		# Set chart title and label axes.
		plt.title(f"{x_title} Against {y_title}, \n Holding {constant} Constant", fontsize=20)
		plt.xlabel(f"{x_title}", fontsize=20)
		plt.ylabel(f"{y_title}", fontsize=20)
		plt.tick_params(axis='both', which='major', labelsize=10)

		# Set size of tick labels.
		plt.tick_params(axis='both', labelsize=14)
		plt.tight_layout()
		plt.show()

		return ax








	
import matplotlib.pyplot as plt 

def simulation_graphs(data):

		data['time'] = data['time'][:-2]
		data['alpha'] = data['alpha'][:-2]
		data['flight_path_angle'] = data['flight_path_angle'][:-2]  

		graph_vars = ['h_vel', 'v_vel','q', 'theta', 'flight_path_angle','ze', 'alpha', 'altitude']
		graph_titles = ['uB', 'wB', 'q', 'theta', 'flight path gamma', 'zE', 'alpha', 'altitude h']
		
		fig = plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
		for i, key in enumerate(graph_vars):
			ax = fig.add_subplot(4, 2, i+1)
			ax.plot(data['time'], data[key])
			ax.set(xlabel='time', ylabel=graph_titles[i])
			ax.tick_params(axis='both', which='major', labelsize=10)

		plt.tight_layout()
		plt.show()
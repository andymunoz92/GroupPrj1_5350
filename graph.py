import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into a DataFrame
df = pd.read_csv('target\\results.csv')

def plot_for_p(df, m=None, n=None, q=None):
    # Filter DataFrame based on provided dimensions
    filtered_df = df
    filter_conditions = []
    if m is not None:
        filtered_df = filtered_df[filtered_df['m'] == m]
        filter_conditions.append(f'm={m}')
    if n is not None:
        filtered_df = filtered_df[filtered_df['n'] == n]
        filter_conditions.append(f'n={n}')
    if q is not None:
        filtered_df = filtered_df[filtered_df['q'] == q]
        filter_conditions.append(f'q={q}')

    # Define algorithm types and their labels
    algorithms = {
        'Parallel': {'label': 'Parallel', 'marker_speedup': 'o', 'marker_cost': 's', 'color': 'blue'},
        '1-DParallel': {'label': '1-D Parallel', 'marker_speedup': '^', 'marker_cost': 'p', 'color': 'green'},
        '2-DParallel': {'label': '2-D Parallel', 'marker_speedup': 'x', 'marker_cost': '*', 'color': 'red'}
    }

    # Plotting
    plt.figure(figsize=(10, 6))
    ax1 = plt.gca()  # Get current axis for Speedup
    ax2 = ax1.twinx()  # Create another axis for Cost

    for algo, details in algorithms.items():
        # Speedup and Cost column names
        speedup_column = f'{algo}Speedup'
        cost_column = f'{algo}Cost'

        if speedup_column in filtered_df.columns and cost_column in filtered_df.columns:
            ax1.plot(filtered_df['P'], filtered_df[speedup_column], label=f'{details["label"]} Speedup', 
                     marker=details['marker_speedup'], color=details['color'])
            ax2.plot(filtered_df['P'], filtered_df[cost_column], label=f'{details["label"]} Cost', 
                     marker=details['marker_cost'], color=details['color'])

    ax1.set_xlabel('Number of Processors (P)')
    ax1.set_ylabel('Speedup', color='blue')
    ax2.set_ylabel('Cost', color='red')

    # Construct the title with the available information
    title_elements = ['Speedup and Cost']
    title_elements.extend(filter_conditions)
    plt.title(' vs. '.join(title_elements))
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.grid(True)
    plt.show()





def plot_control_shape(df, m=None, n=None, q=None, P=16):
    # Filter DataFrame based on provided dimensions and number of processors
    filtered_df = df[df['P'] == P]
    if m is not None:
        filtered_df = filtered_df[filtered_df['m'] == m]
    if n is not None:
        filtered_df = filtered_df[filtered_df['n'] == n]
    if q is not None:
        filtered_df = filtered_df[filtered_df['q'] == q]

    # Define algorithm types, their labels, and unique markers
    algorithms = {
        'Parallel': {'label': 'Parallel', 'marker_speedup': 'o', 'marker_cost': 's', 'color': 'blue'},
        '1-DParallel': {'label': '1-D Parallel', 'marker_speedup': '^', 'marker_cost': 'p', 'color': 'green'},
        '2-DParallel': {'label': '2-D Parallel', 'marker_speedup': 'x', 'marker_cost': '*', 'color': 'red'}
    }

    # Plotting
    plt.figure(figsize=(10, 6))
    ax1 = plt.gca()  # Get current axis for Speedup
    ax2 = ax1.twinx()  # Create another axis for Cost

    x_axis_dim = 'm' if m is None else 'n' if n is None else 'q'
    
    for algo, details in algorithms.items():
        # Speedup and Cost column names
        speedup_column = f'{algo}Speedup'
        cost_column = f'{algo}Cost'

        sorted_df = filtered_df.sort_values(by=x_axis_dim)
        if speedup_column in sorted_df and cost_column in sorted_df:
            ax1.plot(sorted_df[x_axis_dim], sorted_df[speedup_column], label=f'{details["label"]} Speedup', 
                     marker=details['marker_speedup'], color=details['color'])
            ax2.plot(sorted_df[x_axis_dim], sorted_df[cost_column], label=f'{details["label"]} Cost', 
                     marker=details['marker_cost'], color=details['color'])

    ax1.set_xlabel(f'Value of {x_axis_dim.upper()}')
    ax1.set_ylabel('Speedup', color='blue')
    ax2.set_ylabel('Cost', color='red')
    title_elements = [f'Speedup and Cost for P={P}']
    if m is not None:
        title_elements.append(f'm={m}')
    if n is not None:
        title_elements.append(f'n={n}')
    if q is not None:
        title_elements.append(f'q={q}')
    plt.title(' and '.join(title_elements))
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.grid(True)
    plt.show()




def plot_times_for_size_steps(df, P):
   # Define the sizes for m, n, and q 
    size_steps = [(10, 10, 10), (25, 25, 25), (50, 50, 50), (100, 100, 100), (250, 250, 250), (500, 500, 500)]
    
    # Prepare size labels for x-axis
    size_labels = ['10,10,10', '25, 25, 25', '50,50,50', '100, 100, 100', '250,250,250', '500,500,500']
    
    # Define the algorithms and their properties for plotting
    algorithms = {
        'Serial' : {'color': 'black', 'marker': 's'},
        'Parallel': {'color': 'blue', 'marker': 'o'},
        '1-DParallel': {'color': 'green', 'marker': '^'},
        '2-DParallel': {'color': 'red', 'marker': 'x'}
    }

    # Prepare the plot
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # Dictionary to collect time data for plotting
    time_data = {algo: [] for algo in algorithms}

    # Collect data for each size step
    for sizes in size_steps:
        m, n, q = sizes
        subset_df = df[(df['P'] == P) & (df['m'] == m) & (df['n'] == n) & (df['q'] == q)]
        
        for algo in algorithms.keys():
            time_column = f'{algo}Time'
            if time_column in subset_df.columns:
                # Compute mean time to handle multiple entries
                mean_time = subset_df[time_column].mean()
                time_data[algo].append(mean_time)
            else:
                # Append None if no data available, to keep the indexes aligned
                time_data[algo].append(None)

    # Plotting each algorithm's time data
    for algo, times in time_data.items():
        if any(times):  # Check if there are any non-None times to plot
            ax.plot(size_labels, times, label=f'{algo}', 
                    color=algorithms[algo]['color'], marker=algorithms[algo]['marker'], linestyle='-', markersize=10)

    ax.set_xlabel('Matrix Size Increments (m, n, q)')
    ax.set_ylabel('Execution Time')
    plt.title(f'Connected Parallel Execution Times for Varying Matrix Sizes at P={P}')
    plt.legend()
    plt.grid(True)
    plt.show()


"""
Calls for shapeliness
"""
# # Vary m
# plot_control_shape(df, n=100, q=100)
# # Vary n
# plot_control_shape(df, m=100, q=100)
# # Vary q
# plot_control_shape(df, m=100, n=100)


"""
Calls for processorness
"""
# plot_for_p(df, m=10, n=10, q=10)
# plot_for_p(df, m=100, n=100, q=100)
# plot_for_p(df, m=500, n=500, q=500)


"""
Call for duration for asymptotic comparison
"""
# plot_times_for_size_steps(df, 16)
import json
import matplotlib.pyplot as plt
import os


def load_results(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return None

def plot_histograms_random(results,output_filename):
    ob_values = [result['OB_value'] for result in results]
    computing_times = [result['computing_time'] for result in results]

    # Plot histogram for OB values
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.hist(ob_values, bins=200, color='blue', edgecolor='black')
    plt.title('Histogram of OB Values')
    plt.xlabel('OB Value')
    plt.ylabel('Frequency')

    # Plot histogram for Computing Times
    plt.subplot(1, 2, 2)
    plt.hist(computing_times, bins=200, color='green', edgecolor='black')
    plt.title('Histogram of Computing Times')
    plt.xlabel('Computing Time (seconds)')
    plt.ylabel('Frequency')

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.savefig(output_filename, format='png')

    #plt.show()

def plot_histograms_comparing(results,output_filename):
    # Extract values from the results
    initial_ob_values = [result['initial_OB_value'] for result in results]
    new_ob_values = [result['new_OB_value'] for result in results]
    computing_times = [result['computing_time'] for result in results]
    
    # Plot histogram for OB values
    plt.figure(figsize=(12, 6))

    # Plot initial OB values
    plt.subplot(1, 2, 1)
    plt.hist(initial_ob_values, bins=50, alpha=0.5, label='Initial OB', color='blue', edgecolor='black', density=True)
    plt.hist(new_ob_values, bins=50, alpha=0.5, label='New OB', color='orange', edgecolor='black', density=True)
    plt.title('Histogram of OB Values')
    plt.xlabel('OB Value')
    plt.ylabel('Density')
    plt.legend()

    # Plot histogram for Computing Times
    plt.subplot(1, 2, 2)
    plt.hist(computing_times, bins=50, color='green', edgecolor='black')
    plt.title('Histogram of Computing Times')
    plt.xlabel('Computing Time (seconds)')
    plt.ylabel('Frequency')

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.savefig(output_filename, format='png')
    # plt.show()  # Uncomment this line if you want to display the plot

    #plt.show()

def plot_histograms_comparing_two(results1, results2, output_filename):
    # Extract values from the first results file
    initial_ob_values1 = [result['initial_OB_value'] for result in results1]
    new_ob_values1 = [result['new_OB_value'] for result in results1]
    computing_times1 = [result['computing_time'] for result in results1]
    
    # Extract values from the second results file
    initial_ob_values2 = [result['initial_OB_value'] for result in results2]
    new_ob_values2 = [result['new_OB_value'] for result in results2]
    computing_times2 = [result['computing_time'] for result in results2]

    # Create figure for OB value histograms
    plt.figure(figsize=(14, 6))

    # Plot OB values for both result sets in the first subplot
    plt.subplot(1, 2, 1)
    plt.hist(initial_ob_values1, bins=50, alpha=0.5, label='Initial OB - Set 1', edgecolor='black', density=True)
    plt.hist(new_ob_values1, bins=50, alpha=0.5, label='New OB - Set 1', edgecolor='black', density=True)
    plt.hist(initial_ob_values2, bins=50, alpha=0.5, label='Initial OB - Set 2', edgecolor='black', linestyle='dashed', density=True)
    plt.hist(new_ob_values2, bins=50, alpha=0.5, label='New OB - Set 2', edgecolor='black', linestyle='dashed', density=True)
    plt.title('Histogram of OB Values for Two Results Sets')
    plt.xlabel('OB Value')
    plt.ylabel('Density')
    plt.legend()

    # Plot computing times for both result sets in the second subplot
    plt.subplot(1, 2, 2)
    plt.hist(computing_times1, bins=50, color='green', alpha=0.5, edgecolor='black', label='Computing Time - Set 1')
    plt.hist(computing_times2, bins=50, color='purple', alpha=0.5, edgecolor='black', label='Computing Time - Set 2')
    plt.title('Histogram of Computing Times for Two Results Sets')
    plt.xlabel('Computing Time (seconds)')
    plt.ylabel('Frequency')
    plt.legend()

    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig(output_filename, format='png')
    plt.close()  # Close the plot to free up memory if running multiple plots

if __name__ == "__main__":
    os.makedirs('plots', exist_ok=True)

# Load the results from the JSON file
    iteration=1
    for i in range(1, 2):
        for cities in range(20, 120, 20):
            for n in range (1,5,1):     
                items=n*cities          
                results_filename = f'tour_results/random_results/TTP_instances_{cities}_items_{items}/results_random_iteration_{i}_cities_{cities}_items_{items}.json'
                output_filename=f'plots/visualization_random_tour_cities_iteration_{i}_cities_{cities}_items_{items}.png'
                results = load_results(results_filename)
                plot_histograms_random(results,output_filename)
                print(f"Results saved to {output_filename}")
#results_filename = 'results_random.json'
#results = load_results(results_filename,'visualization_random_tour_cities_20_items_20')
    for cities in range(20, 120, 20):
        #print(cities)
        for n in range(1, 5): 
            #print(n)    
            items = n * cities
            #input_folder_problem_instances = f'problem_instances_ttp/json_files_TTP_instances_{cities}_items_{items}'

            result_file=f'tour_results/hillclimber_tsp_swapping_results/TTP_instances_{cities}_items_{items}/results_hillclimber_tsp_cities_{cities}_items_{items}.json'
            output_filename=f'plots/visualization_hillclimber_test_cities_iteration_cities_{cities}_items_{items}.png'
            results = load_results(result_file)
            plot_histograms_comparing(results,output_filename)
            print(f"Results saved to {output_filename}")
    
    for cities in range(20, 120, 20):
        #print(cities)
        for n in range(1, 5): 
            #print(n)    
            items = n * cities
            #input_folder_problem_instances = f'problem_instances_ttp/json_files_TTP_instances_{cities}_items_{items}'
            result_file_TSP=f'tour_results/hillclimber_tsp_swapping_results/TTP_instances_{cities}_items_{items}/results_hillclimber_tsp_cities_{cities}_items_{items}.json'
            result_file_hybride=f'tour_results/hillclimber_hybride_results/TTP_instances_{cities}_items_{items}/results_hillclimber_tsp_cities_{cities}_items_{items}.json'
            output_filename=f'plots/visualization_hillclimber_hybride_TSP_comparison_cities_{cities}_items_{items}.png'
            results1 = load_results(result_file_TSP)
            results2= load_results(result_file_hybride)
            plot_histograms_comparing_two(results1,results2,output_filename)
            print(f"Results saved to {output_filename}")
       
    for cities in range(20, 120, 20):
        #print(cities)
        for n in range(1, 5): 
            #print(n)    
            items = n * cities
            #input_folder_problem_instances = f'problem_instances_ttp/json_files_TTP_instances_{cities}_items_{items}'

            result_file=f'tour_results/hillclimber_hybride_results/TTP_instances_{cities}_items_{items}/results_hillclimber_tsp_cities_{cities}_items_{items}.json'
            output_filename=f'plots/visualization_hillclimber_hybride_cities_{cities}_items_{items}.png'
            results = load_results(result_file)
            plot_histograms_comparing(results,output_filename)
            print(f"Results saved to {output_filename}")

# Plot histograms
#plot_histograms(results)
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

def plot_histograms(results,output_filename):
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

os.makedirs('plots', exist_ok=True)

# Load the results from the JSON file
for cities in range(20, 120, 20):
    for n in range (1,5,1):     
        items=n*cities          
        results_filename = f'tour_results/results_random_cities_{cities}_items{items}.json'
        output_filename=f'plots/visualization_random_tour_cities_{cities}_items_{items}.png'
        results = load_results(results_filename)
        plot_histograms(results,output_filename)
        print(f"Results saved to {results_filename}")
#results_filename = 'results_random.json'
#results = load_results(results_filename,'visualization_random_tour_cities_20_items_20')

# Plot histograms
#plot_histograms(results)
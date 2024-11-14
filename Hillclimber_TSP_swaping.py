import json
import random
import math
import os
import matplotlib.pyplot as plt
import TTP_random_tour_and_packing_list
import TTP_Generator
from multiprocessing import Pool, cpu_count
import Iteration_search
import time


def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_json(filename):
    """Load a JSON file and return its contents."""
    with open(filename, 'r') as file:
        return json.load(file)

#def objective_function(tour, items, distances, vmax, vmin, W, R):
#    total_value = 0
#    total_weight = 0
#    total_distance = 0
#    for i in range(len(tour)):
#        current_city = tour[i]
#        next_city = tour[(i + 1) % len(tour)]
#        total_distance += distances[current_city][next_city]
#        for item in items:
#            if item['city'] == current_city:
#                total_value += item['value']
#                total_weight += item['weight']
#    speed = vmax - (vmax - vmin) * (total_weight / W)
#    travel_time = total_distance / speed
#    cost = travel_time * R
#    return total_value - cost

def hillclimber_tsp_swap(ttp, random_sample, iterations):
    cities = ttp['cities']
    #print(cities)
    items = ttp['items']
    distances = ttp['distances']
    num_cities = len(cities)
    #print(num_cities)
    packinglist = random_sample['random_packing_list']
    total_weight_ttp_instance = 0
    
    # Calculate the total weight of all items in the TTP instance
    for item in items:
        total_weight_ttp_instance += item['weight']

    Tr = 0.25  # Tightness ratio interval [0,1], suggested 0.25,0.5,0.75
    W = round(Tr * total_weight_ttp_instance)  # Example formula, may be adjusted
    vmax = 1.0
    vmin = 0.1
    R = 1.0

    # Initial random tour
    best_tour = random_sample['random_tour']
    #print(best_tour)
    # Ensure that `best_tour` is a list and correctly formatted
    if not isinstance(best_tour, list):
        raise ValueError("Expected `random_tour` to be a list, but got an integer or other non-iterable object.")

    # Ensure the initial tour starts and ends at node 0
    if best_tour[0] != 0 or best_tour[-1] != 0:
        best_tour = [0] + [city for city in best_tour if city != 0] + [0]

    best_value = random_sample['OB_value']
    random_actual_packing_list = ""
    #print(f"Type of best_tour: {type(best_tour)}, Value: {best_tour}")
    #print(f"Type of random_sample['random_tour']: {type(random_sample['random_tour'])}, Value: {random_sample['random_tour']}")
    for _ in range(iterations):
        # Generate a new tour by swapping two cities, ensuring start and end at 0
        new_tour = best_tour[:]
        
        # Only swap between positions 1 and num_cities - 2 to keep 0 fixed
        if num_cities > 2:  # Ensure there's enough to swap
            i, j = random.sample(range(1, num_cities - 1), 2)
            
            # Swap the two cities
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

            # Evaluate the new tour
            new_value, random_actual_packing_list = TTP_random_tour_and_packing_list.objective_function(
                new_tour, packinglist, items, distances, vmax, vmin, W, R)
            
            # If the new tour is better, update the best tour and value
            if new_value > best_value:
                best_tour, best_value = new_tour, new_value

    return best_tour, best_value

# Read TTP instances from JSON files and save results
def process_ttp_instances_results_hill_swap( input_folders_results_random, output_file):
    results = []
    iterations = 1000
    random_results=Iteration_search.load_iteration_results(input_folders_results_random)
    #print('okay')
    for result in random_results:
        filename_problem_instance = result['problem_instance_filename']
        if not os.path.exists(filename_problem_instance):
            print(f"Error: {filename_problem_instance} does not exist.")
            return
        #print(result)
        ttp_problem_instance = load_json(filename_problem_instance)
        #cities = ttp_problem_instance.get("cities", [])
        #items = ttp_problem_instance.get("items", [])
    #for filename in os.listdir(input_folder):
    #    if filename.endswith('.json'):
    #        with open(os.path.join(input_folder, filename), 'r') as f:
    #            ttp = json.load(f)
        start_time = time.time()  
        best_tour, best_value = hillclimber_tsp_swap(ttp_problem_instance, result,iterations)
        end_time = time.time()
        computing_time = end_time - start_time
        results.append({
                'filename': filename_problem_instance,
                'Iteration_random_sample':result['Iteration'],
                'old_random_tour':result['random_tour'],
                'best_new_tour': best_tour,
                'fixed_packinglist':result['random_packing_list'],
                'actual_fixed_packinglist':result['random_actual_packing_list'],
                'initial_OB_value':result['OB_value'],
                'new_OB_value': best_value,
                'computing_time': computing_time
            })
    save_to_json(results, output_file)

def parallel_process_ttp(input_folders_results_random, output_files, iterations):
    try:
        num_cores = cpu_count()
        print("number of cores is ", num_cores)
        with Pool(num_cores) as pool:
            pool.starmap(process_ttp_instances_results_hill_swap, zip(input_folders_results_random, output_files))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pool.close()
        pool.join()

if __name__ == "__main__":
    iterations = 1000
    os.makedirs('tour_results/hillclimber_tsp_swapping_results', exist_ok=True)
    input_folders_problem_instances = []
    input_folders_results_random = []
    output_files = []

    for cities in range(20, 120, 20):
        #print(cities)
        for n in range(1, 5): 
            #print(n)    
            items = n * cities
            name_directory = f'tour_results/hillclimber_tsp_swapping_results/TTP_instances_{cities}_items_{items}'
            os.makedirs(name_directory, exist_ok=True)
            #input_folder_problem_instances = f'problem_instances_ttp/json_files_TTP_instances_{cities}_items_{items}'
            input_folder_results_random = f'tour_results/random_results/TTP_instances_{cities}_items_{items}'
           # input_folders_problem_instances.append(input_folder_problem_instances)
            input_folders_results_random.append(input_folder_results_random)
            output_file=f'{name_directory}/results_hillclimber_tsp_cities_{cities}_items_{items}.json'
            output_files.append(output_file)
    # Process the TTP instances and save results
    #output_file = 'results.json'
    #print("okay")
    parallel_process_ttp(input_folders_results_random, output_files, iterations)

    print(f"Results saved to {output_file}")
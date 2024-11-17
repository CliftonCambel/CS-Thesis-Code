import random
import TTP_random_tour_and_packing_list
import Iteration_search
import os
import time
import Hillclimber_TSP_swaping
from multiprocessing import Pool, cpu_count
import logging
from tqdm import tqdm
from functools import partial
import math

def simulated_annealing_tsp_swap(ttp, random_sample, iterations, initial_temperature=1000, cooling_rate=0.99):
    cities = ttp['cities']
    items = ttp['items']
    distances = ttp['distances']
    num_cities = len(cities)
    packinglist = random_sample['random_actual_packing_list']
    total_weight_ttp_instance = sum(item['weight'] for item in items)

    Tr = 0.25  # Tightness ratio interval [0,1]
    W = round(Tr * total_weight_ttp_instance)
    vmax, vmin, R = 1.0, 0.1, 1.0

    best_tour = random_sample['random_tour']
    if not isinstance(best_tour, list):
        raise ValueError("Expected `random_tour` to be a list, but got an integer or other non-iterable object.")

    # Ensure the initial tour starts and ends at node 0
    if best_tour[0] != 0 or best_tour[-1] != 0:
        best_tour = [0] + [city for city in best_tour if city != 0] + [0]

    best_value = random_sample['OB_value']
    current_tour = best_tour[:]
    current_value = best_value
    temperature = initial_temperature

    for _ in range(iterations):
        # Generate a new tour by swapping two cities
        new_tour = current_tour[:]
        if num_cities > 2:  # Ensure there's enough to swap
            i, j = random.sample(range(1, num_cities - 1), 2)
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

        # Evaluate the new tour
        new_value, _, _ = TTP_random_tour_and_packing_list.objective_function(
            new_tour, packinglist, items, distances, vmax, vmin, W, R
        )

        # Calculate change in fitness
        delta_value = new_value - current_value

        # Accept new solution based on simulated annealing acceptance criteria
        if delta_value > 0 or random.random() < math.exp(delta_value / temperature):
            current_tour = new_tour
            current_value = new_value

            # Update the best solution if the new one is better
            if current_value > best_value:
                best_value = current_value
                best_tour = current_tour[:]

        # Cool the temperature
        temperature *= cooling_rate

        # Optional: Stop early if the temperature is very low
        #if temperature < 1e-3:
        #    break

    return best_tour, best_value

def process_ttp_instances_results_SA_swap( input_folders_results_random, output_file):
    results = []
    iterations = 10000
    random_results=Iteration_search.load_iteration_results(input_folders_results_random)
    for idx, result in enumerate(random_results, start=1):
        filename_problem_instance = result['problem_instance_filename']
        if not os.path.exists(filename_problem_instance):
            print(f"Error: {filename_problem_instance} does not exist.")
            return
        ttp_problem_instance = Hillclimber_TSP_swaping.load_json(filename_problem_instance)
        start_time = time.time()  
        best_tour, best_value = simulated_annealing_tsp_swap(ttp_problem_instance, result,iterations)
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
        if idx % 100 == 0 or idx == len(random_results):
            Hillclimber_TSP_swaping.save_to_json(results, output_file)

def parallel_process_ttp(input_folders_results_random, output_files):
    try:
        num_tasks = len(list(zip(input_folders_results_random, output_files)))
        cpu_count_sys = cpu_count()
        num_cores = min(cpu_count_sys, num_tasks)
        with Pool(num_cores) as pool:
            pool.starmap(process_ttp_instances_results_SA_swap, zip(input_folders_results_random, output_files))
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    os.makedirs('tour_results/hillclimber_tsp_swapping_results', exist_ok=True)
    input_folders_problem_instances = []
    input_folders_results_random = []
    output_files = []

    for cities in range(20, 120, 20):
        for n in range(1, 5): 
            items = n * cities
            name_directory = f'tour_results/hillclimber_tsp_swapping_results/TTP_instances_{cities}_items_{items}'
            os.makedirs(name_directory, exist_ok=True)
            input_folder_results_random = f'tour_results/random_results/TTP_instances_{cities}_items_{items}'
            input_folders_results_random.append(input_folder_results_random)
            output_file=f'{name_directory}/results_hillclimber_tsp_cities_{cities}_items_{items}.json'
            output_files.append(output_file)
    parallel_process_ttp(input_folders_results_random, output_files)


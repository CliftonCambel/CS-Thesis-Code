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

def simulated_annealing_KP(ttp, random_sample, iterations, initial_temperature=1000, cooling_rate=0.99):
    #cities = ttp['cities']
    items = ttp['items']
    item_dict = {item['id']: item for item in items}  # Precompute item lookup
    distances = ttp['distances']
    num_items = len(items)
    packinglist = random_sample['random_actual_packing_list']
    total_weight_ttp_instance = sum(item['weight'] for item in items)

    Tr = 0.25
    W = round(Tr * total_weight_ttp_instance)
    vmax, vmin, R = 1.0, 0.1, 1.0

    best_tour = random_sample['random_tour']
    best_fitness = random_sample['OB_value']
    current_tour = best_tour[:]
    current_packinglist = packinglist[:]
    current_fitness = best_fitness

    temperature = initial_temperature

    for _ in range(iterations):
        # Generate a neighboring solution
        new_packinglist = current_packinglist[:]
        random_item_id = random.randint(0, num_items - 1)
        random_item = item_dict.get(random_item_id)

        if random_item and random_item_id not in new_packinglist and sum(item['weight'] for item in items) + random_item['weight'] <= W:
            new_packinglist.append(random_item_id)
        elif new_packinglist:
            new_packinglist.remove(random.choice(new_packinglist))

        # Evaluate the new solution
        new_fitness, _, _ = TTP_random_tour_and_packing_list.objective_function(
            current_tour, new_packinglist, items, distances, vmax, vmin, W, R
        )

        # Calculate change in fitness
        delta_fitness = new_fitness - current_fitness

        # Accept the new solution probabilistically
        if delta_fitness > 0 or random.random() < math.exp(delta_fitness / temperature):
            current_packinglist = new_packinglist
            current_fitness = new_fitness

        # Update the best solution
        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_tour = current_tour[:]
            best_knapsack = current_packinglist[:]

        # Update temperature
        temperature *= cooling_rate

        # Optional: Stop if the temperature is too low
        #if temperature < 1e-3:
        #    break

    return best_tour, best_knapsack, best_fitness

def process_ttp_instances_results_SA_KP( input_folders_results_random, output_file):
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
        best_tour, best_knapsack, best_value = simulated_annealing_KP(ttp_problem_instance, result,iterations)
        end_time = time.time()
        computing_time = end_time - start_time
        results.append({
                'filename': filename_problem_instance,
                'Iteration_random_sample':result['Iteration'],
                'old_random_tour':result['random_tour'],
                'best_new_tour': best_tour,
                'old_actual_fixed_packinglist':result['random_actual_packing_list'],
                'optimized_packinglist': best_knapsack,
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
            pool.starmap(process_ttp_instances_results_SA_KP, zip(input_folders_results_random, output_files))
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    os.makedirs('tour_results/SA_KP_results', exist_ok=True)
    input_folders_problem_instances = []
    input_folders_results_random = []
    output_files = []

    for cities in range(20, 120, 20):
        for n in range(1, 5): 
            items = n * cities
            name_directory = f'tour_results/SA_KP_results/TTP_instances_{cities}_items_{items}'
            os.makedirs(name_directory, exist_ok=True)
            input_folder_results_random = f'tour_results/random_results/TTP_instances_{cities}_items_{items}'
            input_folders_results_random.append(input_folder_results_random)
            output_file=f'{name_directory}/results_SA_tsp_cities_{cities}_items_{items}.json'
            output_files.append(output_file)
    parallel_process_ttp(input_folders_results_random, output_files)
